import requests
import urllib
from pprint import pprint
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()
APP_ACCESS_TOKEN = response['access_token']
#APP_ACCESS_TOKEN = response['4624450705.f63fb78.8a54d25e019441b29be87e6e8557da4d']
BASE_URL = 'https://api.instagram.com/v1/'

def owner_info():
    r = requests.get("%susers/self/?access_token=%s" %(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print "Username :: %s" %(r['data']['username'])
        print "No. of Followers :: %s" %(r['data']['counts']['followed_by'])
        print "No. of People You are Following :: %s" %(r['data']['counts']['follows'])
        print "No. of Posts :: %s" %(r['data']['counts']['media'])
    else:
        print"Invalid Information"

def owner_recent_posts():
    r = requests.get("%susers/self/media/recent/?access_token=%s" %(BASE_URL,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            name = r['data'][0]['id'] + ".jpg"
            url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url,name)
            print url
            print "Image Downloaded"
        else:
            print "No Post to Show"
    else:
        print"Invalid Information"

def get_user_id(uname):
    r = requests.get("%susers/search?q=%s&access_token=%s" %(BASE_URL, uname, APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        return r['data'][0]['id']
    else:
        print "No Such User Exist"

def get_user_info(uname):
    uid = get_user_id(uname)
    r = requests.get("%susers/%s/?access_token=%s" %(BASE_URL,uid,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        print "Username of User :: " + r['data']['username']
        print "No. of Followers :: " + str(r['data']['counts']['followed_by'])
        print "No. of People You are Following :: " + str(r['data']['counts']['follows'])
        print "No. of Posts :: " + str(r['data']['counts']['media'])
    else:
        print"Invalid Information"

def get_user_posts(uname):
    uid = get_user_id(uname)
    r = requests.get("%susers/%s/media/recent/?access_token=%s" %(BASE_URL,uid,APP_ACCESS_TOKEN)).json()
    if r['meta']['code']==200:
        if len(r['data'])>0:
            name = r['data'][0]['id'] + ".jpg"
            url = r['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(url,name)
            print url
            print "Image Downloaded"
        else:
            print "No Post to Show"
    else:
        print"Invalid Information"

def get_media_id(uname):
    uid = get_user_id(uname)
    r = requests.get("%susers/%s/media/recent/?access_token=%s" %(BASE_URL, uid, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:
        if len(r['data']) > 0:
            return r['data'][0]['id']

        else:
            print "No Post to Show"
    else:
        print"Invalid Information"

def like_a_post(uname):
    media_id = get_media_id(uname)
    url = (BASE_URL + 'media/%s/likes') %(media_id)
    payload = {"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' %(url)
    r = requests.post(url,payload).json()
    if r['meta']['code']==200:
        print "Like Successful"
    else:
        print "Like Unsuccessful"

def comment_on_post(uname):
    media_id = get_media_id(uname)
    comment = raw_input("What is Your Comment? ")
    url = (BASE_URL + 'media/%s/comments') %(media_id)
    payload = {"access_token":APP_ACCESS_TOKEN, 'text': comment}
    print 'POST request url : %s' %(url)
    r = requests.post(url,payload).json()
    if r['meta']['code']==200:
        print "Comment Successful"
    else:
        print "Comment Unsuccessful"

def delete_post(uname):
    media_id = get_media_id(uname)
    r = requests.get("%smedia/%s/comments?access_token=%s" %(BASE_URL,media_id,APP_ACCESS_TOKEN)).json()
    for index in range(0,len(r['data'])):
        cmnt_id = r['data'][index]['id']
        cmnt_text = r['data'][index]['text']
        blob = TextBlob(cmnt_text, analyzer=NaiveBayesAnalyzer())
        if blob.sentiment.p_neg > blob.sentiment.p_pos:
            r = requests.delete("%smedia/%s/comments/%s?access_token=%s" %(BASE_URL,media_id,cmnt_id,APP_ACCESS_TOKEN)).json()
            print "Comment Deleted"
        else:
            print "Comment is Positive"

while True:
    var = True
    question = input("""\nWhat do You want to do?
    1. Get Owner Info
    2. Get Recent Posts of Owner
    3. Get User Info
    4. Get User Recent Post
    5. Like a Post
    6. Comment a Post
    7. Delete Comment
    0. Exit\n""")
    if question == 1:
        owner_info()
    elif question == 2:
        owner_recent_posts()
    elif question == 3:
        uname = raw_input("What is the Username of the User? ")
        get_user_info(uname)
    elif question == 4:
        uname = raw_input("What is the Username of the User? ")
        get_user_posts(uname)
    elif question == 5:
        uname = raw_input("What is the Username of the User? ")
        like_a_post(uname)
    elif question == 6:
        uname = raw_input("What is the Username of the User? ")
        comment_on_post(uname)
    elif question == 7:
        uname = raw_input("What is the Userename? ")
        delete_post(uname)
    elif question == 0:
        exit()
    else:
        print "Invalid Input"