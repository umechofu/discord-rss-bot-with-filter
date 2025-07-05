#!/bin/bash

# Discord RSS Bot - Mac/Linux実行スクリプト

echo "Discord RSS Bot を起動しています..."

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在しない場合は作成
if [ ! -d "venv" ]; then
    echo "仮想環境を作成しています..."
    python3 -m venv venv
fi

# 仮想環境をアクティベート
echo "仮想環境をアクティベートしています..."
source venv/bin/activate

# 依存関係をインストール
echo "依存関係をインストールしています..."
pip install -r requirements.txt

# 設定ファイルの確認
if [ ! -f "config.json" ]; then
    echo "❌ エラー: config.json が見つかりません"
    echo "config.json.example を config.json にコピーして設定を編集してください:"
    echo "cp config.json.example config.json"
    exit 1
fi

# Botを実行
echo "Discord RSS Bot を開始します..."
python rss_discord_bot.py

# 仮想環境を終了
deactivate