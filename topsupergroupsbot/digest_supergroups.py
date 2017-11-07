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

import html

from topsupergroupsbot import database
from topsupergroupsbot import get_lang
from topsupergroupsbot import keyboards
from topsupergroupsbot import utils
from topsupergroupsbot import emojis

from telegram.error import (TelegramError, 
                            Unauthorized, 
                            BadRequest, 
                            TimedOut, 
                            ChatMigrated, 
                            NetworkError)
from telegram.ext.dispatcher import run_async


@run_async
def weekly_groups_digest(bot, job):
    near_interval = '7 days'
    far_interval = '14 days'

    query = """
        SELECT
            group_id,
            lang,
            nsfw,
            joined_the_bot
        FROM supergroups
        WHERE weekly_digest = TRUE AND bot_inside = TRUE
        ORDER BY last_date DESC
        """
    lst = database.query_r(query)

    #############
    # MESSAGES
    ############

    query = """
        SELECT 
            group_id,
            COUNT(msg_id) AS msgs, 
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY COUNT(msg_id) DESC)
        FROM messages 
        LEFT OUTER JOIN supergroups as s 
        USING (group_id)
        WHERE message_date > now() - interval %s
        GROUP BY s.lang, group_id;

    """
    msgs_this_week = database.query_r(query, near_interval)

    query = """
        SELECT 
            group_id, 
            COUNT(msg_id) AS msgs,
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY COUNT(msg_id) DESC)
        FROM messages
        LEFT OUTER JOIN supergroups as s 
        USING (group_id)
        WHERE message_date BETWEEN now() - interval %s AND now() - interval %s
        GROUP BY s.lang, group_id
    """
    msgs_last_week = database.query_r(query, far_interval, near_interval)
    
    #############
    # MEMBERS
    ############

    query = """
         SELECT
            last_members.group_id,
            last_members.amount, 
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY last_members.amount DESC)
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


    query = """
        SELECT 
            last_members.group_id, 
            last_members.amount,
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY last_members.amount DESC)
        FROM
            (
            SELECT 
                *, 
                ROW_NUMBER() OVER (
                    PARTITION BY group_id
                    ORDER BY updated_date DESC
                    ) AS row 
            FROM members
            WHERE updated_date <= now() - interval %s
        ) AS last_members 
        LEFT OUTER JOIN supergroups AS s 
        USING (group_id)
        WHERE last_members.row=1
        """
    members_last_week = database.query_r(query, near_interval)

    ####################
    # SUM AND AVG VOTES
    ####################

    query = """
        SELECT 
            group_id,
            COUNT(vote) AS amount, 
            ROUND(AVG(vote), 1) AS average
        FROM votes
        GROUP BY group_id
    """
    this_week_votes_avg = database.query_r(query, near_interval)

    query = """
        SELECT 
            group_id,
            COUNT(vote) AS amount, 
            ROUND(AVG(vote), 1) AS average
        FROM votes
        WHERE vote_date BETWEEN (now() - interval %s) AND (now() - interval %s)
        GROUP BY group_id
    """
    last_week_votes_avg = database.query_r(query, far_interval, near_interval)

    ##################
    # ACTIVE USERS
    ##################

    query = """
         SELECT
            group_id,
            COUNT(DISTINCT user_id), 
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY COUNT(DISTINCT user_id) DESC)
        FROM messages 
        LEFT OUTER JOIN supergroups AS s 
        USING (group_id)
        WHERE message_date > (now() - interval %s)
        GROUP BY group_id, s.lang
        """
    this_week_active_users = database.query_r(query, near_interval)

    query = """
        SELECT 
            group_id,
            COUNT(DISTINCT user_id), 
            DENSE_RANK() OVER(PARTITION BY s.lang ORDER BY COUNT(DISTINCT user_id) DESC)
        FROM messages
        LEFT OUTER JOIN supergroups AS s 
        USING (group_id)
        WHERE message_date BETWEEN (now() - interval %s) AND (now() - interval %s)
        GROUP BY group_id, s.lang
        """
    last_week_active_users = database.query_r(query, far_interval, near_interval)

    start_in = 0
    for group in lst:
        start_in += 0.1
        group_id = group[0]
        lang = group[1]

        msgs_new = 0
        msgs_old = 0

        members_new = 0
        members_old = 0

        sum_v_new = 0
        avg_v_new = 0
        sum_v_old = 0
        avg_v_old = 0

        act_users_new = 0
        act_users_old = 0

        for i in msgs_this_week:
            if i[0] == group_id:
                msgs_new = i[1]
                break

        for i in msgs_last_week:
            if i[0] == group_id:
                msgs_old = i[1]
                break

        for i in members_this_week:
            if i[0] == group_id:
                members_new = i[1]
                break

        for i in members_last_week:
            if i[0] == group_id:
                members_old = i[1]
                break

        for i in this_week_votes_avg:
            if i[0] == group_id:
                sum_v_new = i[1]
                avg_v_new = i[2]
                break

        for i in last_week_votes_avg:
            if i[0] == group_id:
                sum_v_old = i[1]
                avg_v_old = i[2]
                break

        for i in this_week_active_users:
            if i[0] == group_id:
                act_users_new = i[1]
                break

        for i in last_week_active_users:
            if i[0] == group_id:
                act_users_old = i[1]
                break

        diff_msg, percent_msg = diff_percent(msgs_new, msgs_old, lang)
        diff_members, percent_members = diff_percent(members_new, members_old, lang) 
        diff_act, percent_act = diff_percent(act_users_new, act_users_old, lang)
        text = get_lang.get_string(lang, "weekly_groups_digest").format(
                    utils.sep_l(msgs_old, lang), utils.sep_l(msgs_new, lang), 
                    diff_msg, percent_msg,
                    utils.sep_l(members_old, lang), utils.sep_l(members_new, lang), 
                    diff_members, percent_members, 
                    utils.sep_l(avg_v_old, lang), emojis.STAR, utils.sep_l(sum_v_old, lang),
                    utils.sep_l(avg_v_new, lang), emojis.STAR, utils.sep_l(sum_v_new, lang),
                    utils.sep_l(act_users_old, lang), utils.sep_l(act_users_new, lang),
                    diff_act, percent_act)

        ##############
        # TOP n USERS
        ##############

        query_top_users = """
            SELECT 
                user_id,
                COUNT(msg_id) AS num_msgs, 
                name 
            FROM messages AS m
            LEFT OUTER JOIN users_ref AS u_ref
            USING (user_id)
            WHERE group_id = %s AND m.message_date > (now() - interval %s)
            GROUP BY user_id, name
            ORDER BY num_msgs DESC
            LIMIT %s
            """
        top_users_of_the_group = database.query_r(query_top_users, group_id, near_interval, 10)
        count = 0
        for user in top_users_of_the_group:
            count += 1
            text += "{}) <a href=\"tg://user?id={}\">{}</a>: {}\n".format(
                    count,
                    user[0],
                    html.escape(user[2]),
                    utils.sep_l(user[1], lang)
                    )

        reply_markup = keyboards.disable_group_weekly_digest_kb(lang)
        # schedule send
        job.job_queue.run_once(
                send_one_by_one_weekly_group_digest, 
                start_in, 
                context=[group_id, text, reply_markup]
                )


def diff_percent(new, old, lang):
    diff = new - old
    diff_s = utils.sep_l(diff, lang) if diff < 0 else "+"+utils.sep_l(diff, lang)
    try:
        percent = round(diff*100/old, 2)
        percent_s = (utils.sep_l(percent, lang) if percent < 0 else "+"+utils.sep_l(percent, lang))+"%"
    except ZeroDivisionError:
        percent_s = "—" 
    return diff_s, percent_s


@run_async
def send_one_by_one_weekly_group_digest(bot, job):
    group_id = job.context[0]
    message = job.context[1]
    reply_markup = job.context[2]
    try:
        bot.send_message(
                chat_id=group_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode='HTML',
                disable_notification=True)
    except Unauthorized:
        query = "UPDATE supergroups SET bot_inside = FALSE WHERE group_id = %s"
        database.query_w(query, group_id)
    except Exception as e:
        print("{} exception is send_one_by_one group digest".format(e))
