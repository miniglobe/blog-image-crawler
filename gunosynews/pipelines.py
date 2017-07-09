# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
sys.path.append('./model')
import repository
from datetime import datetime
from gcloud import datastore


class GunosynewsPipeline(object):
    def process_item(self, item, spider):
        repository.register(item)
        return item
