from telegram.ext import Updater, CommandHandler
from commands import tag, addsubgroup

with open('token') as f:
    token = f.readline().strip()
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('tag', tag))
updater.dispatcher.add_handler(CommandHandler('addsubgroup', addsubgroup))

updater.start_polling()
updater.idle()
