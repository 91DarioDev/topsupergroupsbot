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
import json

from topsupergroupsbot import database as db
from collections import OrderedDict

CACHE_SECONDS = 60*3
LATEST_UPDATE_KEY = 'latest_update'
REDIS_KEY = 'cached_users'

def group_extract(lst):
    # thank https://stackoverflow.com/a/46493187/8372336 for the help in this func
    # and a bit modified by me
    d = OrderedDict()

    for k, *v in lst:
        k = k, *v[:4]
        d.setdefault(k, []).append(v[4:])

    final = list(d.items())
    return final

def cache_users_stats(bot, job):
    at_seconds = time.time()
    lst = get_all_users_stats()
    dct = {}
    for i in lst:
        user_id = i[0][0]
        dct[user_id] = json.dumps(i).encode('UTF-8')
    dct[LATEST_UPDATE_KEY] = at_seconds
    db.REDIS.hmset(REDIS_KEY, dct)
    db.REDIS.expire(REDIS_KEY, CACHE_SECONDS*2)


def get_cached_user(user_id):
    user_cache, latest_update = db.REDIS.hmget(REDIS_KEY, user_id, LATEST_UPDATE_KEY)
    user_cache = user_cache if user_cache is None else json.loads(user_cache.decode('UTF-8'))
    latest_update = latest_update if latest_update is None else float(latest_update.decode('UTF-8'))
    return user_cache, latest_update

def get_all_users_stats():
    query = """
        WITH tleft AS (
        SELECT  main.user_id, u.lang, main.num_msgs, main.num_grps, main.rnk 
        FROM (
        SELECT
            user_id,
            num_grps,
            num_msgs,
            RANK() OVER(ORDER BY num_msgs DESC, num_grps DESC, user_id DESC) rnk
        FROM (
            SELECT
                user_id,
                COUNT(distinct group_id) AS num_grps,
                COUNT(*)                 AS num_msgs
            FROM messages
            WHERE message_date > date_trunc('week', now())
            GROUP BY user_id
            ) AS sub
        ) AS main
        LEFT OUTER JOIN users AS u
        USING (user_id)
        WHERE u.weekly_own_digest = TRUE
        AND bot_blocked = FALSE
        )
        , tright AS (
        SELECT main.user_id, main.group_id, s_ref.title, s_ref.username, main.m_per_group, main.pos
        FROM (
            SELECT user_id, group_id, COUNT(user_id) AS m_per_group,
                RANK() OVER (
                    PARTITION BY group_id
                    ORDER BY COUNT(group_id) DESC
                    ) AS pos 
            FROM messages
            WHERE message_date > date_trunc('week', now())
            GROUP BY group_id, user_id
        ) AS main 
        LEFT OUTER JOIN supergroups_ref AS s_ref
        USING (group_id)
        ORDER BY m_per_group DESC
        )
        SELECT l.user_id, l.lang, l.num_msgs, l.num_grps, l.rnk, r.title, r.username, r.m_per_group, r.pos
        FROM tleft AS l
        INNER JOIN tright AS r
        USING (user_id)
        """
    return group_extract(db.query_r(query))
    # for i in extract: i[0] = (user_id, lang, msg, grps, pos)
    # i[1] = [[],[]] anyone inside = [groupname, groupusername, msg in group, pos in group]

