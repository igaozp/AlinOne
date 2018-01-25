import telegram

token = open(r'/home/alinone/env.txt', 'r').read()
bot = telegram.Bot(token=token)

print(bot.get_me())
