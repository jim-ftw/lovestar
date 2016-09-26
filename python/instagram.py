import requests
import re
import json
import os.path
import time
import random
import logging
import sys
from pprint import pprint
import pickle
from PIL import Image


def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


lsphotos_json = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lsphotos', 'lsphotos.json'))
media_file_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lsphotos'))

insta_url = 'https://www.instagram.com/explore/tags/'

tags = [
    'lovestarbicyclebags',
    'lovestarraceclub',
    'lovestarfactoryteam'
]

tag_page = {}


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def resize_big_images(image_path):
    fname, file_extension = os.path.splitext(image_path)
    img = Image.open(image_path)
    max_size = 800
    original_size = max(img.size[0], img.size[1])
    if original_size >= max_size:
        if (img.size[0] < img.size[1]):
            resized_width = max_size
            resized_height = int(round((max_size / float(img.size[0])) * img.size[1]))
        else:
            resized_height = max_size
            resized_width = int(round((max_size / float(img.size[1])) * img.size[0]))
        img = img.resize((resized_width, resized_height), Image.ANTIALIAS)
        img.save(image_path, 'JPEG')
        logger.info('image resized')


def parse_json(tag_page_json):
    for item, entry in enumerate(tag_page_json):
        dir_list = os.listdir(media_file_folder)
        max_list = []
        for item in dir_list:
            if item[:5] == 'image':
                max_list.append(item)
        if not max_list:
            n = 1
        else:
            max_item = max(max_list)
            n = int(get_numbers_from_filename(max_item))
            n += 1
        fej = open(os.path.join(media_file_folder, 'downloaded_photos.pkl'), 'rb')
        try:
            downloaded_photos = pickle.load(fej)
        except EOFError:
            downloaded_photos = []
        media_id = entry['id']
        media_url = entry['display_src']
        media_caption = entry['caption']
        media_file_name = 'image' + '%0.6d' % n + '.jpg'
        media_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lsphotos', media_file_name))
        if entry['is_video'] is False and media_id not in downloaded_photos:
            with open(media_file_path, 'wb') as handle:
                response = requests.get(media_url, stream=True)
                if not response.ok:
                    print 'couldn\'t download file: ' + media_id
                for block in response.iter_content(1024):
                    handle.write(block)
            entry = {}
            media_index = n - 1
            entry['media_id'] = media_id
            entry['media_url'] = media_url
            entry['caption'] = media_caption
            entry['media_file_path'] = os.path.relpath(
                media_file_path, os.path.join(os.path.dirname(__file__), '..'))
            f = open(lsphotos_json, 'r')
            lsphotos_dict = json.loads(f.read())
            f.close()
            lsphotos_dict['images'].insert(media_index, entry)
            with open(lsphotos_json, 'w') as fp:
                json.dump(lsphotos_dict, fp)
            downloaded_photos.append(media_id)
            with open(os.path.join(media_file_folder, 'downloaded_photos.pkl'), 'wb') as outfile:
                pickle.dump(downloaded_photos, outfile)
            logging.info('photo added ' + media_id)
            resize_big_images(media_file_path)
            time.sleep(random.randint(1, 10))


def get_json(url, tag):
    # new_url = insta_url + tag
    r = requests.get(url)
    text = r.text
    insta_json = json.loads(re.search(r"window._sharedData\s*=\s*(.*);", text).group(1))
    top_posts = insta_json['entry_data']['TagPage'][0]['tag']['top_posts']['nodes']
    parse_json(top_posts)
    tag_page = insta_json['entry_data']['TagPage'][0]['tag']['media']['nodes']
    parse_json(tag_page)
    while insta_json['entry_data']['TagPage'][0]['tag']['media']['page_info']['has_next_page'] is True:
        cursor = insta_json['entry_data']['TagPage'][0]['tag']['media']['page_info']['end_cursor']
        new_url = insta_url + tag + '/?max_id=' + cursor
        logging.info('new_url: ' + new_url)
        return new_url


def rename_files():
    dir_list = os.listdir(media_file_folder)
    max_list = []
    for item in dir_list:
        if item[:5] == 'image':
            max_list.append(item)
    if not max_list:
        n = 1
    else:
        max_item = max(max_list)
        n = int(get_numbers_from_filename(max_item))
        n += 1
    for filename in os.listdir(media_file_folder):
        fname, file_extension = os.path.splitext(filename)
        if file_extension == '.jpg' and fname[:5] != 'image':
            file_name = 'image' + '%0.6d' % n + file_extension
            os.rename(os.path.join(media_file_folder, filename), os.path.join(media_file_folder, file_name))
            ls_json = open(lsphotos_json)
            ls_json = json.loads(ls_json.read())
            ls_json[fname]['java_array_id'] = n - 1
            ls_json[fname]['media_file_path'] = os.path.relpath(
                os.path.join(media_file_folder, file_name), os.path.join(os.path.dirname(__file__), '..'))
            with open(lsphotos_json, 'w') as fp:
                json.dump(ls_json, fp)
            n += 1
            logging.info('photo renamed ' + fname + ' ' + file_name)

for item in tags:
    tagged_url = insta_url + item
    while tagged_url:
        tagged_url = get_json(tagged_url, item)
        time.sleep(random.randint(1, 10))
