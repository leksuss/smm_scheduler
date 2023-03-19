import requests
from dotenv import load_dotenv
from os import environ
from requests.exceptions import HTTPError
from dataclasses import dataclass
from api_services.type_annotation import UploadPhoto, SavePhoto


def post_context_to_vk(post_text, post_image):

    load_dotenv()
    vk_access_token = environ['VK_ACCESS_TOKEN']
    vk_group_id = environ['VK_GROUP_ID']
    actual_api_version = '5.131'       
    try:
        return post_comic_in_vk(vk_access_token, vk_group_id, actual_api_version, post_image, post_text)
    except HTTPError as err:
        print('Ошибка опубликования')
        print(err.args[0])        
        

def get_upload_vk_server_url(vk_access_token, vk_group_id, api_version):
    
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    payloads = {
        'access_token': vk_access_token, 
        'v': api_version,
        'group_id': vk_group_id
    }
    response = requests.get(url, params=payloads)
    response.raise_for_status()    
    upload_url_response = response.json()
    if 'error' in upload_url_response:
        raise HTTPError(upload_url_response['error']['error_msg'])          
    return upload_url_response['response']['upload_url']


def upload_post_image(url, post_image):

    image = requests.get(post_image, stream=True)
    file = {
        'photo': ("image.jpg", image.raw, image.headers['Content-Type'])
    }
    response = requests.post(url, files=file)
    response.raise_for_status()
    return response


def upload_wall_photo(post_image, url):    
    
    upload_file_response = upload_post_image(url, post_image)
    upload_wall_photo_response = upload_file_response.json()        
    if 'error' in upload_wall_photo_response:
        raise HTTPError(upload_wall_photo_response['error']['error_msg'])  
    elif upload_wall_photo_response['photo'] == '[]':
        raise HTTPError('Изображение не загружено в группу')
    upload_photo = UploadPhoto(
        photo=upload_wall_photo_response['photo'],
        server=upload_wall_photo_response['server'],
        hash_wall=upload_wall_photo_response['hash']
    )          
    return upload_photo
                 

def save_wall_photo(vk_access_token, vk_group_id,  api_version, upload_photo: UploadPhoto):

    url = 'https://api.vk.com/method/photos.saveWallPhoto'  
    payloads = {
        'access_token': vk_access_token,         
        'group_id': vk_group_id,
        'photo': upload_photo.photo,
        'server': upload_photo.server,
        'v': api_version,
        'hash': upload_photo.hash_wall
        }
    response = requests.post(url, params=payloads)
    response.raise_for_status()
    save_wall_photo_response = response.json()    
    if 'error' in save_wall_photo_response:
        raise HTTPError(save_wall_photo_response['error']['error_msg'])
    save_photo = SavePhoto(
        owner_id=save_wall_photo_response['response'][0]['owner_id'],
        media_id=save_wall_photo_response['response'][0]['id']
    ) 
    return save_photo


def post_wall_photo(vk_access_token, vk_group_id, api_version, post_text, save_photo: SavePhoto):

    url = 'https://api.vk.com/method/wall.post'  
    owner_id = save_photo.owner_id
    media_id = save_photo.media_id
    payloads = {
        'access_token': vk_access_token,         
        'owner_id': -int(vk_group_id),
        'from_group': 1,
        'message': post_text,
        'attachments': f'photo{owner_id}_{media_id}',        
        'v': api_version,        
    }
    response = requests.post(url, params=payloads)
    response.raise_for_status()
    post_wall_photo_response = response.json()
    post_id = post_wall_photo_response['response']['post_id']     
    if 'error' in post_wall_photo_response:
        raise HTTPError(post_wall_photo_response['error']['error_msg'])
    return f'https://vk.com/club{vk_group_id}?w=wall-{vk_group_id}_{post_id}%2Fall' 
               

def post_comic_in_vk(vk_access_token, vk_group_id, api_version, post_image, post_text):

    upload_vk_server_url = get_upload_vk_server_url(vk_access_token, vk_group_id, api_version)
    upload_photo = upload_wall_photo(post_image, upload_vk_server_url)
    save_photo = save_wall_photo(vk_access_token, vk_group_id,  api_version, upload_photo)
    post_url = post_wall_photo(vk_access_token, vk_group_id, api_version, post_text, save_photo)
    return post_url
