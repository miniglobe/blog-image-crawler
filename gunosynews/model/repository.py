# -*- coding: utf-8 -*-
from urllib import request
import tempfile
import uuid
from datetime import datetime
from google.cloud import datastore
from google.cloud import storage

PROJECT_ID = "persian-172808"
DATA_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-3a9988725cae.json"
STORAGE_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-efe392f65854.json"
BUCKET_NAME = "persian-172808.appspot.com"

def register(items):
  if not items['image']:
    return
  _put(items)


def _put(items):
  '''Cloudにエンティティを生成します
  '''
  _put_storage(items)
  _put_datastore(items)


def _put_storage(items):
  client = storage.Client()
  bucket = client.get_bucket(BUCKET_NAME)
  res = request.urlopen('http:' + items['image'])
  blob = bucket.blob('blog_image' + '/' + uuid.uuid4().hex)
  blob.upload_from_string(res.read())
  blob.make_public()
  items['image_store_url'] = blob.public_url


def _put_datastore(items):
  client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)
  key = client.key('blog_data')
  entity = datastore.Entity(key, exclude_from_indexes=('text', 'title', 'article_url', 'image_url'))
  entity.update({
    'image_url': items['image_store_url']
    , 'title': items['title']
    , 'text': items['text']
    , 'article_url': items['url']
    , 'created': datetime.now()
  })
  client.put(entity)