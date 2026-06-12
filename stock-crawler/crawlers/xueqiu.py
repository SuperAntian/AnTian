# -*- coding: utf-8 -*-
"""
雪球爬虫
"""

from crawlers.base import BaseCrawler
from config import XUEQIU_API_URL, XUEQIU_TOKEN, XUEQIU_DEFAULT_STOCK
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time


class XueqiuNewsCrawler(BaseCrawler):
    """
    雪球爬虫（需要登录token）
    """
    
    def __init__(self, token=None):
        super().__init__(name='XueqiuNewsCrawler')
        self.api_url = XUEQIU_API_URL
        self.token = token or XUEQIU_TOKEN
    
    def get_headers(self):
        """
        获取请求头
        """
        headers = super().get_headers()
        if self.token:
            headers['Cookie'] = f'xq_a_token={self.token}'
        return headers
    
    def fetch(self, stock_code=None, count=20):
        """
        爬取雪球新闻
        
        Args:
            stock_code: 股票代码（如 'SH600519'）
            count: 爬取数量
        
        Returns:
            list: 新闻列表
        """
        stock_code = stock_code or XUEQIU_DEFAULT_STOCK
        all_news = []
        
        if not self.token:
            logger.warning('雪球: 未设置token，无法爬取。请在config中设置XUEQIU_TOKEN或手动传入')
            return all_news
        
        try:
            params = {
                'symbol': stock_code,
                'count': count
            }
            
            resp = self.request(self.api_url, params=params)
            if not resp:
                return all_news
            
            data = resp.json()
            articles = data.get('list', [])
            
            for item in articles:
                news = {
                    'source': '雪球',
                    'title': clean_title(item.get('title', '')),
                    'url': clean_url(f"https://xueqiu.com{item.get('target', '')}"),
                    'publish_time': item.get('created_at', ''),
                    'summary': item.get('text', '')[:200]  # 截取前200字
                }
                all_news.append(news)
            
            logger.info(f'雪球: 成功爬取 {stock_code}，获得 {len(articles)} 条新闻')
        
        except Exception as e:
            logger.error(f'雪球: 爬取失败 - {str(e)}')
        
        return all_news
