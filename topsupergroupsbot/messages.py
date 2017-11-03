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


from topsupergroupsbot import feedback
from topsupergroupsbot import messages_private
from topsupergroupsbot import messages_supergroups
from topsupergroupsbot import config
from topsupergroupsbot import regular_buttons
from topsupergroupsbot.antiflood import Antiflood

from telegram.ext import DispatcherHandlerStop


def before_processing(bot, update):
    if update.message.chat.type == "private":
        before_processing_private(bot, update)
        
    elif update.message.chat.type == "supergroup":
        before_processing_supergroups(bot, update)


def processing(bot, update):
    if update.message.chat.type == "private":
        processing_private(bot, update)

    elif update.message.chat.type == "supergroup":
        processing_supergroups(bot, update)


#    _          __                                          _           
#   | |__  ___ / _|___ _ _ ___   _ __ _ _ ___  __ ___ _____(_)_ _  __ _ 
#   | '_ \/ -_)  _/ _ \ '_/ -_) | '_ \ '_/ _ \/ _/ -_|_-<_-< | ' \/ _` |
#   |_.__/\___|_| \___/_| \___| | .__/_| \___/\__\___/__/__/_|_||_\__, |
#                               |_|                               |___/                                                                       


def before_processing_supergroups(bot, update): 
    # leave if the group is not public
    if messages_supergroups.leave_unsupported_chat(bot, update):
        raise DispatcherHandlerStop

    # check if the group is not banned, otherwise leave
    if messages_supergroups.this_bot_has_been_added(bot, update):
        if messages_supergroups.is_banned(bot, update):
            messages_supergroups.leave_banned_group(bot, update)
            raise DispatcherHandlerStop

    # log stuff on the tables
    lang = messages_supergroups.add_supergroup_db(bot, update)
    messages_supergroups.add_user_ref(bot, update)
    messages_supergroups.add_supergroup_ref(bot, update)

    # check if the bot has been added and send a welcome message
    if messages_supergroups.this_bot_has_been_added(bot, update):
        if lang is None:
            messages_supergroups.choose_group_language(bot, update)
        else:
            messages_supergroups.added_again_message(bot, update, lang)
    # if it hasn't been added remember to set the language
    # this is run even for commands (before processing)
    else:
        if lang is None:
            messages_supergroups.remember_to_set_lang(bot, update)
        

def before_processing_private(bot, update):
    messages_private.add_user_db(bot, update)

    if feedback.is_a_feedback(bot, update):
        feedback.handle_receive_feedback(bot, update)
        raise DispatcherHandlerStop  # nothing should be done anymore

    if feedback.is_a_feedback_reply(bot, update):
        feedback.handle_reply_feedback(bot, update)


#                               _           
#    _ __ _ _ ___  __ ___ _____(_)_ _  __ _ 
#   | '_ \ '_/ _ \/ _/ -_|_-<_-< | ' \/ _` |
#   | .__/_| \___/\__\___/__/__/_|_||_\__, |
#   |_|                               |___/ 


def processing_supergroups(bot, update):
    user_id = update.message.from_user.id
    group_id = update.message.chat.id
    # check if is flood and handle flood
    for i in config.FLOOD_CHECKS:
        af = Antiflood(
                limit=i, 
                interval=config.FLOOD_CHECKS[i], 
                user_id=user_id, 
                group_id=group_id)
        if af.is_flood():
            raise DispatcherHandlerStop

    # log message in the database   
    messages_supergroups.add_message_db(bot, update)
    messages_supergroups.ee(bot, update)


def processing_private(bot, update):
    if regular_buttons.is_button_syntax(bot, update):
        button = regular_buttons.RegularButtons(bot, update)
        button.call_button_func()
