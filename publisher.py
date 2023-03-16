import requests

from api_services import google_api

from environs import Env

env = Env()
env.read_env()

DELAY_BETWEEN_CHECKS = 60  # in seconds

spreadsheet_id = env('SPREADSHEET_ID')


def publish_to_OK(text, picture):
    pass


def publish_to_TG(text, picture):
    pass


def publish_to_VK(text, picture):
    pass


SOCIAL_MEDIA = {
    'OK': publish_to_OK,
    'TG': publish_to_TG,
    'VK': publish_to_VK,
}


def get_picture(picture_url):

    response = requests.get(picture_url)
    response.raise_for_status()

    return response.content


unpublished_posts = google_api.get_unpublished_posts(spreadsheet_id)

if unpublished_posts:
    sm_publish_statuses = dict.fromkeys(SOCIAL_MEDIA)
    for post in unpublished_posts:
        text = google_api.get_publishing_text(post['Текст'])
        picture = get_picture(post['Фото'])
        for sm in SOCIAL_MEDIA:
            if post[sm].strip():
                link = SOCIAL_MEDIA[sm](text, picture)
                sm_publish_statuses[sm] = link
    print(sm_publish_statuses)
