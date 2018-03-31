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

	start_in = 0
	for item in lst:
		start_in += 0.2
		group_id = item[0]
		job.job_queue.run_once(send_chat_action_inactive_group, start_in, context=[group_id])


@run_async
def send_chat_action_inactive_group(bot, job):
	errors = [
		"Forbidden: bot was kicked from the supergroup chat",
		"Forbidden: bot is not a member of the supergroup chat"
	]
	group_id = job.context[0]
	try:
		bot.sendChatAction(chat_id=group_id, action='typing')
	except Exception as e:
		if e in errors:
			print(e)
			print('right usage in clean_db inactive groups')
			query = "UPDATE supergroups SET bot_inside=FALSE WHERE group_id=%s"
			database.query_w(query, group_id)
		else:
			print(e)
			print("cleandb inactive groups")


