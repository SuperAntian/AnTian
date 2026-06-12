# 使用指南 📖

## 安装和配置

### 1. 克隆仓库
```bash
git clone https://github.com/SuperAntian/AnTian.git
cd AnTian/stock-crawler
```

### 2. 创建虚拟环境（推荐）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，根据需要修改配置
```

## 使用方式

### 方式1：单次爬取
运行一次爬虫，爬取指定页数的新闻，然后退出。

```bash
python main.py
```

**优点**：
- 快速测试
- 可以集成到定时任务（cron、任务计划）

**使用场景**：
- 定期通过系统计划任务运行
- 快速获取最新新闻

### 方式2：持续定时爬取
启动后台定时任务，按设定间隔持续爬取新闻。

```bash
python main_scheduler.py
```

**优点**：
- 自动持续更新
- 无需额外配置系统任务

**使用场景**：
- 服务器长期运行
- 需要实时更新的场景

## 配置说明

### 爬取配置
```python
# config.py

# 爬取间隔（秒）
CRAWL_INTERVAL = 600  # 10分钟

# 单次爬取的页数
PAGES_TO_CRAWL = 3

# 启用的数据源
ENABLED_CRAWLERS = [
    'sina',       # 新浪财经
    'eastmoney',  # 东方财富
    'ths',        # 同花顺
    # 'xueqiu',   # 雪球（需要token）
]
```

### 存储配置
```python
# 存储类型
STORAGE_TYPE = 'sqlite'  # 或 'csv'

# SQLite 数据库路径
DB_PATH = 'data/news.db'

# CSV 保存目录
CSV_DIR = 'data'
```

### 日志配置
```python
# 日志级别
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR

# 日志文件
LOG_FILE = 'logs/crawler.log'
```

## 常见用法

### 修改爬取页数
编辑 `config.py`：
```python
PAGES_TO_CRAWL = 5  # 改为爬5页
```

### 只爬取部分数据源
编辑 `config.py`：
```python
ENABLED_CRAWLERS = ['sina', 'eastmoney']  # 只爬新浪和东方财富
```

### 修改爬取间隔
编辑 `config.py`：
```python
CRAWL_INTERVAL = 300  # 改为5分钟
```

### 使用CSV存储而不是数据库
编辑 `config.py`：
```python
STORAGE_TYPE = 'csv'
```

### 自定义爬虫类
```python
from crawlers.sina import SinaNewsCrawler

crawler = SinaNewsCrawler()

# 爬取5页
news = crawler.fetch(page=1, num_pages=5)

# 处理数据
for item in news:
    print(f"{item['source']}: {item['title']}")
    print(f"  URL: {item['url']}")
    print(f"  时间: {item['publish_time']}")
    print()
```

## 数据查询

### 使用SQLite数据库
```python
from storage.db_storage import DBStorage

db = DBStorage()

# 获取最新100条新闻
all_news = db.get_all(limit=100)

# 获取特定来源的新闻
sina_news = db.get_by_source('新浪财经', limit=50)

# 获取总记录数
count = db.get_count()
print(f'数据库中共有 {count} 条新闻')
```

### 直接查询数据库
```bash
sqlite3 data/news.db

# 查看所有表
.tables

# 查看新闻表结构
.schema news

# 查询最新10条新闻
SELECT * FROM news ORDER BY crawl_time DESC LIMIT 10;

# 统计各来源的新闻数
SELECT source, COUNT(*) as count FROM news GROUP BY source;

# 退出
.exit
```

## 错误排查

### 导入错误
```
ModuleNotFoundError: No module named 'xxx'
```
**解决**：重新安装依赖
```bash
pip install -r requirements.txt
```

### 请求超时
```
RequestTimeout / ConnectionError
```
**原因**：网络问题或网站响应慢
**解决**：
- 检查网络连接
- 增加 `REQUEST_TIMEOUT` 值
- 增加 `RETRY_TIMES` 重试次数

### 被封IP
```
HTTP 403 / 429 错误
```
**原因**：请求过于频繁
**解决**：
- 增加 `REQUEST_DELAY_MIN` 和 `REQUEST_DELAY_MAX`
- 使用代理IP
- 减少爬取频率

### 数据库锁定
```
Database is locked
```
**原因**：多个进程同时访问数据库
**解决**：
- 不要同时运行多个爬虫实例
- 关闭其他使用数据库的程序

## 高级用法

### 使用代理IP
编辑 `config.py`：
```python
USE_PROXY = True
PROXY_LIST = [
    'http://proxy1.com:8080',
    'http://proxy2.com:8080',
]
```

然后修改 `crawlers/base.py`：
```python
def request(self, url, method='GET', **kwargs):
    # ...
    if USE_PROXY:
        proxy = random.choice(PROXY_LIST)
        kwargs['proxies'] = {'http': proxy, 'https': proxy}
    # ...
```

### 多线程爬取
```python
import threading
from main import crawl_all_news

# 创建线程
thread = threading.Thread(target=crawl_all_news, daemon=True)
thread.start()

# 主线程继续执行
print('爬虫在后台运行...')
```

### 定时任务（使用系统cron）

**Linux/macOS**：
```bash
# 编辑crontab
crontab -e

# 每10分钟运行一次
*/10 * * * * cd /path/to/stock-crawler && /usr/bin/python3 main.py >> logs/crawler.log 2>&1
```

**Windows**：
使用"任务计划程序"创建定时任务，执行 `python main.py`

## 性能监控

### 查看日志
```bash
# 实时查看日志
tail -f logs/crawler.log

# 查看最后100行
tail -100 logs/crawler.log

# 搜索错误
grep ERROR logs/crawler.log
```

### 数据库统计
```python
from storage.db_storage import DBStorage

db = DBStorage()

# 统计信息
print(f'总新闻数: {db.get_count()}')

# 按来源统计
conn = db._get_connection()
cursor = conn.cursor()
cursor.execute('SELECT source, COUNT(*) as count FROM news GROUP BY source')
for row in cursor.fetchall():
    print(f'{row[0]}: {row[1]} 条')
conn.close()
```

## 备份数据

### 备份SQLite数据库
```bash
cp data/news.db data/news.backup.db
```

### 导出为CSV
```python
from storage.db_storage import DBStorage
import pandas as pd

db = DBStorage()
all_news = db.get_all(limit=10000)
df = pd.DataFrame(all_news)
df.to_csv('news_export.csv', index=False, encoding='utf-8')
```

## 停止爬虫

### 停止定时任务
在终端按 `Ctrl+C` 即可停止

### 清理日志和数据
```bash
# 清理日志
rm logs/crawler.log

# 清理数据
rm data/news.db
# 或
rm data/*.csv
```

## 获取帮助

如有问题，请：
1. 检查日志文件
2. 查阅本指南的常见问题部分
3. 查看源代码注释
4. 提交 Issue
