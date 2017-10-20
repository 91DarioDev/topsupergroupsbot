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

class Pages:

    def __init__(self, lst, chosen_page=1, elements_per_page=10):
        self.elements_per_page = elements_per_page
        self.lst = lst
        self.number_of_pages = self.get_number_of_pages()
        self.chosen_page = self._adjust_chosen_page(chosen_page)


    def get_number_of_pages(self):
        return (math.ceil(len(self.lst)/self.elements_per_page))

    def _adjust_chosen_page(self, chosen_page):
        if self.number_of_pages == 0:
            chosen_page = 1
        if chosen_page > self.number_of_pages:
            chosen_page = self.number_of_pages
        return chosen_page

    def first_number_of_page(self):
        return (self.chosen_page*self.elements_per_page - self.elements_per_page + 1)


    def displayed_pages(self):
        """
        Returns a list containing the numbers from 1 to `total_pages`, with
        `chosen_page` indicated, and abbreviated if too long.
        """

        max_on_line_number = 5

        # Build list of pages to display
        pages = []

        if self.number_of_pages == 0:
            return pages
        if self.chosen_page > self.number_of_pages:
            self.chosen_page = self.number_of_pages

        if self.number_of_pages <= max_on_line_number:
            for i in range(1, self.number_of_pages + 1):
                pages.append(i)
        else:
            pages.append(1) # add first page

            if self.chosen_page - 1 > 1:
                pages.append(self.chosen_page - 1) # add before current page

            if self.chosen_page != 1 and self.chosen_page != self.number_of_pages:
                pages.append(self.chosen_page) # add current page - 1 and last are added with other stuff

            if self.chosen_page + 1 < self.number_of_pages:
                pages.append(self.chosen_page + 1) #add after current page

            pages.append(self.number_of_pages) # add last page
        return pages

    def chosen_page_items(self):
        offset = self.first_number_of_page() - 1
        return self.lst[offset:offset+self.elements_per_page]