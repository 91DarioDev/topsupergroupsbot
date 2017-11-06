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

import psycopg2

from topsupergroupsbot import keyboards
from topsupergroupsbot import database
from topsupergroupsbot import utils
from topsupergroupsbot import emojis

from topsupergroupsbot import votelink
from topsupergroupsbot import leaderboards
from topsupergroupsbot import get_lang

from telegram import ParseMode
from telegram.error import (TelegramError,
                            Unauthorized,
                            BadRequest,
                            TimedOut,
                            ChatMigrated,
                            NetworkError)


def callback_query(bot, update):
    query = update.callback_query

    if query.data.startswith("set_group_lang_"):
        choose_lang(bot, query)

    elif query.data == "main_group_settings_creator":
        main_group_settings_creator(bot, query)

    elif query.data == "main_group_settings_admin":
        main_group_settings_admin(bot, query)

    elif query.data == "group_lang":
        group_lang_button(bot, query)

    elif query.data == "adult_contents":
        adult_menu(bot, query)

    elif query.data.startswith("set_adult_"):
        set_adult(bot, query)

    elif query.data.startswith("rate"):
        set_vote(bot, query)

    elif query.data == "vote_link":
        vote_link(bot, query)

    elif query.data == "current_page":
        current_page(bot, query)

    elif query.data == "current_page_admin":
        current_page_admin(bot, query)

    elif query.data.startswith("lbpage"):
        lbpage(bot, query)

    elif query.data == "private_lang":
        private_lang(bot, query)

    elif query.data == "private_region":
        private_region(bot, query)

    elif query.data == "main_private_settings":
        main_private_settings(bot, query)

    elif query.data.startswith("set_private_lang_"):
        set_private_lang(bot, query)

    elif query.data.startswith("set_private_region"):
        set_private_region(bot, query)

    elif query.data == "private_digest_button":
        private_digest(bot, query)

    elif query.data.startswith("private_your_own_digest"):
        private_your_own_digest(bot, query)

    elif query.data == "private_groups_digest":
        private_groups_digest(bot, query)

    elif query.data.startswith("set_weekly_own_digest"):
        set_weekly_own_digest(bot, query)

    elif query.data == "back_private_digest":
        private_digest(bot, query)

    elif query.data.startswith("leaderboard_by:"):
        redirect_ledearboard(bot, query)

    elif query.data.startswith("digest_group"):
        group_digest_menu(bot, query)

    elif query.data.startswith("set_weekly_group_digest"):
        set_weekly_group_digest(bot, query)

    elif query.data == "feedback_reply":
        feedback_reply(bot, query)


@utils.creator_button_only
def choose_lang(bot, query):
    lang = query.data.replace("set_group_lang_", "")
    text = get_lang.get_string(lang, "choose_group_lang")
    reply_markup = keyboards.select_group_lang_kb(lang)
    query.answer()
    query_db = "UPDATE supergroups SET lang = %s WHERE group_id = %s"
    database.query_w(query_db, lang, query.message.chat.id)
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def main_group_settings(bot, query):
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    lang = database.query_r(query_db, query.message.chat.id, one=True)[0]
    text = get_lang.get_string(lang, "group_settings")
    reply_markup = keyboards.main_group_settings_kb(lang)
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


@utils.creator_button_only
def main_group_settings_creator(bot, query):
    main_group_settings(bot, query)


@utils.admin_button_only
def main_group_settings_admin(bot, query):
    main_group_settings(bot, query)


@utils.creator_button_only
def group_lang_button(bot, query):
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    lang = database.query_r(query_db, query.message.chat.id, one=True)[0]
    text = get_lang.get_string(lang, "choose_group_lang")
    reply_markup = keyboards.select_group_lang_kb(lang)
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


@utils.creator_button_only
def adult_menu(bot, query):
    query_db = "SELECT lang, nsfw FROM supergroups WHERE group_id = %s"
    extraction = database.query_r(query_db, query.message.chat.id, one=True)
    lang = extraction[0]
    nsfw = extraction[1]
    text = get_lang.get_string(lang, "have_adult")
    reply_markup = keyboards.adult_content_kb(lang, nsfw)
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


@utils.creator_button_only
def set_adult(bot, query):
    value = query.data.replace("set_adult_", "")
    final_value = True if value == "true" else False
    query_db = "UPDATE supergroups SET nsfw = %s WHERE group_id = %s RETURNING lang"
    extract = database.query_wr(query_db, final_value, query.message.chat.id, one=True)
    lang = extract[0]
    query.answer()
    text = get_lang.get_string(lang, "have_adult")
    reply_markup = keyboards.adult_content_kb(lang, final_value)
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


@utils.admin_button_only
def vote_link(bot, query):
    group_id = query.message.chat.id
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    extraction = database.query_r(query_db, group_id, one=True)
    lang = extraction[0]
    text = get_lang.get_string(lang, "here_group_vote_link")
    text += "\n\n{}".format(votelink.create_vote_link(group_id))
    reply_markup = keyboards.vote_link_kb(lang)
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


@utils.creator_button_only
def group_digest_menu(bot, query):
    group_id = query.message.chat.id
    query_db = "SELECT lang, weekly_digest FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query_db, group_id, one=True)
    lang = extract[0]
    weekly_digest = extract[1]
    text = get_lang.get_string(lang, "group_weekly_digest")
    reply_markup = keyboards.weekly_group_digest_kb(lang, weekly_digest)
    if query.data.endswith("new_msg"):
        query.message.edit_reply_markup()
        query.message.reply_text(text=text, reply_markup=reply_markup)
        return
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def set_weekly_group_digest(bot, query):
    value = True if query.data.split(":")[1] == "true" else False
    query_db = "UPDATE supergroups SET weekly_digest = %s WHERE group_id = %s RETURNING lang"
    extract = database.query_wr(query_db, value, query.message.chat.id)
    lang = extract[0][0]
    reply_markup = keyboards.weekly_group_digest_kb(lang, value)
    query.answer()
    query.message.edit_reply_markup(reply_markup=reply_markup)


def set_vote(bot, query):
    lang = utils.get_db_lang(query.from_user.id)
    vote = query.data.split(":")[1]
    if vote == "cancel":
        query.answer()
        text = "{}\n\n{}".format(query.message.text, get_lang.get_string(lang, "canceled"))
        try:
            query.edit_message_text(text=text)
        except TelegramError as e:
            if str(e) != "Message is not modified": print(e)
        return
    vote = int(vote)
    group_id = query.data.split(":")[2]
    alert = ""
    query_db = """
    INSERT INTO votes 
    (user_id, group_id, vote, vote_date) 
    VALUES (%s, %s, %s, now())
    ON CONFLICT DO NOTHING
    RETURNING*
    """
    extract = database.query_wr(query_db, query.from_user.id, group_id, vote, one=True)
    if extract is not None:
        alert = get_lang.get_string(lang, "registered_vote")
    else:
        query_db = """
        UPDATE votes 
        SET 
            vote = %s, 
            vote_date = now() 
        WHERE 
            user_id = %s AND 
            group_id = %s
        """
        database.query_w(query_db, vote, query.from_user.id, group_id)
        alert = get_lang.get_string(lang, "updated_vote")
    query.answer(text=alert, show_alert=True)
    text = "{}\n\n{}\n{}".format(query.message.text, alert, emojis.STAR * vote)
    try:
        query.edit_message_text(text=text)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def current_page(bot, query):
    lang = utils.get_db_lang(query.from_user.id)
    query.answer(get_lang.get_string(lang, "already_this_page"), show_alert=True)


@utils.admin_button_only
def current_page_admin(bot, query):
    group_id = query.chat.id
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query_db, group_id, one=True)
    lang = extract[0] if extract is not None else None
    query.answer(get_lang.get_string(lang, "already_this_page"), show_alert=True)


def lbpage(bot, query):
    params = query.data.split(":")
    page = params[1]
    lb_type = params[2]
    region = params[3]

    if lb_type == leaderboards.Leaderboard.GROUP:
        lbpage_igl(bot, query, params)
    elif lb_type in [
        leaderboards.Leaderboard.VOTES,
        leaderboards.Leaderboard.MESSAGES,
        leaderboards.Leaderboard.MEMBERS
    ]:
        lbpage_private(bot, query, lb_type, page, region)
    query.answer()


@utils.admin_button_only
def lbpage_igl(bot, query, params):
    group_id = query.message.chat.id
    query_db = "SELECT lang FROM supergroups WHERE group_id = %s"
    extract = database.query_r(query_db, group_id, one=True)
    lang = extract[0]
    page = params[1]
    leaderboard = leaderboards.GroupLeaderboard(lang=lang, page=int(page))
    result = leaderboard.build_page(group_id)
    try:
        query.edit_message_text(
            text=result[0], reply_markup=result[1],
            parse_mode=ParseMode.HTML, disable_notification=True)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def lbpage_private(bot, query, lb_type, page, region):
    lang = utils.get_db_lang(query.from_user.id)
    if lb_type == leaderboards.Leaderboard.VOTES:
        leaderboard = leaderboards.VotesLeaderboard(lang, region, int(page))
    elif lb_type == leaderboards.Leaderboard.MESSAGES:
        leaderboard = leaderboards.MessagesLeaderboard(lang, region, int(page))
    elif lb_type == leaderboards.Leaderboard.MEMBERS:
        leaderboard = leaderboards.MembersLeaderboard(lang, region, int(page))
    result = leaderboard.build_page()
    try:
        query.edit_message_text(
            text=result[0], reply_markup=result[1],
            parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def set_private_lang(bot, query):
    lang = query.data.replace("set_private_lang_", "")
    query_db = "UPDATE users SET lang = %s WHERE user_id = %s"
    database.query_w(query_db, lang, query.from_user.id)
    query.answer()
    query.message.edit_reply_markup(reply_markup=keyboards.private_language_kb(lang))
    bot.sendMessage(
        chat_id=query.from_user.id, 
        text=get_lang.get_string(lang, "updating_buttons"), 
        reply_markup=keyboards.default_regular_buttons_kb(lang)
    )


def set_private_region(bot, query):
    region = query.data.split(":")[1]
    query_db = "UPDATE users SET region = %s WHERE user_id = %s RETURNING lang"
    extract = database.query_wr(query_db, region, query.from_user.id, one=True)
    lang = extract[0]
    query.answer()
    query.message.edit_reply_markup(reply_markup=keyboards.private_region_kb(lang, region))


def main_private_settings(bot, query):
    lang = utils.get_db_lang(query.from_user.id)
    text = get_lang.get_string(lang, "private_settings")
    reply_markup = keyboards.main_private_settings_kb(lang)
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def private_region(bot, query):
    query.answer()
    query_db = "SELECT lang, region FROM users WHERE user_id = %s"
    extract = database.query_r(query_db, query.from_user.id, one=True)
    lang = extract[0]
    region = extract[1]
    text = get_lang.get_string(lang, "choose_region")
    reply_markup = keyboards.private_region_kb(lang, region)
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def private_lang(bot, query):
    query.answer()
    query_db = "SELECT lang FROM users WHERE user_id = %s"
    extract = database.query_r(query_db, query.from_user.id, one=True)
    lang = extract[0]
    text = get_lang.get_string(lang, "choose_your_lang")
    reply_markup = keyboards.private_language_kb(lang)
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def private_digest(bot, query):
    query.answer()
    lang = utils.get_db_lang(query.from_user.id)
    text = get_lang.get_string(lang, "private_digest")
    reply_markup = keyboards.private_digest_kb(lang)
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def private_your_own_digest(bot, query):
    query_db = "SELECT lang, weekly_own_digest FROM users WHERE user_id = %s"
    extract = database.query_r(query_db, query.from_user.id, one=True)
    lang = extract[0]
    weekly_own_digest = extract[1]
    text = get_lang.get_string(lang, "weekly_own_digest")
    reply_markup = keyboards.weekly_own_digest_kb(lang, weekly_own_digest)
    if query.data.endswith("new_msg"):
        query.message.edit_reply_markup()
        query.message.reply_text(text=text, reply_markup=reply_markup)
        return
    query.answer()
    try:
        query.edit_message_text(text=text, reply_markup=reply_markup)
    except TelegramError as e:
        if str(e) != "Message is not modified": print(e)


def private_groups_digest(bot, query):
    query.answer("coming soon", show_alert=True)


def set_weekly_own_digest(bot, query):
    value = True if query.data.split(":")[1] == "true" else False
    query_db = "UPDATE users SET weekly_own_digest = %s WHERE user_id = %s RETURNING lang"
    extract = database.query_wr(query_db, value, query.from_user.id)
    lang = extract[0][0]
    reply_markup = keyboards.weekly_own_digest_kb(lang, value)
    query.answer()
    query.message.edit_reply_markup(reply_markup=reply_markup)


def redirect_ledearboard(bot, query):
    splitted = query.data.split(":")
    lb_type = splitted[1]
    region = splitted[2]
    if lb_type in [
        leaderboards.Leaderboard.VOTES,
        leaderboards.Leaderboard.MESSAGES,
        leaderboards.Leaderboard.MEMBERS
    ]:
        lbpage_private(bot, query, lb_type, 1, region)
    query.answer()


def feedback_reply(bot, query):
    query.message.edit_reply_markup(reply_markup=None)
    lang = utils.get_db_lang(query.from_user.id)
    text = get_lang.get_string(lang, "feedback_message")
    bot.sendMessage(chat_id=query.from_user.id, text=text)
