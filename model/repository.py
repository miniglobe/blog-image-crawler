# -*- coding: utf-8 -*-
from datetime import datetime
from gcloud import datastore

PROJECT_ID = "persian-172808"
KEY_PATH = "~/.json_keys/persian-0d004cfe2bd2.json"

def register(items):
  _put(items)


def _put(items):
  '''Cloud Datastoreにエンティティを生成します
  '''
  client = datastore.Client.from_service_account_json(KEY_PATH, project=PROJECT_ID)
  key = client.key('blog-data')
  entity = datastore.Entity(key)
  entity.update({
    'image-url': items['image']
    , 'title': items['title']
    , 'text': items['text']
    , 'article-url': item['url']
    , 'created': datetime.now()
  })
  client.put(entity)
