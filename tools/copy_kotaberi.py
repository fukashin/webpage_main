# こたべりの特設サイト（こたべりの世界観・デザイン担当が作る）を、日本語と英語の2つのページに写す。
#   日本語: static/kotaberi/index.html     → civildot.dev/kotaberi/
#   英語:   static/kotaberi-en/index.html  → civildot.dev/en/kotaberi/
# 使い方: python tools/copy_kotaberi.py → npx @11ty/eleventy
# 元のページは1枚で、文は <script> の中の表 STR（ja / en）から引く。言語はアドレス（/en/ で始まるか、?lang=）で決まる。
# 公開版で変えるのは:
#   - 「配信・動画のきまり」は連絡先が決まるまで出さない（const SITE = { stream: true → false）
#   - ページの頭（doctype・charset・viewport・言語ごとの title と説明・hreflang）を足す
#   - 画像・動画のパスを /kotaberi/… にそろえる（英語のページは /en/kotaberi/ にあるので、相対パスだと外れる）
#   - 使っている画像・動画だけ写す（JavaScript で名前を組み立てる img/av/ はフォルダごと）
import os, re, shutil, json

SRC = r"G:\kaihatu2\youtube_ch\kaisetsu\zatsudan3d\design\特設サイト"
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC = os.path.join(SITE, "static")
DST = os.path.join(STATIC, "kotaberi")        # 日本語のページと、画像・動画（両方の言語で使う）
DST_EN = os.path.join(STATIC, "kotaberi-en")  # 英語のページだけ
ORIGIN = "https://civildot.dev"

html = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()

# 「配信・動画のきまり」は、連絡先が決まるまで公開版では出さない
assert "const SITE = { stream: true" in html
html = html.replace("const SITE = { stream: true", "const SITE = { stream: false", 1)

# 上の帯（目次）が細い画面で重ならない直しは、元のページに入っている（目次の項目を縮めない）。
# 抜けていたら公開しない（以前、携帯の縦画面で文字が重なった）
assert "flex-shrink: 0" in html.split("</style>")[0], "上の帯の重なりの直し（flex-shrink: 0）が元のページに無い"

# 画像・動画のパスを /kotaberi/ からにそろえる（HTML の中と、JavaScript で組み立てる所の両方）
html = re.sub(r'(src|poster)="(img|video)/', r'\1="/kotaberi/\2/', html)
assert 'src="img/' not in html and 'src="video/' not in html and 'poster="video/' not in html

# 頭を外して、本文（<style> から）だけにする
for pat in [r"<title>.*?</title>\n", r'<meta name="claude:viewport-fit-sides"[^>]*>\n', r'<meta name="description"[^>]*>\n']:
    html = re.sub(pat, "", html, count=1)
fonts = re.findall(r"<link [^>]*>", html.split("<style>")[0])
for f in fonts:
    html = html.replace(f, "", 1)
html = html.lstrip()
style_end = html.index("</style>") + len("</style>")
style, body = html[:style_end].strip(), html[style_end:].strip()

# 言語ごとの title と説明は、表 STR から取る
def meta(lang, key):
    block = html[html.index(f"\n{lang}: {{"):]
    m = re.search(r"'" + re.escape(key) + r"': '((?:[^'\\]|\\.)*)'", block)
    return m.group(1).replace("\\'", "'")

def page(lang, path):
    title, desc = meta(lang, "meta.title"), meta(lang, "meta.desc")
    esc = lambda s: s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{ORIGIN}{path}">
<link rel="alternate" hreflang="ja" href="{ORIGIN}/kotaberi/">
<link rel="alternate" hreflang="en" href="{ORIGIN}/en/kotaberi/">
<link rel="alternate" hreflang="x-default" href="{ORIGIN}/kotaberi/">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{"".join(fonts)}
{style}
</head>
<body>
{body}
</body>
</html>
"""

for d in (DST, DST_EN):
    os.makedirs(d, exist_ok=True)
open(os.path.join(DST, "index.html"), "w", encoding="utf-8", newline="\n").write(page("ja", "/kotaberi/"))
open(os.path.join(DST_EN, "index.html"), "w", encoding="utf-8", newline="\n").write(page("en", "/en/kotaberi/"))

# 使っている画像・動画だけ写す（名前を組み立てる img/av/ はフォルダごと。ワールドの絵は WORLDS の表から）
used = set(re.findall(r"/kotaberi/((?:img|video)/[\w\-/]+\.(?:jpg|png|webp|mp4))", html))
used |= {"img/" + m for m in re.findall(r"'([\w\-]+\.(?:jpg|png|webp))'\]", html)}
used = {u for u in used if "${" not in u}
av = os.path.join(SRC, "img", "av")
if os.path.isdir(av):
    used |= {f"img/av/{f}" for f in os.listdir(av)}
for u in sorted(used):
    src = os.path.join(SRC, *u.split("/"))
    assert os.path.exists(src), f"元のフォルダに無い: {u}"
    dst = os.path.join(DST, *u.split("/"))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)
# 使わなくなった物は消す（写した先の中だけ）
removed = []
for root, _, files in os.walk(DST):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), DST).replace(os.sep, "/")
        if rel != "index.html" and rel not in used:
            os.remove(os.path.join(root, f)); removed.append(rel)
print(len(used), "files copied;", "removed:", removed)
