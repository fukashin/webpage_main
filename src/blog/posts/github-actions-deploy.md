---
title: "GitHub Actionsで静的サイトを自動デプロイする"
description: "pushするだけでサイトが更新される仕組みをGitHub Actionsで構築します。11tyのビルドからGitHub Pagesへのデプロイまで。"
date: 2025-05-14
tags:
  - GitHub
  - CI/CD
  - 自動化
---

## やりたいこと

`main`ブランチにpushしたら、自動的にサイトがビルドされてGitHub Pagesに公開される仕組みを作ります。

手動でビルドしてアップロードする手間がなくなるので、記事を書くことだけに集中できます。

## GitHub Actionsのワークフロー

`.github/workflows/deploy.yml` を作成します：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm ci

      - run: npm run build

      - uses: actions/upload-pages-artifact@v3
        with:
          path: '_site'

  deploy:
    needs: build-and-deploy
    runs-on: ubuntu-latest
    permissions:
      pages: write
      id-token: write
    environment:
      name: github-pages
    steps:
      - uses: actions/deploy-pages@v4
```

## 設定のポイント

### リポジトリの設定

1. Settings → Pages → Source を「GitHub Actions」に変更
2. これだけでOK。ブランチ指定は不要

### ビルドコマンド

`package.json` に以下が定義されていれば動きます：

```json
{
  "scripts": {
    "build": "npx @11ty/eleventy"
  }
}
```

## 動作確認

1. ワークフローファイルをcommit & push
2. Actionsタブでビルドが走るのを確認
3. 成功すれば `https://username.github.io/repo-name/` でサイトが公開される

## まとめ

GitHub Actionsを使えば、記事を書いてpushするだけで自動的にサイトが更新されます。無料枠（月2,000分）で個人ブログなら余裕で足ります。

一度設定してしまえば、あとはMarkdownを書くことだけに集中できる環境の完成です。
