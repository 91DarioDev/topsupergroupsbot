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

from topsupergroupsbot import constants as c
from topsupergroupsbot import get_lang
from topsupergroupsbot import utils
from topsupergroupsbot import commands
from topsupergroupsbot import keyboards


class RegularButtons:
    def __init__(self, bot, update):
        self.bot = bot
        self.update = update
        self.string = self.button_string()
        self.kee = self.get_corresponding_key()

    def button_string(self):
        return self.update.message.text[1:-1]

    def get_corresponding_key(self):
        for lang in get_lang.lang_obj:
            dct = getattr(get_lang.lang_obj[lang], 'buttons_strings')
            for kee in dct:
                if dct[kee] == self.string:
                    return kee
        return None

    def call_button_func(self):
        if self.kee is None:
            self.unrecognized_button()
        elif self.kee == 'leaderboard':
            commands.leaderboard(self.bot, self.update)
        elif self.kee == 'about_you':
            commands.aboutyou(self.bot, self.update)
        elif self.kee == 'region':
            commands.region(self.bot, self.update)
        elif self.kee == 'settings':
            commands.settings(self.bot, self.update)

    def unrecognized_button(self):
        user_id = self.update.message.from_user.id
        lang = utils.get_db_lang(user_id)
        text = get_lang.get_string(lang, "unrecognized_button")
        reply_markup = keyboards.default_regular_buttons_kb(lang)
        self.update.message.reply_text(text=text, reply_markup=reply_markup)


def is_button_syntax(bot, update):
    if not update.message:
        return False
    if not update.message.text:
        return False
    text = update.message.text
    if not (text.startswith(c.BUTTON_START) and text.endswith(c.BUTTON_END)):
        return False
    return True




