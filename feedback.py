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

from config import config

class Feedback:
    def __init__(self, bot, update):
        self.is_a_feedback = self.is_a_feedback(bot, update)

    def is_a_feedback(self, bot, update):
        if update.message.reply_to_message is None:
            return False
        if update.message.reply_to_message.text is None:
            return False

        if update.message.reply_to_message.from_user.id == bot.id and (
                update.message.reply_to_message.text).startswith(c.FEEDBACK_INV_CHAR):
            return True

    def feedback_key(self, sender_id):
        return self.key = "feedback_flood:{}".from_user(self.sender_id)

    def receive_feedback(self, bot, update):
        sender_id = update.message.from_user.id
        lang = utils.get_db_lang(sender_id)
        if is_allowed(sender_id):
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

    def is_allowed(self, sender_id):
        key = feedback_key(self, sender_id)

