# -*- coding: utf-8 -*-
"""
levistock 市场数据获取模块
与爬虫框架集成，获取实时行情、板块、涨停板等数据
"""

import time
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional, Any
import levistock as lk
from config_levistock import (
    ENABLE_MARKET_DATA, FETCH_REALTIME_PRICE, FETCH_LIMIT_UP,
    FETCH_SECTOR_DATA, FETCH_INDEX_DATA, HOT_STOCK_SYMBOLS,
    KEYWORD_STOCK_MAP, SAVE_MARKET_DATA_SEPARATELY, MARKET_DATA_DIR,
    ANALYZE_SECTORS, RECORD_MARKET_OVERVIEW, TOP_N_HOT_STOCKS
)
from utils.logger import logger
import os


class LeviStockFetcher:
    """levistock 行情数据获取器"""
    
    def __init__(self):
        self.cache = {}
        self.cache_time = {}
        self.last_update = None
        
    def get_all_stocks(self) -> Optional[pd.DataFrame]:
        """获取全市场所有股票"""
        try:
            logger.info("📊 正在获取全市场股票列表...")
            df = lk.stocks_all_em()
            logger.info(f"✅ 获取 {len(df)} 只股票")
            return df
        except Exception as e:
            logger.error(f"❌ 获取全市场股票失败: {str(e)}")
            return None
    
    def get_realtime_prices(self, symbols: List[str]) -> Optional[pd.DataFrame]:
        """获取多只股票实时价格
        
        Args:
            symbols: 股票代码列表 ['600519', '000001']
        """
        if not FETCH_REALTIME_PRICE:
            return None
            
        try:
            logger.info(f"💰 获取实时价格: {symbols}")
            df = lk.stocks_quote_em(symbol=symbols)
            return df
        except Exception as e:
            logger.error(f"❌ 获取实时价格失败: {str(e)}")
            return None
    
    def get_limit_up_stocks(self) -> Optional[pd.DataFrame]:
        """获取涨停板股票"""
        if not FETCH_LIMIT_UP:
            return None
            
        try:
            logger.info("🚀 获取涨停板股票...")
            df = lk.stocks_limit_up_em()
            if df is not None and len(df) > 0:
                logger.info(f"✅ 获取 {len(df)} 只涨停股票")
            return df
        except Exception as e:
            logger.error(f"❌ 获取涨停板失败: {str(e)}")
            return None
    
    def get_limit_down_stocks(self) -> Optional[pd.DataFrame]:
        """获取跌停板股票"""
        try:
            logger.info("📉 获取跌停板股票...")
            df = lk.stocks_limit_down_em()
            if df is not None and len(df) > 0:
                logger.info(f"✅ 获取 {len(df)} 只跌停股票")
            return df
        except Exception as e:
            logger.error(f"❌ 获取跌停板失败: {str(e)}")
            return None
    
    def get_sectors(self) -> Optional[pd.DataFrame]:
        """获取行业板块"""
        if not FETCH_SECTOR_DATA:
            return None
            
        try:
            logger.info("🏭 获取行业板块...")
            df = lk.stock_sector_em()
            logger.info(f"✅ 获取 {len(df)} 个板块")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块失败: {str(e)}")
            return None
    
    def get_sector_stocks(self, sector_name: str) -> Optional[pd.DataFrame]:
        """获取指定板块的股票"""
        try:
            logger.info(f"📍 获取 {sector_name} 板块股票...")
            df = lk.stock_sector_detail_em(symbol=sector_name)
            if df is not None and len(df) > 0:
                logger.info(f"✅ 获取 {sector_name} 板块 {len(df)} 只股票")
            return df
        except Exception as e:
            logger.error(f"❌ 获取板块股票失败: {str(e)}")
            return None
    
    def get_market_indexes(self) -> Optional[pd.DataFrame]:
        """获取主要指数"""
        if not FETCH_INDEX_DATA:
            return None
            
        try:
            logger.info("📊 获取市场指数...")
            df = lk.stocks_all_index_em()
            logger.info(f"✅ 获取 {len(df)} 个指数")
            return df
        except Exception as e:
            logger.error(f"❌ 获取指数失败: {str(e)}")
            return None
    
    def get_market_overview(self) -> Dict[str, Any]:
        """获取市场概览"""
        if not RECORD_MARKET_OVERVIEW:
            return {}
        
        try:
            logger.info("🌍 获取市场概览...")
            overview = {
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            # 获取主要指数
            indexes = self.get_market_indexes()
            if indexes is not None:
                overview['indexes'] = indexes
            
            # 获取涨跌停统计
            limit_up = self.get_limit_up_stocks()
            limit_down = self.get_limit_down_stocks()
            
            overview['limit_up_count'] = len(limit_up) if limit_up is not None else 0
            overview['limit_down_count'] = len(limit_down) if limit_down is not None else 0
            
            logger.info(f"✅ 涨停: {overview['limit_up_count']} | 跌停: {overview['limit_down_count']}")
            return overview
            
        except Exception as e:
            logger.error(f"❌ 获取市场概览失败: {str(e)}")
            return {}
    
    def extract_stocks_from_news(self, news_content: str) -> List[str]:
        """从新闻内容中提取股票代码"""
        stocks = []
        
        # 使用关键词映射
        for keyword, stock_code in KEYWORD_STOCK_MAP.items():
            if keyword in news_content:
                stocks.append(stock_code)
        
        # 直接检查热门股票代码
        for symbol in HOT_STOCK_SYMBOLS:
            if symbol in news_content:
                if symbol not in stocks:
                    stocks.append(symbol)
        
        return list(set(stocks))  # 去重


class NewsEnricher:
    """新闻数据丰富器 - 融合行情数据"""
    
    def __init__(self):
        self.fetcher = LeviStockFetcher()
        self.market_data_cache = {}
    
    def enrich_single_news(self, news: Dict[str, Any]) -> Dict[str, Any]:
        """为单条新闻添加行情数据
        
        Args:
            news: 新闻字典，必须包含 'title' 或 'content' 字段
        """
        enriched = news.copy()
        
        # 提取新闻中的股票代码
        content = news.get('content', '') or news.get('title', '') or ''
        stocks = self.fetcher.extract_stocks_from_news(content)
        
        # 获取这些股票的实时价格
        if stocks:
            try:
                realtime_data = self.fetcher.get_realtime_prices(stocks)
                if realtime_data is not None and len(realtime_data) > 0:
                    enriched['related_stocks'] = realtime_data.to_dict('records')
                    enriched['stock_symbols'] = stocks
                    logger.info(f"✅ 新闻已关联 {len(stocks)} 只股票")
            except Exception as e:
                logger.warning(f"⚠️ 关联股票失败: {str(e)}")
        
        # 记录处理时间
        enriched['market_data_updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return enriched
    
    def enrich_batch_news(self, news_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """为一批新闻添加行情数据"""
        logger.info(f"🔗 正在为 {len(news_list)} 条新闻关联行情数据...")
        enriched_list = []
        
        for idx, news in enumerate(news_list, 1):
            enriched = self.enrich_single_news(news)
            enriched_list.append(enriched)
            
            if idx % 10 == 0:
                logger.info(f"⏳ 已处理 {idx}/{len(news_list)} 条新闻")
        
        logger.info(f"✅ 新闻关联完成")
        return enriched_list
    
    def save_market_data_snapshot(self) -> str:
        """保存市场数据快照"""
        if not SAVE_MARKET_DATA_SEPARATELY:
            return ""
        
        try:
            # 创建数据目录
            os.makedirs(MARKET_DATA_DIR, exist_ok=True)
            
            # 获取市场数据
            overview = self.fetcher.get_market_overview()
            limit_up = self.fetcher.get_limit_up_stocks()
            limit_down = self.fetcher.get_limit_down_stocks()
            sectors = self.fetcher.get_sectors()
            
            # 生成时间戳文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 保存涨停板
            if limit_up is not None and len(limit_up) > 0:
                file_path = os.path.join(MARKET_DATA_DIR, f"limit_up_{timestamp}.csv")
                limit_up.to_csv(file_path, index=False, encoding='utf-8')
                logger.info(f"💾 涨停板数据已保存: {file_path}")
            
            # 保存跌停板
            if limit_down is not None and len(limit_down) > 0:
                file_path = os.path.join(MARKET_DATA_DIR, f"limit_down_{timestamp}.csv")
                limit_down.to_csv(file_path, index=False, encoding='utf-8')
                logger.info(f"💾 跌停板数据已保存: {file_path}")
            
            # 保存板块数据
            if ANALYZE_SECTORS and sectors is not None and len(sectors) > 0:
                file_path = os.path.join(MARKET_DATA_DIR, f"sectors_{timestamp}.csv")
                sectors.to_csv(file_path, index=False, encoding='utf-8')
                logger.info(f"💾 板块数据已保存: {file_path}")
            
            return timestamp
            
        except Exception as e:
            logger.error(f"❌ 保存市场数据失败: {str(e)}")
            return ""


def get_market_summary() -> Dict[str, Any]:
    """获取市场汇总信息"""
    logger.info("\n" + "="*60)
    logger.info("📊 市场数据汇总")
    logger.info("="*60)
    
    fetcher = LeviStockFetcher()
    summary = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'overview': fetcher.get_market_overview(),
    }
    
    # 获取热门股票
    try:
        realtime = fetcher.get_realtime_prices(HOT_STOCK_SYMBOLS[:TOP_N_HOT_STOCKS])
        if realtime is not None:
            summary['hot_stocks'] = realtime
    except Exception as e:
        logger.warning(f"⚠️ 获取热门股票失败: {str(e)}")
    
    logger.info("="*60 + "\n")
    return summary
