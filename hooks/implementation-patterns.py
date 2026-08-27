#!/usr/bin/env python3
"""Claude Code PostToolUse hook: nudge with implementation patterns after edits.

Reads the hook JSON from stdin, checks the edited file against the pattern
rules in ~/.agents/patterns/, and returns matching nudges as additionalContext.

Guarantees:
- Always exits 0. Never blocks the turn. Any internal error is silent.
- Silent when nothing matches. At most 2 nudges per edit.
- Each rule fires once per session (tracked in a temp state file).

Pattern file format (see patterns/general.md):
    ## rule-name
    trigger: <python regex matched against the file's content, multiline>
    <nudge text until the next ## heading>
"""

import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

PATTERNS_DIR = Path.home() / ".agents" / "patterns"
MAX_NUDGES_PER_EDIT = 2

# extension -> pattern files (general.md always applies)
EXT_FILES = {
    ".ts": ["general.md", "typescript.md"],
    ".tsx": ["general.md", "typescript.md", "react.md"],
    ".jsx": ["general.md", "react.md"],
    ".js": ["general.md"],
    ".mjs": ["general.md"],
    ".mts": ["general.md", "typescript.md"],
    ".py": ["general.md"],
    ".go": ["general.md"],
    ".rb": ["general.md"],
    ".java": ["general.md"],
    ".kt": ["general.md"],
    ".swift": ["general.md"],
    ".rs": ["general.md"],
}

RULE_RE = re.compile(
    r"^##\s+(?P<name>\S+)\s*\ntrigger:\s*(?P<trigger>.+?)\s*\n(?P<text>.*?)(?=^##\s|\Z)",
    re.MULTILINE | re.DOTALL,
)


def parse_rules(path: Path):
    if not path.is_file():
        return []
    rules = []
    for m in RULE_RE.finditer(path.read_text(encoding="utf-8", errors="replace")):
        text = m.group("text").strip()
        if text:
            rules.append((m.group("name"), m.group("trigger"), text))
    return rules


def main() -> None:
    payload = json.load(sys.stdin)
    file_path = (payload.get("tool_input") or {}).get("file_path", "")
    session_id = payload.get("session_id", "no-session")
    target = Path(file_path)

    pattern_files = EXT_FILES.get(target.suffix.lower())
    if not pattern_files or not target.is_file():
        return

    content = target.read_text(encoding="utf-8", errors="replace")

    # one firing per rule per session
    sid = hashlib.sha256(session_id.encode()).hexdigest()[:16]
    state_path = Path(tempfile.gettempdir()) / f"impl-patterns-{sid}"
    try:
        seen = set(state_path.read_text().split())
    except OSError:
        seen = set()

    nudges = []
    for fname in pattern_files:
        for name, trigger, text in parse_rules(PATTERNS_DIR / fname):
            if name in seen or len(nudges) >= MAX_NUDGES_PER_EDIT:
                continue
            try:
                if re.search(trigger, content, re.MULTILINE):
                    nudges.append(f"[{name}] {text}")
                    seen.add(name)
            except re.error:
                continue

    if not nudges:
        return

    try:
        state_path.write_text(" ".join(sorted(seen)))
    except OSError:
        pass

    context = (
        f"Implementation-pattern nudges for {target.name} (from ~/.agents/patterns/, "
        "advisory only — apply if it fits, no need to reply):\n" + "\n".join(nudges)
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": context,
                }
            }
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
