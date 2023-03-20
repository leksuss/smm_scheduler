import os
import time

from dotenv import load_dotenv

from api_services import google_api, odnoklassniki_api, tg_api, vk_api
from text_modifier import beautify_text


DELAY_BETWEEN_CHECKS = 60  # in seconds
SOCIAL_MEDIA_NAMES = {
    'OK': odnoklassniki_api.post_context_to_ok,
    'TG': tg_api.post_context_to_tg,
    'VK': vk_api.post_context_to_vk,
}


def main():

    load_dotenv()
    sheet_id = os.environ['SPREADSHEET_ID']
    debug = os.environ['DEBUG']

    creds = google_api.get_credentials()
    sheet_service = google_api.get_spreadsheet_service(creds)
    doc_service = google_api.get_document_service(creds)

    while True:
        unpublished_posts = google_api.get_unpublished_posts(
            sheet_id, sheet_service
        )
        if unpublished_posts:
            for post in unpublished_posts:
                text = google_api.get_publishing_text(
                    post['Текст'], doc_service
                )
                text = beautify_text(text)
                for sm_name in SOCIAL_MEDIA_NAMES:
                    if post[sm_name]:
                        link_or_none = SOCIAL_MEDIA_NAMES[sm_name](
                            text, post['Фото']
                        )
                        post[sm_name] = link_or_none
                google_api.update_post_row(
                    SOCIAL_MEDIA_NAMES, post, sheet_id, sheet_service
                )

        if debug:
            break

        time.sleep(DELAY_BETWEEN_CHECKS)


if __name__ == '__main__':
    main()
