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


import html
import time
import json

from topsupergroupsbot import utils
from topsupergroupsbot import database
from topsupergroupsbot import constants
from topsupergroupsbot import get_lang
from topsupergroupsbot import supported_langs
from topsupergroupsbot import emojis
from topsupergroupsbot import keyboards
from topsupergroupsbot import categories
from topsupergroupsbot.pages import Pages

from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown

M_C_G = constants.MAX_CHARS_LEADERBOARD_PAGE_GROUP
M_C_P = constants.MAX_CHARS_LEADERBOARD_PAGE_PRIVATE

class Leaderboard:
    GROUP = 'igl'  # inside the group
    VOTES = 'vl'
    MESSAGES = 'ml'
    MEMBERS = 'mml'

    NEW_INTERVAL = 60*60*24*7

    def __init__(self, lang=None, region="", page=1, category=None, group_id=None):
        self.lang = lang
        self.region = region
        self.page = page
        self.category = "" if category is None else category
        self.group_id = group_id

    def buttons_callback_base(self):
        if self.CODE == GroupLeaderboard.CODE:
            return "lbpage:{page}:{lb_type}:{group_id}".format(page='{page}', lb_type=self.CODE, group_id=self.group_id)
        return "lbpage:{page}:{lb_type}:{region}:{category}".format(
                page='{page}',
                lb_type=self.CODE, 
                region=self.region,
                category=self.category)

    def cache_key_base(self):
        if self.CODE == GroupLeaderboard.CODE:
            return 'cached_lb:{}:{}'.format(self.CODE, self.group_id)
        return 'cached_lb:{}:{}'.format(
                self.CODE, 
                self.region)

    def get_list_from_cache(self):
        key = self.cache_key_base()
        lst = database.REDIS.get(key)
        if lst is None:
            return None
        lst_and_time = json.loads(lst.decode('UTF-8'))
        lst = lst_and_time['list']
        time = lst_and_time['time']
        return lst, time

    @run_async
    def cache_the_list(self, lst, doubled_cache_seconds=False):
        key = self.cache_key_base()
        lst_and_time = {'list': lst, 'time': time.time()}
        dumped_lst = json.dumps(lst_and_time).encode('UTF-8')
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
    MIN_REVIEWS = 10
    CACHE_SECONDS = 60*3
    INDEX_LANG = 8
    INDEX_CATEGORY = 9

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
            RANK() OVER (ORDER BY ROUND(AVG(vote), 1) DESC, COUNT(vote) DESC),
            s.lang,
            s.category
        FROM votes AS v
        LEFT OUTER JOIN supergroups_ref AS s_ref
        USING (group_id)
        LEFT OUTER JOIN supergroups AS s
        USING (group_id)
        GROUP BY v.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang, s.category
        HAVING 
            (s.banned_until IS NULL OR s.banned_until < now()) 
            AND s.lang = %s
            AND COUNT(vote) >= %s 
        """

        lst_and_time = self.get_list_from_cache()
        if lst_and_time is None:
            extract = database.query_r(query, self.region, self.MIN_REVIEWS)
            self.cache_the_list(extract)
            cached_sec_ago = 1
        else:
            extract, cached_at = lst_and_time
            cached_sec_ago = int(time.time() - cached_at)
        updated_ago_string = utils.round_seconds(cached_sec_ago, self.lang, short=True)

        if self.category != "":
            extract = [i for i in extract if i[self.INDEX_CATEGORY] == self.category]

        pages = Pages(extract, self.page)

        callback_base = self.buttons_callback_base()
        reply_markup = pages.build_buttons(base=callback_base, footer_buttons=keyboards.filter_category_button(self.lang, callback_base, pages.chosen_page))

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadervote").format(self.MIN_REVIEWS, emoji_region)
        if self.category != "":
            text += "\n{}: {}".format(get_lang.get_string(self.lang, "category"), get_lang.get_string(self.lang, "categories")[categories.CODES[self.category]])
        text += "\n_{}: {}_".format(
            utils.get_lang.get_string(self.lang, "latest_update"),
            updated_ago_string
        )        
        text += "\n\n"
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[5] is True else ""
            new = emojis.NEW if (group[6]+self.NEW_INTERVAL > time.time()) else ""
            text += "{}) {}[{}](t.me/{}): {}{}|{}{}\n".format(
                    group[7],
                    nsfw, 
                    utils.replace_markdown_chars(utils.truncate(group[1], M_C_P)), 
                    group[2],
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
                  RANK() OVER (PARTITION BY s.lang ORDER BY ROUND(AVG(vote), 1) DESC, COUNT(vote) DESC),
                  s.lang,
                  s.category
              FROM votes AS v
              LEFT OUTER JOIN supergroups_ref AS s_ref
              ON s_ref.group_id = v.group_id
              LEFT OUTER JOIN supergroups AS s
              ON s.group_id = v.group_id
              GROUP BY v.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang, s.category
              HAVING 
                  (s.banned_until IS NULL OR s.banned_until < now()) 
                  AND COUNT(vote) >= %s 
              """
        return database.query_r(query, self.MIN_REVIEWS)


class MessagesLeaderboard(Leaderboard):
    CODE = 'ml'
    CACHE_SECONDS = 60*3
    INDEX_LANG = 7
    INDEX_CATEGORY = 8

    def build_page(self):
        query = """
            SELECT 
                m.group_id, 
                COUNT (m.group_id) AS leaderboard,
                s_ref.title, 
                s_ref.username,
                s.nsfw, 
                extract(epoch from s.joined_the_bot at time zone 'utc') AS dt,
                RANK() OVER (ORDER BY COUNT(m.group_id) DESC),
                s.lang,
                s.category
            FROM messages AS m
            LEFT OUTER JOIN supergroups_ref AS s_ref
            ON s_ref.group_id = m.group_id
            LEFT OUTER JOIN supergroups AS s
            ON s.group_id = m.group_id
            WHERE m.message_date > date_trunc('week', now())
                AND (s.banned_until IS NULL OR s.banned_until < now()) 
                AND s.lang = %s
            GROUP BY m.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang, s.category
        """

        lst_and_time = self.get_list_from_cache()
        if lst_and_time is None:
            extract = database.query_r(query, self.region)
            self.cache_the_list(extract)
            cached_sec_ago = 1
        else:
            extract, cached_at = lst_and_time
            cached_sec_ago = int(time.time() - cached_at)
        updated_ago_string = utils.round_seconds(cached_sec_ago, self.lang, short=True)    

        if self.category != "":
            extract = [i for i in extract if i[self.INDEX_CATEGORY] == self.category]

        pages = Pages(extract, self.page)
        
        callback_base = self.buttons_callback_base()
        reply_markup = pages.build_buttons(base=callback_base, footer_buttons=keyboards.filter_category_button(self.lang, callback_base, pages.chosen_page))

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadermessage").format(emoji_region)
        if self.category != "":
            text += "\n{}: {}".format(get_lang.get_string(self.lang, "category"), get_lang.get_string(self.lang, "categories")[categories.CODES[self.category]])
        text += "\n_{}: {}_".format(
            utils.get_lang.get_string(self.lang, "latest_update"),
            updated_ago_string
        )        
        text += "\n\n"
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[4] is True else ""
            new = emojis.NEW if (group[5]+self.NEW_INTERVAL) > time.time() else ""
            text += "{}) {}[{}](t.me/{}): {}{}\n".format(
                    group[6],
                    nsfw, 
                    utils.replace_markdown_chars(utils.truncate(group[2], M_C_P)), 
                    group[3], 
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
                RANK() OVER (PARTITION BY s.lang ORDER BY COUNT(m.group_id) DESC),
                s.lang,
                s.category
            FROM messages AS m
            LEFT OUTER JOIN supergroups_ref AS s_ref
            ON s_ref.group_id = m.group_id
            LEFT OUTER JOIN supergroups AS s
            ON s.group_id = m.group_id
            WHERE m.message_date > date_trunc('week', now())
                AND (s.banned_until IS NULL OR s.banned_until < now()) 
            GROUP BY m.group_id, s_ref.title, s_ref.username, s.nsfw, dt, s.banned_until, s.lang, s.category
            ORDER BY leaderboard DESC
            """
        return database.query_r(query)


class MembersLeaderboard(Leaderboard):
    CODE = 'mml'
    CACHE_SECONDS = 60*10
    INDEX_LANG = 2
    INDEX_CATEGORY = 8

    def build_page(self):
        # Thank https://stackoverflow.com/a/46496407/8372336 to make clear this query
        query = """
        SELECT 
            members.*, 
            supergroups.lang, 
            supergroups_ref.title, 
            supergroups_ref.username, 
            extract(epoch from supergroups.joined_the_bot at time zone 'utc') AS dt,
            supergroups.nsfw,
            RANK() OVER(ORDER BY members.amount DESC),
            supergroups.category
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
        """

        lst_and_time = self.get_list_from_cache()
        if lst_and_time is None:
            extract = database.query_r(query, self.region)
            self.cache_the_list(extract)
            cached_sec_ago = 1
        else:
            extract, cached_at = lst_and_time
            cached_sec_ago = int(time.time() - cached_at)
        updated_ago_string = utils.round_seconds(cached_sec_ago, self.lang, short=True)            
        
        if self.category != "":
            extract = [i for i in extract if i[self.INDEX_CATEGORY] == self.category]    
        
        pages = Pages(extract, self.page)

        callback_base = self.buttons_callback_base()
        reply_markup = pages.build_buttons(base=callback_base, footer_buttons=keyboards.filter_category_button(self.lang, callback_base, pages.chosen_page))

        emoji_region = supported_langs.COUNTRY_FLAG[self.region]
        text = get_lang.get_string(self.lang, "pre_leadermember").format(emoji_region)
        if self.category != "":
            text += "\n{}: {}".format(get_lang.get_string(self.lang, "category"), get_lang.get_string(self.lang, "categories")[categories.CODES[self.category]])
        text += "\n_{}: {}_".format(
            utils.get_lang.get_string(self.lang, "latest_update"),
            updated_ago_string
        )
        text += "\n\n"
        for group in pages.chosen_page_items():
            nsfw = emojis.NSFW if group[6] is True else ""
            new = emojis.NEW if (group[5]+self.NEW_INTERVAL) > time.time() else ""
            text += "{}) {}[{}](t.me/{}): {}{}\n".format(
                group[7],
                nsfw, 
                utils.replace_markdown_chars(utils.truncate(group[3], M_C_P)),
                group[4], 
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
                supergroups.nsfw,
                RANK() OVER (PARTITION BY supergroups.lang ORDER BY members.amount DESC),
                supergroups.category
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
            """
        return database.query_r(query)


class GroupLeaderboard(Leaderboard):
    CODE = 'igl'
    CACHE_SECONDS = 60*3

    def build_page(self, group_username, only_admins=True):
        query = """
            SELECT 
                m.user_id, 
                COUNT(m.msg_id) AS leaderboard,
                u_ref.name, 
                u_ref.last_name, 
                u_ref.username,
                RANK() OVER (ORDER BY COUNT(m.msg_id) DESC)
            FROM messages AS m
            LEFT OUTER JOIN users_ref AS u_ref
            USING (user_id)
            WHERE m.group_id = %s
                AND m.message_date > date_trunc('week', now())
            GROUP BY m.user_id, u_ref.name, u_ref.last_name, u_ref.username
            """

        lst_and_time = self.get_list_from_cache()
        if lst_and_time is None:
            extract = database.query_r(query, self.group_id)
            self.cache_the_list(extract)
            cached_sec_ago = 1
        else:
            extract, cached_at = lst_and_time
            cached_sec_ago = int(time.time() - cached_at)

        updated_ago_string = utils.round_seconds(cached_sec_ago, self.lang, short=True)

        pages = Pages(extract, self.page)

        footer_buttons = keyboards.check_groupleaderboard_in_private_button(self.lang, self.group_id) if only_admins else None
        reply_markup = pages.build_buttons(
            base=self.buttons_callback_base(), 
            only_admins=only_admins, 
            footer_buttons=footer_buttons 
        )

        text = get_lang.get_string(self.lang, "pre_groupleaderboard").format(escape_markdown(group_username))
        text += "\n_{}: {}_".format(
            utils.get_lang.get_string(self.lang, "latest_update"),
            updated_ago_string
        )
        text += "\n\n"
        first_number_of_page = pages.first_number_of_page()
        offset = first_number_of_page - 1
        for user in pages.chosen_page_items():
            offset += 1  # for before IT numeration
            if only_admins:  # it means it's in a group
                text += "{}) [{}](tg://user?id={}): {}\n".format(
                    user[5], 
                    utils.replace_markdown_chars(utils.truncate(user[2], M_C_G)),
                    user[0],
                    utils.sep_l(user[1], self.lang)
                )
            else:  # it's a private chat
                text += "{}) {}: {}\n".format(
                    user[5], 
                    escape_markdown("@"+str(user[4]) if user[4] is not None else user[2]), 
                    utils.sep_l(user[1], self.lang)
                )
        return text, reply_markup


@utils.admin_command_only(possible_in_private=True)
def groupleaderboard(bot, update, args):
    group_id = update.message.chat.id
    query = "SELECT lang FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query, group_id, one=True)
    lang = extract[0]
    page = 1

    if len(args) == 1:
        try:
            page = int(args[0])
            if page <= 0:
                update.message.reply_text(
                    text=get_lang.get_string(lang, "groupleaderboard_command_error").format(update.message.text.split(" ")[0]),
                    parse_mode='HTML'
                )
                return
        except ValueError:
            update.message.reply_text(
                text=get_lang.get_string(lang, "groupleaderboard_command_error").format(update.message.text.split(" ")[0]),
                parse_mode='HTML'
            )
            return

    update.effective_chat.send_action('typing')
    leaderboard = GroupLeaderboard(lang=lang, page=page, group_id=group_id)
    result = leaderboard.build_page(group_username=update.message.chat.username)
    try:
        update.message.reply_text(
                text=result[0],
                reply_markup=result[1],
                parse_mode=ParseMode.MARKDOWN,
                disable_notification=True)
    except BadRequest as e:
        if str(e) == "Reply message not found":
            update.message.reply_text(
                text=result[0],
                reply_markup=result[1],
                parse_mode=ParseMode.MARKDOWN,
                disable_notification=True,
                quote=False)
        else:
            raise


def filter_private_leaderboards_params(bot, update, args, lang):
    page = 1
    category = None
    for arg in args:
        # check correct use of args
        if len(args) >= 1 and not ( arg.startswith("p=") or arg.startswith("c=") ):
            update.message.reply_text(
                text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                parse_mode='HTML'
            )
            return None

        # check if page is specified
        if arg.startswith('p='):
            try:
                page = int(arg.replace("p=", ""))
            except ValueError:
                update.message.reply_text(
                    text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                    parse_mode='HTML'
                )
                return None
            if page <= 0: # page should be positive
                update.message.reply_text(
                text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                parse_mode='HTML'
                )
                return None

        # check if category is specified
        if arg.startswith("c="):
            try:
                category_number = int(arg.replace("c=", ""))
            except ValueError:
                update.message.reply_text(
                    text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                    parse_mode='HTML'
                )
                return None
            if category_number <= 0: # category should be positive
                update.message.reply_text(
                text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                parse_mode='HTML'
                )
                return None
            dct = sorted(categories.CODES.items(), key=lambda x: x[1])
            try:
                category = dct[category_number - 1][0]
            except IndexError:
                update.message.reply_text(
                text=get_lang.get_string(lang, "avdanced_leaderboard_command_error").format(update.message.text.split(" ")[0]),
                parse_mode='HTML'
                )
                return None                

    return page, category


@utils.private_only
def leadervote(bot, update, args):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]

    result = filter_private_leaderboards_params(bot, update, args, lang)
    if result is None:
        return
    else:
        page, category = result


    leaderboard = VotesLeaderboard(lang, region, page, category)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)


@utils.private_only
def leadermessage(bot, update, args):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]

    result = filter_private_leaderboards_params(bot, update, args, lang)
    if result is None:
        return
    else:
        page, category = result

    leaderboard = MessagesLeaderboard(lang, region, page, category)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)



@utils.private_only
def leadermember(bot, update, args):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]

    result = filter_private_leaderboards_params(bot, update, args, lang)
    if result is None:
        return
    else:
        page, category = result
        
    leaderboard = MembersLeaderboard(lang, region, page, category)
    result = leaderboard.build_page()
    update.message.reply_text(
            text=result[0],
            reply_markup=result[1],
            parse_mode=ParseMode.MARKDOWN,
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