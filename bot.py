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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler  
from telegram.ext.dispatcher import run_async
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)
from telegram import InlineKeyboardButton
import logging
import datetime

from config import config
import messages
import buttons_callback
import commands
import utils
import leaderboards
import cleandb
import memberslog
import digest_private
import commands_private

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
	# define the updater
	updater = Updater(token=config.BOT_TOKEN , workers=7)
	
	# define the dispatcher
	dp = updater.dispatcher

	# define jobs
	j = updater.job_queue

	#this will run async the process_update
	dp.process_update = run_async(dp.process_update)

	# handlers

	#before processing
	dp.add_handler(MessageHandler(Filters.all, messages.before_processing), -1)

	# commands
	dp.add_handler(CommandHandler('settings', commands.settings))
	dp.add_handler(CommandHandler('vote', commands.vote, pass_args=True))
	dp.add_handler(CommandHandler('start', commands.start, pass_args=True))
	dp.add_handler(CommandHandler('help', commands.help))
	dp.add_handler(CommandHandler('groupleaderboard', commands.groupleaderboard))
	dp.add_handler(CommandHandler('leaderboard', commands.leaderboard))
	dp.add_handler(CommandHandler('leadervote', leaderboards.leadervote))
	dp.add_handler(CommandHandler('leadermessage', leaderboards.leadermessage))
	dp.add_handler(CommandHandler('leadermember', leaderboards.leadermember))
	dp.add_handler(CommandHandler('aboutyou', commands.aboutyou))
	dp.add_handler(CommandHandler('language', commands.language))
	dp.add_handler(CommandHandler('region', commands.region))
	# private commands
	dp.add_handler(CommandHandler('statsusers', commands_private.stats_users))
	dp.add_handler(CommandHandler('statsgroups', commands_private.stats_groups))
	dp.add_handler(CommandHandler('infoid', commands_private.infoid, pass_args=True))
	dp.add_handler(CommandHandler('reverseusername', commands_private.reverse_username, 
									pass_args=True))
	#invalid command
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

	# handle errors
	dp.add_error_handler(error)

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()