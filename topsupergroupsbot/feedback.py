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


from topsupergroupsbot import get_lang
from topsupergroupsbot import commands_private
from topsupergroupsbot import utils
from topsupergroupsbot import constants as c
from topsupergroupsbot import database as db

from config import config

from telegram.error import (TelegramError, 
                            Unauthorized, 
                            BadRequest, 
                            TimedOut, 
                            ChatMigrated, 
                            NetworkError)


INTERVAL = 60*60*24*7
MAX_ALLOWED = 5


class Feedback:
    def __init__(self, bot, update, receive=False, reply=False):
        if receive:
            self.feedback_from = update.message.from_user
        elif reply:
            self.feedback_from = update.message.reply_to_message.forward_from

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
        if result == 1:
            db.REDIS.expire(key, INTERVAL)

    def remove_key(self):
        key = self.feedback_key()
        result = db.REDIS.delete(key)

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

    def do_not_receive_feedback(self, bot, update):
        sender_id = self.feedback_from.id
        lang = utils.get_db_lang(sender_id)
        update.message.reply_text(get_lang.get_string(lang, "feedback_flood"), quote=True)

    def reply_feedback(self, bot, update):
        first = None
        try:
            lang = utils.get_db_lang(self.feedback_from.id)

            if update.message.text:
                first = bot.sendMessage(
                        chat_id=self.feedback_from.id, 
                        text=update.message.text)

            elif update.message.voice:
                media = update.message.voice.file_id
                duration = update.message.voice.duration
                caption = update.message.caption
                first = bot.sendVoice(
                        chat_id=self.feedback_from.id, 
                        voice=media, 
                        duration=duration, 
                        caption=caption)

            elif update.message.photo:
                media = update.message.photo[-1].file_id
                caption = update.message.caption
                first = bot.sendPhoto(
                        chat_id=self.feedback_from.id, 
                        photo=media, 
                        caption=caption)

            elif update.message.sticker:
                media = update.message.sticker.file_id
                first = bot.sendSticker(
                        chat_id=self.feedback_from.id, 
                        sticker=media)

            elif update.message.document:
                media = update.message.document.file_id
                filename = update.message.document.file_name
                caption = update.message.caption
                first = bot.sendDocument(
                        chat_id=self.feedback_from.id, 
                        document=media, 
                        filename=filename, 
                        caption=caption)
                
            elif update.message.audio:
                media = update.message.audio.file_id
                duration = update.message.audio.duration
                performer = udpate.message.audio.performer
                title = update.message.audio.title
                caption = update.message.caption
                first = bot.sendAudio(
                        chat_id=self.feedback_from.id, 
                        audio=media, 
                        duration=duration, 
                        performer=performer, 
                        title=title, 
                        caption=caption)
                
            elif update.message.video:
                media = update.message.video.file_id
                caption = update.message.caption
                duration = update.message.video.duration
                first = bot.sendVideo(
                        chat_id=self.feedback_from.id, 
                        video=media, 
                        duration=duration, 
                        caption=caption)

            bot.sendMessage(
                    chat_id=self.feedback_from.id, 
                    text=get_lang.get_string(lang, "from_developer"), 
                    parse_mode='HTML', 
                    reply_to_message_id=first.message_id)

            confirm = "sent to #id_{}".format(self.feedback_from.id)
            bot.sendMessage(chat_id=config.FOUNDER, text=confirm, disable_notification=True)
            
        except Unauthorized as e:
            reason = "Message not sent.\n\n<code>{}</code>".format(e.message)
            update.message.reply_text(reason, quote=True, parse_mode='HTML')


def is_a_feedback(bot, update):
    if update.message.reply_to_message is None:
        return False
    if update.message.reply_to_message.text is None:
        return False
    if update.message.reply_to_message.from_user.id == bot.id and (
            update.message.reply_to_message.text).startswith(c.FEEDBACK_INV_CHAR):
        return True


def handle_receive_feedback(bot, update):
    fb = Feedback(bot, update, receive=True)
    if fb.is_allowed():
        fb.receive_feedback(bot, update)
        fb.increment_feedback()
    else:
        fb.do_not_receive_feedback(bot, update)


def is_a_feedback_reply(bot, update):
    if update.message.from_user.id != config.FOUNDER:
        return False
    if update.message.reply_to_message is None:
        return False
    if update.message.reply_to_message.forward_from is None:
        return False
    if update.message.reply_to_message.from_user.id == bot.id:
        return True


def handle_reply_feedback(bot, update):
    fb = Feedback(bot, update, reply=True)
    fb.reply_feedback(bot, update)
    fb.remove_key()
