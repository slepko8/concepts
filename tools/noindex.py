"""Ставить заборону індексації в кожну HTML-сторінку перед публікацією.

    python3 tools/noindex.py site

Наявні <meta name="robots"> прибирає і вставляє один спільний одразу після <head>.
Запускається в GitHub Actions, тож у самих файлах репозиторію цього рядка може й не бути.
"""
import pathlib, re, sys

META = '<meta name="robots" content="noindex, nofollow, noarchive">'
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'site')
pages = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in ('.html', '.htm'))

for p in pages:
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<meta\b[^>]*\bname\s*=\s*["\']?robots\b[^>]*>\s*', '', s, flags=re.I)
    for pattern in (r'<head\b[^>]*>', r'<html\b[^>]*>', r'<!doctype\b[^>]*>'):
        m = re.search(pattern, s, flags=re.I)
        if m:
            s = s[:m.end()] + '\n' + META + s[m.end():]
            break
    else:
        s = META + '\n' + s
    p.write_text(s, encoding='utf-8')

print(f'noindex: {len(pages)} сторінок')
for p in pages:
    print('  ', p.relative_to(root))
