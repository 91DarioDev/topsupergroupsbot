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

from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, 
                            ChatMigrated, NetworkError)

from telegram.ext.dispatcher import run_async


INTERVAL = 2

DEADLINE = '5 hours' # so if i restart the bot they are not updated after few time


@run_async
def members_log(bot, job):
    bulk_list = get_groups_to_log(bot, job) # retrieve groups to update
    set_bulk(bot, job, bulk_list) # set a bulk one by one with delay


def get_groups_to_log(bot, job):
    query = """
    SELECT s.group_id 
    FROM supergroups AS s
    LEFT OUTER JOIN members AS m
    USING (group_id)
        WHERE s.bot_inside = TRUE
        AND m.updated_date < (now() - interval %s) OR m.updated_date IS NULL
    ORDER BY m.updated_date ASC NULLS FIRST
    """

    extract = database.query_r(query, DEADLINE)
    return extract


def set_bulk(bot, job, extract):
    start_in = 0
    for i in extract:
        group_id = i[0]
        start_in += INTERVAL
        job.job_queue.run_once(handle_one_by_one, start_in, context=group_id)
        


def handle_one_by_one(bot, job):
    group_id = job.context

    try:
        info = bot.getChat(group_id)
        members = bot.getChatMembersCount(group_id)

        query = """
        INSERT INTO members(group_id, amount, updated_date)
        VALUES(%s, %s, now())
        """
        database.query_w(query, group_id, members)

        query = """
        INSERT INTO 
        supergroups_ref(group_id, title, username) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (group_id) DO 
        UPDATE SET title = %s, username = COALESCE(%s, supergroups_ref.username) 
        WHERE supergroups_ref.group_id = %s"""

        database.query_w(query, group_id, info.title, info.username, info.title, 
                        info.username, group_id)
    
    except Unauthorized:
        query = """
        UPDATE supergroups
        SET bot_inside = FALSE
        WHERE group_id = %s
        """
        database.query_w(query, group_id)

    except Exception as e:
        print("{} in memberslog".format(e))



