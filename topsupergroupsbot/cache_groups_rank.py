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

import time

from topsupergroupsbot import database

CACHE_SECONDS = 60*3

CACHE_KEY = 'cached_groups_rank'
BY_MESSAGES = 'by_messages'
BY_MEMBERS = 'by_members'
BY_VOTES = 'by_votes'
RANK = 'rank'
CACHED_AT = 'cached_at'


def filling_dict(dct_name, group_id, by, value):
    data = {RANK: value, CACHED_AT: time.time()}
    try:
        dct_name[group_id][by] = data
    except KeyError:
        dct_name[group_id] = {}
        dct_name[group_id][by] = data
    return dct_name


def caching_ranks():
    #############
    # MESSAGES
    ############

    query = """
        SELECT 
            group_id,
            COUNT(msg_id) AS msgs, 
            RANK() OVER(PARTITION BY s.lang ORDER BY COUNT(msg_id) DESC)
        FROM messages 
        LEFT OUTER JOIN supergroups as s 
        USING (group_id)
        WHERE message_date > date_trunc('week', now())
        GROUP BY s.lang, group_id;
    
    """
    msgs_this_week = database.query_r(query)


    ##################
    #   MEMBERS
    ##################

    query = """
         SELECT
            last_members.group_id,
            last_members.amount, 
            RANK() OVER(PARTITION BY s.lang ORDER BY last_members.amount DESC)
        FROM
            (
            SELECT
                *,
                ROW_NUMBER() OVER (
                    PARTITION BY group_id
                    ORDER BY updated_date DESC
                    ) AS row
            FROM members
        ) AS last_members 
        LEFT OUTER JOIN supergroups AS s 
        USING (group_id)
        WHERE last_members.row=1
    """
    members_this_week = database.query_r(query)

    ####################
    # SUM AND AVG VOTES
    ####################

    query = """
        SELECT
            group_id,
            COUNT(vote) AS amount,
            ROUND(AVG(vote), 1) AS average, 
            RANK() OVER(PARTITION BY s.lang ORDER BY ROUND(AVG(VOTE), 1)DESC, COUNT(VOTE)DESC)
        FROM votes 
        LEFT OUTER JOIN supergroups AS s 
        USING (group_id)
        GROUP BY group_id, s.lang;
    """
    this_week_votes_avg = database.query_r(query)

    dct = {}
    for group in msgs_this_week:
        dct = filling_dict(dct, group[0], BY_MESSAGES, group[2])

    for group in members_this_week:
        dct = filling_dict(dct, group[0], BY_MEMBERS, group[2])

    for group in this_week_votes_avg:
        dct = filling_dict(dct, group[0], BY_VOTES, group[3])

    print(dct)



caching_ranks()