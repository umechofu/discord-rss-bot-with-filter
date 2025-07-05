@echo off
setlocal

REM Discord RSS Bot - Windows テスト実行スクリプト

echo Discord RSS Bot をテスト実行しています...

REM スクリプトのディレクトリに移動
cd /d "%~dp0"

REM 仮想環境が存在しない場合は作成
if not exist "venv" (
    echo 仮想環境を作成しています...
    python -m venv venv
)

REM 仮想環境をアクティベート
echo 仮想環境をアクティベートしています...
call venv\Scripts\activate.bat

REM 依存関係をインストール
echo 依存関係をインストールしています...
pip install -r requirements.txt

REM 設定ファイルの確認
if not exist "config.json" (
    echo ❌ エラー: config.json が見つかりません
    echo config.json.example を config.json にコピーして設定を編集してください:
    echo copy config.json.example config.json
    pause
    exit /b 1
)

REM Botをテスト実行（一度だけ）
echo Discord RSS Bot をテスト実行します（一度だけ）...
python rss_discord_bot.py --once

echo テスト実行完了しました。

REM 仮想環境を終了
call venv\Scripts\deactivate.bat

pause