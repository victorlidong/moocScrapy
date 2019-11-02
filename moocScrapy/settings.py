# -*- coding: utf-8 -*-

# Scrapy settings for moocScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#course.config
COURSE_ID="SCU-1003253003"
VIDEO_TYPE="a"
#download.url
DOWNLOAD_UEL=""


DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 100
CONCURRENT_REQUESTS_PER_IP = 10
COOKIES_ENABLED = False




BOT_NAME = 'moocScrapy'
SPIDER_MODULES = ['moocScrapy.spiders']
NEWSPIDER_MODULE = 'moocScrapy.spiders'

ROBOTSTXT_OBEY = False
# URL不去重
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}
import datetime
Today=datetime.datetime.now()
Log_file_path='log/scrapy_{}_{}_{}.log'.format(Today.year,Today.month,Today.day)# 则在目标下增加log文件夹项目下  和scrapy.cfg同级

#Log_file_path='scrapy_{}_{}_{}.log'.format(Today.year,Today.month,Today.day)#时间为名字
LOG_LEVEL="WARNING"#级别，则高于或者等于该等级的信息就能输出到我的日志中，低于该级别的信息则输出不到我的日志信息中
LOG_FILE =Log_file_path
#mongodb.config
MONGO_URI = 'localhost'
MONGO_DB = 'mooc'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'moocScrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules


# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'moocScrapy.middlewares.MoocscrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   #'moocScrapy.middlewares.MoocscrapyDownloaderMiddleware': 543,
   'moocScrapy.middlewares.RandomUserAgent': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'moocScrapy.pipelines.MoocscrapyPipeline': 400,
}
