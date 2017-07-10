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


class Repository(object):
  '''BlogDataのRepositoryクラス
  現状は保存のみ処理のみ対応
  '''
  def __init__(self):
    '''初期化処理
    Cloud Storage, Cloud Datastoreのクライエントオブジェクト生成
    StorageのBucketとDataStoreのKeyを生成
    '''
    self.storage_client = storage.Client()
    self.datastore_client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)
    self.bucket = self.storage_client.get_bucket(BUCKET_NAME)
    self.key = self.datastore_client.key('blog_data')


  def _register(self, items):
    '''登録処理
    '''
    if not items['image'] or self._duplicate(items):
      return
    self._put(items)


  def _put(self, items):
    '''Cloudにデータを保存します
    '''
    self._put_storage(items)
    self._put_datastore(items)


  def _put_storage(self, items):
    '''Cloud Storageに画像を保存
    '''
    res = request.urlopen('http:' + items['image'])
    blob = self.bucket.blob('blog_image' + '/' + uuid.uuid4().hex)
    blob.upload_from_string(res.read())
    blob.make_public()
    items['image_store_url'] = blob.public_url


  def _put_datastore(self, items):
    '''DataStoreにEntityを生成
    '''
    entity = datastore.Entity(self.key, exclude_from_indexes=('text', 'title'))
    entity.update({
      'image_url': items['image_store_url']
      , 'title': items['title']
      , 'text': items['text']
      , 'article_url': items['url']
      , 'created': datetime.now()
    })
    self.datastore_client.put(entity)


  def _duplicate(self, items):
    '''データの重複をチェックします
    重複データ対してにTrue、新規データに対してFalseを返却
    '''
    query = self.datastore_client.query(kind='blog_data')
    query.add_filter('article_url', '=', items['url'])
    return len(list(query.fetch())) != 0

  
  def __call__(self, items):
    '''Repositoryクラスのデータ保存用の関数のエントリーポイント
    self._register()のエイリアス
    こっちをcallしてください
    '''
    self._register(items)