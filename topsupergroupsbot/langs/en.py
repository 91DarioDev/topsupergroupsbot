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

buttons_strings = {
    "leaderboard": "leaderboard",
    "about_you": "about you",
    "region": "region",
    "settings": "settings",
    "info_and_help": "info & help"
}


hello = "Hello!"

choose_group_lang = (
        "Choose the language of the group. "
        "Your group will be added in the leaderboard of the right language. "
        "Don't lie or we'll ban this group")

group_settings = "Group settings:"
messages_in_groups_position = "— {} messages in @{}. Position: {}\n"
have_adult = "Does this group contains adult content?"
here_group_vote_link = "This is the link to directly redirect users to vote this group"
canceled = "Canceled"
already_this_page = "You are already on this page!"

vote_this_group = "id: {}\nusername: @{}\ntitle: {}"
already_voted = "Already voted {} on {}"
choose_your_lang = "Select your language"

group_lang_button = "Group Lang"
adult_button = "Adult Emoji"
vote_link_button = "Vote link"
back = "Back"
yes = "Yes"
no = "No"
cancel = "Cancel"

this_command_only_private = "The commmand you gave is only for private chats"
this_command_only_admins = "This command is only for the creator or admins in groups"
this_command_only_creator = "This command is only for the creator in groups"
button_for_creator = "This button is only for the creator"
button_for_admins = "This button is only for admins"
invalid_command = "command not valid"

cant_vote_this = "I am not inside this group, so you can't vote it, sorry!"
registered_vote = "Vote registered!"
updated_vote = "Vote updated!"

choose_region = (
        "Choose your region. It will be the default language filter when you "
        "ask for a leaderboard")

pre_leadervote = "Top supergroups ordered by average of votes. Having at least {} votes.\nRegion: {}"
pre_leadermessage = "Top supergroups ordered by amount of sent messages during this week (UTC).\nRegion: {}"
pre_groupleaderboard = "Top users ordered by more messages sent during this week (UTC) in this group."
pre_leadermember = "Top supergroups ordered by amount of members.\nRegion: {}"


private_lang_button = "Language"
private_region_button = "Region"
private_settings = "Settings:"
private_digest_button = "Digest"
private_your_own_digest_button = "About you"
private_groups_digest_button = "About groups"
private_digest = "You can receive a digest at the end of every week. Disable or enable them anytime you want"
weekly_own_digest = "Do you want to get anytime a week is over statistic about you during the past week?"
hello_name = "Hello {name}"
digest_of_the_week_global = ("Another week is over!\nDuring the last week you globally sent {} messages "
                             "in {} groups. Position: {}\n")

digest_of_the_week_detail = "— {} messages in @{}. Position: {}\n"

generic_leaderboard = (
        "Choose one of the following order criterias for the leaderboard.\n" 
        "If you want to be faster next time there are shortcuts for leaderboards:\n\n"
        "/leadermember - <i>ordered by amount of members</i>\n"
        "/leadermessage - <i>ordered by sent messages during the week</i>\n"
        "/leadervote - <i>ordered by votes average</i>\n\n"
        "Your region: {}. Press /region in case you want to check groups of other regions")

by_members = "By members"
by_messages = "By messages"
by_votes = "By votes"


help_commands = (
        "here are the commands you can use:\n\n"
        "/leaderboard - <i>check out supergroups leaderboards</i>\n"
        "/vote - <i>vote a group</i>\n"
        "/aboutyou - <i>get stats about you</i>\n"
        "/settings - <i>change your settings</i>\n"
        "/feedback - <i>send a feedback</i>"
)

help_message = "This bot does statistics and leaderboards about public supergrous and their users"

insert_param_vote = (
        "To vote a group send the username (no matter the presence of the '@')"
        " as a parameter of the /vote command.\n\nExample:\n<code>/vote @NonEntrate</code>")


disable = "Disable"
hey_no_lang_set = (
        "Hey! You haven't set any language yet, so in which region of the leaderboards should"
        " i put this group?. No, really, set a language.")

you_inactive_this_week = "This week you didn't sent messages in groups yet"
this_week_you_sent_this = "This week you already sent:"
you_globally_this_week = "You globally already sent {} messages in {} groups during this week. Position: {}"

unsupported_chat = (
        "I have been programmed to take part only in public groups. "
        "This is not a public group. I leave, bye")

banned_until_leave = "This group has been banned. The ban will end on {} UTC.\nReason: {}.\nI leave."
not_specified = "Not specified"

group_digest_button = "Digest"
group_weekly_digest = (
        "Would you like to receive a digest of this group anytime a week is over?"
        " You can change your mind at anytime.")


groups_working = (
        "Do you want your group to be part of our leaderboards? Simply add this bot in"
        " your group and be sure to set the right language of the group. The group will "
        "be added in the region of leaderboards that you specified with the language.\n"
        "If your group has adult contents, select the right option in /settings. Please "
        "be sure to insert only the correct values or we may ban your group from our bot.\n"
        "We do not apply any kind of censorship about topics, but we may ban groups cheating "
        "in leaderboards.\nIn /settings you will even find the link to redirect users to "
        "automatically vote your group.\n\n"
        "<b>SUPPORTED COMMANDS IN GROUPS</b>:\n"
        "/settings - <i>set group settings</i>\n"
        "/groupleaderboard - <i>get a message containing leaderboard of users that wrote"
        "more messages in the group during the current week (UTC)</i>\n"
        "/grouprank - <i>Check the rank of the group</i>"
)

weekly_groups_digest = (
        "Hello! Another week is over. Here there are some stats of this group:\n\n"
        
        "-- BY MESSAGES --\n"
        "sent messages last week: {}\n"
        "sent messages this week: {}\n"
        "difference: {}  percent: {}\n"
        "position last week: {}\n"
        "position this week: {}\n\n"
        
        "-- BY MEMBERS --\n"
        "members last week: {}\n"
        "members this week: {}\n"
        "difference: {}  percent: {}\n"
        "position last week: {}\n"
        "position this week: {}\n\n"
        
        "-- BY VOTES AVERAGE --\n"
        "average and number of votes last week: {}{}|({})\n"
        "average and number of votes this week: {}{}|({})\n"
        "position last week: {}\n"
        "position this week: {}\n\n"
        
        "-- BY ACTIVE USERS --\n"
        "active users last week: {}\n"
        "active users this week: {}\n"
        "difference: {}  percent: {}\n"
        "position last week: {}\n"
        "position this week: {}\n\n"
        
        "TOP USERS OF THE WEEK:\n"
        )

added_again = "Hello! Do you want to check the group settings again?"

feedback_message = ("The only way to send a feedback is sending your message as a reply of this message"
        ".\n\nYou can send any kind of message or media.")

thanks_feedback = "Feedback succesfully sent! thank you!"

feedback_flood = ("Sorry, you already sent many feedbacks. Wait for a reply first or wait for a while."
        "No way to send this feedback")

from_developer = "This is a message from the developer of the bot."

feedback_reply = "Reply"

unrecognized_button = ("a message starting and ending with that character is handled as a button. "
        "The button you pressed is invalid. I sent you an updated keyboard.\n\nIf you were instead "
        "sending that message as just message, append another char at the beginning or at the end.")

updating_buttons = "I update buttons"

latest_update = "Updated"
seconds_ago = "{} seconds ago"
about_minutes_ago = "about {} minutes ago"
about_hours_ago = "about {} hours ago"

group_rank = {
    "title": "<b>GROUP RANK:</b>",
    "by_messages": "<b>Leaderboard ordered by messages sent during the current week</b> (region: <code>{}</code>):",
    "by_members": "<b>Leaderboard ordered by amount of members</b> (region: <code>{}</code>):",
    "by_votes": "<b>Leaderboard ordered by votes average</b> (region: <code>{}</code>):",
    "position": "- Position: {}",
    "updated": "<i>{}: {}</i>",
    "None": "Unfortunately this group isn't in any leaderboard",
    "messages": "- messages: {}",
    "members": "- members: {}",
    "votes": "- votes average|number: {}|({})"
}

feedback = "feedback"
source_code = "source code"
commands = "commands"
how_to_use_in_groups = "usage in groups"


category = "Category"
choose_group_category = "Choose the category that better fits this group. Do not lie or we'll ban the group."
categories = {
    'news': 'news',
    'science_and_education': 'science&education',
    'religion': 'religion',
    'entertainment': 'entertainment',
    'family_and_home': 'family&home',
    'sport': 'sport',
    'art_and_culture': 'art&culture',
    'politicts': 'politicts',
    'information_technology': 'IT&tech',
    'game_and_apps': 'games&apps',
    'love': 'love',
    'tourism': 'tourism',
    'economics': 'economics'
}
filter_by_category = 'filter category'
choose_category_to_filter = "choose one of the following categories to filter the leaderboard"
remove_filter = "remove filter"

change_vote = "change vote"