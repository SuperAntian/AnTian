# -*- coding: utf-8 -*-
"""
定时任务爬虫（持续运行）
"""

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from main import crawl_all_news
from config import CRAWL_INTERVAL
from utils.logger import logger
import time
import sys


def start_scheduler():
    """
    启动定时任务
    """
    scheduler = BackgroundScheduler()
    
    # 添加定时任务
    scheduler.add_job(
        crawl_all_news,
        'interval',
        seconds=CRAWL_INTERVAL,
        id='crawl_news',
        name='爬取股票新闻'
    )
    
    # 启动调度器
    scheduler.start()
    logger.info('='*50)
    logger.info(f'定时爬虫已启动，间隔时间: {CRAWL_INTERVAL}秒')
    logger.info('='*50)
    logger.info('按 Ctrl+C 停止运行')
    logger.info('='*50)
    
    # 立即执行一次
    crawl_all_news()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('正在关闭爬虫...')
        scheduler.shutdown()
        logger.info('爬虫已停止')
        sys.exit(0)


if __name__ == '__main__':
    start_scheduler()
