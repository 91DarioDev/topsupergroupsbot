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


import database as db 
import json

CACHE_SECONDS = 60*3

def key_name(name_type, region):
    return 'cached_lb:{}:{}'.format(name_type, region)

def get_leaderboard(name_type, region):
    key = key_name(name_type, region)
    lst = db.REDIS.get(key)
    if lst is None:
        return None
    lst = json.loads(lst.decode('UTF-8'))
    return lst


def set_leaderboard(name_type, region, lst):
    key = key_name(name_type, region)
    dumped_lst = json.dumps(lst).encode('UTF-8')
    db.REDIS.setex(key, dumped_lst, CACHE_SECONDS)