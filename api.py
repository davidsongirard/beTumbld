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

def get_by_tag(tag):

  q = queue.Queue()

  for i in range(2):
    t = TagDownloader(q)
    t.setDaemon(True)
    t.start()

  tumblr = []
  flickr = []

  q.put((_get_tumblr_by_tag, tag, tumblr))
  q.put((_get_flickr_by_tag, tag, flickr))

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

def _get_flickr_by_tag(tag):
  response = request.urlopen("http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&tags={1}&format=json&nojsoncallback=1&per_page=20".format(constants.FLICKR_KEY, tag))
  response_obj = json.loads(response.read().decode("utf-8"))
  image_list = []
  for x in response_obj["photos"]["photo"]:
    photo_request = request.urlopen("http://api.flickr.com/services/rest/?method=flickr.photos.getSizes&api_key={0}&photo_id={1}&format=json&nojsoncallback=1".format(constants.FLICKR_KEY, x["id"]))
    photo_response = json.loads(photo_request.read().decode("utf-8"))
    image_list.append(photo_response["sizes"]["size"][1]["source"])

  return image_list

def get_image(url):
  response = request.urlopen(url)
  return io.BytesIO(response.read())
