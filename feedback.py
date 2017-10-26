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


import get_lang
import commands_private
import utils
import constants as c
import database as db

from config import config



INTERVAL = 60*60*24*7
MAX_ALLOWED = 5

class Feedback:
    def __init__(self, bot, update):
        self.feedback_from = update.message.from_user

    def feedback_key(self):
        key = "feedback_flood:{}".format(self.feedback_from.id)
        return key

    def is_allowed(self):
        key = self.feedback_key()
        result = db.REDIS.get(key)
        if result is None:
            return True
        return True if int(result) <= MAX_ALLOWED else False

    def increment_feedback(self):
        key = self.feedback_key()
        result = db.REDIS.incr(key, amount=1)
        if result.decode('UTF-8') == 1:
            db.REDIS.expire(key, INTERVAL)

    def receive_feedback(self, bot, update):
        sender_id = self.feedback_from.id
        lang = utils.get_db_lang(sender_id)
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
        self.increment_feedback()

    def do_not_receive_feedback(self, bot, update):
        sender_id = self.feedback_from.id
        lang = utils.get_db_lang(sender_id)
        update.message.reply_text(get_lang.get_string(lang, "feedback_flood"), quote=True)


def is_a_feedback(bot, update):
    if update.message.reply_to_message is None:
        return False
    if update.message.reply_to_message.text is None:
        return False
    if update.message.reply_to_message.from_user.id == bot.id and (
            update.message.reply_to_message.text).startswith(c.FEEDBACK_INV_CHAR):
        return True


def handle_receive_feedback(bot, update):
    fb = Feedback(bot, update)
    if fb.is_allowed():
        fb.receive_feedback(bot, update)
        fb.increment_feedback()
    else:
        fb.do_not_receive_feedback(bot, update)