#!/bin/bash

# RSS Bot 定時実行スクリプト
# 使用方法: ./scheduled_rss.sh

# スクリプトがあるディレクトリに移動
cd "$(dirname "$0")"

# 仮想環境をアクティベート
source venv/bin/activate

# ログファイルの設定
LOG_FILE="scheduled_rss.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] RSS Bot 定時実行開始" >> $LOG_FILE

# RSS Botを実行（1回だけ）
python rss_discord_bot.py --once >> $LOG_FILE 2>&1

echo "[$TIMESTAMP] RSS Bot 定時実行完了" >> $LOG_FILE
echo "----------------------------------------" >> $LOG_FILE