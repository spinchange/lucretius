import re, sys, pathlib, collections
from xml.etree import ElementTree as ET
src = pathlib.Path(sys.argv[1]); out = pathlib.Path(sys.argv[2])
ns = {'t':'http://www.tei-c.org/ns/1.0'}
root = ET.parse(src).getroot()
total = 0; report = []
for book in root.findall('.//t:div[@subtype="book"]', ns):
    n = int(book.get('n')); lines = []; prev = 0; seen = collections.Counter()
    for l in book.findall('t:l', ns):
        num = l.get('n'); txt = re.sub(r'\s+', ' ', ''.join(l.itertext())).strip()
        if num is None or txt == '':
            report.append(f"{n}.{prev}+ : lacuna marker (unnumbered/empty line in source)")
            lines.append(('', '[lacuna]')); continue
        seen[num] += 1
        k = int(re.match(r'\d+', num).group())
        if k != prev + 1: report.append(f"{n}.{num} : follows {n}.{prev} (transposition in source order)")
        prev = k; lines.append((num, txt))
    dups = [k for k,v in seen.items() if v > 1]
    if dups: report.append(f"book {n}: duplicate numbers {dups}")
    with open(out / f"book_{n:02d}.txt", 'w', encoding='utf-8') as f:
        for num, txt in lines: f.write(f"{num:>5}  {txt}\n")
    numbered = sum(1 for a,_ in lines if a); total += numbered
    report.append(f"book {n}: {numbered} numbered lines, {len(lines)-numbered} lacuna markers, highest {prev}")
report.append(f"total numbered {total}")
print("\n".join(report))
