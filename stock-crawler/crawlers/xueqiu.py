# -*- coding: utf-8 -*-
"""
雪球爬虫（更新版本 - 使用公开接口）
"""

from crawlers.base import BaseCrawler
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time


class XueqiuNewsCrawler(BaseCrawler):
    """
    雪球爬虫
    """
    
    def __init__(self, token=None):
        super().__init__(name='XueqiuNewsCrawler')
        self.token = token
    
    def get_headers(self):
        """
        获取请求头
        """
        headers = super().get_headers()
        headers['Referer'] = 'https://xueqiu.com/'
        headers['X-Requested-With'] = 'XMLHttpRequest'
        if self.token:
            headers['Cookie'] = f'xq_a_token={self.token}'
        return headers
    
    def fetch(self, stock_code='SH600519', count=20):
        """
        爬取雪球新闻
        
        Args:
            stock_code: 股票代码
            count: 爬取数量
        
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        try:
            # 雪球API
            url = 'https://xueqiu.com/statuses/stock_timeline.json'
            params = {
                'symbol': stock_code,
                'count': count
            }
            
            resp = self.request(url, params=params)
            if not resp:
                logger.warning(f'雪球: 请求失败')
                return all_news
            
            data = resp.json()
            articles = data.get('list', [])
            
            for item in articles:
                try:
                    title = clean_title(item.get('title', ''))
                    target = item.get('target', '')
                    url = clean_url(f'https://xueqiu.com{target}') if target else ''
                    
                    if not title or not url:
                        continue
                    
                    news = {
                        'source': '雪球',
                        'title': title,
                        'url': url,
                        'publish_time': item.get('created_at', ''),
                        'summary': item.get('text', '')[:200]
                    }
                    all_news.append(news)
                except Exception as item_e:
                    logger.debug(f'雪球: 解析单条新闻失败 - {str(item_e)}')
                    continue
            
            logger.info(f'雪球: 成功爬取 {stock_code}，获得 {len(articles)} 条新闻')
        
        except Exception as e:
            logger.error(f'雪球: 爬取失败 - {str(e)}')
        
        return all_news
