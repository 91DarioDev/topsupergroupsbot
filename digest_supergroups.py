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

import database

def weekly_groups_digest(bot, job):
	query = """
		SELECT
			group_id,
			lang,
			nsfw,
			joined_the_bot
		FROM supergroups
		WHERE weekly_digest = TRUE AND bot_inside = TRUE
		ORDER BY last_date DESC
		"""
	lst = database.query_r(query)


	#############
	# MESSAGES
	############

	query = """
	SELECT 
		group_id, 
		COUNT(msg_id) AS msgs
	FROM messages
	WHERE message_date > now() - interval '7 days'
	GROUP BY group_id
	"""
	msgs_this_week = database.query_r(query)

	query = """
	SELECT 
		group_id, 
		COUNT(msg_id) AS msgs
	FROM messages
	WHERE message_date BETWEEN now() - interval '14 days' AND now() - interval '7 days'
	GROUP BY group_id
	"""
	msgs_last_week = database.query_r(query)
	
	#############
	# MEMBERS
	############

	query = """
	    SELECT 
	    	last_members.group_id, 
	    	last_members.amount
	    FROM
		    (
		    SELECT 
		    	*, 
		    	ROW_NUMBER() OVER (
			    	PARTITION BY group_id
			    	ORDER BY updated_date DESC
			    	) AS row 
			FROM members
			) AS last_members
	    WHERE last_members.row=1
		"""
	members_this_week = database.query_r(query)


	query = """
	    SELECT 
	    	last_members.group_id, 
	    	last_members.amount
	    FROM
		    (
		    SELECT 
		    	*, 
		    	ROW_NUMBER() OVER (
			    	PARTITION BY group_id
			    	ORDER BY updated_date DESC
			    	) AS row 
			FROM members
			WHERE updated_date <= now() - interval '7 days'
			) AS last_members
	    WHERE last_members.row=1
		"""
	members_last_week = database.query_r(query)
	print(members_this_week)

	####################
	# SUM AND AVG VOTES
	####################

	query = """
		SELECT 
			group_id,
			COUNT(vote) AS amount, 
			ROUND(AVG(vote), 1) AS average
		FROM votes
		WHERE vote_date > (now() - interval '7 days')
		GROUP BY group_id
	"""
	this_week_votes_avg = database.query_r(query)

	query = """
		SELECT 
			group_id,
			COUNT(vote) AS amount, 
			ROUND(AVG(vote), 1) AS average
		FROM votes
		WHERE vote_date BETWEEN (now() - interval '14 days') AND (now() - interval '7 days')
		GROUP BY group_id
	"""
	last_week_votes_avg = database.query_r(query)

	##################
	# ACTIVE USERS
	##################

	query = """
		SELECT 
			DISTINCT group_id,
			COUNT(user_id) OVER (PARTITION BY group_id)
		FROM messages
		WHERE message_date > (now() - interval '7 days')
		GROUP BY group_id, user_id
		"""
	this_week_active_users = database.query_r(query)

	query = """
		SELECT 
			DISTINCT group_id,
			COUNT(user_id) OVER (PARTITION BY group_id)
		FROM messages
		WHERE message_date BETWEEN (now() - interval '14 days') AND (now() - interval '7 days')
		GROUP BY group_id, user_id
		"""
	last_week_active_users = database.query_r(query)


	for group in lst:
		group_id = group[0]
		lang = group[1]

		msgs_new = None
		msgs_old = None

		members_new = None
		members_old = None

		sum_v_new = None
		avg_v_new = None
		sum_v_old = None
		avg_v_old = None

		act_users_new = None
		act_users_old = None

		for i in msgs_this_week:
			if i[0] = group_id:
				msgs_new = i[1]
				break

		for i in msgs_last_week:
			if i[0] = group_id:
				msgs_old = i[1]
				break

		for i in members_this_week:
			if i[0] = group_id:
				members_new = i[1]
				break

		for i in members_last_week:
			if i[0] = group_id:
				members_old = i[1]
				break

		for i in this_week_votes_avg:
			if i[0] = group_id:
				sum_v_new = i[1]
				avg_v_new = i[2]
				break


		for i in last_week_votes_avg:
			if i[0] = group_id:
				sum_v_old = i[1]
				avg_v_old = i[2]
				break

		for i in this_week_active_users:
			if i[0] = group_id:
				act_users_new = i[1]
				break

		for i in last_week_votes_avg:
			if i[0] = group_id:
				act_users_old = i[1]
				break


#weekly_groups_digest(None, None)