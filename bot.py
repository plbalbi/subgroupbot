from telegram.ext import Updater, CommandHandler
from telegram import ParseMode


def command_decorator(func):
    def func_wrapper(*args, **kwargs):
        bot, update = args
        if update.effective_chat.type != 'group':
            bot.send_message(chat_id=update.message.chat_id, text="This bot is for groups.")
            return
        if update.effective_chat.all_members_are_administrators:
            return func(*args, **kwargs)
        return bot.send_message(chat_id=update.message.chat_id, text="All members of the group must be administrators to use me.")
    return func_wrapper


def get_group_members(chat):
    return [member.user for member in chat.get_administrators()]


@command_decorator
def tag(bot, update):
    msg = ' '.join([user.mention_markdown() for user in get_group_members(update.effective_chat)])
    bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.MARKDOWN)

@command_decorator
def addsubgroup(bot, update):
    # import pdb; pdb.set_trace()
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    group_name = words[1]
    bot.send_message(chat_id=update.message.chat_id, text="Adding {}".format(group_name))

with open('token') as f:
    token = f.readline().strip()
updater = Updater(token)

updater.dispatcher.add_handler(CommandHandler('tag', tag))
updater.dispatcher.add_handler(CommandHandler('addsubgroup', addsubgroup))

updater.start_polling()
updater.idle()
