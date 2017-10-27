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

# library
from telegram import InlineKeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram import ParseMode
from telegram import ReplyKeyboardRemove
from telegram import InlineKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# files
from topsupergroupsbot import supported_langs
from topsupergroupsbot import constants
from topsupergroupsbot import leaderboards
from topsupergroupsbot import get_lang


# INLINE KEYBOARDS

def build_menu(buttons: list,
               n_cols: int,
               header_buttons: list = None,
               footer_buttons: list = None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def main_group_settings_kb(lang):
    button_lang = InlineKeyboardButton(
            text=get_lang.get_string(lang, "group_lang_button"),
            callback_data="group_lang")
    button_adult = InlineKeyboardButton(
            text=get_lang.get_string(lang, "adult_button"),
            callback_data="adult_contents")
    vote_link = InlineKeyboardButton(
            text=get_lang.get_string(lang, "vote_link_button"),
            callback_data="vote_link")
    digest = InlineKeyboardButton(
            text=get_lang.get_string(lang, "group_digest_button"),
            callback_data="digest_group")
    buttons_list = [[button_lang], [button_adult], [vote_link], [digest]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def select_group_lang_kb(group_lang, back=True):
    buttons_list = []
    for i in sorted(supported_langs.GROUP_LANGS):
        buttons_list.append(InlineKeyboardButton(
            text=str(constants.CURRENT_CHOICE+i if i == group_lang else i)+str(supported_langs.COUNTRY_FLAG[i]), 
            callback_data="set_group_lang_"+str(i)))
    footer = InlineKeyboardButton(
                text=get_lang.get_string(group_lang, "back"), 
                callback_data="main_group_settings_creator")
    footer_buttons = [footer]
    buttons_list = build_menu(
            buttons_list,
            n_cols=3,
            footer_buttons=footer_buttons if back is True else None)
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def adult_content_kb(lang, value):
    yes = get_lang.get_string(lang, "yes")
    no = get_lang.get_string(lang, "no")
    back = get_lang.get_string(lang, "back")
    button_yes = InlineKeyboardButton(
            text=constants.CURRENT_CHOICE+yes if value is True else yes,
            callback_data="set_adult_true")
    button_no = InlineKeyboardButton(
            text=constants.CURRENT_CHOICE+no if value is False else no,
            callback_data="set_adult_false")
    button_back = InlineKeyboardButton(
            text=back,
            callback_data="main_group_settings_creator")
    buttons_list = [[button_yes, button_no], [button_back]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def vote_group_kb(group_id, lang):
    buttons_list = []
    for i in range(1, 6):
        buttons_list.append([InlineKeyboardButton(
                text=(constants.EMOJI_STAR*i),
                callback_data="rate:{}:{}".format(i, group_id))])
    buttons_list.append([InlineKeyboardButton(
            text=get_lang.get_string(lang, "cancel"),
            callback_data="rate:cancel")])
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def weekly_group_digest_kb(lang, value):
    yes = get_lang.get_string(lang, "yes")
    no = get_lang.get_string(lang, "no")
    back = get_lang.get_string(lang, "back")
    button_yes = InlineKeyboardButton(
            text=constants.CURRENT_CHOICE+yes if value is True else yes,
            callback_data="set_weekly_group_digest:true")
    button_no = InlineKeyboardButton(
            text=constants.CURRENT_CHOICE+no if value is False else no,
            callback_data="set_weekly_group_digest:false")
    button_back = InlineKeyboardButton(
            text=back,
            callback_data="main_group_settings_creator")
    buttons_list = [[button_yes, button_no], [button_back]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def vote_link_kb(lang):
    button_back = InlineKeyboardButton(
            text=get_lang.get_string(lang, "back"),
            callback_data="main_group_settings_admin")
    buttons_list = [[button_back]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def displayed_pages_kb(pages, chosen_page=1, lb_type="", region=""):
    texted_pages = []

    for page in pages:
        callback_data = "lbpage:{}:{}:{}".format(page, lb_type, region)
        current_page = "current_page" if lb_type not in [leaderboards.GROUP_LEADERBOARD] else "current_page_admin"
        # this is necessary not to get list out of range
        # because later it checks pages[1]
        if len(pages) <= 1:
            # keyboard is not needed if one page
            break

        if page == chosen_page:
            texted_pages.append(InlineKeyboardButton(
                    text="•{}•".format(page), 
                    callback_data=current_page))
            continue

        if page == pages[0] and pages[1] > 2:
            texted_pages.append(InlineKeyboardButton(
                    text="«"+str(page), 
                    callback_data=callback_data))
            continue

        if page == pages[-1] and pages[-2] < (pages[-1] - 1):
            texted_pages.append(InlineKeyboardButton(
                    text=str(page)+"»", 
                    callback_data=callback_data))
            continue

        texted_pages.append(InlineKeyboardButton(
                text=str(page), 
                callback_data=callback_data))

    keyboard = InlineKeyboardMarkup(build_menu(texted_pages, n_cols=8))
    return keyboard


def private_language_kb(lang, back=True):
    buttons_list = []
    for i in sorted(supported_langs.PRIVATE_LANGS):
        buttons_list.append(InlineKeyboardButton(
            text=str(constants.CURRENT_CHOICE+i if i == lang else i)+str(supported_langs.COUNTRY_FLAG[i]), 
            callback_data="set_private_lang_"+str(i)))
    footer = InlineKeyboardButton(
            text=get_lang.get_string(lang, "back"),
            callback_data="main_private_settings")
    footer_buttons = [footer]
    buttons_list = build_menu(
            buttons_list,
            n_cols=3,
            footer_buttons=footer_buttons if back is True else None)
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def private_region_kb(lang, region, back=True):
    buttons_list = []
    for i in sorted(supported_langs.PRIVATE_REGIONS):
        buttons_list.append(InlineKeyboardButton(
            text=str(constants.CURRENT_CHOICE+i if i == region else i)+str(supported_langs.COUNTRY_FLAG[i]), 
            callback_data="set_private_region:"+str(i)))
    footer = InlineKeyboardButton(
            text=get_lang.get_string(lang, "back"),
            callback_data="main_private_settings")
    footer_buttons = [footer]
    buttons_list = build_menu(
            buttons_list,
            n_cols=3,
            footer_buttons=footer_buttons if back == True else None)
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def main_private_settings_kb(lang):
    button0 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "private_lang_button"),
            callback_data="private_lang")
    button1 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "private_region_button"),
            callback_data="private_region")
    button2 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "private_digest_button"),
            callback_data="private_digest_button")
    buttons_list = [[button0], [button1], [button2]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def private_digest_kb(lang):
    button0 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "private_your_own_digest_button"),
            callback_data="private_your_own_digest")
    button1 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "private_groups_digest_button"),
            callback_data="private_groups_digest")
    button2 = InlineKeyboardButton(
            text=get_lang.get_string(lang, "back"),
            callback_data="main_private_settings")
    buttons_list = [[button0], [button1], [button2]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def weekly_own_digest_kb(lang, value):
    yes = get_lang.get_string(lang, "yes")
    no = get_lang.get_string(lang, "no")
    back = get_lang.get_string(lang, "back")
    button_yes = InlineKeyboardButton(
                text=constants.CURRENT_CHOICE+yes if value is True else yes, 
                callback_data="set_weekly_own_digest:true")
    button_no = InlineKeyboardButton(
                text=constants.CURRENT_CHOICE+no if value is False else no, 
                callback_data="set_weekly_own_digest:false")
    button_back = InlineKeyboardButton(text=back, 
                callback_data="back_private_digest")
    buttons_list = [[button_yes, button_no], [button_back]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def generic_leaderboard_kb(lang, region):
    members = InlineKeyboardButton(
                text=get_lang.get_string(lang, "by_members"), 
                callback_data="leaderboard_by:"+leaderboards.MEMBER_LEADERBOARD+":"+region)
    messages = InlineKeyboardButton(
                text=get_lang.get_string(lang, "by_messages"), 
                callback_data="leaderboard_by:"+leaderboards.MESSAGE_LEADERBOARD+":"+region)
    votes = InlineKeyboardButton(
                text=get_lang.get_string(lang, "by_votes"), 
                callback_data="leaderboard_by:"+leaderboards.VOTE_LEADERBOARD+":"+region)
    buttons_list = [[members], [messages], [votes]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def disable_private_own_weekly_digest_kb(lang):
    disable = InlineKeyboardButton(
                text=get_lang.get_string(lang, "disable"), 
                callback_data="private_your_own_digest:new_msg")
    buttons_list = [[disable]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def disable_group_weekly_digest_kb(lang):
    disable = InlineKeyboardButton(
                text=get_lang.get_string(lang, "disable"), 
                callback_data="digest_group:new_msg")
    buttons_list = [[disable]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard
