from environs import Env
from ok_api import OkApi
import json
import requests
from api_services.vk_api import upload_post_image


def post_context_to_ok(post_text, post_image):

    env = Env()
    env.read_env()

    access_token = env.str('OK_ACCESS_TOKEN')
    application_key = env.str('OK_APPLICATION_KEY')
    application_secret_key = env.str('OK_APPLICATION_SECRET_KEY')
    ok_group_id = env.int('OK_GROUP_ID')
    ok = OkApi(access_token=access_token,
               application_key=application_key,
               application_secret_key=application_secret_key)

    
    answer = ok.photosV2.getUploadUrl(gid=ok_group_id, count=1).json()
    upload_url = answer.get('upload_url', None)
    upload_response = upload_post_image(upload_url, post_image).json()
    for photo_id in upload_response['photos']:
        post_image_token = upload_response['photos'][photo_id]['token']    
    attachment = {
            "media":[
                {
                    "type": "text",
                    "text": post_text
                },
                {
                    "type": "photo",
                    "list": [
                    { "id": post_image_token },                    
                    ]
                }
            ]
    }
    attachment = json.dumps(attachment)
    response = ok.mediatopic.post(gid=ok_group_id, attachment=attachment, type='GROUP_THEME')
    return f'https://ok.ru/group/{ok_group_id}/topic/{response.json()}'
