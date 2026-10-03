"""Збирач концепту «Icon × Origin»: перші три екрани лендінга «Infiltracja Icon od A do Z»
у стилі референса Origin Financial.

    python3 sources/icon-origin/build.py

page.html       — шаблон (повний документ) з мітками %%LOGO%%, %%LAUREL%%, %%PORTRAIT%%
portrait.jpg    — квадратний кроп фото Домініки Йордан
laurel.svg      — <symbol id="laurel"> для лаврових знаків
logo-white.svg  — білий логотип Edutologia

Результат:
site/icon-origin/index.html          — сторінка, що публікується: slepko8.github.io/concepts/icon-origin/
sources/icon-origin/_artifact.html   — той самий вміст без doctype/html/head/body для claude.ai
                                       (https://claude.ai/artifact/W5nF5kUQdgDrhz5aV6C46N, оновлювати з url)
"""
import base64, pathlib, re

here = pathlib.Path(__file__).resolve().parent
page = here.parents[1] / 'site' / here.name / 'index.html'

src = (here / 'page.html').read_text(encoding='utf-8')

logo = (here / 'logo-white.svg').read_text(encoding='utf-8')
logo = re.sub(r'<\?xml[^>]*\?>', '', logo)
logo = re.sub(r'<title>.*?</title>', '', logo, flags=re.S)
logo = re.sub(r'\s(width|height|role|aria-label)="[^"]*"', '', logo, count=4)
logo = logo.replace('fill="#FFFFFF"', 'fill="currentColor"').replace('<svg ', '<svg aria-hidden="true" focusable="false" ', 1).strip()

laurel = (here / 'laurel.svg').read_text(encoding='utf-8')
portrait = 'data:image/jpeg;base64,' + base64.b64encode((here / 'portrait.jpg').read_bytes()).decode()

html = src.replace('%%LOGO%%', logo).replace('%%LAUREL%%', laurel).replace('%%PORTRAIT%%', portrait)
assert '%%' not in html, 'лишилась незамінена мітка'
page.parent.mkdir(parents=True, exist_ok=True)
page.write_text(html, encoding='utf-8')

frag = html.split('<!--FRAG-->', 1)[1].split('<!--/FRAG-->', 1)[0].replace('</head>\n<body>\n', '\n', 1)
assert '<body' not in frag and '</head>' not in frag
(here / '_artifact.html').write_text(frag.strip() + '\n', encoding='utf-8')
print(page.relative_to(here.parents[1]), len(html), '· _artifact.html', len(frag))
