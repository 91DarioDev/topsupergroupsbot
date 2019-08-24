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

import threading
import redis
import psycopg2
from threading import Semaphore

from topsupergroupsbot import config

class ReallyThreadedConnectionPool(psycopg2.pool.ThreadedConnectionPool):
    def __init__(self, minconn, maxconn, *args, **kwargs):
        self._semaphore = Semaphore(maxconn)
        super().__init__(minconn, maxconn, *args, **kwargs)

    def getconn(self, *args, **kwargs):
        self._semaphore.acquire()
        return super().getconn(*args, **kwargs)

    def putconn(self, *args, **kwargs):
        super().putconn(*args, **kwargs)
        self._semaphore.release()

#                            _   _          
#    __ ___ _ _  _ _  ___ __| |_(_)___ _ _  
#   / _/ _ \ ' \| ' \/ -_) _|  _| / _ \ ' \ 
#   \__\___/_||_|_||_\___\__|\__|_\___/_||_|
#        


REDIS = redis.Redis(host=config.REDIS_HOST, 
                    port=config.REDIS_PORT, 
                    db=config.REDIS_DB)



DB_POOL_CONNECTIONS = ReallyThreadedConnectionPool(
    minconn=config.MIN_DB_CONNECTIONS, 
    maxconn=config.MAX_DB_CONNECTIONS,
    user = config.DB_USER,
    password = config.DB_PASSWORD,
    dbname = config.DB_NAME
)


#                                      _                     _        
#   __ __ ___ _ __ _ _ __ _ __  ___ __| |  __ _ _  _ ___ _ _(_)___ ___
#   \ V  V / '_/ _` | '_ \ '_ \/ -_) _` | / _` | || / -_) '_| / -_|_-<
#    \_/\_/|_| \__,_| .__/ .__/\___\__,_| \__, |\_,_\___|_| |_\___/__/
#                   |_|  |_|                 |_|                      



def query(query, *params, one=False, read=False):
    connect = DB_POOL_CONNECTIONS.getconn()
    c = connect.cursor()
    try:
        c.execute(query, params)
        c.connection.commit()
        if read:
            if not one:
                return c.fetchall()
            else:
                return c.fetchone()
    except:
        c.connection.rollback()
        raise
    finally:
        DB_POOL_CONNECTIONS.putconn(connect)

# for retrocompatibilty
def query_w(raw_query, *params):
    query(raw_query, *params)


# for retrocompatibility
def query_r(raw_query, *params, one=False):
    return query(raw_query, *params, one=one, read=True)


# because the commit is now added in the query_r too
query_wr = query_r


#                    _            _ _    
#    __ _ _ ___ __ _| |_ ___   __| | |__ 
#   / _| '_/ -_) _` |  _/ -_) / _` | '_ \
#   \__|_| \___\__,_|\__\___| \__,_|_.__/
#                                        

def create_db():

    # for private purposes

    query = """CREATE TABLE IF NOT EXISTS users(
        user_id BIGINT PRIMARY KEY, 
        lang TEXT DEFAULT 'en', 
        region TEXT DEFAULT NULL, 
        tg_lang TEXT DEFAULT NULL, 
        bot_blocked BOOLEAN DEFAULT FALSE, 
        banned_on TIMESTAMP DEFAULT NULL, 
        banned_until TIMESTAMP DEFAULT NULL, 
        weekly_own_digest BOOLEAN DEFAULT TRUE, 
        weekly_groups_digest TEXT [], 
        message_date timestamp,
        registered_at TIMESTAMP DEFAULT NOW()
    )"""
    query_w(query)

    query = """CREATE TABLE IF NOT EXISTS supergroups(
        group_id BIGINT PRIMARY KEY, 
        lang TEXT DEFAULT NULL, 
        nsfw BOOLEAN DEFAULT FALSE, 
        weekly_digest BOOLEAN DEFAULT TRUE, 
        joined_the_bot timestamp DEFAULT NULL, 
        banned_on TIMESTAMP DEFAULT NULL, 
        banned_until TIMESTAMP DEFAULT NULL, 
        ban_reason TEXT DEFAULT NULL, 
        bot_inside BOOLEAN DEFAULT TRUE, 
        last_date timestamp DEFAULT NULL,
        category TEXT DEFAULT NULL
    )"""
    query_w(query)

    # --------------------------

    # to collect messages for stats

    query = """CREATE TABLE IF NOT EXISTS messages(
        msg_id BIGINT, 
        group_id BIGINT, 
        user_id BIGINT, 
        message_date timestamp, 
        PRIMARY KEY (msg_id, group_id)
    )"""
    query_w(query)

    # --------------------------

    # collect any user (also if didn't start the bot), to log info for many stuff
    
    query = """CREATE TABLE IF NOT EXISTS users_ref(
        user_id BIGINT PRIMARY KEY, 
        name TEXT DEFAULT NULL, 
        last_name TEXT DEFAULT NULL, 
        username TEXT DEFAULT NULL, 
        tg_lang TEXT DEFAULT NULL, 
        message_date timestamp
    )"""
    query_w(query)

    query = """CREATE TABLE IF NOT EXISTS supergroups_ref(
        group_id BIGINT PRIMARY KEY, 
        title TEXT DEFAULT NULL, 
        username TEXT DEFAULT NULL, 
        message_date timestamp
    )"""
    query_w(query)

    # --------------------------

    # for reviews

    query = """ CREATE TABLE IF NOT EXISTS votes(
        user_id BIGINT,
        group_id BIGINT,
        vote SMALLINT,
        vote_date timestamp,
        PRIMARY KEY (user_id, group_id)
    )"""
    query_w(query)

    # --------------------------

    # for members

    query = """
    CREATE TABLE IF NOT EXISTS members(
        group_id BIGINT, 
        amount INT, 
        updated_date timestamp
    )
    """
    query_w(query)


#    _         _         
#   (_)_ _  __| |_____ __
#   | | ' \/ _` / -_) \ /
#   |_|_||_\__,_\___/_\_\
#     


def create_index():

    ###############
    #
    #   MESSAGES
    #
    ###############

    query = "CREATE INDEX IF NOT EXISTS index_messages_msg_id ON messages (msg_id)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS index_messages_group_id ON messages (group_id)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS index_messages_user_id ON messages (user_id)"
    query_w(query)
    query = "CREATE INDEX IF NOT EXISTS index_messages_message_date ON messages (message_date)"
    query_w(query)

    #######################
    #
    #   SUPERGROUPS_REF
    #
    #######################

    query = "CREATE INDEX IF NOT EXISTS index_supergroups_ref_username ON supergroups_ref (username)"
    query_w(query)




create_db()
create_index()