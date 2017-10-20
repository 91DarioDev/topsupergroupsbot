"""
this file contains functions to detect if the user is flooding or not. 
if he is flooding the bot stop taking count of his messages and delete from the db
the messages considered flood to keep leaderboards safe of cheats.
The functions are not shown to avoid that people can workaround the antiflood.
You should rename the file `antiflood.py` instead of `antiflood.example.py`
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

def is_flood(bot, update):
    pass