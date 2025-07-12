#!/usr/bin/env python3
import json
import time
import logging
import hashlib
import os
from datetime import datetime
from typing import List, Dict, Set

# Python 3.13 compatibility fix for feedparser
try:
    import cgi
except ImportError:
    # For Python 3.13+, create a minimal cgi module replacement
    import sys
    from types import ModuleType
    
    cgi = ModuleType('cgi')
    cgi.parse_header = lambda value: (value.split(';')[0].strip(), {})
    sys.modules['cgi'] = cgi

import feedparser
import requests

class RSSDiscordBot:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.seen_articles_file = "seen_articles.json"
        self.seen_articles = self.load_seen_articles()
        self.setup_logging()
    
    def load_config(self, config_file: str) -> Dict:
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"Config file {config_file} not found")
            raise
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON in config file {config_file}")
            raise
    
    def load_seen_articles(self) -> Set[str]:
        try:
            with open(self.seen_articles_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return set(data)
        except FileNotFoundError:
            return set()
        except json.JSONDecodeError:
            logging.warning("Invalid JSON in seen articles file, starting fresh")
            return set()
    
    def save_seen_articles(self):
        try:
            with open(self.seen_articles_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.seen_articles), f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.error(f"Failed to save seen articles: {e}")
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('rss_bot.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def get_article_id(self, article) -> str:
        """Generate unique ID for article based on title and link"""
        content = f"{article.get('title', '')}{article.get('link', '')}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def matches_keywords(self, text: str, keywords: List[str], mode: str, case_sensitive: bool = False) -> bool:
        """Check if text matches the keyword filter criteria"""
        if not keywords:
            return True  # No keywords means no filtering
        
        if not case_sensitive:
            text = text.lower()
            keywords = [k.lower() for k in keywords]
        
        # Check if any keyword is found in the text
        matches = any(keyword in text for keyword in keywords)
        
        # Return based on mode
        if mode == 'include':
            return matches  # True if any keyword is found
        else:  # exclude mode
            return not matches  # True if no keywords are found
    
    def apply_keyword_filters(self, article: Dict, feed_config: Dict) -> bool:
        """Apply both global and feed-specific keyword filters"""
        # Combine title and summary for searching
        search_text = f"{article['title']} {article['summary']}"
        
        # Apply global keywords filter first (if exists)
        global_keywords_config = self.config.get('global_keywords', {})
        if global_keywords_config:
            keywords = global_keywords_config.get('keywords', [])
            mode = global_keywords_config.get('mode', 'exclude')
            case_sensitive = global_keywords_config.get('case_sensitive', False)
            
            if not self.matches_keywords(search_text, keywords, mode, case_sensitive):
                logging.debug(f"Article filtered by global keywords: {article['title']}")
                return False
        
        # Apply feed-specific keywords filter
        if 'keywords' in feed_config:
            keywords = feed_config['keywords']
            mode = feed_config.get('keyword_mode', 'include')
            case_sensitive = feed_config.get('case_sensitive', False)
            
            if not self.matches_keywords(search_text, keywords, mode, case_sensitive):
                logging.debug(f"Article filtered by feed keywords: {article['title']}")
                return False
        
        return True
    
    def parse_rss_feed(self, feed_url: str, feed_config: Dict) -> List[Dict]:
        try:
            feed = feedparser.parse(feed_url)
            if feed.bozo:
                logging.warning(f"RSS feed parsing warning for {feed_url}: {feed.bozo_exception}")
            
            articles = []
            max_articles = self.config.get('max_articles_per_feed', 5)
            
            for entry in feed.entries[:max_articles]:
                article_id = self.get_article_id(entry)
                
                if article_id not in self.seen_articles:
                    article = {
                        'id': article_id,
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'published': entry.get('published', ''),
                        'summary': entry.get('summary', '')
                    }
                    
                    # Apply keyword filters
                    if self.apply_keyword_filters(article, feed_config):
                        articles.append(article)
            
            return articles
        
        except Exception as e:
            logging.error(f"Error parsing RSS feed {feed_url}: {e}")
            return []
    
    def send_to_discord(self, message: str) -> bool:
        try:
            webhook_url = self.config['discord_webhook_url']
            payload = {
                'content': message,
                'username': 'RSS Bot'
            }
            
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            
            logging.info("Message sent to Discord successfully")
            return True
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to send message to Discord: {e}")
            return False
    
    def translate_text(self, text: str) -> str:
        try:
            # Google Translate API (無料版)
            url = "https://translate.googleapis.com/translate_a/single"
            params = {
                'client': 'gtx',
                'sl': 'en',
                'tl': 'ja',
                'dt': 't',
                'q': text
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            result = response.json()
            translated = result[0][0][0]
            
            return translated
        
        except Exception as e:
            logging.warning(f"Translation failed: {e}")
            return text  # 翻訳に失敗した場合は元のテキストを返す
    
    def format_article_message(self, article: Dict, feed_name: str, feed_config: Dict) -> str:
        title = article['title']
        link = article['link']
        
        # 翻訳が必要な場合
        if feed_config.get('translate', False):
            translated_title = self.translate_text(title)
            display_title = translated_title
            # X投稿用は元の英語タイトルを使用
            tweet_title = title
        else:
            display_title = title
            tweet_title = title
        
        # X(Twitter)への投稿リンクを作成（元のタイトルを使用）
        tweet_text = f"\n\n{tweet_title} {link}"
        x_intent_url = f"https://x.com/intent/post?text={requests.utils.quote(tweet_text)}"
        
        message = f"**{feed_name}**\n"
        message += f"📰 {display_title}\n"
        message += f"🔗 {link}\n"
        message += f"🐦 [Xに投稿]({x_intent_url})"
        
        return message
    
    def process_feeds(self):
        logging.info("Starting RSS feed processing")
        
        for feed_config in self.config['rss_feeds']:
            feed_name = feed_config['name']
            feed_url = feed_config['url']
            
            logging.info(f"Processing feed: {feed_name}")
            
            articles = self.parse_rss_feed(feed_url, feed_config)
            
            if articles:
                logging.info(f"Found {len(articles)} new articles matching filters for {feed_name}")
            else:
                logging.info(f"No new articles matching filters for {feed_name}")
            
            for article in articles:
                message = self.format_article_message(article, feed_name, feed_config)
                
                if self.send_to_discord(message):
                    self.seen_articles.add(article['id'])
                    logging.info(f"Sent article: {article['title']}")
                else:
                    logging.error(f"Failed to send article: {article['title']}")
                
                time.sleep(1)  # Rate limiting
        
        self.save_seen_articles()
        logging.info("RSS feed processing completed")
    
    def run_once(self):
        """Run the bot once"""
        self.process_feeds()
    
    def run_forever(self):
        """Run the bot continuously with specified interval"""
        interval_minutes = self.config.get('check_interval_minutes', 60)
        interval_seconds = interval_minutes * 60
        
        logging.info(f"Starting RSS Discord Bot with {interval_minutes} minute intervals")
        
        while True:
            try:
                self.process_feeds()
                logging.info(f"Sleeping for {interval_minutes} minutes...")
                time.sleep(interval_seconds)
            
            except KeyboardInterrupt:
                logging.info("Bot stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying


if __name__ == "__main__":
    import sys
    
    bot = RSSDiscordBot()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        bot.run_once()
    else:
        bot.run_forever()