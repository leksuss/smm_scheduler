from environs import Env
import telegram


def post_image_with_message(post_text, post_image, tg_chat_id, bot):

    message = bot.send_photo(
        chat_id=tg_chat_id, photo=post_image, caption=post_text
    )
    return message['message_id']


def post_message(post_text, tg_chat_id, bot):

    message = bot.send_message(chat_id=tg_chat_id, text=post_text)
    return message['message_id']


def publish_to_tg(post_text, post_image=None):

    env = Env()
    env.read_env()

    tg_token = env.str('TELEGRAM_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')

    tg_bot = telegram.Bot(tg_token)

    try:
        if post_image:
            message_id = post_image_with_message(
                post_text, post_image, tg_chat_id, tg_bot
            )
        else:
            message_id = post_message(post_text, tg_chat_id, tg_bot)

        if message_id:
            return f"https://t.me/{tg_chat_id}/{message_id}"
        return None

    except telegram.error.NetworkError as e:
        print('Network connection problem', e, sep='\n')
        return None
