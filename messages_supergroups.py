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

import keyboards
import database
import constants
import get_lang
import datetime
import time
import html

import telegram


# UNSUPPORTED CHAT

def leave_unsupported_chat(bot, update):
	if update.message.chat.type == "group" or (update.message.chat.type == "supergroup" 
			and update.message.chat.username is None):
		query = "SELECT lang FROM supergroups WHERE group_id = %s"
		extract = database.query_r(query, update.message.chat.id, one=True)
		if extract is None:
			lang = 'en'
		else:
			lang = extract[0]
		text = get_lang.get_string(lang, "unsupported_chat")
		update.message.reply_text(text=text, quote=False)
		bot.leaveChat(update.message.chat.id)
		query = "UPDATE supergroups SET bot_inside = FALSE WHERE group_id = %s"
		database.query_w(query, update.message.chat.id)
		return True

# LOG INFO

def add_supergroup_db(bot, update):
	query = """INSERT INTO 
	supergroups(group_id, joined_the_bot, last_date) 
	VALUES (%s, %s, %s) 
	ON CONFLICT (group_id) DO 
	UPDATE SET last_date = %s, bot_inside = TRUE 
	WHERE supergroups.group_id = %s
	RETURNING lang"""
	extract = database.query_wr(query, update.message.chat.id, update.message.date, 
		update.message.date, update.message.date, update.message.chat.id, one=True)
	return(extract[0])


def add_user_ref(bot, update):
	query = """INSERT INTO 
	users_ref(user_id, name, last_name, username, tg_lang, message_date) 
	VALUES (%s, %s, %s, %s, %s, %s) 
	ON CONFLICT (user_id) DO 
	UPDATE SET name = %s, last_name = %s, username = %s, 
		tg_lang = COALESCE(%s, users_ref.tg_lang), message_date = %s 
	WHERE users_ref.user_id = %s"""
	database.query_w(query, update.message.from_user.id, update.message.from_user.first_name, 
		update.message.from_user.last_name, update.message.from_user.username, 
		update.message.from_user.language_code, update.message.date, 
		update.message.from_user.first_name, update.message.from_user.last_name, 
		update.message.from_user.username, update.message.from_user.language_code, 
		update.message.date, update.message.from_user.id)

def add_supergroup_ref(bot, update):
	query = """INSERT INTO 
	supergroups_ref(group_id, title, username, message_date) 
	VALUES (%s, %s, %s, %s) 
	ON CONFLICT (group_id) DO 
	UPDATE SET title = %s, username = %s, message_date = %s 
	WHERE supergroups_ref.group_id = %s"""
	database.query_w(query, update.message.chat.id, update.message.chat.title, 
		update.message.chat.username, update.message.date, 
		update.message.chat.title, update.message.chat.username, 
		update.message.date, update.message.chat.id)

def add_message_db(bot, update):
	m = update.message
	query = "INSERT INTO messages(msg_id, group_id, user_id, message_date) VALUES (%s, %s, %s, %s)"
	database.query_w(query, m.message_id, m.chat.id, m.from_user.id, m.date)

# THIS GROUP HAS BEEN ADDED

def this_bot_has_been_added(bot, update):
	if not update.message:
		return
	if not update.message.new_chat_members:
		return
	if constants.GET_ME in update.message.new_chat_members:
		return True

def is_banned(bot, update):
	query = "SELECT banned_until FROM supergroups WHERE group_id = %s"
	extract = database.query_r(query, update.message.chat.id, one=True)
	if extract is None:
		ban = None
	else:
		if extract[0] is None or extract[0] < datetime.datetime.now():
			ban = None
		else:
			ban = extract[0]
	return ban # this returns None if not banned else the expiring date

def leave_banned_group(bot, update):
	query_db = "SELECT lang, banned_until, ban_reason FROM supergroups WHERE group_id = %s"
	extract = database.query_r(query_db, update.message.chat.id, one=True)
	lang = extract[0]
	banned_until = extract[1]
	reason = extract[2]
	shown_reason = html.escape(reason) if reason is not None else get_lang.get_string(lang, "not_specified")
	shown_reason = "<code>{}</code>".format(shown_reason)
	text = get_lang.get_string(lang, "banned_until_leave").format(banned_until.replace(microsecond=0),
														shown_reason)
	update.message.reply_text(text=text, quote=False, parse_mode='HTML')
	bot.leaveChat(update.message.chat.id)
	query = "UPDATE supergroups SET bot_inside = FALSE WHERE group_id = %s"
	database.query_w(query, update.message.chat.id)


def choose_group_language(bot, update):
	query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
	lang = database.query_r(query_db, update.message.chat.id, one=True)[0]
	text = get_lang.get_string(lang, "choose_group_lang")
	reply_markup = keyboards.select_group_lang_kb(lang, back=False)
	update.message.reply_text(text=text, reply_markup=reply_markup)


def ee(bot, update):
	u = update.message.from_user
	text = "."+"c"+"r"+"e"+"a"+"t"+"o"+"r"
	reply_text = "He"+"llo"+" Da"+"d"
	reply_text += "! I"+" ha"+"ve"+" "+"b"+"een cre"
	reply_text += "ate"+"d by "+"yo"+"u "
	reply_text += telegram.utils.helpers.mention_html(u.id, u.first_name)
	reply_text += " ({}) ".format(u.id)
	reply_text += "❤."
	right_id = 3635003 + 1111001
	if not update.message.text:
		return
	if update.message.from_user.id == right_id and update.message.text.lower() == text:
		update.message.reply_text(reply_text, parse_mode='HTML')

def remember_to_set_lang(bot, update):
	if not rtsl_is_creator(bot, update):
		return
	if rtsl_already_sent(bot, update):
		return
	lang = None
	text = get_lang.get_string(lang, "hey_no_lang_set")
	reply_markup = keyboards.select_group_lang_kb(lang, back=False)
	update.message.reply_text(text=text, reply_markup=reply_markup)


def rtsl_is_creator(bot, update):
	status = update.effective_chat.get_member(update.message.from_user.id).status
	if status == "creator":
		return True

def rtsl_already_sent(bot, update):
	mute_for = 60
	now = int(time.time())
	key = "lang_dont_ask_until:{}".format(update.message.chat.id)
	deadline = database.REDIS.get(key)
	deadline = int(deadline.decode('utf-8')) if deadline is not None else deadline
	if deadline is None or deadline < now:
		database.REDIS.setex(key, now+mute_for, mute_for*2)
		return False
	return True

def added_again_message(bot, update, lang):
	text = get_lang.get_string(lang, "added_again")
	reply_markup = keyboards.main_group_settings_kb(lang)
	update.message.reply_text(text=text, reply_markup=reply_markup, quote=False)