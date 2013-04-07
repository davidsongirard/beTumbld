import json
from urllib import request

FLICKR_KEY = "382051cb16dfd074f0fe909905963c4d"
TUMBLR_KEY = "i6WAqrUkYT0oZVrYO1xGMdoUFTYWiiZVKAZVAG1x62dsNCdDm3"

def get_by_tag(tag):
  return _get_flickr_by_tag(tag)

def _get_tumblr_by_tag(tag):
  response = request.urlopen('http://api.tumblr.com/v2/tagged?tag={0}&api_key={1}'.format(tag, TUMBLR_KEY))
  response_obj = json.loads(response.read().decode("utf-8"))
  image_list = []
  for x in response_obj["response"]:
    if x["type"] == "photo":
      image_list.append(x["photos"][0]["original_size"]["url"])

  return image_list 

def _get_flickr_by_tag(tag):
  response = request.urlopen('http://api.tumblr.com/v2/tagged?tag={0}&api_key={1}'.format(tag, TUMBLR_KEY))
  response_obj = json.loads(response.read().decode("utf-8"))
  image_list = []
  for x in response_obj["response"]:
    if x["type"] == "photo":
      image_list.append(x["photos"][0]["original_size"]["url"])

  return image_list 

l = get_by_tag("horse")
print(l)
