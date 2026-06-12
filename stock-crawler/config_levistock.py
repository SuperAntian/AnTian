# -*- coding: utf-8 -*-
"""
levistock 市场数据配置文件
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== levistock 基础配置 ====================
# 是否启用市场数据获取
ENABLE_MARKET_DATA = os.getenv('ENABLE_MARKET_DATA', 'True').lower() == 'true'

# 是否在爬虫中融合新闻与行情数据
ENRICH_NEWS_WITH_MARKET = os.getenv('ENRICH_NEWS_WITH_MARKET', 'True').lower() == 'true'

# 市场数据缓存时间（秒）- 避免频繁调用
MARKET_DATA_CACHE_TIME = int(os.getenv('MARKET_DATA_CACHE_TIME', 300))  # 5分钟

# ==================== 数据获取配置 ====================
# 是否获取实时价格
FETCH_REALTIME_PRICE = True

# 是否获取涨停板
FETCH_LIMIT_UP = True

# 是否获取板块数据
FETCH_SECTOR_DATA = True

# 是否获取指数数据
FETCH_INDEX_DATA = True

# 是否获取新股数据
FETCH_NEW_STOCKS = True

# 是否获取融资融券数据
FETCH_MARGIN_DATA = False  # 默认关闭，数据较大

# ==================== 数据处理配置 ====================
# 热门股票代码列表（用于实时价格获取）
HOT_STOCK_SYMBOLS = [
    '600519',  # 贵州茅台
    '600000',  # 浦发银行
    '000001',  # 平安银行
    '000858',  # 五粮液
    '600036',  # 招商银行
    '601939',  # 建设银行
    '601988',  # 中国银行
    '603259',  # 药明康德
    '300750',  # 宁德时代
    '601398',  # 工商银行
]

# 关键词对应的股票映射
KEYWORD_STOCK_MAP = {
    '茅台': '600519',
    '浦发': '600000',
    '平安': '000001',
    '五粮液': '000858',
    '招商': '600036',
    '建设银行': '601939',
    '中国银行': '601988',
    '宁德': '300750',
    '工商': '601398',
}

# ==================== 存储配置 ====================
# 市场数据是否单独保存
SAVE_MARKET_DATA_SEPARATELY = os.getenv('SAVE_MARKET_DATA_SEPARATELY', 'True').lower() == 'true'

# 市场数据保存目录
MARKET_DATA_DIR = os.getenv('MARKET_DATA_DIR', 'data/market_data')

# 行情数据更新频率（秒）
MARKET_UPDATE_INTERVAL = int(os.getenv('MARKET_UPDATE_INTERVAL', 600))  # 10分钟

# ==================== 日志配置 ====================
# 市场数据相关日志
LOG_MARKET_DATA = os.getenv('LOG_MARKET_DATA', 'True').lower() == 'true'

# ==================== 分析配置 ====================
# 是否进行板块分析
ANALYZE_SECTORS = os.getenv('ANALYZE_SECTORS', 'True').lower() == 'true'

# 是否记录市场概览
RECORD_MARKET_OVERVIEW = os.getenv('RECORD_MARKET_OVERVIEW', 'True').lower() == 'true'

# 热点股票数量（按涨幅排序）
TOP_N_HOT_STOCKS = int(os.getenv('TOP_N_HOT_STOCKS', 10))

# 热点板块数量（按涨幅排序）
TOP_N_HOT_SECTORS = int(os.getenv('TOP_N_HOT_SECTORS', 5))
