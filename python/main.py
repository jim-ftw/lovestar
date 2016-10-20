import logging
import sys
import strava
import instagram
import create_html


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


ls_club_id = '102393'
access_token = os.getenv('strava_access_token')
strava_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'strava'))
strava_json = os.path.join(strava_dir, 'strava.json')
