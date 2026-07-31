#!/usr/bin/env python3
"""Example deterministic source check. It cannot replace rendered visual review."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

root = Path(sys.argv[1])
text = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in root.rglob("*") if p.is_file() and p.suffix in {".tsx", ".jsx", ".vue", ".html", ".css"})
card_terms = len(re.findall(r"\b(Card|card-grid|grid-cols-[234])\b", text, flags=re.I))
fade_terms = len(re.findall(r"opacity\s*[:=]|fade(In|Up)?", text, flags=re.I))
print(json.dumps({"card_pattern_mentions": card_terms, "fade_pattern_mentions": fade_terms, "note": "Use this only as a warning; inspect rendered output."}, ensure_ascii=False))
