#!/bin/bash

# Discord RSS Bot - Mac/Linux実行スクリプト

echo "Discord RSS Bot を起動しています..."

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境が存在しない場合は作成
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Trying with --system-site-packages..."
        python3 -m venv --system-site-packages venv
    fi
fi

# 仮想環境をアクティベート
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    
    # 依存関係をインストール
    echo "Installing dependencies..."
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install feedparser requests
else
    echo "Warning: Virtual environment not found, using system Python..."
    echo "Installing dependencies..."
    pip3 install --user feedparser requests
fi

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