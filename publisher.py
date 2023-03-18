import requests

from api_services import google_api

from environs import Env

DELAY_BETWEEN_CHECKS = 60  # in seconds

env = Env()
env.read_env()

sheet_id = env('SPREADSHEET_ID')


def publish_to_OK(text, picture):
    return 'https://foo.com/ok'


def publish_to_TG(text, picture):
    return 'https://foo.com/tg'


def publish_to_VK(text, picture):
    return 'https://foo.com/vk'


SOCIAL_MEDIA_NAMES = {
    'OK': publish_to_OK,
    'TG': publish_to_TG,
    'VK': publish_to_VK,
}


def get_picture(picture_url):

    response = requests.get(picture_url)
    response.raise_for_status()

    return response.content


creds = google_api.get_credentials()
sheet_service = google_api.get_spreadsheet_service(creds)
doc_service = google_api.get_document_service(creds)

unpublished_posts = google_api.get_unpublished_posts(sheet_id, sheet_service)

if unpublished_posts:
    for post in unpublished_posts:

        text = google_api.get_publishing_text(post['Текст'], doc_service)
        picture = get_picture(post['Фото'])

        for sm_name in SOCIAL_MEDIA_NAMES:
            if post[sm_name]:
                link_or_none = SOCIAL_MEDIA_NAMES[sm_name](text, picture)
                post[sm_name] = link_or_none
        google_api.update_post_row(
            SOCIAL_MEDIA_NAMES, post, sheet_id, sheet_service
        )
