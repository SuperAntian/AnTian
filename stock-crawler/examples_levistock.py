# -*- coding: utf-8 -*-
"""
levistock 完整使用示例
演示如何单独使用 levistock 获取各类市场数据
"""

import pandas as pd
from utils.levistock_fetcher import LeviStockFetcher, NewsEnricher, get_market_summary
from config_levistock import HOT_STOCK_SYMBOLS, TOP_N_HOT_STOCKS
from utils.logger import logger


def example_1_get_all_stocks():
    """示例1: 获取全市场股票"""
    logger.info("\n" + "="*60)
    logger.info("示例1: 获取全市场股票")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    stocks = fetcher.get_all_stocks()
    
    if stocks is not None:
        logger.info(f"\n全市场共 {len(stocks)} 只股票")
        logger.info("\n前10只股票：")
        logger.info(stocks.head(10).to_string())


def example_2_get_realtime_prices():
    """示例2: 获取实时价格"""
    logger.info("\n" + "="*60)
    logger.info("示例2: 获取实时价格 - 热门股票")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    symbols = HOT_STOCK_SYMBOLS[:5]  # 前5只
    
    realtime = fetcher.get_realtime_prices(symbols)
    if realtime is not None:
        logger.info(f"\n实时价格信息：")
        logger.info(realtime[['代码', '名称', '现价', '涨跌幅', '成交量']].to_string())


def example_3_get_limit_up_down():
    """示例3: 获取涨跌停板"""
    logger.info("\n" + "="*60)
    logger.info("示例3: 获取涨跌停板股票")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    
    limit_up = fetcher.get_limit_up_stocks()
    limit_down = fetcher.get_limit_down_stocks()
    
    if limit_up is not None and len(limit_up) > 0:
        logger.info(f"\n涨停板 ({len(limit_up)} 只)：")
        logger.info(limit_up[['代码', '名称', '现价', '涨跌幅']].head().to_string())
    
    if limit_down is not None and len(limit_down) > 0:
        logger.info(f"\n跌停板 ({len(limit_down)} 只)：")
        logger.info(limit_down[['代码', '名称', '现价', '涨跌幅']].head().to_string())


def example_4_get_sectors():
    """示例4: 获取板块数据"""
    logger.info("\n" + "="*60)
    logger.info("示例4: 获取行业板块")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    sectors = fetcher.get_sectors()
    
    if sectors is not None:
        logger.info(f"\n行业板块 ({len(sectors)} 个)：")
        logger.info(sectors[['代码', '名称', '现价', '涨跌幅']].head(10).to_string())


def example_5_get_sector_stocks():
    """示例5: 获取指定板块的股票"""
    logger.info("\n" + "="*60)
    logger.info("示例5: 获取板块内股票")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    sector_name = '计算机'
    
    stocks = fetcher.get_sector_stocks(sector_name)
    if stocks is not None:
        logger.info(f"\n{sector_name}板块 ({len(stocks)} 只)：")
        logger.info(stocks[['代码', '名称', '现价', '涨跌幅']].head().to_string())


def example_6_get_indexes():
    """示例6: 获取市场指数"""
    logger.info("\n" + "="*60)
    logger.info("示例6: 获取市场指数")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    indexes = fetcher.get_market_indexes()
    
    if indexes is not None:
        logger.info(f"\n市场指数 ({len(indexes)} 个)：")
        logger.info(indexes[['代码', '名称', '现价', '涨跌幅']].to_string())


def example_7_get_market_overview():
    """示例7: 获取市场概览"""
    logger.info("\n" + "="*60)
    logger.info("示例7: 获取市场概览")
    logger.info("="*60)
    
    overview = get_market_summary()
    logger.info(f"\n市场概览时间: {overview.get('timestamp')}")


def example_8_enrich_news():
    """示例8: 为新闻融合行情数据"""
    logger.info("\n" + "="*60)
    logger.info("示例8: 新闻融合行情数据")
    logger.info("="*60)
    
    enricher = NewsEnricher()
    
    # 模拟新闻
    sample_news = [
        {
            'title': '贵州茅台发布年报，业绩超预期',
            'content': '贵州茅台发布年报，业绩超预期。代码: 600519',
            'source': '新浪财经',
            'url': 'http://example.com/1'
        },
        {
            'title': '平安银行启动战略转型',
            'content': '平安银行启动战略转型。代码: 000001',
            'source': '东方财富',
            'url': 'http://example.com/2'
        },
        {
            'title': '茅台与五粮液竞争加剧',
            'content': '茅台与五粮液竞争加剧，白酒板块波动',
            'source': '雪球',
            'url': 'http://example.com/3'
        }
    ]
    
    enriched_news = enricher.enrich_batch_news(sample_news)
    
    for idx, news in enumerate(enriched_news, 1):
        logger.info(f"\n新闻 {idx}: {news.get('title')}")
        if 'related_stocks' in news:
            logger.info(f"  关联股票数: {len(news['related_stocks'])}")
            for stock in news['related_stocks']:
                logger.info(f"    - {stock.get('名称')}({stock.get('代码')}): {stock.get('现价')} 涨幅{stock.get('涨跌幅')}")


def example_9_extract_stocks_from_content():
    """示例9: 从内容中提取股票代码"""
    logger.info("\n" + "="*60)
    logger.info("示例9: 从内容中提取股票代码")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    
    test_contents = [
        "贵州茅台今日涨停",
        "平安银行发布新闻",
        "宁德时代市值突破万亿",
        "招商银行与建设银行合作"
    ]
    
    for content in test_contents:
        stocks = fetcher.extract_stocks_from_news(content)
        logger.info(f"\n内容: {content}")
        logger.info(f"  提取的股票: {stocks}")


def run_all_examples():
    """运行所有示例"""
    logger.info("\n" + "="*70)
    logger.info("🚀 levistock 完整使用示例")
    logger.info("="*70)
    
    try:
        example_1_get_all_stocks()
        example_2_get_realtime_prices()
        example_3_get_limit_up_down()
        example_4_get_sectors()
        example_5_get_sector_stocks()
        example_6_get_indexes()
        example_7_get_market_overview()
        example_8_enrich_news()
        example_9_extract_stocks_from_content()
        
    except Exception as e:
        logger.error(f"❌ 运行示例失败: {str(e)}")
    
    logger.info("\n" + "="*70)
    logger.info("✅ 所有示例运行完成！")
    logger.info("="*70 + "\n")


if __name__ == '__main__':
    run_all_examples()
