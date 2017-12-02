# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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
from topsupergroupsbot import get_lang
from topsupergroupsbot import keyboards
from topsupergroupsbot import utils

from collections import OrderedDict

from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, 
                            ChatMigrated, NetworkError)
from telegram.ext.dispatcher import run_async


def group_extract(lst):
    # thank https://stackoverflow.com/a/46493187/8372336 for the help in this func
    # and a bit modified by me
    d = OrderedDict()

    for k, *v in lst:
        k = k, *v[:4]
        d.setdefault(k, []).append(v[4:])

    final = list(d.items())
    return final


@run_async
def weekly_own_private(bot, job):
    interval = '7 days'

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
        WHERE message_date > now() - interval %s
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
        WHERE message_date > now() - interval %s
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

    # it returns the global stuff for all the users that want the private digist own
    extract = database.query_r(query, interval, interval)
    data = (group_extract(extract))
    schedule_own_private_digest(bot, job, data)
    # for i in extract: i[0] = (user_id, lang, msg, grps, pos)
    # i[1] = [[],[]] anyone inside = [groupname, groupusername, msg in group, pos in group]


def schedule_own_private_digest(bot, job, data):
    start_in = 0
    for i in data:
        start_in += 0.1
        user = i[0]
        groups = i[1]
        
        user_id = user[0]
        lang = user[1]
        tot_msg = user[2]
        tot_grps = user[3]
        tot_pos = user[4]

        text = get_lang.get_string(lang, "digest_of_the_week_global").format(
                utils.sep_l(tot_msg, lang), 
                utils.sep_l(tot_grps, lang), 
                utils.sep_l(tot_pos, lang)
                )
        reply_markup = keyboards.disable_private_own_weekly_digest_kb(lang)
        # append the text of any group for the same user
        for group in groups:
            title = group[0]
            username = group[1]
            msg_g = group[2]
            pos_g = group[3]    
            text += get_lang.get_string(lang, "digest_of_the_week_detail").format(
                    utils.sep_l(msg_g, lang), 
                    username, 
                    utils.sep_l(pos_g, lang)
                    )
        text += "\n#weekly_private_digest"
        # text completed can be scheduled
        job.job_queue.run_once(send_one_by_one, start_in, context=[user_id, text, reply_markup])


@run_async
def send_one_by_one(bot, job):
    user_id = job.context[0]
    message = job.context[1]
    reply_markup = job.context[2]
    try:
        utils.send_message_long(
                bot, 
                chat_id=user_id, 
                text=message, 
                reply_markup=reply_markup,
                disable_notification=True)
    except Unauthorized:
        query = "UPDATE users SET bot_blocked = TRUE WHERE user_id = %s"
        database.query_w(query, user_id)
    except Exception as e:
        print("{} exception is send_one_by_one private own digest".format(e))
