# -*- coding: utf-8 -*-
import scrapy
import moocScrapy.settings
from moocScrapy.settings import *
from moocScrapy.items import *
import re
import os
import json
import requests


class MoocSpider(scrapy.Spider):
    name = 'mooc'
    allowed_domains = []  # 定义爬虫域

    def __init__(self):
        self.infor_page_url = 'http://www.icourse163.org/course/'
        self.course_page_url = 'http://www.icourse163.org/learn/'
        self.SOURCE_INFO_URL = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr'
        self.SOURCE_RESOURCE_URL = 'http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
        self.course = COURSE_ID

    def start_requests(self):
        base_infor_url = self.infor_page_url + self.course

        # 获取课程名称并且新建文件夹
        content = requests.get(base_infor_url).text
        course_name_compile = re.compile(r'class="course-title f-ib f-vam">(.*?)<')
        course_name = re.findall(course_name_compile, content)[0]
        tmp_download_url = getDownloadUrl()

        if tmp_download_url.endswith('\\') == False and tmp_download_url != '':
            tmp_download_url = tmp_download_url + '\\'
        course_name = re.sub(r'[\\/:\*\?"<>\|：]', '', course_name)
        tmp_download_url = tmp_download_url + 'data\\' + course_name + '\\'

        if not os.path.isdir(tmp_download_url):
            os.makedirs(tmp_download_url)
        setDownloadUrl(tmp_download_url)

        yield scrapy.Request(url=base_infor_url, dont_filter=True, callback=self.infor_parse)
        tmp_url = self.course_page_url + self.course
        yield scrapy.Request(url=tmp_url, dont_filter=True, callback=self.parse)

    def infor_parse(self, response):
        print('课程基本信息开始提取')
        context = response.text
        # 使用正则表达式提取
        c_item = CourseItem()
        c_item['course_introduction'] = response.xpath(
            './/div[@id="content-section"]/div[@class="category-content j-cover-overflow"][1]/div[@class="f-richEditorText"]/p//text()').extract()
        # 去除空格和\xa0
        for index, introduction in enumerate(c_item['course_introduction']):
            c_item['course_introduction'][index] = introduction.replace(u'\xa0', u' ').lstrip()
        while '' in c_item['course_introduction']:
            c_item['course_introduction'].remove('')

        teacher_pattern_compile = re.compile(r'chiefLector = \{([\s\S]*?)\}')  # 主要授课教师
        teacher_set = re.findall(teacher_pattern_compile, context)
        teacher_set[0] = teacher_set[0].replace('\n', '').replace(' ', '')
        teacher_name_compile = re.compile(r'lectorName:"(.*?)"')
        teacher_lectorTitle_compile = re.compile(r'lectorTitle:"(.*?)"')

        teacher_name = re.findall(teacher_name_compile, teacher_set[0])[0]
        teacher_lectorTitle = re.findall(teacher_lectorTitle_compile, teacher_set[0])[0]
        other_teacher_pattern_compile = re.compile(r'staffLectors = \[([\s\S]*?)\]')  # 其他授课教师
        other_teacher_set = re.findall(other_teacher_pattern_compile, context)
        other_teacher_info_set = []
        if len(other_teacher_set) > 0 and other_teacher_set[0] != '\n':
            other_teacher_set[0] = other_teacher_set[0].replace('\n', '').replace(' ', '')
            other_teacher_info_pattern = re.compile(r'lectorName:"(.*?)",lectorTitle:"(.*?)"')
            other_teacher_info_set = re.findall(other_teacher_info_pattern, other_teacher_set[0])
            print(other_teacher_info_set)

        tmplist = []
        for info in other_teacher_info_set:
            tmpdict = dict([('lectorName', info[0]), ('lectorTitle', info[1])])
            tmplist.append(tmpdict)
        c_item['course_other_teacher'] = tmplist
        # TODO 需要增加错误判断，没有考虑正则匹配失败的情况

        c_item['course_teacher_title'] = teacher_lectorTitle
        c_item['course_teacher'] = teacher_name
        collage_pattern_compile = re.compile(r'.schoolDto = \{([\s\S]*?)\}')
        collage_set = re.findall(collage_pattern_compile, context)
        collage_set[0] = collage_set[0].replace('\n', '').replace(' ', '')
        collage_name = re.findall(r'name:"(.*?)"', collage_set[0])[0]
        c_item['course_collage'] = collage_name
        c_item['course_title'] = response.xpath('.//span[@class="course-title f-ib f-vam"]//text()').extract()[0]
        c_item['course_url'] = self.infor_page_url + self.course
        # 将item转换字典
        item_dict = dict(c_item)
        tmp_download_url = getDownloadUrl()
        with open(tmp_download_url + '课程信息.json', 'w', encoding='utf-8') as file:
            json.dump(item_dict, file, ensure_ascii=False)
        # with open(DOWNLOAD_UEL + '课程信息.json', 'r',encoding='utf-8') as file:
        #     pop_data = json.load(file)
        print(item_dict)
        print('课程基本信息提取结束，存放地址为：' + tmp_download_url + '课程信息.json')

    def parse(self, response):

        data = self.get_course_info(response)
        #  print(data)
        print(data.get("course_id"))
        # c0-param0：代表课程id
        # batchId：可以为任意时间戳
        # 其他字段为固定不变字段
        post_data = {
            'callCount': '1',
            'scriptSessionId': '${scriptSessionId}190',
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'getMocTermDto',
            'c0-id': '0',
            'c0-param0': 'number:' + data.get("course_id"),
            'c0-param1': 'number:1',
            'c0-param2': 'boolean:true',
            'batchId': '1492167717772'
        }
        yield scrapy.FormRequest(url=self.SOURCE_INFO_URL, formdata=post_data, meta=data,
                                 callback=self.get_course_all_source)

    def get_course_all_source(self, response):
        context = response.text.encode('utf-8').decode('unicode_escape')
        meta_data = response.meta
        chapter_pattern_compile = re.compile(
            r'homeworks=.*?;.+id=(\d+).*?name="(.*?)";')

        chapter_set = re.findall(chapter_pattern_compile, context)

        tmp_download_url = getDownloadUrl()
        print('目录信息开始提取，存放地址为：' + tmp_download_url + '目录结构.txt')
        with open(tmp_download_url + '目录结构.txt', 'w', encoding='utf-8') as file:
            # 写入目录结构
            for index, single_chaper in enumerate(chapter_set):
                file.write('%s    \n' % (single_chaper[1]))

                lesson_pattern_compile = re.compile(
                    r'chapterId=' + single_chaper[0] +
                    r'.*?contentType=1.*?id=(\d+).+name="(.*?)".*?test')
                # 查找所有二级目录id和name
                lesson_set = re.findall(lesson_pattern_compile,
                                        context)
                # 遍历所有二级目录id和name并写入目录
                for sub_index, single_lesson in enumerate(lesson_set):

                    file.write('　%s    \n' % (single_lesson[1]))
                    # 查找二级目录下视频，
                    video_pattern_compile = re.compile(
                        r'contentId=(\d+).+contentType=(1).*?id=(\d+).*?lessonId='
                        + single_lesson[0] + r'.*?name="(.+)"')
                    video_set = re.findall(video_pattern_compile,
                                           context)
                    # 查找二级目录下文档
                    pdf_pattern_compile = re.compile(
                        r'contentId=(\d+).+contentType=(3).+id=(\d+).+lessonId=' +
                        single_lesson[0] + r'.+name="(.+)"')
                    pdf_set = re.findall(pdf_pattern_compile,
                                         context)

                    # Todo 这个正则可以优化
                    name_pattern_compile = re.compile(
                        r'^[第一二三四五六七八九十123456789\d]+[\s\d\._章课节讲]*[\.\s、]\s*\d*')
                    # 遍历二级目录下视频集合，写入目录并下载

                    for video_index, single_video in enumerate(video_set):  # 这里item必须放在循环里
                        item = MoocscrapyItem()
                        item["course_title"] = meta_data["course_title"]
                        item["course_collage"] = meta_data["course_collage"]
                        item["course_id"] = meta_data["course_id"]
                        item["single_chaper"] = single_chaper[1]
                        item["single_chaper_id"] = single_chaper[0]
                        item["single_lesson"] = single_lesson[1]
                        item["single_lesson_id"] = single_lesson[0]
                        rename = re.sub(name_pattern_compile, '', single_video[3])
                        video_name = '%d.%d.%d [视频] %s' % (index + 1, sub_index + 1, video_index + 1, rename)
                        file.write('　　[视频] %s \n' % (video_name))
                        item['video_name'] = video_name
                        (getMethod_url, video_id) = self.get_video_getMethod_url(single_video, video_name)
                        item['video_id'] = video_id
                        param = {
                            "type": single_video[1],
                            "item": item
                        }
                        if getMethod_url != None:
                            yield scrapy.Request(getMethod_url, dont_filter=True, meta=param,
                                                 callback=self.get_video_download_url)
                    # 遍历二级目录下pdf集合，写入目录并下载
                    for pdf_index, single_pdf in enumerate(pdf_set):
                        item = MoocscrapyItem()
                        item["course_title"] = meta_data["course_title"]
                        item["course_collage"] = meta_data["course_collage"]
                        item["course_id"] = meta_data["course_id"]
                        item["single_chaper"] = single_chaper[1]
                        item["single_chaper_id"] = single_chaper[0]
                        item["single_lesson"] = single_lesson[1]
                        item["single_lesson_id"] = single_lesson[0]
                        rename = re.sub(name_pattern_compile, '', single_pdf[3])
                        pdf_name = '%d.%d.%d [文档] %s' % (index + 1, sub_index + 1, pdf_index + 1, rename)
                        file.write('　　[文档] %s \n' % (pdf_name))
                        item['pdf_name'] = pdf_name
                        param = {
                            "type": single_pdf[1],
                            "item": item
                        }
                        post_data = self.get_post_data(single_pdf, pdf_name)
                        if post_data != None:
                            yield scrapy.FormRequest(self.SOURCE_RESOURCE_URL, dont_filter=True, formdata=post_data,
                                                     meta=param,
                                                     callback=self.get_pdf_download_url)

        print('目录信息提取结束，存放地址为：' + tmp_download_url + '目录结构.txt')

    def get_video_getMethod_url(self, single_content, name, *args):

        # 检查文件命名，防止网站资源有特殊字符本地无法保存
        file_pattern_compile = re.compile(r'[\\/:\*\?"<>\|]')
        name = re.sub(file_pattern_compile, '', name)
        # 检查是否有重名的（即已经下载过的）
        tmp_download_url = getDownloadUrl()
        if os.path.exists(tmp_download_url + 'PDFs\\' + name + '.pdf'):
            print(name + "------------->已下载")
            return (None, None)
        if os.path.exists(tmp_download_url + 'Videos\\' + name + '.mp4'):
            print(name + "------------->已下载")
            return (None, None)

        # 获取video的下载链接
        signature_data_url = "https://www.icourse163.org/web/j/resourceRpcBean.getResourceToken.rpc?csrfKey=1cd5127f309e40a1a0c78abce8234635"
        signature_get_post_data = {
            'bizId': single_content[2],
            'bizType': '1',
            'contentType': 1
        }
        signature_get_HEADER = {
            'User-Agent': 'Mozilla/5.0',
            'Cookie': 'NTESSTUDYSI=1cd5127f309e40a1a0c78abce8234635',
        }
        signature_data = requests.post(signature_data_url, headers=signature_get_HEADER,
                                       data=signature_get_post_data).text
        signature_pattern_compile = re.compile(r'signature":"(.*?)"')  # 获取视频需要的标签值
        video_id = re.search(r'videoId":(.*?),', signature_data).group(1)
        signature = re.search(signature_pattern_compile, signature_data).group(1)
        video_param = 'videoId=' + video_id + '&signature=' + signature + '&clientType=1'
        get_video_url = 'https://vod.study.163.com/eds/api/v1/vod/video?' + video_param
        return (get_video_url, video_id)

    def get_video_download_url(self, response):

        video_data = response.text
        dict_data = json.loads(video_data)
        meta_data = response.meta
        item = meta_data.get("item")
        name = item['video_name']
        if 'srtCaptions' in dict_data['result'].keys() and len(dict_data['result']['srtCaptions']) > 0:  # 如果视频有字幕
            srt_link = dict_data['result']['srtCaptions'][0]['url']  # 获取字幕链接 ，默认第一个字幕
            item['srt_url'] = srt_link
        else:
            item['srt_url'] = None
        quality = int(VIDEO_TYPE)  # 视频质量默认最低，以后可以改
        quality_len = len(dict_data['result']['videos'])
        if quality > quality_len:
            quality = quality_len
        video_download_dict = dict_data['result']['videos'][quality - 1]
        item['video_url'] = video_download_dict['videoUrl']
        item['video_type'] = video_download_dict['format']
        item['pdf_url'] = None
        print('正在下载：' + item['video_name'] + '.mp4')
        yield item

    def get_post_data(self, single_content, name, *args):

        # 检查文件命名，防止网站资源有特殊字符本地无法保存
        file_pattern_compile = re.compile(r'[\\/:\*\?"<>\|]')
        name = re.sub(file_pattern_compile, '', name)
        # 检查是否有重名的（即已经下载过的）
        tmp_download_url = getDownloadUrl()
        if os.path.exists(tmp_download_url + 'PDFs\\' + name + '.pdf'):
            print(name + "------------->已下载")
            return None
        if os.path.exists(tmp_download_url + 'Videos\\' + name + '.mp4'):
            print(name + "------------->已下载")
            return None
        post_data = {
            'callCount': '1',
            'scriptSessionId': '${scriptSessionId}190',
            'httpSessionId': '5531d06316b34b9486a6891710115ebc',
            'c0-scriptName': 'CourseBean',
            'c0-methodName': 'getLessonUnitLearnVo',
            'c0-id': '0',
            'c0-param0': 'number:' + single_content[0],  # 二级目录id
            'c0-param1': 'number:' + single_content[1],  # 判定文件还是视频
            'c0-param2': 'number:0',
            'c0-param3': 'number:' + single_content[2],  # 具体资源id
            'batchId': '1492168138043'
        }
        return post_data

    def get_pdf_download_url(self, response):
        context = response.text
        meta_data = response.meta
        item = meta_data.get("item")
        pdf_download_url = re.search(r'textOrigUrl:"(.*?)"', context).group(1)
        print('正在下载：' + item['pdf_name'] + '.pdf')
        item["pdf_url"] = pdf_download_url
        item["video_url"] = None
        yield item

    def get_course_info(self, course_page):
        '''
        获取课程基本信息
        获取课程id用于发送post请求
        '''
        id_pattern_compile = re.compile(r'id:(\d+),')
        # 获取课程名称
        basicinfo_pattern_compile = re.compile(
            r'<meta name="description" .*?content=".*?,(.*?),(.*?),.*?/>')
        basic_set = re.search(basicinfo_pattern_compile, course_page.text)
        param = {
            "course_title": basic_set.group(1),
            "course_collage": basic_set.group(2),
            "course_id": re.search(id_pattern_compile, course_page.text).group(1),

        }
        return param
