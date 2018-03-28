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

from topsupergroupsbot import constants
from topsupergroupsbot import database
from topsupergroupsbot import keyboards
from topsupergroupsbot import get_lang
from topsupergroupsbot import utils
from topsupergroupsbot import emojis


def create_vote_link(group_id):
    schema = "https://t.me/{}?start=vote{}".format(constants.GET_ME.username, group_id)
    return schema


@utils.private_only
def send_vote_by_link(bot, update, first_arg):
    group_id = first_arg.replace("vote", "")
    user_id = update.message.from_user.id
    lang = utils.get_db_lang(user_id)

    query = """
    SELECT s.group_id, s_ref.username, s_ref.title, v.vote, v.vote_date 
    FROM supergroups AS s 
    LEFT OUTER JOIN supergroups_ref AS s_ref -- right so None it's returned if not there
    ON s_ref.group_id = s.group_id
    LEFT OUTER JOIN votes AS v
    ON v.group_id = s.group_id 
    AND v.user_id = %s
    WHERE s.group_id = %s
    """

    extract = database.query_r(query, user_id, group_id, one=True)

    if extract is None:
        # the group does not exist otherwise anything is returned and if None is NULL
        text = get_lang.get_string(lang, "cant_vote_this")
        update.message.reply_text(text=text)
        return

    text = get_lang.get_string(lang, "vote_this_group").format(
        extract[0], extract[1], extract[2])
    if extract[3] is not None and extract[4] is not None:
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
