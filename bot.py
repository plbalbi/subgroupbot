from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from commands import tag, addsubgroup, start, addmember, buttons_callback

with open('token') as f:
    token = f.readline().strip()
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('tag', tag))
updater.dispatcher.add_handler(CommandHandler('addsubgroup', addsubgroup))
updater.dispatcher.add_handler(CommandHandler('addmember', addmember))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(buttons_callback))

updater.start_polling()
updater.idle()
