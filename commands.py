from telegram import ParseMode

from helpers import command_decorator, to_tag_str, get_group_members

@command_decorator
def tag(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=to_tag_str(get_group_members(update.effective_chat)), parse_mode=ParseMode.MARKDOWN)

@command_decorator
def addsubgroup(bot, update):
    words = update.message.text.split(' ')
    if len(words) == 1:
        return bot.send_message(chat_id=update.message.chat_id, text="You should type the name of the subgroup (\addsubgroup subgroup_name)")
    elif len(words) > 2:
        return bot.send_message(chat_id=update.message.chat_id, text="The subgroup name should be only one word")

    group_name = words[1]
    bot.send_message(chat_id=update.message.chat_id, text="Adding {}".format(group_name))
