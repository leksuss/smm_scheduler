import telegram
from telegram.error import NetworkError
from dotenv import load_dotenv
from os import environ
from retry import retry


@retry(NetworkError, tries=3, delay=1, backoff=5)
def post_image_file(image_files, tg_chat_id, bot):
    with open(image_files, 'rb') as file:
       message = bot.send_photo(chat_id=tg_chat_id, photo=file)
    return f"https://t.me/smm_planer_dev/{message['message_id']}"


@retry(NetworkError, tries=3, delay=1, backoff=5)
def post_message(post_text, tg_chat_id, bot):
    message = bot.send_message(chat_id=tg_chat_id, text=post_text)
    return f"https://t.me/smm_planer_dev/{message['message_id']}"


def post_context_to_tg(post_text, post_image):

    load_dotenv()
    telegram_token = environ['TELEGRAM_TOKEN']
    tg_chat_id = environ['TG_CHAT_ID']
    telegram_bot = telegram.Bot(telegram_token)   
    if not post_image and not post_text:
        return None   
    try:
        if post_image:
            post_link_photo = post_image_file(post_image, tg_chat_id, telegram_bot)
        if post_text:
            post_link_text = post_message(post_text, tg_chat_id, telegram_bot)
            return post_link_text
        return post_link_photo
    except NetworkError:
        print('Ошибка подключения')
        return None
    

#TELEGRAM_TOKEN = 6158617927:AAGRfhA2_b4Cw6MYoUx4anUNJU4u-_tMXH8
#TG_CHAT_ID = @smm_planer_dev