from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import telegram
import logging
import base64

token = open(r'/home/alinone/env.txt', 'r').read()
bot = telegram.Bot(token=token)
updater = Updater(token=token)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# start 命令
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


# 显示用户输入的字符串
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


# 字符串转换为大写
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)


# base64加密
def base64_encode(bot, update, args):
    str = " ".join(args).encode()
    result = base64.b64encode(str)
    bot.send_message(chat_id=update.message.chat_id, text=result.decode())


# base64解密
def base64_decode(bot, update, args):
    str = " ".join(args).encode()
    result = base64.b64decode(str)
    bot.send_message(chat_id=update.message.chat_id, text=result.decode())


base64_encode_handler = CommandHandler('encode', base64_encode, pass_args=True)
base64_decode_handler = CommandHandler('decode', base64_decode, pass_args=True)
dispatcher.add_handler(base64_encode_handler)
dispatcher.add_handler(base64_decode_handler)


def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


# 处理未知的命令
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)
