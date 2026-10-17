# システム概要: シヴィルドット ポートフォリオサイト（webpage_main）

最終更新: 2026-10-17

## 1. 概要（何のサイトか・誰向けか）

シヴィルドット（個人開発者、屋号: シヴィルドット制作室）の制作物ポートフォリオサイト。作ったWebアプリ・Androidアプリ・VRゲームを一覧と個別ページで紹介する。

主な読者:
- 仕事を頼むか検討している人、採用担当など「この人は何が作れるか」を10秒で知りたい人
- Google Play / Stripe の審査担当者（プライバシーポリシー・特定商取引法に基づく表記のページ）
- YouTube・X から流入してくる視聴者（動画で扱ったツール＝シヴツールへの導線）

法務ページ2つは外部サービスに登録しているURLなので、パスを変えてはいけない:
- `/privacy-policy.html`（Google Play のシヴツールに登録。`#shivtool` アンカーあり）
- `/tokushoho.html`（Stripe の特商法表記に登録）

## 2. 公開先 URL・リポジトリ・ブランチ運用

| 項目 | 値 |
|---|---|
| 公開URL | https://civildot.dev/ （2026-10-16 から） |
| 旧URL | https://fukashin.github.io/webpage_main/ → 新ドメインへ 301 転送（配下パスも維持） |
| リポジトリ | https://github.com/fukashin/webpage_main （private） |
| ブランチ | `main` のみが本番。`main` への push で GitHub Actions がビルド・配信する |
| 作業ブランチ | 大きな改修は別ブランチ（例: `redesign`）で作り、`main` にマージして公開。GitHub Pages は `main` 以外を配信しない |

ローマ字表記は **civildot**（シヴツールの Android パッケージ名 `jp.civildot.toolbox` に合わせた）。`sivildot` は使わない。

## 3. 構成（Eleventy、ホスティング、ドメイン・DNS、計測）

```
GitHub (main) --push--> GitHub Actions (npm ci && eleventy) --> GitHub Pages (配信元)
                                                                    ^
ブラウザ --> Cloudflare (DNS + プロキシ, civildot.dev) ------------+
```

- **静的サイトジェネレータ**: Eleventy 3（`@11ty/eleventy`）。入力 `src/`、出力 `_site/`（gitignore）
  - `src/_data/works.json` — 作品一覧。配列の順番がそのまま表示順（力を入れている順）。作品追加はここに1件足して画像を `src/image/` に置くだけ
  - `src/_data/site.json` — サイト名・URL・連絡先・SNS・GA4測定ID・表記ゆれ（altNames）
  - `src/index.njk` — トップ（作品グリッド＋自己紹介）
  - `src/works.njk` — 作品ごとに `/works/<slug>/` を生成（pagination）
  - `src/privacy-policy.njk` / `src/tokushoho.njk` — 法務ページ（装飾なしのプレーン表示）
  - `src/redirects.njk` — 旧テンプレート時代のURL（`aplisakusei_*.html`, `company.html` 等）から新トップへの転送ページ
  - `src/sitemap.njk` / `src/robots.njk` — sitemap.xml / robots.txt
  - `src/blog/` — ブログ（Markdown、`blog-base.njk` レイアウト）
  - `src/_includes/base.njk` — 共通レイアウト。meta description / OGP / canonical / JSON-LD（Person、別名 civildot・シビルドット等）/ GA4 タグ / Search Console 確認タグの差し込み口
  - `src/css/site.css` — ダーク基調（サイバーパンク調）のスタイル。法務ページは `body.legal` で装飾を抑制
- **ホスティング**: GitHub Pages（Source = GitHub Actions、`.github/workflows/pages.yml`）。カスタムドメイン `civildot.dev`、HTTPS 強制 ON
- **ドメイン・DNS**: Cloudflare Registrar で取得、Cloudflare DNS
  - `@` A ×4 → GitHub Pages の IP（185.199.108〜111.153）、`www` CNAME → `fukashin.github.io`、いずれもプロキシ ON
  - `@` TXT `google-site-verification=...`（Search Console のドメイン所有権確認。消さない）
  - SSL/TLS モード: フル（厳格）。※「フレキシブル」にすると GitHub Pages との間でリダイレクトループになる
- **計測**
  - Google Analytics 4: プロパティ「シヴィルドット ポートフォリオサイト」、ストリームURL `https://civildot.dev`、測定ID は `site.json` の `ga4`
  - Google Search Console: ドメインプロパティ `civildot.dev`（DNS TXT で確認済み、sitemap 送信済み）。旧 URL プレフィックスプロパティ `https://fukashin.github.io/webpage_main/` も残っている
  - Cloudflare Web Analytics: `civildot.dev` を自動セットアップで登録（ページ配信時にスクリプトを自動挿入）

## 4. 使っている外部サービスと課金

| サービス | 用途 | 料金の目安 | 備考 |
|---|---|---|---|
| GitHub（Pages / Actions） | ソース管理・ビルド・配信 | 無料（private リポジトリの Actions は無料枠 2,000分/月。ビルドは1回1分未満） | — |
| Cloudflare Registrar | ドメイン `civildot.dev` | 年 約 $12（原価販売、更新も同額） | 2026-10-16 取得。自動更新の設定は要確認 |
| Cloudflare（DNS・プロキシ・Web Analytics） | DNS、CDN、訪問者計測 | 無料プラン | — |
| Google Analytics 4 | アクセス解析 | 無料 | — |
| Google Search Console | 検索状況の確認 | 無料 | — |
| Google Fonts | Web フォント（Share Tech Mono, Noto Sans JP） | 無料 | — |
| YouTube 埋め込み | 作品ページの紹介動画 | 無料 | — |

キー・トークン類はリポジトリに一切置いていない。GA4 の測定ID（`G-...`）は公開情報なので `site.json` に直書き。

## 5. 開発とデプロイの手順

前提: Node.js 20 系、npm。

```bash
npm ci              # 依存のインストール（初回）
npm run serve       # ローカルプレビュー http://localhost:8080/（ファイル変更で自動リロード）
npm run build       # _site/ に出力
```

注意: `npm run serve` 起動中は Eleventy が `src/` を監視してハンドルを掴むため、Windows では `git checkout` / `git merge` が Permission denied で失敗する。ブランチを切り替える前に止めること。

デプロイ:
1. `main` に push する（PR でも直接 push でも可）
2. GitHub Actions `Deploy site` が自動実行（約1分）。`gh run list --workflow=pages.yml` で確認
3. 反映は数十秒〜数分。Cloudflare のキャッシュは HTML を既定でキャッシュしないので通常は即時

作品を追加するとき: `src/_data/works.json` に1件追加（slug, title, kind, filters, year, image, summary, description, tech, links, videos）→ 画像を `src/image/` に置く → push。一覧カードと個別ページが両方生成される。

法務ページを直すとき: `src/privacy-policy.njk` / `src/tokushoho.njk` を編集。シヴツールのプライバシーポリシーの文面の元は youtubeyou リポジトリの `docs/store/privacy-policy.md`（仕様を変えたら両方直す）。

## 6. リリース履歴

| 日付 | 内容 |
|---|---|
| 2024-03〜04 | 無料HTMLテンプレート（s-hoshino.com）ベースでサイト作成。GitHub Pages（ブランチ配信）で公開 |
| 2024-06〜07 | ボールゲーム・ストップウォッチなど小物を追加（後に削除） |
| 2025-07 | 内容・表示の修正 |
| 2026-05-14 | ヘッダー共通化（JSで挿入）、全体修正、ボールゲーム削除 |
| 2026-05-15 | 作業トモのプライバシーポリシー追加 |
| 2026-06-01 | クラウドLLM RAGアプリを作品に追加 |
| 2026-08-15 | Webアプリページに作品4件追加（コトロク、人生シミュレーター、議事録分析、VRゲーム） |
| 2026-09-01 | 特定商取引法に基づく表記ページを新設（Stripe 登録用）。会社概要の代表名をシヴィルドットに。X のリンクを @x_fukase に変更。ナビに法務ページを追加 |
| 2026-09-25 | プライバシーポリシーを「共通事項＋アプリ別」構成に改定しシヴツール節を追加（Play 審査用）。サポート用メールを fukashe.shintaro@gmail.com に。モバイルページにシヴツール追加（スクショ合成画像・YouTube埋め込み）。報告機能の記載追加、v1.0.1 仕様に同期 |
| 2026-10-02 | 再構築版を `redesign` ブランチで作成（Eleventy 化、作品データ駆動、サイバーパンク調トップ、個別ページ、SEO 対応） |
| 2026-10-12 | `redesign` を `main` にマージして本番切り替え。Pages の配信元を GitHub Actions に変更。旧URLの転送ページ追加。SEO（h1・表記ゆれ・JSON-LD）、GA4 導入、Search Console 登録・sitemap 送信。プライバシーポリシーにランニングメイト節を追加 |
| 2026-10-16 | シヴツールの Google Play リンク追加（製品版公開）。独自ドメイン `civildot.dev` へ移行（Cloudflare DNS、GitHub Pages カスタムドメイン、HTTPS 強制、プロキシ ON、Web Analytics、Search Console ドメインプロパティ、GA4 ストリームURL更新） |

## 7. 運用（監視、更新のしかた、障害時の復旧手順）

監視（いずれもダッシュボードを見に行く方式。アラートは未設定）:
- 配信の成否: GitHub Actions の `Deploy site` の結果（失敗時は GitHub からメール通知）
- アクセス: GA4（詳細）、Cloudflare ドメイン一覧の「ユニーク訪問者数」と Web Analytics（概況）
- 検索: Search Console の「ページ」（インデックス状況）と「検索パフォーマンス」

更新のしかた: §5 のとおり。本番は `main` のみなので、試したいときはブランチを切って `npm run serve` で確認してからマージする。

障害時の切り分けと復旧:
- **サイトが開かない（証明書エラー / 522 / リダイレクトループ）**
  1. Cloudflare の SSL/TLS モードが「フル（厳格）」か確認（フレキシブルだとループ）
  2. `curl -I https://civildot.dev/` で `Server: cloudflare` か `GitHub.com` かを見る。Cloudflare を一時的に外して切り分けるには、DNS レコードのプロキシを OFF（DNS のみ）にする
  3. GitHub 側: `gh api repos/fukashin/webpage_main/pages` で `https_certificate.state` が `approved` か確認。証明書の発行が始まらないときは、カスタムドメインを一度空にして付け直す（`gh api -X PUT repos/fukashin/webpage_main/pages -f cname=` → `-f cname=civildot.dev`）。2026-10-16 にこの手順で解決した
- **デプロイが失敗する**: Actions のログを確認。Eleventy のテンプレートエラーが大半。ローカルで `npm run build` を通してから push する
- **壊れたページを公開してしまった**: `git revert` して push すれば1分で戻る
- **ドメインが失効した**: Cloudflare Registrar で更新。失効しても GitHub Pages 側は `fukashin.github.io/webpage_main/` で引き続き配信される（ただしカスタムドメイン設定を外すまでそちらへ転送し続ける）

## 8. 背景と経緯（なぜ作ったか、主な判断とその理由）

- **目的**: 個人開発の作品を一か所で見せる。シヴツール（Android）や kotoroku などのアプリから「作者のサイト」として参照される受け皿にする
- **法務ページを先に整えた理由**: Stripe の利用と Google Play の審査に、特商法表記とプライバシーポリシーの公開URLが必要だったため（2026-09）。URLを登録しているので以後パスは固定
- **Eleventy で作り直した理由（2026-10）**: 旧サイトは無料テンプレート由来で、FAQ・会社案内サンプル・関係ない画像など「何を作ったか」に関係ない部分が多く、作品が2クリック先にあった。さらにテンプレートの利用条件で「Design by / Template by」のPR枠を消せない制約があった。ゼロから作り直して、作品を JSON 1 ファイルで管理し、一覧と個別ページ（1作品1URL）を自動生成する形にした
- **デザインをサイバーパンク調にした理由**: 「解説動画 → 作ってみた」というチャンネルの性格と動画サムネのダーク基調に合わせ、落ち着いた制作会社風より「個人がガリガリ作っている」ことが伝わる方向にした。ただし本文の可読性は守り、法務ページは審査担当者向けにプレーンにした
- **CloudFront / Cloudflare Pages に移行しなかった理由**: ホスティング先は SEO に影響しない。アクセス計測はドメインを Cloudflare に置いてプロキシ経由にするだけで取れるため、GitHub Pages のまま独自ドメインを乗せる最小構成にした。管理者ログイン（Cloudflare Access）やブランチプレビューが必要になったら Cloudflare Pages に移す
- **ドメイン名を civildot.dev にした理由**: `civildot.com` は取得できなかった。Play のパッケージ名 `jp.civildot.toolbox` が永久に変更できない識別子なので、ローマ字表記は civildot に統一。開発者のサイトなので `.dev`
- **Search Console の所有権確認で Cloudflare 連携を使わなかった理由**: Google に Cloudflare アカウントへの OAuth 権限を渡す方式だったため、手動の DNS TXT 方式にした

## 9. 未解決の課題・次の候補

- **外部リンクが無い**: X・YouTube（チャンネルの「リンク」欄と各動画の概要欄）・GitHub プロフィール・kotoroku.com のフッターから `https://civildot.dev/` へリンクする。「シヴィルドット」で検索されたときに出るための最重要作業
- **Play Console / Stripe の登録URLを新ドメインに更新**: プライバシーポリシー `https://civildot.dev/privacy-policy.html`、ウェブサイト `https://civildot.dev/`、特商法 `https://civildot.dev/tokushoho.html`。旧URLは転送されるので壊れてはいないが、登録は新URLにしておくのが望ましい。Play の「ウェブサイト」欄は以前 `https://fukashin.github.io/`（ルート）が入っていてポートフォリオに届いていなかった
- **Cloudflare Web Analytics のスクリプト自動挿入の確認**: 登録直後の確認では未挿入だった。ページビューが出なければ手動でスクリプトを `base.njk` に入れる
- **人生シミュレーター・議事録分析プラットフォームが Basic 認証付き**: 作品ページから「限定公開」としてリンクしているが、訪問者は開けない。公開するか、スクリーンショット中心の紹介に割り切るか
- **Search Console の旧プロパティの扱い**: URL プレフィックス型のため「アドレス変更」ツールが使えず、301 転送に任せている。インデックスが新ドメインに移ったら旧プロパティは削除してよい
- **特商法ページの運営責任者**: 「フカワ」のまま。特商法上は本名が必要なので、Stripe 審査で指摘されたら本名に差し替える
- **シヴツールのカード用スクリーンショット**: 開発用セット名（「テスト 1/1 ×2（開発用）」）が写った画面を使っている。通常のセットで撮り直すときれい
- **ブログ**: 記事が2本のまま。動画と連動した記事を出すなら、`src/blog/posts/` に Markdown を足すだけで載る

## 10. 要確認

- Cloudflare Registrar のドメイン自動更新が ON になっているか（取得はユーザーが行ったため未確認）
- Play Console / Stripe の登録URLを新ドメインに更新したか（ユーザー作業。§9 参照）
- 作業トモ（Android）が実際に Google Play に公開されているか、ストアURLは何か（作品ページのストアリンクが未設定）
- 「その他のアプリ」としてプライバシーポリシーに残した Google Analytics / Firebase / Supabase の利用は、具体的にどのアプリか（旧ポリシーの記載を引き継いだもの。使っているアプリがあるとの回答は得たが、アプリ名は未確認）
- YouTube チャンネルのリンク先は動画ページから特定したチャンネルID（UCg7QKK46s1yDoUg4fFXD3Aw）を使っている。ハンドル付きURL（@〜）に変えたい場合は要指定
- 作品の年表記（works.json の `year`）は制作時期の推測。ユーザーから「大体合っているので可」との回答はあるが、正確な年は未確認
