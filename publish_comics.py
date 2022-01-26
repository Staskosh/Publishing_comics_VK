import os
import shutil

import requests
from dotenv import load_dotenv
from download_comics import download_random_comic


def check_VK_response(response):
    vallues = response.json()
    for vallue in vallues:
        if vallue == 'error':
            raise requests.HTTPError()


def get_group_server_address(vk_access_token, group_id):
    url = 'https://api.vk.com/method/photos.gtWallUploadServer'
    payload = {
        'access_token': vk_access_token,
        'group_id': group_id,
        'v': 5.131,
    }
    response = requests.get(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    check_VK_response(response)
    group_server_address = response_json['response']['upload_url']
    return group_server_address


def upload_photo(group_server_address, img_name):
    with open(img_name, 'rb') as file:
        url = group_server_address
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        check_VK_response(response)
        uploaded_photo = response.json()
        return uploaded_photo


def save_album_photo(vk_access_token, group_id, uploaded_photo):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'access_token': vk_access_token,
        'group_id': group_id,
        'photo': uploaded_photo['photo'],
        'server': uploaded_photo['server'],
        'hash': uploaded_photo['hash'],
        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    response_json = response.json()
    check_VK_response(response)
    album_photo = response_json['response'][0]
    return album_photo
    # except requests.HTTPError:
    #     print('Ошибка в сохранении фото в альбом')


def post_wall(vk_access_token, group_id, album_photo, comics_title):
    owner_id = album_photo['owner_id']
    id = album_photo['id']
    url = 'https://api.vk.com/method/wall.post'

    payload = {
        'access_token': vk_access_token,
        'owner_id': f'-{group_id}',
        'message': comics_title,
        'attachments': f'photo{owner_id}_{id}',

        'v': 5.131,
    }
    response = requests.post(url, params=payload)
    response.raise_for_status()
    check_VK_response(response)
    # except requests.HTTPError:
    #     print('Не удалось опубликовать фото')


def remove_files(img_name):
    """ param <path> could either be relative or absolute. """
    if os.path.isfile(img_name) or os.path.islink(img_name):
        os.remove(img_name)
    elif os.path.isdir(img_name):
        shutil.rmtree(img_name)
    else:
        raise ValueError("file {} is not a file or dir.".format(img_name))


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    group_id = os.getenv('VK_GROUP_ID')
    comics_title, img_name = download_random_comic()
    try:
        group_server_address = get_group_server_address(vk_access_token, group_id)
        uploaded_photo = upload_photo(group_server_address, img_name)
        album_photo = save_album_photo(vk_access_token, group_id, uploaded_photo)
        post_wall(vk_access_token, group_id, album_photo, comics_title)
    except requests.HTTPError:
        print('Ошибка в запросе к VK api')
    remove_files(img_name)


if __name__ == '__main__':
    main()
