import logging
import sys
import strava
import instagram
import create_html
import time
import random


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


ls_club_id = '102393'


insta_url = 'https://www.instagram.com/explore/tags/'

tags = [
    'lovestarbicyclebags',
    'lovestarraceclub',
    'lovestarfactoryteam'
]


if __name__ == "__main__":
    strava.reset_strava_json()
    strava.get_json(ls_club_id)
    logger.info('strava complete')
    for item in tags:
        tagged_url = insta_url + item
        while tagged_url:
            tagged_url = instagram.get_json(tagged_url, item)
            time.sleep(random.randint(1, 10))
    instagram.get_photo_info()
    instagram.create_thumbnail()
    create_html.reset_dir()
    create_html.iterate_json()
