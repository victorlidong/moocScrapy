# -*- coding: utf-8 -*-
"""
MoocScrapy项目的Scrapy设置
"""

import datetime
import os

DOWNLOAD_URL = input("请输入保存路径：")
course_url = input("输入你想爬取的课程链接：")
print("输入下载的视频质量（1-3）：")
VIDEO_TYPE = input()
print("VIDEO_TYPE = ", VIDEO_TYPE)


def getDownloadUrl():
    return DOWNLOAD_URL


def setDownloadUrl(downloadurl):
    global DOWNLOAD_URL
    DOWNLOAD_URL = downloadurl


COURSE_ID = ''
for i in range(len(course_url)):
    if course_url[len(course_url) - i - 1] == '/':
        COURSE_ID = course_url[-i:]
        break

print("COURSE_ID =", COURSE_ID)

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

Today = datetime.datetime.now()
# 则在目标下增加log文件夹项目下  和scrapy.cfg同级
Log_file_path = 'log/scrapy_{}_{}_{}.log'.format(Today.year, Today.month, Today.day)
if not os.path.exists('log'):
    os.mkdir('log')

# 级别，则高于或者等于该等级的信息就能输出到我的日志中，低于该级别的信息则输出不到我的日志信息中
# Log_file_path='scrapy_{}_{}_{}.log'.format(Today.year,Today.month,Today.day)#时间为名字
LOG_LEVEL = "WARNING"
LOG_FILE = Log_file_path

DOWNLOADER_MIDDLEWARES = {
    'moocScrapy.middlewares.RandomUserAgent': 543,
}

ITEM_PIPELINES = {
    'moocScrapy.pipelines.MoocscrapyPipeline': 400,
}
