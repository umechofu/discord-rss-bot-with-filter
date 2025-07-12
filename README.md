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
- **キーワードフィルタリング機能（新機能）**
  - 特定のキーワードを含む記事のみを取得（includeモード）
  - 特定のキーワードを含む記事を除外（excludeモード）
  - グローバルキーワードと個別フィード設定の両方に対応
  - 大文字小文字の区別を選択可能
- エラーハンドリングとログ機能

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/tejastice/discord-rss-bot.git
cd discord-rss-bot
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
    "global_keywords": {
        "keywords": ["広告", "PR", "sponsored"],
        "mode": "exclude",
        "case_sensitive": false
    },
    "rss_feeds": [
        {
            "name": "Tech News",
            "url": "https://example.com/rss",
            "keywords": ["AI", "Python", "JavaScript"],
            "keyword_mode": "include",
            "case_sensitive": false
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

#### キーワードフィルタリング設定

- **global_keywords**: 全フィードに適用されるグローバルフィルター
  - `keywords`: フィルタリング対象のキーワード配列
  - `mode`: "include"（含む記事のみ）または "exclude"（含む記事を除外）
  - `case_sensitive`: 大文字小文字を区別するか（true/false）

- **フィード別設定**: 各RSSフィードに個別のキーワードフィルターを設定可能
  - `keywords`: そのフィード専用のキーワード配列
  - `keyword_mode`: "include" または "exclude"
  - `case_sensitive`: 大文字小文字の区別

フィルタリングは記事のタイトルとサマリー（説明文）の両方を対象に行われます。

### 3. Discord Webhook URLの取得

1. Discordサーバーの設定 → 連携サービス → ウェブフック
2. 「新しいウェブフック」をクリック
3. ウェブフックURLをコピーして`config.json`に貼り付け

## 使用方法

### 自動セットアップ付き実行（推奨）

仮想環境を自動的に作成・管理する実行スクリプトを使用できます：

**Mac/Linux:**
```bash
# 継続実行
./run_mac.sh

# テスト実行（一度だけ）
./test_mac.sh
```

**Windows:**
```cmd
# 継続実行
run_windows.bat

# テスト実行（一度だけ）
test_windows.bat
```

### 手動実行

仮想環境を手動で管理する場合：

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境をアクティベート
# Mac/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt

# 継続実行
python rss_discord_bot.py

# テスト実行（一度だけ）
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
├── requirements.md      # 要件定義書
├── run_mac.sh          # Mac/Linux実行スクリプト
├── run_windows.bat     # Windows実行スクリプト
├── test_mac.sh         # Mac/Linuxテストスクリプト
├── test_windows.bat    # Windowsテストスクリプト
├── .gitignore          # Git除外設定
├── venv/               # 仮想環境（自動生成、Git除外）
├── seen_articles.json   # 投稿済み記事管理（自動生成）
├── rss_bot.log         # 実行ログ（自動生成）
└── README.md           # このファイル
```

## セキュリティ注意事項

- `config.json`には機密情報（Webhook URL）が含まれるため、Gitリポジトリにコミットしないでください
- `.gitignore`で`config.json`は除外設定済みです
- `config.json.example`をテンプレートとして使用してください