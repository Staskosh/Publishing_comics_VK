import random

import requests


def get_random_comic_page():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    all_pages = response.json()['num']
    random_page_number = random.randint(1, all_pages)
    return random_page_number


def download_img(img_url, title):
    response = requests.get(img_url)
    response.raise_for_status()
    file_path = f'{title}.png'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path


def download_comics():
    random_page_number = get_random_comic_page()
    url = f'https://xkcd.com/{random_page_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    response_json = response.json()
    title = response_json['title']
    img_url = response_json['img']
    img_name = download_img(img_url, title)
    return title, img_name
