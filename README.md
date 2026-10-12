# webpage_main

シヴィルドットのポートフォリオサイト。Eleventy で `src/` から `_site/` を生成する。

## 構成

- `src/_data/works.json` — 作品一覧。**上から順に表示される**ので、並び順＝力を入れている順。作品を足すときはここに1件追加し、画像を `src/image/` に置く
- `src/_data/site.json` — サイト名・URL・連絡先・SNSリンク
- `src/index.njk` — トップ（作品グリッド）
- `src/works.njk` — 作品ごとの個別ページを `/works/<slug>/` に生成
- `src/privacy-policy.njk` / `src/tokushoho.njk` — 法務ページ。**URL は Play Console / Stripe に登録しているので変えない**
- `src/blog/` — ブログ（Markdown）
- `src/css/site.css` — サイト全体のスタイル

## ビルド

```
npm ci
npm run build          # 独自ドメイン・Cloudflare Pages 向け（ルート配信）
npm run build:ghpages  # GitHub Pages のプロジェクトサイト（/webpage_main/）向け
npm run serve          # ローカルプレビュー
```

## デプロイ

`.github/workflows/pages.yml` が main への push で Eleventy ビルド → GitHub Pages に配信する。
初回は Settings > Pages > Source を **GitHub Actions** に切り替えること。

独自ドメインに移すとき:
1. `src/_data/site.json` の `url` をドメインに変更
2. `pages.yml` の `PATH_PREFIX` を削除（または Cloudflare Pages ならビルドコマンド `npm run build`、出力 `_site`）
3. Play Console / Stripe に登録した特商法・プライバシーポリシーの URL を更新
