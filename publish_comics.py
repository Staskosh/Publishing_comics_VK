import os

import requests
from dotenv import load_dotenv
from download_comics import download_random_comic


def check_vk_response(response):
    values = response.json()
    if "error" in values.keys():
        raise requests.HTTPError(values)


def get_group_server_address(vk_access_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'group_id': group_id,
        'v': 5.131,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_vk = response.json()
    check_vk_response(response)
    group_server_address = response_vk['response']['upload_url']
    return group_server_address


def upload_photo(group_server_address, img_name):
    with open(img_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(group_server_address, files=files)
    response.raise_for_status()
    check_vk_response(response)
    uploaded_photo = response.json()
    photo = uploaded_photo['photo']
    server = uploaded_photo['server']
    hash_value = uploaded_photo['hash']
    return photo, server, hash_value


def save_album_photo(vk_access_token, group_id, photo, server, hash_value):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': vk_access_token,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash_value,
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_vk = response.json()
    check_vk_response(response)
    album_photo = response_vk['response'][0]
    owner_id = album_photo['owner_id']
    photo_id = album_photo['id']
    return owner_id, photo_id


def post_wall(vk_access_token, group_id, owner_id, photo_id, comics_title):
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'access_token': vk_access_token,
        'owner_id': f'-{group_id}',
        'message': comics_title,
        'attachments': f'photo{owner_id}_{photo_id}',

        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    check_vk_response(response)


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    try:
        comics_title, img_name = download_random_comic()
        group_server_address = get_group_server_address(vk_access_token, group_id)
        photo, server, hash_value = upload_photo(group_server_address, img_name)
        owner_id, photo_id = save_album_photo(vk_access_token, group_id, photo, server, hash_value)
        post_wall(vk_access_token, group_id, owner_id, photo_id, comics_title)
    except requests.HTTPError as error:
        print(error)
    finally:
        os.remove(img_name)


if __name__ == '__main__':
    main()
