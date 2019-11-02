# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import urllib.request
from scrapy.exceptions import DropItem
import os
import time
import m3u8
import requests
from glob import iglob
from natsort import natsorted
from urllib.parse import urljoin
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
from moocScrapy.settings import DOWNLOAD_UEL
class MoocscrapyPipeline(object):
    def process_item(self, item, spider):
        if item["pdf_url"]:
            print("download pdf")

            pdf_file = requests.get(item["pdf_url"])
            if not os.path.isdir(DOWNLOAD_UEL + 'PDFs'):
                os.mkdir(DOWNLOAD_UEL + r'PDFs')
            with open(DOWNLOAD_UEL + 'PDFs\\' + item['pdf_name'] + '.pdf', 'wb') as file:
                file.write(pdf_file.content)
        if item["video_url"]:
            print("download video")
            if not os.path.isdir(DOWNLOAD_UEL+'Videos'):
                os.mkdir(DOWNLOAD_UEL + r'Videos')
            if not os.path.isdir(DOWNLOAD_UEL+'Videos\\temp'):
                os.mkdir(DOWNLOAD_UEL + r'Videos\\temp')
            if item['srt_url']:  # 如果视频有字幕
                urllib.request.urlretrieve(item['srt_url'], DOWNLOAD_UEL+'Videos\\'+item['video_name']+ '.srt')  # 字幕下载
            if item['video_type']=='hls':#hls格式视频
                file_name = DOWNLOAD_UEL+'Videos\\'+item['video_name']+'.mp4'
                file_url=item["video_url"]
                M3U8 = DownLoad_M3U8(file_url, file_name)
                M3U8.run()
            else:#mp4格式则普通下载
                urllib.request.urlretrieve(item['video_url'], DOWNLOAD_UEL+'Videos\\'+item['video_name']+'.mp4')
        return item




class DownLoad_M3U8(object):

    def __init__(self,m3u8_url,file_name):
        self.m3u8_url=m3u8_url
        self.file_name=file_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0', }
        self.threadpool = ThreadPoolExecutor(max_workers=20)
        if not self.file_name:
            self.file_name = 'new.mp4'

    def get_ts_url(self):
        m3u8_obj = m3u8.load(self.m3u8_url)
        base_uri = m3u8_obj.base_uri

        ts_url=[]
        for seg in m3u8_obj.segments:
            ts_url.append(urljoin(base_uri, seg.uri))
        return ts_url

    def download_single_ts(self, urlinfo):
        url, ts_name = urlinfo
        res = requests.get(url)
        with open(DOWNLOAD_UEL+'Videos\\temp\\'+ts_name, 'wb') as fp:
            fp.write(res.content)

    def download_all_ts(self):
        ts_urls = self.get_ts_url()
        for index, ts_url in enumerate(ts_urls):
            print(ts_url)
            # self.download_single_ts([ts_url, str(index)+'.ts'])
            self.threadpool.submit(self.download_single_ts, [ts_url, str(index)+'.ts'])
        self.threadpool.shutdown()

    def run(self):
        self.download_all_ts()
        ts_path = DOWNLOAD_UEL+'Videos\\temp\\'+'*.ts'
        with open(self.file_name, 'wb') as fn:
            for ts in natsorted(iglob(ts_path)):
                with open(ts, 'rb') as ft:
                    scline = ft.read()
                    fn.write(scline)
        for ts in iglob(ts_path):
            os.remove(ts)