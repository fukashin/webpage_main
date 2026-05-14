---
title: "Supabaseの無料枠で個人開発のバックエンドを構築する"
description: "Firebaseの代替として注目されるSupabase。無料プランでどこまでできるのか、実際に使ってみた所感をまとめます。"
date: 2025-05-10
tags:
  - Supabase
  - インフラ
  - 個人開発
---

## Supabaseとは

SupabaseはオープンソースのBaaS（Backend as a Service）で、Firebaseの代替として人気が高まっています。PostgreSQLベースなので、RDBの柔軟性をそのまま活かせるのが強みです。

## 無料プランでできること

Supabaseの無料プラン（Freeティア）で使える主なリソース：

- **データベース**: 500MB（PostgreSQL）
- **ストレージ**: 1GB
- **認証**: 50,000 MAU（月間アクティブユーザー）
- **Edge Functions**: 500,000回/月
- **リアルタイム**: 200同時接続

個人開発やプロトタイプなら十分すぎるスペックです。

## セットアップ手順

### 1. プロジェクト作成

[Supabase](https://supabase.com)にアクセスしてGitHubアカウントでサインアップ。「New Project」からプロジェクトを作成します。

### 2. テーブル作成

SQLエディタから直接テーブルを作成できます：

```sql
CREATE TABLE posts (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 3. クライアントから接続

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)

// データ取得
const { data, error } = await supabase
  .from('posts')
  .select('*')
  .order('created_at', { ascending: false })
```

## 実際に使ってみた感想

- **良い点**: セットアップが爆速。SQLが直接書けるのでRDB経験者には馴染みやすい
- **注意点**: 無料プランはプロジェクトが7日間非アクティブだと一時停止される
- **おすすめ**: 認証機能が組み込みで使えるので、ログイン機能付きアプリが簡単に作れる

## まとめ

個人開発のバックエンドとして、Supabaseの無料枠は非常に優秀です。「とりあえず動くものを作る」フェーズでは、AWSやAzureを使うよりも圧倒的に早く・安く始められます。

ユーザーが増えてきたらProプラン（$25/月）に移行すればスケールも問題なし。まずは無料で試してみることをおすすめします。
