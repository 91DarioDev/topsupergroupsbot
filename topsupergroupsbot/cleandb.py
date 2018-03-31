# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017-2018  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
#
# TopSupergroupsBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TopSupergroupsBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with TopSupergroupsBot.  If not, see <http://www.gnu.org/licenses/>.

from topsupergroupsbot import database

from telegram.ext.dispatcher import run_async

CLEAN_INTERVAL = '1 month'


@run_async
def clean_db(bot, job):
    query = "DELETE FROM messages WHERE message_date < now() - interval %s"
    database.query_w(query, CLEAN_INTERVAL)

    query = "DELETE FROM members WHERE updated_date < now() - interval %s"
    database.query_w(query, CLEAN_INTERVAL)


@run_async
def check_bot_inside_in_inactive_groups(bot, job):
	query = """
		SELECT
			rows_by_group.group_id,
			rows_by_group.message_date,
			rows_by_group.row
		FROM
			(
			SELECT
				group_id,
				message_date,
				ROW_NUMBER() OVER (PARTITION BY group_id ORDER BY message_date DESC) AS row
			FROM messages
		) AS rows_by_group
		LEFT OUTER JOIN supergroups AS s
		USING (group_id)
		WHERE 
			rows_by_group.row=1
			AND s.bot_inside IS TRUE
			AND rows_by_group.message_date < (NOW() - INTERVAL %s); 
	"""

	interval = '3 days'
	lst = database.query_r(query, interval)

	for item in lst:
		group_id = item[0]
		print(group_id)
	print(lst)