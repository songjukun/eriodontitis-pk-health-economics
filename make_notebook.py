"""Generate the distributable notebook from the canonical Python analysis."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "periodontal_miniPBPK_CEA.py"
OUTPUT = ROOT / "periodontal_miniPBPK_CEA.ipynb"


def markdown_from_comments(lines):
    rendered = []
    for line in lines:
        if line.startswith("# "):
            rendered.append(line[2:])
        elif line.rstrip() == "#":
            rendered.append("")
        elif line.startswith("#"):
            rendered.append(line[1:].lstrip())
        else:
            rendered.append(line)
    return "\n".join(rendered).strip() + "\n"


text = SOURCE.read_text(encoding="utf-8")
parts = re.split(r"(?m)^# In\[\d+\]\s*$", text)
preface = parts.pop(0).splitlines()
if preface and preface[0].startswith("# Auto-exported"):
    preface = preface[1:]

cells = [
    {
        "cell_type": "markdown",
        "metadata": {},
        "source": markdown_from_comments(preface).splitlines(keepends=True),
    }
]
for part in parts:
    code = part.lstrip("\r\n")
    if not code.strip():
        continue
    cells.append(
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": code.splitlines(keepends=True),
        }
    )

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.12"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}
OUTPUT.write_text(json.dumps(notebook, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"Wrote {OUTPUT.name} with {len(cells)} cells")
