# -*- coding: utf-8 -*-
"""
改进的主程序 - 集成 levistock 市场数据
爬取新闻 + 获取实时行情 + 进行数据融合
"""

import time
from datetime import datetime
from config import ENABLED_CRAWLERS, STORAGE_TYPE, PAGES_TO_CRAWL
from config_levistock import ENABLE_MARKET_DATA, ENRICH_NEWS_WITH_MARKET
from crawlers.sina import SinaNewsCrawler
from crawlers.eastmoney import EastmoneyNewsCrawler
from crawlers.ths import THSNewsCrawler
from crawlers.xueqiu import XueqiuNewsCrawler
from crawlers.akshare_news import AkshareNewsCrawler
from crawlers.tushare_news import TushareNewsCrawler
from storage.csv_storage import CSVStorage
from storage.db_storage import DBStorage
from utils.logger import logger
from utils.levistock_fetcher import NewsEnricher, get_market_summary


def crawl_all_news_with_market_data():
    """
    爬取新闻 + 融合市场行情数据的完整流程
    """
    logger.info('='*60)
    logger.info(f'🚀 开始爬取新闻与行情 [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    logger.info('='*60)
    
    all_news = []
    crawlers_map = {
        'sina': SinaNewsCrawler(),
        'eastmoney': EastmoneyNewsCrawler(),
        'ths': THSNewsCrawler(),
        'xueqiu': XueqiuNewsCrawler(),
        'akshare': AkshareNewsCrawler(),
        'tushare': TushareNewsCrawler(),
    }
    
    # ============ 第1步：爬取各个数据源的新闻 ============
    logger.info("\n" + "="*60)
    logger.info("📰 第1步: 爬取新闻")
    logger.info("="*60)
    
    for crawler_name in ENABLED_CRAWLERS:
        if crawler_name in crawlers_map:
            try:
                logger.info(f'\n开始爬取 {crawler_name}...')
                crawler = crawlers_map[crawler_name]
                
                # 处理不同类型的爬虫
                if crawler_name in ['akshare', 'tushare']:
                    # API类爬虫
                    news = crawler.fetch(limit=50)
                else:
                    # 网站爬虫
                    news = crawler.fetch(page=1, num_pages=PAGES_TO_CRAWL)
                
                all_news.extend(news)
                logger.info(f'✅ {crawler_name} 爬取完成，获得 {len(news)} 条新闻')
            except Exception as e:
                logger.error(f'❌ 爬取 {crawler_name} 失败: {str(e)}')
            finally:
                # 关闭连接
                if hasattr(crawler, 'close'):
                    crawler.close()
    
    logger.info(f'\n✅ 共爬取 {len(all_news)} 条新闻')
    
    # ============ 第2步：获取市场数据并融合 ============
    if ENABLE_MARKET_DATA and ENRICH_NEWS_WITH_MARKET and all_news:
        logger.info("\n" + "="*60)
        logger.info("📊 第2步: 融合市场行情数据")
        logger.info("="*60)
        
        try:
            enricher = NewsEnricher()
            
            # 保存市场数据快照
            enricher.save_market_data_snapshot()
            
            # 为新闻关联行情数据
            all_news = enricher.enrich_batch_news(all_news)
            logger.info("✅ 新闻与行情数据融合完成")
            
        except Exception as e:
            logger.error(f"❌ 行情数据融合失败: {str(e)}")
    
    # ============ 第3步：获取市场概览 ============
    if ENABLE_MARKET_DATA:
        logger.info("\n" + "="*60)
        logger.info("📊 第3步: 获取市场概览")
        logger.info("="*60)
        
        try:
            get_market_summary()
        except Exception as e:
            logger.error(f"❌ 获取市场概览失败: {str(e)}")
    
    # ============ 第4步：存储数据 ============
    logger.info("\n" + "="*60)
    logger.info("💾 第4步: 存储数据")
    logger.info("="*60)
    
    if all_news:
        logger.info(f'共处理 {len(all_news)} 条新闻')
        
        if STORAGE_TYPE == 'sqlite':
            db = DBStorage()
            db.save_batch(all_news)
            logger.info(f'✅ 数据库中共有 {db.get_count()} 条新闻')
        else:
            csv = CSVStorage()
            for news in all_news:
                csv.save(news)
            csv.flush()
            logger.info('✅ CSV 文件已保存')
    else:
        logger.warning('⚠️ 没有爬取到任何新闻')
    
    logger.info("\n" + "="*60)
    logger.info(f'✅ 完成爬取与融合 [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]')
    logger.info("="*60 + "\n")


def crawl_all_news():
    """
    原始爬取函数 - 仅爬取新闻（不融合行情）
    保持向后兼容性
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
        'akshare': AkshareNewsCrawler(),
        'tushare': TushareNewsCrawler(),
    }
    
    # 爬取各个数据源
    for crawler_name in ENABLED_CRAWLERS:
        if crawler_name in crawlers_map:
            try:
                logger.info(f'开始爬取 {crawler_name}...')
                crawler = crawlers_map[crawler_name]
                
                # 处理不同类型的爬虫
                if crawler_name in ['akshare', 'tushare']:
                    # API类爬虫
                    news = crawler.fetch(limit=50)
                else:
                    # 网站爬虫
                    news = crawler.fetch(page=1, num_pages=PAGES_TO_CRAWL)
                
                all_news.extend(news)
                logger.info(f'{crawler_name} 爬取完成，获得 {len(news)} 条新闻')
            except Exception as e:
                logger.error(f'爬取 {crawler_name} 失败: {str(e)}')
            finally:
                # 关闭连接
                if hasattr(crawler, 'close'):
                    crawler.close()
    
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
    # 使用新的融合函数
    crawl_all_news_with_market_data()
    
    # 或者使用原始函数（仅爬取新闻）
    # crawl_all_news()
