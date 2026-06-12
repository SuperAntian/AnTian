# -*- coding: utf-8 -*-
"""
东方财富爬虫（更新版本）
"""

from crawlers.base import BaseCrawler
from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
from bs4 import BeautifulSoup
import time


class EastmoneyNewsCrawler(BaseCrawler):
    """
    东方财富爬虫（HTML解析版本）
    """
    
    def __init__(self):
        super().__init__(name='EastmoneyNewsCrawler')
    
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
        
        # 东方财富新闻中心
        base_url = 'https://news.eastmoney.com/news'
        
        for p in range(page, page + num_pages):
            try:
                params = {'type': 'gn', 'page': p}  # 国内财经新闻
                resp = self.request(base_url, params=params)
                
                if not resp:
                    continue
                
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'lxml')
                
                # 查找新闻列表项
                news_items = soup.select('div.news-list2 ul li')
                
                if not news_items:
                    # 尝试其他选择器
                    news_items = soup.select('li.tagContent')
                
                for item in news_items:
                    try:
                        # 找标题链接
                        link = item.select_one('a')
                        if not link:
                            continue
                        
                        title = clean_title(link.get_text(strip=True))
                        url = clean_url(link.get('href', ''))
                        
                        # 确保URL是完整的
                        if url and not url.startswith('http'):
                            url = 'https://news.eastmoney.com' + url
                        
                        if not title or not url:
                            continue
                        
                        # 找时间
                        time_elem = item.select_one('span.date')
                        publish_time = time_elem.get_text(strip=True) if time_elem else ''
                        
                        news = {
                            'source': '东方财富',
                            'title': title,
                            'url': url,
                            'publish_time': publish_time,
                            'summary': ''
                        }
                        all_news.append(news)
                    except Exception as item_e:
                        logger.debug(f'东方财富: 解析单条新闻失败 - {str(item_e)}')
                        continue
                
                logger.info(f'东方财富: 成功爬取第 {p} 页，获得 {len(news_items)} 条新闻')
                time.sleep(get_random_delay())
            
            except Exception as e:
                logger.error(f'东方财富: 爬取第 {p} 页失败 - {str(e)}')
                continue
        
        logger.info(f'东方财富: 共爬取 {len(all_news)} 条新闻')
        return all_news
