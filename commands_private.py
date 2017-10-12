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
import get_lang
from telegram.error import (TelegramError, 
							Unauthorized, 
							BadRequest, 
							TimedOut, 
							ChatMigrated, 
							NetworkError)




@utils.bot_owner_only
def stats_users(bot, update):
	# total users grouped by regions
	query = """
	SELECT region, COUNT(user_id) AS amount
	FROM users 
	GROUP BY region
	ORDER BY amount DESC
	"""
	text = "<b>Total users per region:\n</b>"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])

	# users grouped by regions didn't block the bot
	query = """
	SELECT region, COUNT(user_id) AS amount
	FROM users 
	WHERE bot_blocked = FALSE
	GROUP BY region
	ORDER BY amount DESC
	"""
	text += "\n<b>Users didn't block the bot:\n</b>"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])


	# users grouped by regions didn't block the bot active 7 days
	query = """
	SELECT region, COUNT(user_id) AS amount 
	FROM users 
	WHERE bot_blocked = FALSE AND message_date > (now() - interval '7 days')
	GROUP BY region
	ORDER BY amount DESC
	"""
	text += "\n<b>Didn't block the bot and active in the last 7 days per region:</b>\n"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])

	update.message.reply_text(text=text, parse_mode='HTML')


@utils.bot_owner_only
def stats_groups(bot, update):
	# total groups
	query = """
	SELECT lang, COUNT(group_id) AS amount
	FROM supergroups
	GROUP BY lang
	ORDER BY amount DESC
	"""
	text = "<b>Total groups per lang:</b>\n"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])


	# total groups bot not removed
	query = """
	SELECT lang, COUNT(group_id) AS amount
	FROM supergroups
	WHERE bot_inside = TRUE
	GROUP BY lang
	ORDER BY amount DESC
	"""
	text += "<b>\nTotal groups per lang didn't remove the bot:</b>\n"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])


	# total groups bot inside and joined last 7 days
	query = """
	SELECT lang, COUNT(group_id) AS amount
	FROM supergroups
	WHERE bot_inside = TRUE AND last_date > (now() - interval '7 days')
	GROUP BY lang
	ORDER BY amount DESC
	"""
	text += "<b>\nTotal groups per lang didn't remove the bot and joined in the past 7 days:</b>\n"
	extract = database.query_r(query)
	for i in extract:
		text += "— <b>{}:</b> {}\n".format(i[0], i[1])

	update.message.reply_text(text=text, parse_mode='HTML')


@utils.bot_owner_only
def infoid(bot, update, args):
	if len(args) != 1:
		update.message.reply_text("1 args per time")
		return
	tgid = int(args[0])
	try:
		result = bot.getChat(chat_id=tgid)
	except BadRequest as e:
		update.message.reply_text(str(e))
		return

	if tgid < 0:
		text = "title: {}".format(result.title)
		text += "\nusername: @{}".format(result.username)
		text += "\n"+infoid_from_db(tgid)
	else:
		text = "\nName: {}".format(result.first_name)
		text += "\nLast name: {}".format(result.last_name)
		text += "\nUsername: @{}".format(result.username)
		text += "\n"+infoid_from_db(tgid)
	update.message.reply_text(text)


def infoid_from_db(user_id):
	if user_id > 0:
		query = """
			SELECT 		
				lang,
				region, 
				tg_lang,
				bot_blocked,
				banned_on, 
				banned_until,
				weekly_own_digest,
				weekly_groups_digest,
				message_date
			FROM users
			WHERE user_id = %s"""
		extract = database.query_r(query, user_id, one=True)
		text = ""
		text += "lang: {}\n".format(extract[0])
		text += "region: {}\n".format(extract[1])
		text += "tg_lang: {}\n".format(extract[2])
		text += "bot_blocked: {}\n".format(extract[3])
		text += "banned_on: {}\n".format(extract[4])
		text += "banned_until: {}\n".format(extract[5])
		text += "weekly_own_digest: {}\n".format(extract[6])
		text += "weekly_groups_digest: {}\n".format(extract[7])
		text += "message_date: {}\n".format(extract[8])
	else:
		query = """ 
		SELECT
			lang,
			nsfw,
			joined_the_bot,
			banned_on,
			banned_until,
			bot_inside,
			last_date
		FROM supergroups
		WHERE group_id = %s
		"""
		extract = database.query_r(query, group_id, one=True)
		text = ""
		text += "lang: {}\n".format(extract[0])
		text += "nsfw: {}\n".format(extract[1])
		text += "joined_the_bot: {}\n".format(extract[2])
		text += "banned_on: {}\n".format(extract[3])
		text += "banned_until: {}\n".format(extract[4])
		text += "bot_inside: {}\n".format(extract[5])
		text += "last_date: {}\n".format(extract[6])
	return text



@utils.bot_owner_only
def reverse_username(bot, update, args):
	if len(args) != 1:
		update.message.reply_text("1 arg per time")
		return
	username = args[0]
	username = "@"+str(username) if not (username.startswith("@")) else username
	try:
		result = bot.getChat(chat_id=username)
	except BadRequest as e:
		update.message.reply_text(e)
		return
	text = "id: {}".format(result['id'])
	text += ""
	update.message.reply_text(text, quote=True)



@utils.bot_owner_only
def ban_group(bot, update, args):
	if len(args) != 3:
		update.message.reply_text("specify id for days\nexample: -34545322 for 30")
		return
	group_id = args[0]
	days = int(args[2])
	query = """
		UPDATE supergroups 
		SET banned_on = now(), 
		banned_until = now() + interval '%s days' 
		WHERE group_id = %s
		RETURNING lang
	"""
	extract = database.query_wr(query, days, group_id, one=True)
	lang = extract[0]
	text = get_lang.get_string(lang, "banned_leave")
	bot.send_message(chat_id=group_id, text=text)
	bot.leaveChat(group_id)
	query = "UPDATE supergroups SET bot_inside = FALSE WHERE group_id = %s"
	database.query_w(query, group_id)


@utils.bot_owner_only
def unban_group(bot, update, args):
	if len(args) != 1:
		update.message.reply_text("1 args as id")
		return
	group_id = args[0]
	query = """
		UPDATE supergroups SET banned_on = NULL, banned_until = NULL WHERE group_id = %s
	"""
	database.query_w(query, group_id)
	update.message.reply_text("unbanned", quote=True)