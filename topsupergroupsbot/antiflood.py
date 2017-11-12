# TopSupergroupsBot - A telegram bot for telegram public groups leaderboards
# Copyright (C) 2017  Dario <dariomsn@hotmail.it> (github.com/91DarioDev)
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
from topsupergroupsbot import database as db


class Antiflood:
    def __init__(self, limit, interval, group_id, user_id):
        self.limit = limit
        self.interval = interval
        self.group_id = group_id
        self.user_id = user_id
        self.flood_key = self.flood_key()

    def flood_key(self):
        """
        return a redis key to store the amount of sent messages
        during the interval. The key is unique during the interval.
        """
        key = "af:{}:{}:{}:{}:{}".format(
                self.group_id, 
                self.user_id, 
                (time.time()//self.interval),
                self.interval,
                self.limit)
        return key

    def expire_key(self):
        """set a time for redis key expiration"""
        db.REDIS.expire(self.flood_key, self.interval)

    def get_time_key_started(self):
        """
        return the lower value of the interval of time
        when the key has been created.
        """
        return float(self.flood_key.split(":")[3])*self.interval

    def del_messages_from_db(self):
        """
        Delete from the database all the messages sent during
        the interval of the key
        """
        query = """
            DELETE FROM messages 
            WHERE (msg_id, group_id) IN (
                SELECT msg_id, group_id 
                FROM messages
                WHERE 
                    user_id = %s 
                    AND group_id = %s
                    AND message_date >= to_timestamp(%s)
                ORDER BY message_date DESC
                LIMIT %s
            )
        """
        db.query_w(
                query, 
                self.user_id, 
                self.group_id,
                self.get_time_key_started(),
                (self.limit-1))

    def is_flood(self):
        """
        return True if the user is flooding.
        If there is not a key, it sets the key and the expiration time.
        If the user hit the limit, delete messages sent during the interval
        from the db.
        """
        value = db.REDIS.incr(self.flood_key, amount=1)

        if value == 1:
            # the key has been created now
            self.expire_key()
            return False

        elif value == self.limit:
            self.del_messages_from_db()
            print("flood hit in {}".format(self.flood_key))
            return True

        elif value > self.limit:
            return True
    
