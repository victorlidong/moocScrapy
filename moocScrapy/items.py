# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoocscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'course'
    course_title = scrapy.Field()
    course_collage = scrapy.Field()
    course_id = scrapy.Field()
    single_chaper = scrapy.Field()
    single_chaper_id = scrapy.Field()
    single_lesson = scrapy.Field()
    single_lesson_id = scrapy.Field()
    video_type=scrapy.Field()
    video_url = scrapy.Field()
    pdf_url = scrapy.Field()
    srt_url = scrapy.Field()
    pdf_name=scrapy.Field()
    video_name=scrapy.Field()
    video_id=scrapy.Field()
    pass

class CourseItem(scrapy.Item):

    course_introduction=scrapy.Field()
    course_teacher=scrapy.Field()
    course_teacher_title=scrapy.Field()
    course_title=scrapy.Field()
    course_collage=scrapy.Field()
    course_url=scrapy.Field()
    course_other_teacher=scrapy.Field()
    pass
