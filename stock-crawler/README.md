# 股票财经新闻爬虫 📰

一个强大的Python爬虫框架，实时爬取多个财经网站的股票新闻资讯。

## 功能特性 ✨

- 🚀 支持4个主流财经网站：新浪财经、东方财富、雪球、同花顺
- ⏰ 实时定时更新，自动爬取最新新闻
- 💾 多种存储方式：CSV、SQLite数据库
- 🔄 自动重试和错误处理
- 📊 数据去重和清洗
- 📝 详细日志记录
- 🛡️ UA伪装、请求间隔控制

## 支持的数据源

| 来源 | URL | 描述 |
|------|-----|------|
| 新浪财经 | https://feed.sina.com.cn | JSON API，最稳定 |
| 东方财富 | https://np-listapi.eastmoney.com | 官方API接口 |
| 雪球 | https://xueqiu.com | 需要登录或代理 |
| 同花顺 | https://news.10jqka.com.cn | HTML解析 |

## 快速开始 🚀

### 1. 克隆仓库
```bash
git clone https://github.com/SuperAntian/AnTian.git
cd AnTian/stock-crawler
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置文件
编辑 `config.py` 根据需要调整参数：
```python
# 爬虫配置
CRAWL_INTERVAL = 600  # 10分钟更新一次
REQUEST_TIMEOUT = 10  # 请求超时时间
RETRY_TIMES = 3       # 重试次数
```

### 4. 运行爬虫

**方式1：单次爬取**
```bash
python main.py
```

**方式2：启动定时任务**
```bash
python main_scheduler.py
```

## 项目结构 📁

```
stock-crawler/
├── requirements.txt          # 依赖包列表
├── README.md                # 项目说明
├── config.py               # 配置文件
├── main.py                 # 单次爬取主程序
├── main_scheduler.py       # 定时任务主程序
├── crawlers/
│   ├── __init__.py
│   ├── base.py            # 基础爬虫类
│   ├── sina.py            # 新浪财经爬虫
│   ├── eastmoney.py       # 东方财富爬虫
│   ├── xueqiu.py          # 雪球爬虫
│   └── ths.py             # 同花顺爬虫
├── storage/
│   ├── __init__.py
│   ├── csv_storage.py     # CSV存储
│   └── db_storage.py      # SQLite存储
├── utils/
│   ├── __init__.py
│   ├── logger.py          # 日志管理
│   └── helpers.py         # 辅助函数
├── data/                  # 数据存储目录
│   ├── news.db            # SQLite数据库
│   └── *.csv              # CSV文件
└── logs/                  # 日志目录
    └── crawler.log        # 爬虫日志
```

## 使用示例 💻

### 爬取单个源
```python
from crawlers.sina import SinaNewsCrawler

crawler = SinaNewsCrawler()
news = crawler.fetch(page=1)
for item in news:
    print(item['title'])
```

### 爬取所有源
```python
from crawlers.sina import SinaNewsCrawler
from crawlers.eastmoney import EastmoneyNewsCrawler
from crawlers.ths import THSNewsCrawler

all_news = []
for crawler_class in [SinaNewsCrawler, EastmoneyNewsCrawler, THSNewsCrawler]:
    crawler = crawler_class()
    all_news.extend(crawler.fetch())

print(f'获取了 {len(all_news)} 条新闻')
```

### 保存到数据库
```python
from storage.db_storage import DBStorage

db = DBStorage()
for news in all_news:
    db.save(news)
```

## 配置说明 ⚙️

### 环境变量 (.env)
```
# 爬虫配置
CRAWL_INTERVAL=600
REQUEST_TIMEOUT=10
RETRY_TIMES=3

# 存储配置
STORAGE_TYPE=sqlite  # csv 或 sqlite
DB_PATH=data/news.db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=logs/crawler.log

# 雪球配置（可选）
XUEQIU_TOKEN=your_token_here
```

## 注意事项 ⚠️

1. **法律合规**：仅用于学习研究，勿商业用途
2. **频率控制**：请求间隔2-5秒，避免被封IP
3. **定期维护**：网站结构变化时需更新爬虫代码
4. **反爬措施**：
   - 某些网站需要登录（如雪球）
   - 可能需要使用代理IP池
   - 验证码处理需要额外配置

5. **雪球爬虫特别说明**：
   - 需要从浏览器获取登录后的cookie
   - 或使用代理IP服务
   - 也可以改用官方API（付费）

## 常见问题 FAQ

### Q: 爬虫被封IP了怎么办？
A: 
1. 增加请求间隔时间
2. 使用代理IP池
3. 切换网络或等待IP解封

### Q: 如何爬取特定股票的新闻？
A: 修改爬虫中的参数，如：
```python
crawler = XueqiuNewsCrawler()
news = crawler.fetch(stock_code='SH600519')  # 贵州茅台
```

### Q: 数据库表结构是什么？
A: 查看 `storage/db_storage.py` 中的 `create_table()` 方法

### Q: 可以爬取历史新闻吗？
A: 可以，但不同网站有不同的限制，具体查看各爬虫类中的参数说明

## 性能优化建议 🚀

1. **多线程爬取**：同时爬取多个源
2. **异步请求**：使用 aiohttp 替代 requests
3. **数据库索引**：为频繁查询的字段添加索引
4. **缓存机制**：避免重复爬取相同新闻
5. **分布式爬虫**：使用 Celery + Redis

## 贡献指南 🤝

欢迎提交 Issue 和 PR！

## 许可证 📄

MIT License

## 作者

AnTian

## 更新日志

### v1.0.0 (2026-06-12)
- ✅ 初始版本发布
- ✅ 支持4个财经数据源
- ✅ 完整的爬虫框架
- ✅ 定时任务和存储功能
