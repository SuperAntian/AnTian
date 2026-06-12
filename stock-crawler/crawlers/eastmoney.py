# -*- coding: utf-8 -*-
"""
东方财富爬虫
"""

from crawlers.base import BaseCrawler
from config import EASTMONEY_API_URL, EASTMONEY_CHANNEL, EASTMONEY_NEWS_PER_PAGE
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time


class EastmoneyNewsCrawler(BaseCrawler):
    """
    东方财富爬虫
    """
    
    def __init__(self):
        super().__init__(name='EastmoneyNewsCrawler')
        self.api_url = EASTMONEY_API_URL
    
    def fetch(self, page=1, num_pages=3):
        """
        爬取东方财富新闻
        
        Args:
            page: 起始页码
            num_pages: 爬取页数
        
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        for p in range(page, page + num_pages):
            try:
                params = {
                    'channelid': EASTMONEY_CHANNEL,
                    'pageindex': p,
                    'pagesize': EASTMONEY_NEWS_PER_PAGE
                }
                
                resp = self.request(self.api_url, params=params)
                if not resp:
                    continue
                
                data = resp.json()
                articles = data.get('result', {}).get('data', [])
                
                for item in articles:
                    news = {
                        'source': '东方财富',
                        'title': clean_title(item.get('title', '')),
                        'url': clean_url(item.get('url', '')),
                        'publish_time': item.get('showtime', ''),
                        'summary': item.get('summary', '')
                    }
                    all_news.append(news)
                
                logger.info(f'东方财富: 成功爬取第 {p} 页，获得 {len(articles)} 条新闻')
                time.sleep(get_random_delay())
            
            except Exception as e:
                logger.error(f'东方财富: 爬取第 {p} 页失败 - {str(e)}')
                continue
        
        logger.info(f'东方财富: 共爬取 {len(all_news)} 条新闻')
        return all_news
