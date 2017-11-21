import requests
from clarifai.rest import ClarifaiApp
import config
import urllib.request

app = ClarifaiApp(api_key=config.clarifai_key)
model = app.models.get("general-v1.3")
access_token = config.access_token
BASE_URL = "https://api.instagram.com/v1/"
urls = []
captions = []


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
        print
        'Status code other than 200 received!'
        exit()


def get_user_info(username):
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
        for post in posts:
            urls.append(post.get("images").get("standard_resolution").get("url"))
            captions.append(post.get("caption").get("text"))
    else:
        print
        'Status code other than 200 received!'
        exit()


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
    else:
        print
        'Status code other than 200 received!'
        exit()


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
        print
        'Status code other than 200 received!'
        exit()


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
        print("-------")


username = input("Enter instagram name: ")
#get_user_info(username)
download_images(username)
#generate_tags()