# -*- coding: utf-8 -*-
"""
辅助函数模块
"""

import random
import hashlib
from datetime import datetime
from config import REQUEST_DELAY_MIN, REQUEST_DELAY_MAX, USER_AGENTS


def get_random_ua():
    """
    获取随机User-Agent
    """
    return random.choice(USER_AGENTS)


def get_random_delay():
    """
    获取随机延迟时间（秒）
    """
    return random.uniform(REQUEST_DELAY_MIN, REQUEST_DELAY_MAX)


def generate_md5(text):
    """
    生成MD5哈希值
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def clean_title(title):
    """
    清理标题
    """
    if not title:
        return ''
    title = title.strip()
    # 移除多余空格
    title = ' '.join(title.split())
    return title


def clean_url(url):
    """
    清理URL
    """
    if not url:
        return ''
    url = url.strip()
    # 移除查询参数
    if '?' in url:
        url = url.split('?')[0]
    return url


def is_valid_news(title, url, min_length=5):
    """
    验证新闻数据的有效性
    """
    if not title or len(title) < min_length:
        return False
    if not url:
        return False
    return True


def get_current_timestamp():
    """
    获取当前时间戳
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def parse_timestamp(ts):
    """
    解析时间戳
    """
    try:
        if isinstance(ts, int):
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return str(ts)
    except:
        return str(ts)
