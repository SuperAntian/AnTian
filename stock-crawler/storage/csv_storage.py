# -*- coding: utf-8 -*-
"""
CSV存储模块
"""

import os
import pandas as pd
from datetime import datetime
from config import CSV_DIR
from utils.logger import logger


class CSVStorage:
    """
    CSV文件存储
    """
    
    def __init__(self, filename='news.csv'):
        if not os.path.exists(CSV_DIR):
            os.makedirs(CSV_DIR)
        
        self.filepath = os.path.join(CSV_DIR, filename)
        self.data = []
    
    def save(self, news_item):
        """
        保存单条新闻
        """
        self.data.append(news_item)
    
    def flush(self):
        """
        将数据写入CSV文件
        """
        if not self.data:
            logger.warning('CSVStorage: 没有数据需要保存')
            return
        
        try:
            df = pd.DataFrame(self.data)
            df.to_csv(self.filepath, mode='a', header=not os.path.exists(self.filepath),
                     index=False, encoding='utf-8')
            logger.info(f'CSVStorage: 成功保存 {len(self.data)} 条数据到 {self.filepath}')
            self.data = []
        except Exception as e:
            logger.error(f'CSVStorage: 保存失败 - {str(e)}')
    
    def get_all(self):
        """
        读取所有数据
        """
        if not os.path.exists(self.filepath):
            return []
        
        try:
            df = pd.read_csv(self.filepath)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f'CSVStorage: 读取失败 - {str(e)}')
            return []
    
    def clear(self):
        """
        清空文件
        """
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            logger.info(f'CSVStorage: 已清空 {self.filepath}')
