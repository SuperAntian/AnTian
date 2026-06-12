# -*- coding: utf-8 -*-
"""
同花顺爬虫
"""

from crawlers.base import BaseCrawler
from config import THS_BASE_URL
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
from bs4 import BeautifulSoup
import time


class THSNewsCrawler(BaseCrawler):
    """
    同花顺爬虫
    """
    
    def __init__(self):
        super().__init__(name='THSNewsCrawler')
        self.base_url = THS_BASE_URL
    
    def fetch(self, page=1, num_pages=3):
        """
        爬取同花顺新闻
        
        Args:
            page: 起始页码
            num_pages: 爬取页数
        
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        for p in range(page, page + num_pages):
            try:
                url = f'{self.base_url}/index_{p}.shtml'
                resp = self.request(url)
                if not resp:
                    continue
                
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'lxml')
                
                # 查找新闻列表
                news_items = soup.select('.m-news-list > li')
                
                for item in news_items:
                    try:
                        title_elem = item.select_one('a')
                        date_elem = item.select_one('.date')
                        
                        if not title_elem:
                            continue
                        
                        news = {
                            'source': '同花顺',
                            'title': clean_title(title_elem.get('title', '')),
                            'url': clean_url(title_elem.get('href', '')),
                            'publish_time': date_elem.text if date_elem else ''
                        }
                        all_news.append(news)
                    except Exception as item_e:
                        logger.debug(f'同花顺: 解析单条新闻失败 - {str(item_e)}')
                        continue
                
                logger.info(f'同花顺: 成功爬取第 {p} 页，获得 {len(news_items)} 条新闻')
                time.sleep(get_random_delay())
            
            except Exception as e:
                logger.error(f'同花顺: 爬取第 {p} 页失败 - {str(e)}')
                continue
        
        logger.info(f'同花顺: 共爬取 {len(all_news)} 条新闻')
        return all_news
