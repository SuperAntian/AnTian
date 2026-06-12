# -*- coding: utf-8 -*-
"""
SQLite数据库存储模块
"""

import sqlite3
import os
from config import DB_PATH
from utils.logger import logger


class DBStorage:
    """
    SQLite数据库存储
    """
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._ensure_db()
    
    def _ensure_db(self):
        """
        确保数据库和表存在
        """
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        if not os.path.exists(self.db_path):
            self._create_table()
    
    def _get_connection(self):
        """
        获取数据库连接
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def _create_table(self):
        """
        创建表
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    title TEXT NOT NULL,
                    url TEXT NOT NULL,
                    summary TEXT,
                    publish_time TEXT,
                    crawl_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(title, url)
                )
            ''')
            
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON news(source)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_publish_time ON news(publish_time)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_crawl_time ON news(crawl_time)')
            
            conn.commit()
            logger.info('DBStorage: 数据库表创建成功')
        except Exception as e:
            logger.error(f'DBStorage: 创建表失败 - {str(e)}')
        finally:
            conn.close()
    
    def save(self, news_item):
        """
        保存单条新闻
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO news (source, title, url, summary, publish_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                news_item.get('source', ''),
                news_item.get('title', ''),
                news_item.get('url', ''),
                news_item.get('summary', ''),
                news_item.get('publish_time', '')
            ))
            conn.commit()
        except Exception as e:
            logger.error(f'DBStorage: 保存失败 - {str(e)}')
        finally:
            conn.close()
    
    def save_batch(self, news_list):
        """
        批量保存新闻
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            for news_item in news_list:
                cursor.execute('''
                    INSERT OR IGNORE INTO news (source, title, url, summary, publish_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    news_item.get('source', ''),
                    news_item.get('title', ''),
                    news_item.get('url', ''),
                    news_item.get('summary', ''),
                    news_item.get('publish_time', '')
                ))
            conn.commit()
            logger.info(f'DBStorage: 成功保存 {len(news_list)} 条新闻')
        except Exception as e:
            logger.error(f'DBStorage: 批量保存失败 - {str(e)}')
        finally:
            conn.close()
    
    def get_all(self, limit=100):
        """
        获取所有新闻
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM news ORDER BY crawl_time DESC LIMIT ?', (limit,))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'DBStorage: 查询失败 - {str(e)}')
            return []
        finally:
            conn.close()
    
    def get_by_source(self, source, limit=50):
        """
        按来源获取新闻
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'SELECT * FROM news WHERE source = ? ORDER BY crawl_time DESC LIMIT ?',
                (source, limit)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f'DBStorage: 查询失败 - {str(e)}')
            return []
        finally:
            conn.close()
    
    def get_count(self):
        """
        获取总记录数
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) as count FROM news')
            result = cursor.fetchone()
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f'DBStorage: 统计失败 - {str(e)}')
            return 0
        finally:
            conn.close()
    
    def clear(self):
        """
        清空数据
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('DELETE FROM news')
            conn.commit()
            logger.info('DBStorage: 已清空所有数据')
        except Exception as e:
            logger.error(f'DBStorage: 清空失败 - {str(e)}')
        finally:
            conn.close()
