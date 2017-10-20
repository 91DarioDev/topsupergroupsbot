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

import utils
import database
import keyboards
import constants
import get_lang
import supported_langs
import cached_leaderboards

import datetime
import html
import time

from pages import Pages
from telegram import ParseMode


GROUP_LEADERBOARD = 'igl' # inside the group
VOTE_LEADERBOARD = 'vl'
MESSAGE_LEADERBOARD = 'ml'
MEMBER_LEADERBOARD = 'mml'


NEW_INTERVAL = 60*60*24*7


@utils.admin_command_only
def groupleaderboard(bot, update):
    group_id = update.message.chat.id
    query = "SELECT lang FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query, group_id, one=True)
    lang = extract[0]

    result = offset_groupleaderboard(lang, group_id, chosen_page=1)

    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_notification=True)


def offset_groupleaderboard(lang, group_id, chosen_page):
    query = """
    SELECT m.user_id, COUNT(m.user_id) AS leaderboard,
        u_ref.name, u_ref.last_name, u_ref.username
    FROM messages AS m
    LEFT OUTER JOIN users_ref AS u_ref
    ON u_ref.user_id = m.user_id
    WHERE m.group_id = %s
        AND m.message_date > date_trunc('week', now())
    GROUP BY m.user_id, u_ref.name, u_ref.last_name, u_ref.username
    ORDER BY leaderboard DESC
    """

    extract = database.query_r(query, group_id)
    
    pages = Pages(extract, chosen_page)

    reply_markup = keyboards.displayed_pages_kb(
            pages=pages.displayed_pages(), 
            chosen_page=pages.chosen_page, 
            lb_type=GROUP_LEADERBOARD)

    text = get_lang.get_string(lang, "pre_groupleaderboard")
    text += "\n\n"
    first_number_of_page = pages.first_number_of_page()
    offset = first_number_of_page - 1
    for user in pages.chosen_page_items():
        offset += 1 # for before IT numeration
        text += "{}) <a href=\"tg://user?id={}\">{}</a>: {}\n".format(
                offset, 
                user[0], 
                html.escape(user[2]), 
                utils.sep_l(user[1], lang)
                )
    return text, reply_markup


@utils.private_only
def leadervote(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    result = offset_leadervote(lang, region, 1)
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)


def offset_leadervote(lang, region, chosen_page):
    min_reviews = 1

    query = """
    SELECT 
        v.group_id, 
        s_ref.title, 
        s_ref.username, 
        COUNT(vote) AS amount, 
        ROUND(AVG(vote), 1)::float AS average,
        s.nsfw, 
        extract(epoch from s.joined_the_bot at time zone 'utc') AS dt
    FROM votes AS v
    LEFT OUTER JOIN supergroups_ref AS s_ref
    ON s_ref.group_id = v.group_id
    LEFT OUTER JOIN supergroups AS s
    ON s.group_id = v.group_id
    GROUP BY v.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang
    HAVING 
        (s.banned_until IS NULL OR s.banned_until < now()) 
        AND s.lang = %s
        AND COUNT(vote) >= %s 
    ORDER BY average DESC, amount DESC
    """

    extract = cached_leaderboards.get_leaderboard(name_type=VOTE_LEADERBOARD, region=region)
    if extract is None:
        extract = database.query_r(query,region, min_reviews)
        cached_leaderboards.set_leaderboard(VOTE_LEADERBOARD, region, extract)

    pages = Pages(extract, chosen_page)

    reply_markup = keyboards.displayed_pages_kb(
            pages=pages.displayed_pages(), 
            chosen_page=pages.chosen_page, 
            lb_type=VOTE_LEADERBOARD, 
            region=region)

    emoji_region = supported_langs.COUNTRY_FLAG[region]
    text = get_lang.get_string(lang, "pre_leadervote").format(min_reviews, emoji_region)
    text += "\n\n" 
    first_number_of_page = pages.first_number_of_page()
    offset = first_number_of_page - 1
    for group in pages.chosen_page_items():
        nsfw = constants.EMOJI_NSFW if group[5] is True else ""
        new = constants.EMOJI_NEW if (group[6]+NEW_INTERVAL > time.time()) else ""
        offset += 1 # for before IT numeration
        text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}|{}{}\n".format(
                offset, 
                nsfw, 
                group[2], 
                html.escape(group[1]), 
                group[4], 
                constants.EMOJI_STAR, 
                utils.sep_l(group[3], lang),
                new
                )
    return text, reply_markup


@utils.private_only
def leadermessage(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    result = offset_leadermessage(lang, region,  1)
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)


def offset_leadermessage(lang, region, chosen_page):
    query = """
    SELECT 
        m.group_id, 
        COUNT (m.group_id) AS leaderboard,
        s_ref.title, 
        s_ref.username,
        s.nsfw, 
        extract(epoch from s.joined_the_bot at time zone 'utc') AS dt
    FROM messages AS m
    LEFT OUTER JOIN supergroups_ref AS s_ref
    ON s_ref.group_id = m.group_id
    LEFT OUTER JOIN supergroups AS s
    ON s.group_id = m.group_id
    WHERE m.message_date > date_trunc('week', now())
        AND (s.banned_until IS NULL OR s.banned_until < now()) 
        AND s.lang = %s
    GROUP BY m.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until 
    ORDER BY leaderboard DESC
    """

    extract = cached_leaderboards.get_leaderboard(name_type=MESSAGE_LEADERBOARD, region=region)
    if extract is None:
        extract = database.query_r(query, region)
        cached_leaderboards.set_leaderboard(MESSAGE_LEADERBOARD, region, extract)

    pages = Pages(extract, chosen_page)

    reply_markup = keyboards.displayed_pages_kb(
            pages=pages.displayed_pages(), 
            chosen_page=pages.chosen_page, 
            lb_type=MESSAGE_LEADERBOARD, 
            region=region)

    emoji_region = supported_langs.COUNTRY_FLAG[region]
    text = get_lang.get_string(lang, "pre_leadermessage").format(emoji_region)
    text += "\n\n"
    first_number_of_page = pages.first_number_of_page()
    offset = first_number_of_page - 1
    for group in pages.chosen_page_items():
        nsfw = constants.EMOJI_NSFW if group[4] is True else ""
        new = constants.EMOJI_NEW if (group[5]+NEW_INTERVAL) > time.time() else ""
        offset += 1 # for before IT numeration
        text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}\n".format(
                offset, 
                nsfw, 
                group[3], 
                html.escape(group[2]), 
                utils.sep_l(group[1], lang), 
                new
                )
    return text, reply_markup


@utils.private_only
def leadermember(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    result = offset_leadermember(lang, region,  1)
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)



def offset_leadermember(lang, region, chosen_page):
    # Thank https://stackoverflow.com/a/46496407/8372336 to make clear this query
    query = """
    SELECT 
        members.*, 
        supergroups.lang, 
        supergroups_ref.title, 
        supergroups_ref.username, 
        extract(epoch from supergroups.joined_the_bot at time zone 'utc') AS dt,
        supergroups.nsfw
    FROM
    -- Window function to get only de last_date:
        (SELECT last_members.group_id,last_members.amount
        FROM
        (SELECT *, ROW_NUMBER() OVER (PARTITION BY group_id
        ORDER BY updated_date DESC) AS row FROM members) AS last_members
        WHERE last_members.row=1) AS members
    -- Joins with other tables
    LEFT JOIN supergroups
    ON members.group_id = supergroups.group_id
    LEFT JOIN supergroups_ref 
    ON supergroups.group_id = supergroups_ref.group_id
    WHERE (supergroups.banned_until IS NULL OR supergroups.banned_until < now()) 
        AND lang = %s
    ORDER BY members.amount DESC
    """

    extract = cached_leaderboards.get_leaderboard(name_type=MEMBER_LEADERBOARD, region=region)
    if extract is None:
        extract = database.query_r(query, region)
        cached_leaderboards.set_leaderboard(MEMBER_LEADERBOARD, region, extract)
        
    pages = Pages(extract, chosen_page)

    reply_markup = keyboards.displayed_pages_kb(
            pages=pages.displayed_pages(), 
            chosen_page=pages.chosen_page, 
            lb_type=MEMBER_LEADERBOARD, 
            region=region)

    emoji_region = supported_langs.COUNTRY_FLAG[region]
    text = get_lang.get_string(lang, "pre_leadermember").format(emoji_region)
    text += "\n\n"
    first_number_of_page = pages.first_number_of_page()
    offset = first_number_of_page - 1   
    for group in pages.chosen_page_items():
        nsfw = constants.EMOJI_NSFW if group[6] is True else ""
        new = constants.EMOJI_NEW if (group[5]+NEW_INTERVAL) > time.time() else ""
        offset += 1 # for before IT numeration
        text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}\n".format(
            offset, 
            nsfw, 
            group[4], 
            html.escape(group[3]), 
            utils.sep_l(group[1], lang), 
            new)
    return text, reply_markup
