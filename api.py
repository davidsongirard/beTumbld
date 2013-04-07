import json
import io
import constants
from urllib import request


def get_by_tag(tag):
  return _get_tumblr_by_tag(tag) + _get_flickr_by_tag(tag)

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

_get_tumblr_by_tag("horse")
