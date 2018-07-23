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


import time
import html

from topsupergroupsbot import utils
from topsupergroupsbot import keyboards
from topsupergroupsbot import database
from topsupergroupsbot import constants
from topsupergroupsbot import votelink
from topsupergroupsbot import leaderboards
from topsupergroupsbot import messages_supergroups
from topsupergroupsbot import get_lang
from topsupergroupsbot import supported_langs
from topsupergroupsbot import emojis
from topsupergroupsbot import cache_users_stats
from topsupergroupsbot import cache_groups_rank


def first_start(bot, update):
    user_id = update.message.from_user.id
    query = """
        SELECT 1 
        FROM USERS 
        WHERE user_id = %s 
        FETCH FIRST 1 ROW ONLY
    """
    extract = database.query_r(query, user_id, one=True)
    if extract is None:  # this is the first time the user starts the bot
        # send region choose
        guessed_lang = utils.guessed_user_lang(bot, update)
        text = get_lang.get_string(guessed_lang, "choose_region")
        reply_markup = keyboards.private_region_kb(guessed_lang, guessed_lang)
        update.message.reply_text(text=text, reply_markup=reply_markup)


@utils.private_only
def start(bot, update, args):
    start_help_buttons(bot, update)
    if len(args) == 0:
        if update.message.chat.type == "private":
            start_no_params(bot, update)
        return
    first_arg = args[0]
    if first_arg.lower().startswith("vote"):
        votelink.send_vote_by_link(bot, update, first_arg)
    elif first_arg == "aboutyou":
        aboutyou(bot, update)
    elif first_arg == "groups_working":
        send_groups_working(bot, update)
        return
    elif first_arg.startswith("groupleaderboarddirectlink"):
        group_id = first_arg.replace("groupleaderboarddirectlink", "")
        groupleaderboard_private_direct_link(bot, update, group_id)
        return


def groupleaderboard_private_direct_link(bot, update, group_id):
    user_id = update.message.from_user.id
    lang = utils.get_db_lang(user_id)
    page = 1
    update.effective_chat.send_action('typing')
    query_db = "SELECT username FROM supergroups_ref WHERE group_id = %s LIMIT 1"
    extract = database.query_r(query_db, group_id, one=True)
    leaderboard = leaderboards.GroupLeaderboard(lang=lang, page=page, group_id=group_id)
    result = leaderboard.build_page(group_username=extract[0], only_admins=False)

    update.message.reply_text(
        text=result[0],
        reply_markup=result[1],
        parse_mode='MARKDOWN',
        disable_notification=True
    )


def start_no_params(bot, update):
    lang = utils.get_db_lang(update.message.from_user.id)
    text = get_lang.get_string(lang, "help_message")
    reply_markup = keyboards.help_kb(lang)
    update.message.reply_text(text=text, parse_mode="HTML", reply_markup=reply_markup)


def settings(bot, update):
    if update.message.chat.type == "private":
        settings_private(bot, update)
    elif update.message.chat.type in ['group', 'supergroup']:
        settings_group(bot, update)


def group_rank_private(bot, update, args):
    user_id = update.message.from_user.id
    lang = utils.get_db_lang(user_id)
    if len(args) != 1:
        text = get_lang.get_string(lang, "error_param_group_rank_private")
        update.message.reply_text(text, parse_mode="HTML")
        return
    username = args[0]
    if username.startswith("@"):
        username = username.replace("@", "")

    query = "SELECT group_id FROM supergroups_ref WHERE LOWER(username) = LOWER(%s)"
    extract = database.query_r(query, username)

    if len(extract) > 1:
        print("error too many")
        return

    if len(extract) == 0:
        # the group does not exist otherwise anything is returned and if None is NULL
        text = get_lang.get_string(lang, "cant_check_this").format(html.escape(username))
        update.message.reply_text(text=text)
        return

    group_id = extract[0][0]
    update.message.reply_text(text=group_rank_text(group_id, lang), parse_mode="HTML")


def groupleaderboard_private(bot, update, args):
    user_id = update.message.from_user.id
    lang = utils.get_db_lang(user_id)
    if len(args) > 2 or len(args) == 0:
        text = get_lang.get_string(lang, "error_param_group_leaderboard_private")
        update.message.reply_text(text, parse_mode="HTML")
        return

    if len(args) == 2 and (any([arg.startswith("p=") for arg in args])) is False:
        
        text = get_lang.get_string(lang, "error_param_group_leaderboard_private")
        update.message.reply_text(text, parse_mode="HTML")
        return

    page = 1
    for arg in args:
        if arg.startswith('p='):
            try:
                page = int(arg.replace('p=', ''))
            except ValueError:
                update.message.reply_text(text=get_lang.get_string(lang, "error_param_group_leaderboard_private"), parse_mode='HTML')
                return
            if page <= 0:
                update.message.reply_text(text=get_lang.get_string(lang, "error_param_group_leaderboard_private"), parse_mode='HTML')
        else:
            group_username = arg
            if group_username.startswith("@"):
                group_username = group_username.replace("@", "")

    update.effective_chat.send_action('typing')
    query = "SELECT group_id FROM supergroups_ref WHERE LOWER(username) = LOWER(%s)"
    extract = database.query_r(query, group_username)

    if len(extract) > 1:
        print("error too many")
        return

    if len(extract) == 0:
        # the group does not exist otherwise anything is returned and if None is NULL
        text = get_lang.get_string(lang, "cant_check_this").format(html.escape(group_username))
        update.message.reply_text(text=text)
        return

    group_id = extract[0][0]
    leaderboard = leaderboards.GroupLeaderboard(lang=lang, page=page, group_id=group_id)
    result = leaderboard.build_page(group_username=group_username, only_admins=False)

    update.message.reply_text(
        text=result[0],
        reply_markup=result[1],
        parse_mode='MARKDOWN',
        disable_notification=True)



@utils.private_only
def vote(bot, update, args):
    user_id = update.message.from_user.id
    lang = utils.get_db_lang(user_id)
    if len(args) != 1:
        text = get_lang.get_string(lang, "insert_param_vote")
        update.message.reply_text(text, parse_mode="HTML")
        return
    username = args[0]
    if username.startswith("@"):
        username = username.replace("@", "")
    
    query = """
    SELECT s.group_id, s_ref.username, s_ref.title, v.vote, v.vote_date
    FROM supergroups_ref AS s_ref
    RIGHT JOIN supergroups AS s
    ON s_ref.group_id = s.group_id
    LEFT OUTER JOIN votes AS v 
    ON v.group_id = s.group_id
    AND v.user_id = %s
    WHERE LOWER(s_ref.username) = LOWER(%s) 
        AND s.bot_inside = TRUE
    """

    extract = database.query_r(query, user_id, username)

    if len(extract) == 0:
        # the group does not exist otherwise anything is returned and if None is NULL
        text = get_lang.get_string(lang, "cant_vote_this")
        update.message.reply_text(text=text)
        return

    if len(extract) > 1:
        print("error too many")
        return

    extract = extract[0]
    text = get_lang.get_string(lang, "vote_this_group").format(
                    extract[0], extract[1], extract[2])
    if extract[3] and extract[4] is not None:
        stars = emojis.STAR*extract[3]
        date = utils.formatted_date_l(extract[4].date(), lang)
        text += "\n\n"+get_lang.get_string(lang, "already_voted").format(stars, date)

    if extract[3] and extract[4] is not None:
        reply_markup = keyboards.change_vote_kb(extract[0], lang)
    else:
        text += "\n\n"
        text += get_lang.get_string(lang, "vote_from_one_to_five")
        reply_markup = keyboards.vote_group_kb(extract[0], lang)
    update.message.reply_text(text=text, reply_markup=reply_markup)


def settings_private(bot, update):
    lang = utils.get_db_lang(update.message.from_user.id)
    reply_markup = keyboards.main_private_settings_kb(lang)
    text = get_lang.get_string(lang, "private_settings")
    update.message.reply_text(text=text, reply_markup=reply_markup)


@utils.admin_command_only()
def settings_group(bot, update):
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    lang = database.query_r(query_db, update.message.chat.id, one=True)[0]
    text = get_lang.get_string(lang, "choose_group_lang")
    reply_markup = keyboards.main_group_settings_kb(lang)
    update.message.reply_text(text=text, reply_markup=reply_markup, quote=False)


@utils.admin_command_only(possible_in_private=True)
def groupleaderboard(bot, update, args):
    if update.message.chat.type == "private":
        update.message.reply_text("Only in groups")
        return
    leaderboards.groupleaderboard(bot, update, args)


def language(bot, update):
    if update.message.chat.type == "private":
        language_private(bot, update)
    else:
        language_group(bot, update)


@utils.private_only
def region(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    text = get_lang.get_string(lang, "choose_region")
    reply_markup = keyboards.private_region_kb(lang, region)
    update.message.reply_text(text=text, reply_markup=reply_markup)


@utils.creator_command_only
def language_group(bot, update):
    messages_supergroups.choose_group_language(bot, update)


# this does not need the only private decorator cause the command has the same
# name for groups
def language_private(bot, update):
    query = "SELECT lang FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    text = get_lang.get_string(lang, "choose_your_lang")
    reply_markup = keyboards.private_language_kb(lang, back=False)
    update.message.reply_text(text=text, reply_markup=reply_markup)


@utils.private_only
def aboutyou(bot, update):
    user_id = update.message.from_user.id

    # query = """
    #     WITH tleft AS (
    #         SELECT  main.user_id, u.lang, main.num_msgs, main.num_grps, main.rnk
    #         FROM (
    #         SELECT
    #             user_id,
    #             num_grps,
    #             num_msgs,
    #             DENSE_RANK() OVER(ORDER BY num_msgs DESC, num_grps DESC, user_id DESC) rnk
    #         FROM (
    #             SELECT
    #                 user_id,
    #                 COUNT(distinct group_id) AS num_grps,
    #                 COUNT(*)                 AS num_msgs
    #             FROM messages
    #             WHERE message_date > date_trunc('week', now())
    #             GROUP BY user_id
    #             ) AS sub
    #         ) AS main
    #         LEFT OUTER JOIN users AS u
    #         USING (user_id)
    #         WHERE u.weekly_own_digest = TRUE AND user_id = %s
    #         AND bot_blocked = FALSE
    #         )
    #     , tright AS (
    #         SELECT main.user_id, main.group_id, s_ref.title, s_ref.username, main.m_per_group, main.pos
    #         FROM (
    #             SELECT user_id, group_id, COUNT(user_id) AS m_per_group,
    #                 ROW_NUMBER() OVER (
    #                     PARTITION BY group_id
    #                     ORDER BY COUNT(group_id) DESC
    #                     ) AS pos
    #             FROM messages
    #             WHERE message_date > date_trunc('week', now()) AND user_id = %s
    #             GROUP BY group_id, user_id
    #         ) AS main
    #         LEFT OUTER JOIN supergroups_ref AS s_ref
    #         USING (group_id)
    #         ORDER BY m_per_group DESC
    #         )
    #         SELECT l.user_id, l.lang, l.num_msgs, l.num_grps, l.rnk, r.title, r.username, r.m_per_group, r.pos
    #         FROM tleft AS l
    #         INNER JOIN tright AS r
    #         USING (user_id)
    #         """

    #######################
    #     WARNING!!!!     #
    #######################
    # No more using the query to the db, but using the scheduled cache.
    # by the way the result is returned in the very same form
    # so it can be changed anytime

    # FOLLOWING LINES ARE COMMENTED TO NOT EXECUTE THE QUERY

    #extract = database.query_r(query, user_id, user_id)
    #extract = cache_users_stats.group_extract(extract)[0]


    user_cache, latest_update = cache_users_stats.get_cached_user(user_id)
    lang = utils.get_db_lang(user_id)
    if user_cache is None:
        text = get_lang.get_string(lang, "you_inactive_this_week")

    else:
        text = get_lang.get_string(lang, "this_week_you_sent_this")+"\n\n"
        groups = user_cache[1]
        for group in groups:
            title = group[0]
            username = group[1]
            m_per_group = group[2]
            pos_per_group = group[3]
            text += get_lang.get_string(lang, "messages_in_groups_position").format(
                utils.sep_l(m_per_group, lang),
                username,
                utils.sep_l(pos_per_group, lang)
            )

        # global stats
        text += "\n"+get_lang.get_string(lang, "you_globally_this_week").format(
            utils.sep_l(user_cache[0][2], lang),
            utils.sep_l(user_cache[0][3], lang),
            utils.sep_l(user_cache[0][4], lang)
        )
    text += "\n\n{}: {}.".format(
        utils.get_lang.get_string(lang, "latest_update"),
        utils.round_seconds(int(time.time()-latest_update), lang)
    )
    utils.send_message_long(bot, chat_id=user_id, text=text)


@utils.private_only
def leaderboard(bot, update):
    query = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query, update.message.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    text = get_lang.get_string(lang, "generic_leaderboard").format(supported_langs.COUNTRY_FLAG[region])
    reply_markup = keyboards.generic_leaderboard_kb(lang, region)
    update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="HTML")


@utils.private_only
def help(bot, update):
    start_help_buttons(bot, update)
    lang = utils.get_db_lang(update.message.from_user.id)
    text = get_lang.get_string(lang, "help_message")
    reply_markup = keyboards.help_kb(lang)
    update.message.reply_text(text=text, parse_mode="HTML", reply_markup=reply_markup)


@utils.private_only
def send_groups_working(bot, update):
    lang = utils.get_db_lang(update.message.from_user.id)
    text = get_lang.get_string(lang, "groups_working")
    update.message.reply_text(text=text, parse_mode='HTML')


@utils.private_only
def feedback(bot, update):
    sender_id = update.message.from_user.id
    lang = utils.get_db_lang(sender_id)
    text = constants.FEEDBACK_INV_CHAR
    text += get_lang.get_string(lang, "feedback_message")
    update.message.reply_text(text=text)


def start_help_buttons(bot, update):
    lang = utils.get_db_lang(update.message.from_user.id)
    text = get_lang.get_string(lang, "hello")
    reply_markup = keyboards.default_regular_buttons_kb(lang)
    update.message.reply_text(text=text, reply_markup=reply_markup)


@utils.admin_command_only(possible_in_private=True)
def group_rank(bot, update):
    query = "SELECT lang FROM supergroups WHERE group_id = %s"
    lang = database.query_r(query, update.message.chat.id, one=True)[0]
    update.message.reply_text(text=group_rank_text(update.message.chat.id, lang), parse_mode='HTML', quote=False)


def group_rank_text(group_id, lang):
    strings = get_lang.get_string(lang, "group_rank")
    rank = cache_groups_rank.get_group_cached_rank(group_id)
    if rank is None:
        return strings['None']

    text = strings['title']
    # by messages
    try:
        text += "\n\n"
        text += strings['by_messages'].format(rank[cache_groups_rank.BY_MESSAGES][cache_groups_rank.REGION])
        text += "\n"
        text += strings['position'].format(
            utils.sep_l(rank[cache_groups_rank.BY_MESSAGES][cache_groups_rank.RANK], lang)
        )
        text += "\n"
        text += strings['messages'].format(
            utils.sep_l(rank[cache_groups_rank.BY_MESSAGES][cache_groups_rank.VALUE], lang)
        )
        text += "\n"
        text += strings['updated'].format(
            utils.get_lang.get_string(lang, "latest_update"), 
            utils.round_seconds(int(time.time() - rank[cache_groups_rank.BY_MESSAGES][cache_groups_rank.CACHED_AT]), lang)
        )
    except KeyError:
        pass

    # by members
    try:
        text += "\n\n"
        text += strings['by_members'].format(rank[cache_groups_rank.BY_MEMBERS][cache_groups_rank.REGION])
        text += "\n"
        text += strings['position'].format(
            utils.sep_l(rank[cache_groups_rank.BY_MEMBERS][cache_groups_rank.RANK], lang)
        )
        text += "\n"
        text += strings['members'].format(
            utils.sep_l(rank[cache_groups_rank.BY_MEMBERS][cache_groups_rank.VALUE], lang)
        )
        text += "\n"
        text += strings['updated'].format(
            utils.get_lang.get_string(lang, "latest_update"), 
            utils.round_seconds(int(time.time() - rank[cache_groups_rank.BY_MEMBERS][cache_groups_rank.CACHED_AT]), lang)
        )
    except KeyError:
        pass

    # by votes average
    try:
        text += "\n\n"
        text += strings['by_votes'].format(rank[cache_groups_rank.BY_VOTES][cache_groups_rank.REGION])
        text += "\n"
        text += strings['position'].format(
            utils.sep_l(rank[cache_groups_rank.BY_VOTES][cache_groups_rank.RANK], lang)
        )
        text += "\n"
        text += strings['votes'].format(
            rank[cache_groups_rank.BY_VOTES][cache_groups_rank.VALUE][0],
            utils.sep_l(rank[cache_groups_rank.BY_VOTES][cache_groups_rank.VALUE][1], lang)
        )
        text += "\n"
        text += strings['updated'].format(
            utils.get_lang.get_string(lang, "latest_update"),
            utils.round_seconds(int(time.time() - rank[cache_groups_rank.BY_VOTES][cache_groups_rank.CACHED_AT]), lang)
        )
    except KeyError:
        pass

    return text