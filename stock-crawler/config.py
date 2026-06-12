# -*- coding: utf-8 -*-
"""
股票爬虫配置文件
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================== 爬虫配置 ====================
# 定时爬取间隔（秒）
CRAWL_INTERVAL = int(os.getenv('CRAWL_INTERVAL', 600))  # 默认10分钟

# 请求超时时间（秒）
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))

# 重试次数
RETRY_TIMES = int(os.getenv('RETRY_TIMES', 3))

# 请求间隔范围（秒），随机延迟
REQUEST_DELAY_MIN = 1
REQUEST_DELAY_MAX = 3

# User-Agent列表
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# ==================== 存储配置 ====================
# 存储类型: 'csv' 或 'sqlite'
STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'sqlite')

# 数据库路径
DB_PATH = os.getenv('DB_PATH', 'data/news.db')

# CSV保存目录
CSV_DIR = os.getenv('CSV_DIR', 'data')

# ==================== 日志配置 ====================
# 日志级别
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# 日志文件路径
LOG_FILE = os.getenv('LOG_FILE', 'logs/crawler.log')

# 日志最大大小（字节）
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10MB

# 日志备份数量
LOG_BACKUP_COUNT = 5

# ==================== 数据源配置 ====================
# 新浪财经
SINA_API_URL = 'https://feed.sina.com.cn/api/roll/get'
SINA_PAGEID = 155  # 股票频道
SINA_NEWS_PER_PAGE = 20

# 东方财富
EASTMONEY_API_URL = 'https://np-listapi.eastmoney.com/news/v2/api/list'
EASTMONEY_CHANNEL = 100  # 股票频道
EASTMONEY_NEWS_PER_PAGE = 20

# 雪球
XUEQIU_API_URL = 'https://xueqiu.com/statuses/stock_timeline.json'
XUEQIU_TOKEN = os.getenv('XUEQIU_TOKEN', '')  # 需要手动设置
XUEQIU_DEFAULT_STOCK = 'SH600519'  # 默认股票代码

# 同花顺
THS_BASE_URL = 'https://news.10jqka.com.cn/today_list'

# Tushare
TUSHARE_TOKEN = os.getenv('TUSHARE_TOKEN', 'demo')  # 需要正式配置

# ==================== 爬虫爬取配置 ====================
# 单次爬取的页数
PAGES_TO_CRAWL = 3

# 启用的数据源
# 推荐优先级：akshare > tushare > sina, eastmoney, ths, xueqiu
ENABLED_CRAWLERS = [
    'akshare',    # Akshare API（推荐！不需要配置）
    # 'tushare',   # Tushare API（需要token配置）
    # 'sina',      # 新浪财经
    # 'eastmoney', # 东方财富
    # 'ths',       # 同花顺
    # 'xueqiu',    # 雪球
]

# ==================== 数据处理配置 ====================
# 是否进行数据去重
DEDUPLICATE = True

# 标题最小长度（字符）
MIN_TITLE_LENGTH = 5

# 是否过滤重复标题
FILTER_DUPLICATES = True

# ==================== 代理配置 ====================
# 是否使用代理
USE_PROXY = False

# 代理IP列表（如果需要）
PROXY_LIST = [
    # 'http://proxy1:port',
    # 'http://proxy2:port',
]
