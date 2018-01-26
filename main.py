from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, InlineQueryHandler, CallbackQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, \
    KeyboardButton
import telegram
import logging
import base64


# start 命令
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


# 显示用户输入的字符串
def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


# 字符串转换为大写
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)


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


# 生成菜单
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:1 + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def base64_menu(bot, update):
    keyboards = [
        [
            InlineKeyboardButton("base64文字加密", callback_data='1'),
            InlineKeyboardButton("base64文字解密", callback_data='2')
        ],
        [
            InlineKeyboardButton("base64图片加密", callback_data='3'),
            InlineKeyboardButton("base64图片解密", callback_data='4')
        ]
    ]
    reply_markup = telegram.InlineKeyboardMarkup(keyboards)
    update.message.reply_text('Buttons: ', reply_markup=reply_markup)


def base64_menu_handler(bot, update):
    query = update.callback_query
    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


# 处理未知的命令
def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def main():
    token = open(r'/home/alinone/env.txt', 'r').read()
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(CommandHandler('caps', caps, pass_args=True))
    dispatcher.add_handler(CommandHandler('encode', base64_encode, pass_args=True))
    dispatcher.add_handler(CommandHandler('decode', base64_decode, pass_args=True))
    dispatcher.add_handler(InlineQueryHandler(inline_caps))
    dispatcher.add_handler(CommandHandler('base64', base64_menu))
    dispatcher.add_handler(CallbackQueryHandler(base64_menu_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
