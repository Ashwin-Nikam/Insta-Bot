import requests
from clarifai.rest import ClarifaiApp
import config
import urllib.request
import SentimentAnalysis
import Plot

app = ClarifaiApp(api_key=config.clarifai_key)
model = app.models.get("general-v1.3")
access_token = config.access_token
BASE_URL = "https://api.instagram.com/v1/"
urls = []
captions = []
tags = []
locations = []


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


def get_locations():
    request_url = (BASE_URL + 'users/self/media/recent?access_token=%s') % (access_token)
    print(request_url)
    recent_posts = requests.get(request_url).json()
    if recent_posts['meta']['code'] == 200:
        posts = recent_posts.get("data")
        for post in posts:
            if post.get('location') == None:
                continue
            else:
                temp = [post.get('location')['latitude']]
                temp.append(post.get('location')['longitude'])
            locations.append(temp)
    else:
        print('Status code other than 200 received!')


username = input("Enter name :")

while True:
    print("==========================")
    print("What would you like to do?")
    print("1: Generate Tags from images")
    print("2: Download images")
    print("3. Like a post")
    print("4. Get recent media like by user")
    print("5. Plot locations of photos on map")
    print("6. Exit")
    val = int(input())
    if val == 1:
        get_user_info(username)
        generate_tags()
    elif val == 2:
        download_images(username)
    elif val == 3:
        like_a_post(username)
    elif val == 4:
        self_media_liked()
    elif val == 5:
        get_locations()
        Plot.plot_points(locations)
    elif val == 6:
        break
    else:
        print("Invalid input")