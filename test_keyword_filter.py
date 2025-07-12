#!/usr/bin/env python3
"""キーワードフィルタリング機能のテストスクリプト"""
import json
from rss_discord_bot import RSSDiscordBot

def test_keyword_filtering():
    # テスト用の設定を読み込み
    bot = RSSDiscordBot("test_config.json")
    
    # テスト用の記事データ
    test_articles = [
        {
            'title': 'New AI breakthrough in GPT technology',
            'summary': 'Researchers announce major advances in machine learning'
        },
        {
            'title': 'JavaScript framework comparison 2024',
            'summary': 'Comparing React, Vue, and Angular performance'
        },
        {
            'title': '広告: 最新のプロダクト紹介',
            'summary': 'この商品をPRします'
        },
        {
            'title': 'Python tutorial for beginners',
            'summary': 'Learn Python programming from scratch'
        },
        {
            'title': 'Sponsored content: Best tools',
            'summary': 'Check out these amazing sponsored tools'
        }
    ]
    
    # フィード設定例
    feed_configs = [
        {
            'name': 'AI Focus',
            'keywords': ['AI', 'GPT', 'machine learning'],
            'keyword_mode': 'include',
            'case_sensitive': False
        },
        {
            'name': 'Programming',
            'keywords': ['Python', 'JavaScript', 'React', 'Vue'],
            'keyword_mode': 'include',
            'case_sensitive': False
        },
        {
            'name': 'All Tech (no ads)',
            # グローバルキーワードで広告を除外
        }
    ]
    
    print("=== キーワードフィルタリングテスト ===\n")
    
    for feed_config in feed_configs:
        print(f"フィード: {feed_config['name']}")
        print("-" * 40)
        
        for article in test_articles:
            # フィルタリングテスト
            if bot.apply_keyword_filters(article, feed_config):
                print(f"✅ パス: {article['title']}")
            else:
                print(f"❌ 除外: {article['title']}")
        
        print("\n")

if __name__ == "__main__":
    test_keyword_filtering()