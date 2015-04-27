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
import xsge_gui


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Room(sge.Room):

    def event_room_start(self):
        c = True
        while c:
            i = xsge_gui.get_menu_selection(
                320, 240, ["Item 1", "Item 2", "Item 3", "Exit"],
                font_normal=font, color_normal=sge.Color("black"),
                color_selected=sge.Color("red"),
                background_color=sge.Color("aqua"), height=200, margin=16,
                halign="center", valign="middle")
            if 0 <= i <= 2:
                print("Item {} chosen!".format(i + 1))
            else:
                c = False

        sge.game.end()


Game(640, 480)
xsge_gui.init()

font = sge.Font("Liberation Mono")

sge.game.start_room = Room()


if __name__ == "__main__":
    sge.game.start()
