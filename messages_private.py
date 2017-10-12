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

def add_user_db(bot, update):
	m = update.message

	guessed_lang = utils.guessed_user_lang(bot, update)

	query = """INSERT INTO users(user_id, lang, region, tg_lang, message_date) 
	VALUES (%s, %s, %s, %s, %s) 
	ON CONFLICT (user_id) DO 
	UPDATE SET bot_blocked = FALSE, tg_lang = COALESCE(%s, users.tg_lang), message_date = %s 
		WHERE users.user_id = %s"""
	database.query_w(query, m.from_user.id, guessed_lang, guessed_lang, 
					m.from_user.language_code, m.date, m.from_user.language_code, 
					m.date, m.from_user.id)


