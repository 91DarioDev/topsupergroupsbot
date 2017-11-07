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
import time
import json

from topsupergroupsbot import utils
from topsupergroupsbot import database
from topsupergroupsbot import constants
from topsupergroupsbot import get_lang
from topsupergroupsbot import supported_langs
from topsupergroupsbot import emojis
from topsupergroupsbot.pages import Pages

from telegram import ParseMode
from telegram.ext.dispatcher import run_async


class Leaderboard:
    GROUP = 'igl'  # inside the group
    VOTES = 'vl'
    MESSAGES = 'ml'
    MEMBERS = 'mml'

    NEW_INTERVAL = 60*60*24*7

    def __init__(self, lang=None, region="", page=1):
        self.lang = lang
        self.region = region
        self.page = page

    def buttons_callback_base(self):
        return "lbpage:{page}:{lb_type}:{region}".format(
                page='{page}',
                lb_type=self.CODE, 
                region=self.region)

    def cache_key_base(self):
        return 'cached_lb:{}:{}'.format(
                self.CODE, 
                self.region)

    def get_list_from_cache(self):
        key = self.cache_key_base()
        lst = database.REDIS.get(key)
        if lst is None:
            return None
        lst = json.loads(lst.decode('UTF-8'))
        return lst

    @run_async
    def cache_the_list(self, lst, doubled_cache_seconds=False):
        key = self.cache_key_base()
        dumped_lst = json.dumps(lst).encode('UTF-8')
        sec = self.CACHE_SECONDS if doubled_cache_seconds is False else self.CACHE_SECONDS*2
        database.REDIS.setex(key, dumped_lst, sec)

    def set_scheduled_cache(self):
        total = self.all_results_no_filters()
        by_language = utils.split_list_grouping_by_column(total, self.INDEX_LANG)
        for split in by_language:
            lb = self.__class__(region=split)
            lb.cache_the_list(by_language[split], doubled_cache_seconds=True)

            
class VotesLeaderboard(Leaderboard):
    CODE = 'vl'
    MIN_REVIEWS = 1
    CACHE_SECONDS = 60*3
    INDEX_LANG = 7

    def build_page(self):
        query = """
        SELECT 
            v.group_id, 
            s_ref.title, 
            s_ref.username, 
            COUNT(vote) AS amount, 
            ROUND(AVG(vote), 1)::float AS average,
            s.nsfw, 
            extract(epoch from s.joined_the_bot at time zone 'utc') AS dt,
            RANK() OVER (ORDER BY ROUND(AVG(vote), 1) DESC, COUNT(vote) DESC)
        FROM votes AS v
        LEFT OUTER JOIN supergroups_ref AS s_ref
        USING (group_id)
        LEFT OUTER JOIN supergroups AS s
        USING (group_id)
        GROUP BY v.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang
        HAVING 
            (s.banned_until IS NULL OR s.banned_until < now()) 
            AND s.lang = %s
            AND COUNT(vote) >= %s 
        """

        extract = self.get_list_from_cache()
        if extract is None:
            extract = database.query_r(query, self.region, self.MIN_REVIEWS)
            self.cache_the_list(extract)

        pages = Pages(extract, self.page)

        reply_markup = pages.build_buttons(base=self.buttons_callback_base())

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadervote").format(self.MIN_REVIEWS, emoji_region)
        text += "\n\n"
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[5] is True else ""
            new = emojis.NEW if (group[6]+self.NEW_INTERVAL > time.time()) else ""
            text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}|{}{}\n".format(
                    group[7],
                    nsfw, 
                    group[2], 
                    html.escape(group[1]), 
                    group[4], 
                    emojis.STAR,
                    utils.sep_l(group[3], self.lang),
                    new
                    )
        return text, reply_markup

    def all_results_no_filters(self):
        query = """
              SELECT 
                  v.group_id, 
                  s_ref.title, 
                  s_ref.username, 
                  COUNT(vote) AS amount, 
                  ROUND(AVG(vote), 1)::float AS average,
                  s.nsfw, 
                  extract(epoch from s.joined_the_bot at time zone 'utc') AS dt,
                  s.lang,
                  RANK() OVER (ORDER BY ROUND(AVG(vote), 1) DESC, COUNT(vote) DESC)
              FROM votes AS v
              LEFT OUTER JOIN supergroups_ref AS s_ref
              ON s_ref.group_id = v.group_id
              LEFT OUTER JOIN supergroups AS s
              ON s.group_id = v.group_id
              GROUP BY v.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang
              HAVING 
                  (s.banned_until IS NULL OR s.banned_until < now()) 
                  AND COUNT(vote) >= %s 
              """
        return database.query_r(query, self.MIN_REVIEWS)


class MessagesLeaderboard(Leaderboard):
    CODE = 'ml'
    CACHE_SECONDS = 60*3
    INDEX_LANG = 6

    def build_page(self):
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

        extract = self.get_list_from_cache()
        if extract is None:
            extract = database.query_r(query, self.region)
            self.cache_the_list(extract)

        pages = Pages(extract, self.page)
        
        reply_markup = pages.build_buttons(base=self.buttons_callback_base())

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadermessage").format(emoji_region)
        text += "\n\n"
        first_number_of_page = pages.first_number_of_page()
        offset = first_number_of_page - 1
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[4] is True else ""
            new = emojis.NEW if (group[5]+self.NEW_INTERVAL) > time.time() else ""
            offset += 1 # for before IT numeration
            text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}\n".format(
                    offset, 
                    nsfw, 
                    group[3], 
                    html.escape(group[2]), 
                    utils.sep_l(group[1], self.lang), 
                    new
                    )
        return text, reply_markup

    def all_results_no_filters(self):
        query = """
            SELECT 
                m.group_id, 
                COUNT (m.group_id) AS leaderboard,
                s_ref.title, 
                s_ref.username,
                s.nsfw, 
                extract(epoch from s.joined_the_bot at time zone 'utc') AS dt,
                s.lang
            FROM messages AS m
            LEFT OUTER JOIN supergroups_ref AS s_ref
            ON s_ref.group_id = m.group_id
            LEFT OUTER JOIN supergroups AS s
            ON s.group_id = m.group_id
            WHERE m.message_date > date_trunc('week', now())
                AND (s.banned_until IS NULL OR s.banned_until < now()) 
            GROUP BY m.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang
            ORDER BY leaderboard DESC
            """
        return database.query_r(query)


class MembersLeaderboard(Leaderboard):
    CODE = 'mml'
    CACHE_SECONDS = 60*10
    INDEX_LANG = 2

    def build_page(self):
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

        extract = self.get_list_from_cache()
        if extract is None:
            extract = database.query_r(query, self.region)
            self.cache_the_list(extract)
            
        pages = Pages(extract, self.page)

        reply_markup = pages.build_buttons(base=self.buttons_callback_base())

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadermember").format(emoji_region)
        text += "\n\n"
        first_number_of_page = pages.first_number_of_page()
        offset = first_number_of_page - 1   
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[6] is True else ""
            new = emojis.NEW if (group[5]+self.NEW_INTERVAL) > time.time() else ""
            offset += 1 # for before IT numeration
            text += "{}) {}<a href=\"https://t.me/{}\">{}</a>: {}{}\n".format(
                offset, 
                nsfw, 
                group[4], 
                html.escape(group[3]), 
                utils.sep_l(group[1], self.lang), 
                new)
        return text, reply_markup

    def all_results_no_filters(self):
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
            ORDER BY members.amount DESC
            """
        return database.query_r(query)


class GroupLeaderboard(Leaderboard):
    CODE = 'igl'
    CACHE_SECONDS = 60*3

    def build_page(self, group_id):
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

        pages = Pages(extract, self.page)

        reply_markup = pages.build_buttons(base=self.buttons_callback_base())

        text = get_lang.get_string(self.lang, "pre_groupleaderboard")
        text += "\n\n"
        first_number_of_page = pages.first_number_of_page()
        offset = first_number_of_page - 1
        for user in pages.chosen_page_items():
            offset += 1 # for before IT numeration
            text += "{}) <a href=\"tg://user?id={}\">{}</a>: {}\n".format(
                    offset, 
                    user[0], 
                    html.escape(user[2]), 
                    utils.sep_l(user[1], self.lang)
                    )
        return text, reply_markup


@utils.admin_command_only
def groupleaderboard(bot, update):
    group_id = update.message.chat.id
    query = "SELECT lang FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query, group_id, one=True)
    lang = extract[0]

    leaderboard = GroupLeaderboard(lang=lang, page=1)
    result = leaderboard.build_page(group_id)
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_notification=True)


@utils.private_only
def leadervote(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    leaderboard = VotesLeaderboard(lang, region, 1)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)


@utils.private_only
def leadermessage(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    leaderboard = MessagesLeaderboard(lang, region, 1)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)



@utils.private_only
def leadermember(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    leaderboard = MembersLeaderboard(lang, region, 1)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True)


@run_async
def scheduling_votes_leaderboard_cache(bot, job):
    lb = VotesLeaderboard()
    lb.set_scheduled_cache()


@run_async
def scheduling_messages_leaderboard_cache(bot, job):
    lb = MessagesLeaderboard()
    lb.set_scheduled_cache()


@run_async
def scheduling_members_leaderboard_cache(bot, job):
    lb = MembersLeaderboard()
    lb.set_scheduled_cache()