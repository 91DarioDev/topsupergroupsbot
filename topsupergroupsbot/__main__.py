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

# library
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler  
from telegram.ext.dispatcher import run_async
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from telegram import InlineKeyboardButton
import logging
import datetime

from topsupergroupsbot import config
from topsupergroupsbot import messages
from topsupergroupsbot import buttons_callback
from topsupergroupsbot import commands
from topsupergroupsbot import utils
from topsupergroupsbot import leaderboards
from topsupergroupsbot import cleandb
from topsupergroupsbot import memberslog
from topsupergroupsbot import digest_private
from topsupergroupsbot import commands_private
from topsupergroupsbot import digest_supergroups
from topsupergroupsbot import cache_users_stats
from topsupergroupsbot import cache_groups_rank


license = (
    "\n\n"
    "***\n"
    "TopSupergroupsBot - A telegram bot for telegram public groups leaderboards"
    "Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)"
    "\n\n"
    "TopSupergroupsBot is free software: you can redistribute it and/or modify "
    "it under the terms of the GNU Affero General Public License as published "
    "by the Free Software Foundation, either version 3 of the License, or "
    "(at your option) any later version."
    "\n\n"
    "TopSupergroupsBot is distributed in the hope that it will be useful, "
    "but WITHOUT ANY WARRANTY; without even the implied warranty of "
    "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the "
    "GNU Affero General Public License for more details. "
    "\n\n"
    "You should have received a copy of the GNU Affero General Public License "
    "along with TopSupergroupsBot.  If not, see <http://www.gnu.org/licenses/>."
    "\n***"
    "\n"
)


print(license)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    print("\nrunning...")
    # define the updater
    updater = Updater(token=config.BOT_TOKEN, workers=7)
    
    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # this will run async the process_update
    dp.process_update = run_async(dp.process_update)

    # handlers

    # first start
    dp.add_handler(CommandHandler('start', commands.first_start, filters=Filters.private), -2)

    # before processing
    dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)

    # commands
    dp.add_handler(CommandHandler('settings', commands.settings))
    dp.add_handler(CommandHandler('vote', commands.vote, pass_args=True))
    dp.add_handler(CommandHandler('start', commands.start, pass_args=True))
    dp.add_handler(CommandHandler('help', commands.help))
    dp.add_handler(CommandHandler('groupleaderboard', commands.groupleaderboard, pass_args=True))
    dp.add_handler(CommandHandler('grouprank', commands.group_rank_private, filters=Filters.private, pass_args=True))  # this should come before the one for groups
    dp.add_handler(CommandHandler('grouprank', commands.group_rank))
    dp.add_handler(CommandHandler('leaderboard', commands.leaderboard))
    dp.add_handler(CommandHandler('leadervote', leaderboards.leadervote, pass_args=True))
    dp.add_handler(CommandHandler('leadermessage', leaderboards.leadermessage, pass_args=True))
    dp.add_handler(CommandHandler('leadermember', leaderboards.leadermember, pass_args=True))
    dp.add_handler(CommandHandler('aboutyou', commands.aboutyou))
    dp.add_handler(CommandHandler('language', commands.language))
    dp.add_handler(CommandHandler('region', commands.region))
    dp.add_handler(CommandHandler('feedback', commands.feedback))
    # private commands
    dp.add_handler(CommandHandler('statsusers', commands_private.stats_users))
    dp.add_handler(CommandHandler('statsgroups', commands_private.stats_groups))
    dp.add_handler(CommandHandler('infoid', commands_private.infoid, pass_args=True))
    dp.add_handler(CommandHandler('reverseusername', commands_private.reverse_username, 
                                    pass_args=True))
    dp.add_handler(CommandHandler('bangroup', commands_private.ban_group, pass_args=True))
    dp.add_handler(CommandHandler('unbangroup', commands_private.unban_group, pass_args=True))
    # invalid command
    dp.add_handler(MessageHandler(Filters.command & Filters.private, utils.invalid_command))
    # handle all messages not command. it's obvious because commands are handled before, 
    # but it's more safe
    dp.add_handler(MessageHandler(~Filters.command, messages.processing))

    # handle buttons callback
    dp.add_handler(CallbackQueryHandler(buttons_callback.callback_query))


    # jobs
    j.run_repeating(cleandb.clean_db, interval=60*60*24, first=0)
    j.run_repeating(memberslog.members_log, interval=60*60*24, first=0)
    j.run_daily(digest_private.weekly_own_private, time=datetime.time(0, 0, 0), days=(0,))
    j.run_daily(digest_supergroups.weekly_groups_digest, time=datetime.time(0, 0, 0), days=(0,))
    # leaderboards pre-cache

    j.run_repeating(
        leaderboards.scheduling_votes_leaderboard_cache,
        interval=leaderboards.VotesLeaderboard.CACHE_SECONDS,
        first=0
    )
    j.run_repeating(
        leaderboards.scheduling_messages_leaderboard_cache,
        interval=leaderboards.MessagesLeaderboard.CACHE_SECONDS,
        first=0
    )
    j.run_repeating(
        leaderboards.scheduling_members_leaderboard_cache,
        interval=leaderboards.MembersLeaderboard.CACHE_SECONDS,
        first=0
    )
    # pre-cached users stats
    j.run_repeating(
        cache_users_stats.cache_users_stats,
        interval=cache_users_stats.CACHE_SECONDS,
        first=0
    )

    # pre-cache ranks groups
    j.run_repeating(
        cache_groups_rank.caching_ranks,
        interval=cache_groups_rank.CACHE_SECONDS,
        first=0
    )

    # update cache if the week is over for cached leaderboards related to the week
    j.run_daily(
        leaderboards.scheduling_messages_leaderboard_cache,
        time=datetime.time(0, 0, 0),
        days=(0,)
    )
    j.run_daily(
        cache_users_stats.cache_users_stats,
        time=datetime.time(0, 0, 0),
        days=(0,)
    )
    j.run_daily(
        cache_groups_rank.caching_ranks,
        time=datetime.time(0, 0, 0),
        days=(0,)
    )
    # handle errors
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
