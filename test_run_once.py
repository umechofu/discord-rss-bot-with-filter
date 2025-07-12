#!/usr/bin/env python3
"""実際のRSSフィードでフィルタリング機能をテストするスクリプト（Discordには投稿しない）"""
import json
import logging
from rss_discord_bot import RSSDiscordBot

class TestBot(RSSDiscordBot):
    """テスト用のボット（実際にはDiscordに投稿しない）"""
    
    def send_to_discord(self, message: str) -> bool:
        """Discordへの投稿をシミュレート（実際には投稿しない）"""
        print("\n--- Discord投稿シミュレーション ---")
        print(message)
        print("-" * 40)
        return True

def main():
    # テスト用設定でボットを初期化
    bot = TestBot("test_config.json")
    
    # ログレベルをDEBUGに設定してフィルタリング情報を表示
    logging.getLogger().setLevel(logging.DEBUG)
    
    print("=== RSS フィード & キーワードフィルタリングテスト ===\n")
    print("注意: これはテストモードです。実際にはDiscordに投稿されません。\n")
    
    # 一度だけ実行
    bot.run_once()
    
    print("\n=== テスト完了 ===")

if __name__ == "__main__":
    main()