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

import math


ELEMENTS_PER_PAGE = 10

def get_total_pages(all_elements):
    return (math.ceil(len(all_elements)/ELEMENTS_PER_PAGE))

def adjust_chosen_page(num_of_pages, chosen_page):
    if num_of_pages == 0:
        chosen_page = 1
    if chosen_page > num_of_pages:
        chosen_page = num_of_pages
    return chosen_page

def get_first_number_of_page(page):
    return (page*ELEMENTS_PER_PAGE - ELEMENTS_PER_PAGE + 1)


def which_pages(chosen_page, total_pages):
    """
    Returns a list containing the numbers from 1 to `total_pages`, with
    `chosen_page` indicated, and abbreviated if too long.
    """

    max_on_line_number = 5

    # Build list of pages to display
    pages = []


    if total_pages == 0:
        return pages
    if chosen_page > total_pages:
        chosen_page = total_pages

    if total_pages <= max_on_line_number:
        for i in range(1, total_pages + 1):
            pages.append(i)
    else:
        pages.append(1) # add first page

        if chosen_page - 1 > 1:
            pages.append(chosen_page - 1) # add before current page

        if chosen_page != 1 and chosen_page != total_pages:
            pages.append(chosen_page) # add current page - 1 and last are added with other stuff

        if chosen_page + 1 < total_pages:
            pages.append(chosen_page + 1) #add after current page

        pages.append(total_pages) # add last page
    return pages


def displayed_pages(pages, chosen_page):
    """ receive an array and give buttons"""
    texted_pages = []
    for page in pages:
        if page == pages[1] and page > 2:
            texted_pages.append("..")
        if page == chosen_page:
            texted_pages.append("-{}-".format(page))
            continue
        texted_pages.append(str(page))
        if page == pages[-2] and page < (pages[-1] - 1):
            texted_pages.append("..")
    print (texted_pages)