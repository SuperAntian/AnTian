# -*- coding: utf-8 -*-
"""
日志管理模块
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_LEVEL, LOG_MAX_SIZE, LOG_BACKUP_COUNT


def setup_logger(name=__name__):
    """
    配置日志处理器
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # 创建日志目录
    log_dir = os.path.dirname(LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 文件处理器（带轮转）
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_SIZE,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    
    # 避免重复添加处理器
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# 获取全局logger
logger = setup_logger('stock_crawler')
