# -*- coding: utf-8 -*-
"""
Tushare财经数据爆虫
"""

from utils.logger import logger
from utils.helpers import clean_title, clean_url
import time

try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False
    logger.warning('Tushare 未安装，请运行: pip install tushare')


class TushareNewsCrawler:
    """
    使用Tushare API获取财经新闻
    """
    
    def __init__(self, token='demo'):
        self.name = 'TushareNewsCrawler'
        self.token = token
        if TUSHARE_AVAILABLE:
            try:
                self.pro = ts.pro_connect(token=token)
            except Exception as e:
                logger.error(f'Tushare 连接失败: {str(e)}')
                self.pro = None
    
    def fetch(self, limit=100):
        """
        获取财经新闻
        
        Args:
            limit: 获取数量
        
        Returns:
            list: 新闻列表
        """
        all_news = []
        
        if not TUSHARE_AVAILABLE:
            logger.error('Tushare 未安装')
            return all_news
        
        if not self.pro:
            logger.error('Tushare 未正常连接')
            return all_news
        
        try:
            logger.info(f'{self.name}: 开始获取财经新闻...')
            
            # 获取新闻数据
            df = self.pro.news(src='sina', limit=limit)
            
            if df is None or len(df) == 0:
                logger.warning(f'{self.name}: 没有获取到数据')
                return all_news
            
            for _, row in df.iterrows():
                try:
                    title = clean_title(row.get('title', ''))
                    content = row.get('content', '')
                    ctime = row.get('ctime', '')
                    
                    if not title:
                        continue
                    
                    news = {
                        'source': 'Tushare',
                        'title': title,
                        'url': content,
                        'publish_time': str(ctime),
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
