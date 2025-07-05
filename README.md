# Discord RSS Bot

RSSフィードを定期的に取得し、新着記事をDiscordチャンネルに自動投稿するPythonボットです。

## 機能

- 複数のRSSフィードを監視
- 設定可能な自動実行間隔（デフォルト15分）
- 重複投稿防止
- Discord Webhookによる投稿
- 記事タイトルとリンクを送信
- X(Twitter)への投稿リンク（Intent Post）
- 英語記事の日本語翻訳機能
- エラーハンドリングとログ機能

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 設定ファイルの作成

`config.json.example`を`config.json`にコピーし、Discord WebhookURLとRSSフィードを設定してください：

```bash
cp config.json.example config.json
```

`config.json`を編集：

```json
{
    "discord_webhook_url": "YOUR_DISCORD_WEBHOOK_URL_HERE",
    "rss_feeds": [
        {
            "name": "Tech News",
            "url": "https://example.com/rss"
        },
        {
            "name": "English Tech News",
            "url": "https://example.com/en/rss",
            "translate": true
        }
    ],
    "check_interval_minutes": 15,
    "max_articles_per_feed": 5
}
```

### 3. Discord Webhook URLの取得

1. Discordサーバーの設定 → 連携サービス → ウェブフック
2. 「新しいウェブフック」をクリック
3. ウェブフックURLをコピーして`config.json`に貼り付け

## 使用方法

### 継続実行（推奨）

```bash
python rss_discord_bot.py
```

### 一度だけ実行（テスト用）

```bash
python rss_discord_bot.py --once
```

## 設定項目

- `discord_webhook_url`: Discord WebhookのURL
- `rss_feeds`: 監視するRSSフィードのリスト
  - `name`: フィード名（Discord投稿時に表示）
  - `url`: RSSフィードのURL
  - `translate`: 翻訳機能の有効/無効（オプション、英語記事の場合にtrue）
- `check_interval_minutes`: チェック間隔（分、デフォルト15分）
- `max_articles_per_feed`: フィードあたりの最大記事数（デフォルト5件）

## ログ

- `rss_bot.log`: 実行ログファイル
- `seen_articles.json`: 投稿済み記事のID管理

## 投稿メッセージ形式

各記事は以下の形式でDiscordに投稿されます：

```
**フィード名**
📰 記事タイトル（翻訳機能有効時は日本語）
🔗 記事リンク
🐦 [Xに投稿](https://x.com/intent/post?text=...)
```

## 翻訳機能

- 英語記事を日本語に自動翻訳
- フィード毎に`"translate": true`で有効化
- Discord表示は日本語、X投稿リンクは元の英語タイトル
- 翻訳失敗時は元のタイトルを表示

## 注意事項

- 初回実行時は大量の記事が投稿される可能性があります
- Discord APIの制限により、投稿間隔を1秒空けています
- RSSフィードが利用できない場合はログに記録されます
- 翻訳機能は無料のGoogle Translate APIを使用

## トラブルシューティング

### Discord Webhookエラー
- WebhookURLが正しく設定されているか確認
- Discordサーバーの権限を確認

### RSS取得エラー
- RSSフィードのURLが正しいか確認
- インターネット接続を確認
- RSS 2.0フォーマットに対応しているか確認

### 翻訳エラー
- インターネット接続を確認
- 翻訳失敗時は元のタイトルで投稿継続

### 記事が重複投稿される
- `seen_articles.json`ファイルを削除して再実行

## ファイル構成

```
├── rss_discord_bot.py    # メインプログラム
├── config.json.example  # 設定ファイルのサンプル
├── config.json          # 設定ファイル（ユーザーが作成）
├── requirements.txt     # 依存関係
├── .gitignore          # Git除外設定
├── seen_articles.json   # 投稿済み記事管理（自動生成）
├── rss_bot.log         # 実行ログ（自動生成）
└── README.md           # このファイル
```

## セキュリティ注意事項

- `config.json`には機密情報（Webhook URL）が含まれるため、Gitリポジトリにコミットしないでください
- `.gitignore`で`config.json`は除外設定済みです
- `config.json.example`をテンプレートとして使用してください