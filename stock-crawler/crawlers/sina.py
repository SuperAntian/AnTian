# -*- coding: utf-8 -*-
"""
新浪财经爬虫（更新版本）
"""

from crawlers.base import BaseCrawler
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time
import json


class SinaNewsCrawler(BaseCrawler):
    """
    新浪财经爬虫
    """
    
    def __init__(self):
        super().__init__(name='SinaNewsCrawler')
    
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
        
        # 新浪财经新闻列表接口
        base_url = 'https://feed.sina.com.cn/api/roll/get'
        
        for p in range(page, page + num_pages):
            try:
                params = {
                    'pageid': 155,  # 股票频道
                    'num': 20,
                    'page': p
                }
                
                resp = self.request(base_url, params=params)
                if not resp:
                    continue
                
                try:
                    data = resp.json()
                except json.JSONDecodeError:
                    logger.warning(f'新浪财经: JSON解析失败')
                    continue
                
                if not data or data.get('status') != 1:
                    logger.warning(f'新浪财经: API返回异常状态')
                    continue
                
                articles = data.get('result', {}).get('data', [])
                
                for item in articles:
                    try:
                        title = clean_title(item.get('title', ''))
                        url = clean_url(item.get('url', ''))
                        
                        if not title or not url:
                            continue
                        
                        news = {
                            'source': '新浪财经',
                            'title': title,
                            'url': url,
                            'publish_time': item.get('ctime', ''),
                            'summary': item.get('intro', '')
                        }
                        all_news.append(news)
                    except Exception as item_e:
                        logger.debug(f'新浪财经: 解析单条新闻失败 - {str(item_e)}')
                        continue
                
                logger.info(f'新浪财经: 成功爬取第 {p} 页，获得 {len(articles)} 条新闻')
                time.sleep(get_random_delay())
            
            except Exception as e:
                logger.error(f'新浪财经: 爬取第 {p} 页失败 - {str(e)}')
                continue
        
        logger.info(f'新浪财经: 共爬取 {len(all_news)} 条新闻')
        return all_news
