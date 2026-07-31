#!/usr/bin/env python3
"""Small deterministic helper for checking obvious unsupported placeholders."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
patterns = [r"\bTBD\b", r"\bto be decided\b", r"预算待定但预计", r"预计于\d{4}"]
findings = [p for p in patterns if re.search(p, text, flags=re.I)]
print(json.dumps({"ok": not findings, "matched_patterns": findings}, ensure_ascii=False))
raise SystemExit(0 if not findings else 1)
