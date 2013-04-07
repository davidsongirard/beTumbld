import json
import io
import constants
from urllib import request
import threading
import queue
import itertools

class TagDownloader(threading.Thread):

  def __init__(self, q):
    threading.Thread.__init__(self)

    self.q = q
    self.data = None

  def run(self):
    while True:
      func, tag, l = self.q.get()

      l.extend(func(tag))

      self.q.task_done()

class ImageDownloader(threading.Thread):
  def __init__(self, q):
    threading.Thread.__init__(self)

    self.q = q

  def run(self):
    while True:
      url, image = self.q.get()
      image.append((get_image(url), url))
      self.q.task_done()

class URLDownloader(threading.Thread):
  def __init__(self, q):
    threading.Thread.__init__(self)

    self.q = q

  def run(self):
    while True:
      flickr_id, image_list = self.q.get()

      photo_request = request.urlopen("http://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={0}&photo_id={1}&format=json&nojsoncallback=1".format(constants.FLICKR_KEY, flickr_id))
      photo_response = json.loads(photo_request.read().decode("utf-8"))
      image_list.append(photo_response["sizes"]["size"][1]["source"])

      self.q.task_done()

def get_by_tag(tag):

  q = queue.Queue()

  for i in range(2):
    t = TagDownloader(q)
    t.setDaemon(True)
    t.start()

  tumblr = []
  flickr = []

  q.put((_get_tumblr_by_tag, tag, tumblr))
  q.put((get_flickr_by_tag, tag, flickr))

  q.join()
  return tumblr+flickr

def _get_tumblr_by_tag(tag):
  response = request.urlopen('http://api.tumblr.com/v2/tagged?tag={0}&api_key={1}'.format(tag, constants.TUMBLR_KEY))
  response_obj = json.loads(response.read().decode("utf-8"))
  image_list = []
  for x in response_obj["response"]:
    if x["type"] == "photo":
      image_list.append(x["photos"][0]["original_size"]["url"])

  return image_list

def get_flickr_by_tag(tag, page=1):
  response = request.urlopen("http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&tags={1}&format=json&nojsoncallback=1&per_page=20&page={2}".format(constants.FLICKR_KEY, tag, page))
  response_obj = json.loads(response.read().decode("utf-8"))
  image_list = []

  url_queue = queue.Queue()

  for i in range(constants.THREAD_POOL_SIZE):
    t = URLDownloader(url_queue)
    t.setDaemon(True)
    t.start()

  for x in response_obj["photos"]["photo"]:
    url_queue.put((x["id"], image_list))

  url_queue.join()
  return image_list

def get_image(url):
  response = request.urlopen(url)
  return io.BytesIO(response.read())
