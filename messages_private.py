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

import database
import utils
import constants as c
import commands_private
import get_lang

from config import config


def add_user_db(bot, update):
    m = update.message

    guessed_lang = utils.guessed_user_lang(bot, update)

    query = """INSERT INTO users(user_id, lang, region, tg_lang, message_date) 
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (user_id) DO 
    UPDATE SET bot_blocked = FALSE, tg_lang = COALESCE(%s, users.tg_lang), message_date = %s 
        WHERE users.user_id = %s"""
    database.query_w(
            query, m.from_user.id, guessed_lang, guessed_lang,
            m.from_user.language_code, m.date, m.from_user.language_code,
            m.date, m.from_user.id)


def is_a_feedback(bot, update):
    if update.message.reply_to_message is None:
        return
    if update.message.reply_to_message.text is None:
        return

    if update.message.reply_to_message.from_user.id == bot.id and (
            update.message.reply_to_message.text).startswith(c.FEEDBACK_INV_CHAR):
        return True


def feedback_key(bot, update):
    key = "feedback_flood:{}".from_user(update.message.from_user.id)


def receive_feedback(bot, update):
    sender_id = update.message.from_user.id
    lang = utils.get_db_lang(sender_id)
    if 1:#is_allowed(sender_id):
        forwarded = update.message.forward(config.FOUNDER, disable_notification=True)
        forwarded.reply_text(
                "#id_"+str(sender_id)+"\n#feedback_from_user", 
                quote=True, 
                disable_notification=True)
        forwarded.reply_text(
                commands_private.get_info_id(bot, sender_id), 
                quote=True, 
                disable_notification=True)
        update.message.reply_text(get_lang.get_string(lang, "thanks_feedback"), quote=True)
        return True

    else:
        update.message.reply_text(get_lang.get_string(lang, "feedback_flood"), quote=True)
        return False
