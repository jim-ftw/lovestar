import requests
import os
import json
import urlparse
import logging
import sys


# logger = logging.getLogger()
# handler = logging.StreamHandler(sys.stdout)
# formatter = logging.Formatter('%(levelname)-8s %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)
# logger.setLevel(logging.INFO)
# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)


ls_club_id = '102393'
access_token = os.getenv('strava_access_token')
strava_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'strava'))
strava_json = os.path.join(strava_dir, 'strava.json')


def reset_strava_json():
    for the_file in os.listdir(strava_dir):
        file_path = os.path.join(strava_dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    strava_dict = {
        "members": []
    }
    with open(strava_json, 'w') as f:
        json.dump(strava_dict, f)


def get_json(club_id):
    url = 'https://www.strava.com/api/v3/clubs/' + club_id + '/members'
    payload = {
        'access_token': access_token
    }
    r = requests.get(url, params=payload)
    response = json.loads(r.text)
    for item in response:
        strava_id = item['id']
        first_name = item['firstname']
        last_name = item['lastname']
        strava_pic = item['profile']
        if strava_pic == 'avatar/athlete/large.png':
            strava_pic = 'https://www.strava.com/images/img-error.jpg'
        strava_pic_extension = os.path.splitext(urlparse.urlparse(strava_pic).path)[1]
        strava_pic_path = os.path.join(strava_dir, str(strava_id) + strava_pic_extension)
        with open(strava_pic_path, 'wb') as handle:
            response = requests.get(strava_pic, stream=True)
            if not response.ok:
                print 'couldn\'t download file: ' + strava_pic
            for block in response.iter_content(1024):
                handle.write(block)
        entry = {}
        entry['strava_id'] = strava_id
        entry['first_name'] = first_name
        entry['last_name'] = last_name
        entry['profile_pic'] = os.path.relpath(
            strava_pic_path, os.path.join(os.path.dirname(__file__), '..'))
        entry['strava_link'] = 'https://www.strava.com/athletes/' + str(strava_id)
        f = open(strava_json, 'r')
        strava_dict = json.loads(f.read())
        f.close()
        strava_dict['members'].append(entry)
        with open(strava_json, 'w') as fp:
            json.dump(strava_dict, fp)
        logging.info('photo added ' + str(strava_id))


# reset_strava_json()
# get_json(ls_club_id)
