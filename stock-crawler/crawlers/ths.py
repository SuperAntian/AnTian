# -*- coding: utf-8 -*-
"""
同花顺爬虫（更新版本）
"""

from crawlers.base import BaseCrawler
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
        
        base_url = 'https://news.10jqka.com.cn/'
        
        for p in range(page, page + num_pages):
            try:
                # 构建URL
                if p == 1:
                    url = base_url
                else:
                    url = f'{base_url}today_list/index_{p}.shtml'
                
                resp = self.request(url)
                if not resp:
                    continue
                
                resp.encoding = 'utf-8'
                soup = BeautifulSoup(resp.text, 'lxml')
                
                # 查找新闻列表
                news_items = soup.select('.m-news-list li')
                
                if not news_items:
                    logger.warning(f'同花顺: 第 {p} 页未找到新闻')
                    continue
                
                for item in news_items:
                    try:
                        # 找标题链接
                        link = item.select_one('a')
                        if not link:
                            continue
                        
                        title = clean_title(link.get_text(strip=True))
                        href = link.get('href', '')
                        
                        # 处理相对URL
                        if href and not href.startswith('http'):
                            href = 'https://news.10jqka.com.cn' + href
                        
                        url = clean_url(href)
                        
                        if not title or not url:
                            continue
                        
                        # 找时间
                        time_elem = item.select_one('.date')
                        publish_time = time_elem.get_text(strip=True) if time_elem else ''
                        
                        news = {
                            'source': '同花顺',
                            'title': title,
                            'url': url,
                            'publish_time': publish_time,
                            'summary': ''
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
