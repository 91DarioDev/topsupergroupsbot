
"""
This is an example of the config.py file. Create a file like this but `config.py` instead of
`config.example.py` and replace the values with the right ones
"""

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


BOT_TOKEN = "bot_token"
POSTGRES_DB = "dbname=dbname user=user"

REDIS_HOST = 'redis_host'
REDIS_PORT = 1234
REDIS_DB = 1234

# telegram IDs of the admins of the bot
ADMINS = [
    1234
]

# telegram ID of the founder of the bot (more priviledges)
FOUNDER = 1234