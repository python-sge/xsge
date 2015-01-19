#!/usr/bin/env python3

# Menu example
# Written in 2015 by Julian Marchant <onpon4@riseup.net>
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import six
import sge
from xsge import menu


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


Game(640, 480)

font = sge.Font("Liberation Mono")

mnu = menu.get_text_menu(320, 240, ["Item 1", "Item 2", "Item 3", "Exit"],
                         font=font, color=sge.Color("black"),
                         selected_color=sge.Color("red"),
                         background_color=sge.Color("aqua"), height=200,
                         margin=16, halign="center", valign="middle")

for i in six.moves.range(3):
    mnu.items[i].action = print
    mnu.items[i].action_args = ["Item {} chosen!".format(i + 1)]

mnu.items[3].action = sge.game.end

objects = [mnu]

sge.game.start_room = sge.Room(objects)


if __name__ == "__main__":
    sge.game.start()
