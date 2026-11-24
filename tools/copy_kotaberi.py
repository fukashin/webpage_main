# こたべりの特設サイト（こたべりの担当が作る）を static/kotaberi/ に写し直す。
# 使い方: python tools/copy_kotaberi.py → npx @11ty/eleventy で /kotaberi/ に出る。
# 「配信・動画のきまり」は連絡先が決まるまで外す。ページの頭（doctype など）を足す。使っている画像・動画だけ写す
import os, re, shutil
SRC = r"G:\kaihatu2\youtube_ch\kaisetsu\zatsudan3d\design\特設サイト"
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(SITE, "static", "kotaberi")  # Eleventy の外に置いてそのまま写す（テンプレートとして読ませない）
os.makedirs(os.path.join(DST, "img"), exist_ok=True)
os.makedirs(os.path.join(DST, "video"), exist_ok=True)

html = open(os.path.join(SRC, "index.html"), encoding="utf-8").read()

# 「配信・動画のきまり」は下書き（〔連絡先〕が空欄）なので、連絡先が決まるまで載せない
a = html.index("<!-- 8 配信のきまり -->"); b = html.index("<!-- 9 端末と操作 -->")
html = html[:a] + html[b:]
html = html.replace('  <a class="n" href="#stream">配信のきまり</a>\n', "")
html = html.replace('<a class="btn" href="#stream">配信・動画のきまり</a>', '<a class="btn" href="https://civildot.dev/works/kotaberi/">作品の紹介（シヴィルドット）</a>')
html = html.replace('<p>はい。<a href="#stream">配信・動画のきまり</a>を見てください。同じ部屋の人に、先に断ってからにしてください。</p>',
                    '<p>はい。くわしいきまりは準備中です。同じ部屋の人に、先に断ってからにしてください。</p>')
assert "#stream" not in html and "〔連絡先〕" not in html

# 「遊ぶには」の飛び先
html = html.replace('<h3 style="margin-top:0">いまは「招待制の試作」です</h3>', '<h3 id="join" style="margin-top:0;scroll-margin-top:72px">いまは「招待制の試作」です</h3>')
assert 'id="join"' in html

# ポートフォリオへ戻る道
html = html.replace("  <p>こたべり（試作）。画面の写真は開発中のものです。</p>",
                    '  <p>こたべり（試作）。画面の写真は開発中のものです。</p>\n  <p>作った人: <a href="https://civildot.dev/">シヴィルドット</a>（<a href="https://civildot.dev/works/kotaberi/">作品の紹介</a>）</p>')

# 頭を足す（claude.ai 向けの書き方から、ふつうのページへ）
head_lines = []
body = []
for line in html.split("\n"):
    pass
title = re.search(r"<title>.*?</title>", html).group(0)
desc = re.search(r'<meta name="description"[^>]*>', html).group(0)
fonts = re.findall(r'<link [^>]*>', html.split("<style>")[0])
html = html.replace(title + "\n", "", 1).replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "", 1).replace(desc + "\n", "", 1)
for f in fonts:
    html = html.replace(f, "", 1)
html = re.sub(r"^\n+", "", html)
style_end = html.index("</style>") + len("</style>")
style, rest = html[:style_end], html[style_end:]
page = f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
{desc}
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{"".join(fonts)}
{style.strip()}
</head>
<body>
{rest.strip()}
</body>
</html>
"""
open(os.path.join(DST, "index.html"), "w", encoding="utf-8", newline="\n").write(page)

# 使っている画像・動画だけを写す
used = set(re.findall(r'(img/[\w\-]+\.(?:jpg|png|webp)|video/[\w\-]+\.(?:mp4|jpg))', page))
used |= {"img/" + m for m in re.findall(r"'([\w\-]+\.jpg)'\]", page)}
# JavaScript で名前を組み立てて読む絵（img/av/v${i}.webp）は、名前を探しても見つからないのでフォルダごと写す
for d in ["img/av"]:
    if os.path.isdir(os.path.join(SRC, d)):
        for f in os.listdir(os.path.join(SRC, d)):
            used.add(f"{d}/{f}")
os.makedirs(os.path.join(DST, "img", "av"), exist_ok=True)
for u in sorted(used):
    shutil.copy2(os.path.join(SRC, u.replace("/", os.sep)), os.path.join(DST, u.replace("/", os.sep)))
print(len(used), "files:", sorted(used))
print("missing:", [u for u in used if not os.path.exists(os.path.join(SRC, u.replace("/", os.sep)))])
