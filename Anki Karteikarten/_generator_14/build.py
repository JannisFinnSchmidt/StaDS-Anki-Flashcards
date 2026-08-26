# -*- coding: utf-8 -*-
"""Assemble the Anki import file for the 'Statistician Core Knowledge' deck."""
import glob
import os
import sys

import s1_distributions as s1
import s2_tests as s2
import s3_models as s3
import s4_links as s4
import s5_metrics as s5
import s6_r as s6
import s7_mixed as s7

DECK = "Knowledge::Core::Statistician Core Knowledge"
OUT = os.environ.get("OUT", "14_Statistician_Core_Knowledge.txt")
EXISTING_DIR = ("/mnt/d201168c-a915-44dc-8f0c-9ede7df59d09/LargeStorage/"
                "Knowledge Database/Anki Karteikarten")

NAMES = ["distributions", "tests", "model classes", "link functions",
         "metrics", "R functions", "mixed models"]
SECTIONS = [s1, s2, s3, s4, s5, s6, s7]

rows = []          # (front, back, tags)
per_section = []
for mod in SECTIONS:
    start = len(rows)
    for front, builder, back, tags in getattr(mod, "PIC", []):
        rows.append((front, builder().svg() + "<br><br>" + back, tags))
    for front, back, tags in getattr(mod, "TXT", []):
        rows.append((front, back, tags))
    per_section.append((len(rows) - start, len(getattr(mod, "PIC", []))))

# --- validation ------------------------------------------------------------
errors = []
for i, (f, b, t) in enumerate(rows):
    for name, val in (("front", f), ("back", b), ("tags", t)):
        if "\t" in val:
            errors.append(f"row {i}: TAB inside {name}: {f[:60]}")
        if "\n" in val or "\r" in val:
            errors.append(f"row {i}: newline inside {name}: {f[:60]}")
    if not f.strip() or not b.strip() or not t.strip():
        errors.append(f"row {i}: empty field: {f[:60]}")
    if b.count("\\[") != b.count("\\]"):
        errors.append(f"row {i}: unbalanced \\[ \\]: {f[:60]}")
    if b.count("\\(") != b.count("\\)"):
        errors.append(f"row {i}: unbalanced \\( \\): {f[:60]}")
    for tag in ("b", "pre", "svg", "i"):
        opens = b.count(f"<{tag}>") + b.count(f"<{tag} ")
        if opens != b.count(f"</{tag}>"):
            errors.append(f"row {i}: unbalanced <{tag}>: {f[:60]}")

seen = {}
for i, (f, b, t) in enumerate(rows):
    key = f.strip().lower()
    if key in seen:
        errors.append(f"row {i}: duplicate front, also row {seen[key]}: {f[:70]}")
    seen[key] = i

existing = set()
for path in sorted(glob.glob(os.path.join(EXISTING_DIR, "*.txt"))):
    if os.path.basename(path) == os.path.basename(OUT):
        continue          # do not compare the deck against a previously copied version of itself
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or "\t" not in line:
                continue
            existing.add(line.split("\t")[0].strip().lower())
collisions = [f for f, _, _ in rows if f.strip().lower() in existing]

if collisions:
    print("FRONT COLLISIONS with the existing 13 decks:")
    for c in collisions:
        print("   ", c)
if errors:
    print("VALIDATION ERRORS:")
    for e in errors:
        print("   ", e)
if errors or collisions:
    sys.exit(1)

# --- write ----------------------------------------------------------------
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("#separator:tab\n#html:true\n#notetype:Basic\n")
    fh.write(f"#deck:{DECK}\n#tags column:3\n")
    for f, b, t in rows:
        fh.write(f"{f}\t{b}\t{t}\n")

# --- report ---------------------------------------------------------------
n_svg = sum(1 for _, b, _ in rows if "<svg" in b)
n_math = sum(1 for _, b, _ in rows if "\\[" in b or "\\(" in b)
n_code = sum(1 for _, b, _ in rows if "<pre" in b)
print(f"wrote {OUT}: {len(rows)} cards | {n_svg} diagrams | {n_math} with formulas | "
      f"{n_code} with R code")
for name, (total, pics) in zip(NAMES, per_section):
    print(f"  {name:16s} {total:3d} cards ({pics} with a diagram)")
print(f"file size: {os.path.getsize(OUT) / 1024:.0f} KB")
