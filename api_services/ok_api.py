from dotenv import load_dotenv
from os import environ
from ok_api import OkApi, Upload
import json


def post_context_to_ok(post_text, post_image):
    
    load_dotenv()
    access_token = environ['OK_ACCESS_TOKEN']
    application_key = environ['OK_APPLICATION_KEY']
    application_secret_key = environ['OK_APPLICATION_SECRET_KEY']
    ok_group_id = environ['OK_GROUP_ID']
    ok = OkApi(access_token=access_token,
               application_key=application_key,
               application_secret_key=application_secret_key)

    upload = Upload(ok)
    upload_response = upload.photo(photos=[post_image, ], group_id=ok_group_id)    
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
    return f'https://ok.ru/group/70000002564571/topic/{response.json()}'
