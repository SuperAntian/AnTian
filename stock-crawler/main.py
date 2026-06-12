# -*- coding: utf-8 -*-
"""
单次爬取主程序
"""

import time
from datetime import datetime
from config import ENABLED_CRAWLERS, STORAGE_TYPE, PAGES_TO_CRAWL
from crawlers.sina import SinaNewsCrawler
from crawlers.eastmoney import EastmoneyNewsCrawler
from crawlers.ths import THSNewsCrawler
from crawlers.xueqiu import XueqiuNewsCrawler
from storage.csv_storage import CSVStorage
from storage.db_storage import DBStorage
from utils.logger import logger


def crawl_all_news():
    """
    爬取所有启用的数据源
    """
    logger.info('='*50)
    logger.info(f'开始爬取新闻 [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    logger.info('='*50)
    
    all_news = []
    crawlers_map = {
        'sina': SinaNewsCrawler(),
        'eastmoney': EastmoneyNewsCrawler(),
        'ths': THSNewsCrawler(),
        'xueqiu': XueqiuNewsCrawler(),
    }
    
    # 爬取各个数据源
    for crawler_name in ENABLED_CRAWLERS:
        if crawler_name in crawlers_map:
            try:
                logger.info(f'开始爬取 {crawler_name}...')
                crawler = crawlers_map[crawler_name]
                news = crawler.fetch(page=1, num_pages=PAGES_TO_CRAWL)
                all_news.extend(news)
                logger.info(f'{crawler_name} 爬取完成，获得 {len(news)} 条新闻')
            except Exception as e:
                logger.error(f'爬取 {crawler_name} 失败: {str(e)}')
            finally:
                crawlers_map[crawler_name].close()
    
    # 存储数据
    if all_news:
        logger.info(f'共爬取 {len(all_news)} 条新闻')
        
        if STORAGE_TYPE == 'sqlite':
            db = DBStorage()
            db.save_batch(all_news)
            logger.info(f'数据库中共有 {db.get_count()} 条新闻')
        else:
            csv = CSVStorage()
            for news in all_news:
                csv.save(news)
            csv.flush()
    else:
        logger.warning('没有爬取到任何新闻')
    
    logger.info('='*50)
    logger.info(f'爬取完成 [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    logger.info('='*50)


if __name__ == '__main__':
    crawl_all_news()
