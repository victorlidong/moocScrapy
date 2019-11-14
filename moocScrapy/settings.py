# -*- coding: utf-8 -*-

# Scrapy settings for moocScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# course.config
# COURSE_ID="SCU-1003253003"   #吃货的营养学修养
# COURSE_ID="UIBE-1205987812"   #投资学
# download.url
#DOWNLOAD_URL = r""
DOWNLOAD_URL = input("请输入保存路径：")
course_url = input("输入你想爬取的课程链接：")
input()
print("输入下载的视频质量（1-3）：")
VIDEO_TYPE =input() #1 #(1-3)
print("VIDEO_TYPE = ",VIDEO_TYPE)
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
import datetime
import os

Today = datetime.datetime.now()
Log_file_path = 'log/scrapy_{}_{}_{}.log'.format(Today.year, Today.month, Today.day)  # 则在目标下增加log文件夹项目下  和scrapy.cfg同级
if os.path.exists('log') == False:
    os.mkdir('log')

# Log_file_path='scrapy_{}_{}_{}.log'.format(Today.year,Today.month,Today.day)#时间为名字
LOG_LEVEL = "WARNING"  # 级别，则高于或者等于该等级的信息就能输出到我的日志中，低于该级别的信息则输出不到我的日志信息中
LOG_FILE = Log_file_path

DOWNLOADER_MIDDLEWARES = {
    'moocScrapy.middlewares.RandomUserAgent': 543,
}

ITEM_PIPELINES = {
    'moocScrapy.pipelines.MoocscrapyPipeline': 400,
}
