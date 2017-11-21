import requests
from clarifai.rest import ClarifaiApp
import config
import urllib.request
import WordCloud

app = ClarifaiApp(api_key=config.clarifai_key)
model = app.models.get("general-v1.3")
access_token = config.access_token
BASE_URL = "https://api.instagram.com/v1/"
urls = []
captions = []
tags = []


def get_user_id(username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % \
                  (username, access_token)
    user_info = requests.get(request_url).json()
    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print('Status code other than 200 received!')


def get_user_info(username):
    count = 5
    user_id = get_user_id(username)
    if user_id is None:
        print("User doesn't exist")
        return
    request_url = (BASE_URL + 'users/%s/media/recent?count=%d&access_token=%s') % (user_id, count, access_token)
    print(request_url)
    recent_posts = requests.get(request_url).json()
    if recent_posts['meta']['code'] == 200:
        posts = recent_posts.get("data")
        for post in posts:
            urls.append(post.get("images").get("standard_resolution").get("url"))
            captions.append(post.get("caption").get("text"))
        print(captions)
    else:
        print('Status code other than 200 received!')


def get_self_info():
    count = 5
    request_url = (BASE_URL + 'users/self/media/recent?count=%d&access_token=%s') % (count, access_token)
    print(request_url)
    recent_posts = requests.get(request_url).json()
    if recent_posts['meta']['code'] == 200:
        posts = recent_posts.get("data")
        for post in posts:
            urls.append(post.get("images").get("standard_resolution").get("url"))
            captions.append(post.get("caption").get("text"))
        print(captions)
    else:
        print('Status code other than 200 received!')


def download_images(username):
    count = 5
    user_id = get_user_id(username)
    if user_id is None:
        print("User doesn't exist")
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent?count=%d&access_token=%s') % (user_id, count, access_token)
    print(request_url)
    recent_posts = requests.get(request_url).json()
    if recent_posts['meta']['code'] == 200:
        posts = recent_posts.get("data")
        if len(posts) is 0:
            return
        for post in posts:
            url = post.get("images").get("standard_resolution").get("url")
            filename = post['id'] + ".jpeg"
            urllib.request.urlretrieve(url, filename)
    else:
        print('Status code other than 200 received!')


def generate_tags():
    for i in range(len(urls)):
        print("Picture ", i + 1)
        url = urls[i]
        caption = captions[i]
        dict = model.predict_by_url(url=url)
        new_output = dict.get('outputs')
        concepts = new_output[0].get('data').get('concepts')
        print(caption)
        for concept in concepts:
            print(concept.get('name'), " : ", concept.get('value'))
            tags.append(concept.get('name'))
        print("-------")


def self_media_liked():
    request_url = (BASE_URL + "users/self/media/liked?access_token=%s") % (access_token)
    print(request_url)
    result = requests.get(request_url).json()
    if result['meta']['code'] == 200:
        posts = result.get("data")
        if len(posts) is 0:
            print("No recent liked photos!")
            return
        for post in posts:
            urls.append(post.get("images").get("standard_resolution").get("url"))
            captions.append(post.get("caption").get("text"))
        print(captions)
    else:
        print('Status code other than 200 received!')


def get_post_id(user_id):
    if user_id is None:
        print("User doesn't exist")
        return
    request_url = (BASE_URL + 'users/%s/media/recent?count=1&access_token=%s') % (user_id, access_token)
    post = requests.get(request_url).json()
    if post['meta']['code'] == 200:
        return post.get('data')[0]['id']
    else:
        print('Status code other than 200 received!')


def like_a_post(username):
    user_id = get_user_id(username)
    media_id = get_post_id(user_id)
    if media_id is None:
        print("No recent posts to like")
        return
    request_url = (BASE_URL + 'media/%s/likes') % media_id
    payload = {"access_token": access_token}
    result = requests.post(request_url, payload).json()
    if result['meta']['code'] == 200:
        print('Like was successful')
    else:
        print('Like was unsuccessful, please try again!')


tags = ['boy', 'stadium', 'dark', 'light', 'boy', 'stadium', 'dark', 'stadium', 'dark']
freq_dict = {}
for tag in tags:
    freq_dict[tag] = tags.count(tag)
keys = freq_dict.keys()
values = freq_dict.values()
WordCloud.create_cloud(freq_dict)

#self_media_liked()
#username = input("Enter instagram name: ")
#get_user_info(username)
#generate_tags()
#download_images(username)
#like_a_post(username)