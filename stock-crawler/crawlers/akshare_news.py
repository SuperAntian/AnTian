# -*- coding: utf-8 -*-
"""
Akshare财经数据爆虫
"""

from utils.logger import logger
from utils.helpers import clean_title, clean_url, get_random_delay
import time

try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning('Akshare 未安装，请运行: pip install akshare')


class AkshareNewsCrawler:
    """
    使用Akshare获取财经新闻
    """
    
    def __init__(self):
        self.name = 'AkshareNewsCrawler'
        if not AKSHARE_AVAILABLE:
            logger.error('Akshare 未安装')
    
    def fetch(self, limit=100):
        """
        获取财经新闻
        
        Args:
            limit: 获取数量
        
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        if not AKSHARE_AVAILABLE:
            logger.error('Akshare 未安装')
            return all_news
        
        try:
            logger.info(f'{self.name}: 开始获取财经新闻...')
            
            # 获取股票新闻
            df = ak.stock_news()
            
            if df is None or len(df) == 0:
                logger.warning(f'{self.name}: 没有获取到数据')
                return all_news
            
            for idx, row in df.iterrows():
                if idx >= limit:
                    break
                
                try:
                    title = clean_title(row.get('title', '') if 'title' in row else str(row.get(0, '')))
                    url = clean_url(row.get('url', '') if 'url' in row else row.get(1, ''))
                    publish_time = row.get('time', '') if 'time' in row else row.get(2, '')
                    
                    if not title or not url:
                        continue
                    
                    news = {
                        'source': 'Akshare',
                        'title': title,
                        'url': url,
                        'publish_time': str(publish_time),
                        'summary': ''
                    }
                    all_news.append(news)
                
                except Exception as item_e:
                    logger.debug(f'{self.name}: 解析单条新闻失败 - {str(item_e)}')
                    continue
            
            logger.info(f'{self.name}: 成功获取 {len(all_news)} 条新闻')
        
        except Exception as e:
            logger.error(f'{self.name}: 获取失败 - {str(e)}')
        
        return all_news
