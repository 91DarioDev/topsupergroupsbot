# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# TopSupergroupsBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TopSupergroupsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TopSupergroupsBot.  If not, see <http://www.gnu.org/licenses/>.

import babel
import datetime
import time
from functools import wraps

from topsupergroupsbot import supported_langs
from topsupergroupsbot import constants
from topsupergroupsbot import get_lang
from topsupergroupsbot import database
from topsupergroupsbot import config

from telegram import constants as ptb_consts

from babel.dates import format_datetime, format_date
from babel.numbers import format_decimal


def get_db_lang(user_id):
    query = "SELECT lang FROM users WHERE user_id = %s"
    extract = database.query_r(query, user_id, one=True)
    lang = extract[0] if extract is not None else 'en'
    return lang


def bot_owner_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.from_user.id not in config.ADMINS:
            invalid_command(bot, update)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def private_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.chat.type != "private":
            lang = get_db_lang(update.effective_user.id)
            text = get_lang.get_string(lang, "this_command_only_private")
            try:
                chat_id = update.message.from_user.id
                bot.send_message(chat_id=chat_id, text=text)
            except:
                status = update.effective_chat.get_member(update.message.from_user.id).status
                if status not in ["administrator", "creator"]:
                    return
                update.message.reply_text(text)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def admin_command_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.chat.type == "private":
            lang = get_db_lang(update.effective_user.id)
            text = get_lang.get_string(lang, "this_command_only_admins")
            update.message.reply_text(text)
            return
        if not update.effective_chat.get_member(update.message.from_user.id).status in ["administrator", "creator"]:
            lang = get_db_lang(update.effective_user.id)
            text = get_lang.get_string(lang, "this_command_only_admins")
            try:
                chat_id = update.message.from_user.id
                bot.send_message(chat_id=chat_id, text=text)
            except Exception as e:
                print(e)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def creator_command_only(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        if update.message.chat.type == "private":
            lang = get_db_lang(update.effective_user.id)
            text = get_lang.get_string(lang, "this_command_only_creator")
            update.message.reply_text(text)
            return
        status = update.effective_chat.get_member(update.message.from_user.id).status
        if status not in ["creator"]:
            lang = get_db_lang(update.effective_user.id)
            text = get_lang.get_string(lang, "this_command_only_creator")
            try:
                chat_id = update.message.from_user.id
                bot.send_message(chat_id=chat_id, text=text)
            except:
                if status in ['administrator']:
                    update.message.reply_text(text)
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def creator_button_only(func):
    @wraps(func)
    def wrapped(bot, query, *args, **kwargs):
        if query.message.chat.type == "private":
            return
        if not query.message.chat.get_member(query.from_user.id).status in ["creator"]:
            lang = get_db_lang(query.from_user.id)
            text = get_lang.get_string(lang, "button_for_creator")
            query.answer(text=text, show_alert=True)
            return
        return func(bot, query, *args, **kwargs)
    return wrapped


def admin_button_only(func):
    @wraps(func)
    def wrapped(bot, query, *args, **kwargs):
        if query.message.chat.type == "private":
            return
        if not query.message.chat.get_member(query.from_user.id).status in ["administrator", "creator"]:
            lang = get_db_lang(query.from_user.id)
            text = get_lang.get_string(lang, "button_for_admins")
            query.answer(text=text, show_alert=True)
            return
        return func(bot, query, *args, **kwargs)
    return wrapped


def invalid_command(bot, update):
    lang = get_db_lang(update.effective_user.id)
    text = get_lang.get_string(lang, "invalid_command")
    update.message.reply_text(text=text, quote=True)


def send_message_long(
            bot, chat_id, text, parse_mode=None, disable_web_page_preview=None,
            disable_notification=False, reply_to_message_id=None,
            reply_markup=None, timeout=None):

    list_messages = []
    chars_limit = ptb_consts.MAX_MESSAGE_LENGTH

    for i in range(0, len(text), chars_limit):
        splitted_message = text[i:i+chars_limit]
        list_messages.append(splitted_message)

    for message in list_messages:
        if message == list_messages[0]:
            first = bot.sendMessage(
                    chat_id=chat_id, text=message, parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                    timeout=timeout)
        else:
            bot.sendMessage(
                    chat_id=chat_id, text=message, parse_mode=parse_mode,
                    disable_web_page_preview=disable_web_page_preview,
                    disable_notification=disable_notification,
                    reply_to_message_id=reply_to_message_id, reply_markup=reply_markup,
                    timeout=timeout)
        time.sleep(0.3)

    if len(text) > 1000:
        first.reply_text("\U00002B06", disable_notification, quote=True)


def guessed_user_lang(bot, update):
    if update.message.from_user.language_code is None:
        return "en"
    user2code = str(update.effective_user.language_code.split("-")[0])
    if user2code in supported_langs.PRIVATE_LANGS:
        return user2code
    else:
        return "en"


def sep(num, none_is_zero=False):
    if num is None:
        return 0 if none_is_zero is False else None
    return "{:,}".format(num)


def sep_l(num, locale='en', none_is_zero=False):
    if num is None:
        return None if none_is_zero is False else 0
    if locale is None:
        return "{:,}".format(num)
    try:
        return babel.numbers.format_decimal(num, locale=locale)
    except babel.core.UnknownLocaleError:
        return "{:,}".format(num)


def formatted_datetime_l(datetime, locale='en', formate='medium', tzinfo=None):
    if datetime is None:
        return None
    if locale is None:
        locale = 'en'
    locale = locale.split("-")[0]  # because babel have problems if contains '-'

    try:
        return format_datetime(
                datetime=datetime, 
                locale=locale, 
                format=formate, 
                tzinfo=tzinfo)
    except babel.core.UnknownLocaleError:
        return format_datetime(
                datetime=datetime, 
                locale='en', 
                format=formate, 
                tzinfo=tzinfo)


def formatted_date_l(date, locale='en', formate='medium'):
    if date is None:
        return None
    if locale is None:
        locale = 'en'
    locale = locale.split("-")[0]  # because babel have problems if contains '-'

    try:
        return format_date(
                date=date, 
                locale=locale, 
                format=formate)
    except babel.core.UnknownLocaleError:
        return format_date(
                date=date, 
                locale='en', 
                format=formate)