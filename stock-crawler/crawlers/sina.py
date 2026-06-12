# -*- coding: utf-8 -*-
"""
新浪财经爬虫
"""

from crawlers.base import BaseCrawler
from config import SINA_API_URL, SINA_PAGEID, SINA_NEWS_PER_PAGE
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time
import random


class SinaNewsCrawler(BaseCrawler):
    """
    新浪财经爬虫
    """
    
    def __init__(self):
        super().__init__(name='SinaNewsCrawler')
        self.api_url = SINA_API_URL
    
    def fetch(self, page=1, num_pages=3):
        """
        爬取新浪财经新闻
        
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
                    'pageid': SINA_PAGEID,
                    'num': SINA_NEWS_PER_PAGE,
                    'page': p
                }
                
                resp = self.request(self.api_url, params=params)
                if not resp:
                    continue
                
                data = resp.json()
                if data.get('status') != 1:
                    logger.warning(f'新浪财经: API返回异常状态 {data.get("status")}')
                    continue
                
                articles = data.get('result', {}).get('data', [])
                
                for item in articles:
                    news = {
                        'source': '新浪财经',
                        'title': clean_title(item.get('title', '')),
                        'url': clean_url(item.get('url', '')),
                        'publish_time': item.get('ctime', ''),
                        'summary': item.get('intro', '')
                    }
                    all_news.append(news)
                
                logger.info(f'新浪财经: 成功爬取第 {p} 页，获得 {len(articles)} 条新闻')
                time.sleep(get_random_delay())
            
            except Exception as e:
                logger.error(f'新浪财经: 爬取第 {p} 页失败 - {str(e)}')
                continue
        
        logger.info(f'新浪财经: 共爬取 {len(all_news)} 条新闻')
        return all_news
