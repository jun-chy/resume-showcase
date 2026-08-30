#!/usr/bin/env python3
"""Build index.html from src/template.html by inlining base64 images."""
import base64, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
tpl = (root / 'src' / 'template.html').read_text(encoding='utf-8')

# extracted from the original page (see README in git history)
imgs_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / 'src' / 'images'
out = tpl
for i in range(5):
    p = imgs_dir / f'img{i}.jpeg'
    b64 = base64.b64encode(p.read_bytes()).decode()
    out = out.replace('{{IMG%d}}' % i, 'data:image/jpeg;base64,' + b64)

leftover = re.findall(r'\{\{IMG\d\}\}', out)
if leftover:
    sys.exit('unresolved placeholders: %s' % leftover)
(root / 'index.html').write_text(out, encoding='utf-8')
print('index.html written:', len(out) // 1024, 'KB')
