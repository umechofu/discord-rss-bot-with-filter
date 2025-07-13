# RSS Bot 定時配信設定ガイド

## cronタブの設定方法

### 1. cronタブの編集
```bash
crontab -e
```

### 2. 以下の行を追加（1日3回：8時・12時・17時）
```bash
# RSS Bot 定時配信 - 毎日8時・12時・17時に実行
0 8 * * * /Users/shusakuumemoto/docsLocal/management/discord-rss-bot/scheduled_rss.sh
0 12 * * * /Users/shusakuumemoto/docsLocal/management/discord-rss-bot/scheduled_rss.sh
0 17 * * * /Users/shusakuumemoto/docsLocal/management/discord-rss-bot/scheduled_rss.sh
```

### 3. cronの時刻設定説明
```
# ┌───────────── 分 (0 - 59)
# │ ┌─────────── 時 (0 - 23)
# │ │ ┌───────── 日 (1 - 31)
# │ │ │ ┌─────── 月 (1 - 12)
# │ │ │ │ ┌───── 曜日 (0 - 7) (日曜日は0と7)
# │ │ │ │ │
# * * * * * 実行するコマンド
```

### 4. cronの状態確認
```bash
# 現在のcronタブ確認
crontab -l

# cronサービスの状態確認
sudo systemctl status cron  # Linux
# または
sudo launchctl list | grep cron  # macOS
```

### 5. ログの確認
```bash
# RSS Bot専用ログ
tail -f /Users/shusakuumemoto/docsLocal/management/discord-rss-bot/scheduled_rss.log

# システムcronログ
tail -f /var/log/cron  # Linux
tail -f /var/log/system.log | grep cron  # macOS
```

## トラブルシューティング

### よくある問題
1. **実行権限エラー**
   ```bash
   chmod +x scheduled_rss.sh
   ```

2. **パスエラー**
   - スクリプト内のパスが正しいか確認
   - 絶対パスを使用する

3. **仮想環境エラー**
   ```bash
   # 仮想環境のパスを確認
   which python
   ```

### 手動テスト
```bash
# スクリプトを手動実行してテスト
cd /Users/shusakuumemoto/docsLocal/management/discord-rss-bot
./scheduled_rss.sh
```

## 期待される動作

### 配信スケジュール
- **朝8時**: 1記事配信（主にはてブ人気記事）
- **昼12時**: 1記事配信（主にZenn記事）
- **夕方17時**: 1記事配信（主にnote記事）

### 記事の種類
- はてなブックマーク IT人気記事（AI・デザイン関連）
- 深津貴之（AI・プロダクト関連）
- Zenn デザイン記事（技術的なデザイン記事）

### ログの確認方法
毎回の実行結果は `scheduled_rss.log` に記録されます。