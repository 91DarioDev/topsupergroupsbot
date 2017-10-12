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

import messages_private
import messages_supergroups

from antiflood import antiflood

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

	if messages_supergroups.this_bot_has_been_added(bot, update):
		messages_supergroups.choose_group_language(bot, update)
	else:
		if lang is None:
			messages_supergroups.remember_to_set_lang(bot, update)
		

def before_processing_private(bot, update):
	messages_private.add_user_db(bot, update)


#                               _           
#    _ __ _ _ ___  __ ___ _____(_)_ _  __ _ 
#   | '_ \ '_/ _ \/ _/ -_|_-<_-< | ' \/ _` |
#   | .__/_| \___/\__\___/__/__/_|_||_\__, |
#   |_|                               |___/ 


def processing_supergroups(bot, update):
	# check if flood
	if antiflood.is_flood(bot, update):
		raise DispatcherHandlerStop

	# log message in the database	
	messages_supergroups.add_message_db(bot, update)
	messages_supergroups.ee(bot, update)


def processing_private(bot, update):
	# i will implement here buttons
	pass
