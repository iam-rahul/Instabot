import requests
from pprint import pprint

APP_ACCESS_TOKEN = "1397099411.1436082.205d096159f742f0ae5b7d80389ef7cd"
BASE_URL = "https://api.instagram.com/v1/"

def owner_info():
    r = requests.get("%susers/self/?access_token=%s" %(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print r['data'][0]['full_name']
        print r['data'][0]['profile_picture']['url']
    else:
        print"Invalid Information"

def owner_recent_posts():
    r = requests.get("%susers/media/recent/?access_token=%s" %(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print r['data'][0]['images']['standard_resolution']['url']
    else:
        print"Invalid Information"

question = raw_input("""What do You want to do?
1. Get Owner Info
2. Get Recent Posts of Owner""")

if question == 1:
    owner_info()
elif question == 2:
    owner_recent_posts()