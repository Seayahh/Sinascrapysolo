# encoding=utf-8
BOT_NAME = 'Sina_spider1'

SPIDER_MODULES = ['Sina_spider1.spiders']
NEWSPIDER_MODULE = 'Sina_spider1.spiders'

DOWNLOADER_MIDDLEWARES = {

    "Sina_spider1.middleware.UserAgentMiddleware": 401,
    "Sina_spider1.middleware.CookiesMiddleware": 402,

    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'Sina_spider1.HttpProxyMiddleware.HttpProxyMiddleware': 543,

}

ITEM_PIPELINES = {
    'Sina_spider1.pipelines.MongoDBPipleline': 300,
}

PROXIES = [
	{'ip_port': '180.120.5.33:8118', 'user_pass': ''},
	{'ip_port': '106.46.136.104:808', 'user_pass': ''},
	{'ip_port': '117.28.29.219:8118', 'user_pass': ''},
	{'ip_port': '106.46.136.12:808', 'user_pass': ''},
	{'ip_port': '106.46.136.71:808', 'user_pass': ''},

]

# DOWNLOAD_DELAY = 5  # 间隔时间
# CONCURRENT_ITEMS = 1000

# CONCURRENT_REQUESTS_PER_IP = 0

# DNSCACHE_ENABLED = True
LOG_LEVEL = 'INFO'    # 日志级别

# DOWNLOAD_DELAY = 2  # 间隔时间

# CONCURRENT_REQUESTS = 400
# CONCURRENT_REQUESTS_PER_SPIDER= 400
CONCURRENT_REQUESTS = 400
REDIRECT_ENABLED = False
CONCURRENT_REQUESTS_PER_DOMAIN = 400