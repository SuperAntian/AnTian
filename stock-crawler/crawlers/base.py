# -*- coding: utf-8 -*-
"""
基础爬虫类
"""

import requests
from abc import ABC, abstractmethod
from config import REQUEST_TIMEOUT, RETRY_TIMES
from utils.logger import logger
from utils.helpers import get_random_ua, get_random_delay
import time


class BaseCrawler(ABC):
    """
    爬虫基类
    """
    
    def __init__(self, name='BaseCrawler'):
        self.name = name
        self.timeout = REQUEST_TIMEOUT
        self.retry_times = RETRY_TIMES
        self.session = requests.Session()
    
    def get_headers(self):
        """
        获取请求头
        """
        return {
            'User-Agent': get_random_ua()
        }
    
    def request(self, url, method='GET', **kwargs):
        """
        发送HTTP请求
        """
        headers = self.get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs['headers'])
        
        for attempt in range(self.retry_times):
            try:
                if method.upper() == 'GET':
                    resp = self.session.get(url, headers=headers, timeout=self.timeout, **kwargs)
                else:
                    resp = self.session.post(url, headers=headers, timeout=self.timeout, **kwargs)
                
                resp.raise_for_status()
                return resp
            
            except requests.Timeout:
                logger.warning(f'{self.name}: 请求超时 (尝试 {attempt + 1}/{self.retry_times})')
            except requests.ConnectionError:
                logger.warning(f'{self.name}: 连接错误 (尝试 {attempt + 1}/{self.retry_times})')
            except Exception as e:
                logger.warning(f'{self.name}: 请求异常 {str(e)} (尝试 {attempt + 1}/{self.retry_times})')
            
            if attempt < self.retry_times - 1:
                time.sleep(get_random_delay())
        
        logger.error(f'{self.name}: 请求失败，已重试 {self.retry_times} 次')
        return None
    
    @abstractmethod
    def fetch(self, **kwargs):
        """
        爬取数据（需要子类实现）
        """
        pass
    
    def close(self):
        """
        关闭session
        """
        self.session.close()
