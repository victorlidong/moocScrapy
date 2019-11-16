# -*- coding: utf-8 -*-
"""
定义Spider的中间件
"""

from scrapy import signals
from fake_useragent import UserAgent


class MoocscrapySpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # Scrapy使用此方法创建Spider
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # 每一个response都需要经过spider中间件进入Spider
        # 返回None或引发异常
        return None

    def process_spider_output(self, response, result, spider):
        # 在处理完响应后，调用Spider返回的结果
        # 必须返回一个可迭代的Request，dict或Item对象
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # 当Spider或process_spider_input（）方法（来自其他Spider中间件）
        # 引发异常时调用。

        # 应该返回None或可迭代的Response，dict或Item对象
        pass

    def process_start_requests(self, start_requests, spider):
        # 以Spider的启动请求进行调用，其工作原理与process_spider_output（）
        # 方法类似，不同之处在于它没有关联的响应

        # 必须仅返回请求（不返回项目）
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class MoocscrapyDownloaderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        # Scrapy使用此方法创建Spider
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # 调用通过下载器中间件的每个请求

        # 满足以下一个：
        # - return None: 继续处理此请求
        # - return一个Response对象
        # - return一个Request对象
        # - 引发IgnoreRequest：已安装的下载程序中间件的process_exception（）方法将被调用
        return None

    def process_response(self, request, response, spider):
        # 调用下载器返回的响应

        # 满足以下一个：
        # - return一个Response对象
        # - return一个Request对象
        # - 引发IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # 当下载处理程序或process_request（）（来自其他下载器中间件）引发异常时调用

        # 满足以下一个：
        # - return None: 继续处理此异常
        # - return一个Response对象: 停止process_exception()链
        # - return一个Request object:停止process_exception()链
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgent(object):

    def process_request(self, request, spider):
        # TODO 使用随机agent可以提高效率
        ua = UserAgent()
        s = ua.random
        request.headers['User-Agent'] = s
        # print(request.headers)
