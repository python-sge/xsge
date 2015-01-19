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

menu_sprite = sge.Sprite(width=200, height=200, origin_x=100)
menu_sprite.draw_rectangle(0, 0, 200, 200, fill=sge.Color("#0ff"))
item_sprites = [sge.Sprite.from_text(font, "Item 1", halign=sge.ALIGN_CENTER),
                sge.Sprite.from_text(font, "Item 2", halign=sge.ALIGN_CENTER),
                sge.Sprite.from_text(font, "Item 3", halign=sge.ALIGN_CENTER),
                sge.Sprite.from_text(font, "Exit", halign=sge.ALIGN_CENTER)]
item_sprites_selected = [
    sge.Sprite.from_text(font, "Item 1", color=sge.Color("white"),
                         halign=sge.ALIGN_CENTER),
    sge.Sprite.from_text(font, "Item 2", color=sge.Color("white"),
                         halign=sge.ALIGN_CENTER),
    sge.Sprite.from_text(font, "Item 3", color=sge.Color("white"),
                         halign=sge.ALIGN_CENTER),
    sge.Sprite.from_text(font, "Exit", color=sge.Color("white"),
                         halign=sge.ALIGN_CENTER)]

item1 = menu.SimpleItem(320, 150, item_sprites_selected[0], item_sprites[0],
                        action=print, action_args=["Item 1 chosen!"])
item2 = menu.SimpleItem(320, 175, item_sprites_selected[1], item_sprites[1],
                        action=print, action_args=["Item 2 chosen!"])
item3 = menu.SimpleItem(320, 200, item_sprites_selected[2], item_sprites[2],
                        action=print, action_args=["Item 3 chosen!"])
item4 = menu.SimpleItem(320, 225, item_sprites_selected[3], item_sprites[3],
                        action=sge.game.end)
menu = menu.Menu(320, 140, [item1, item2, item3, item4], sprite=menu_sprite)
objects = [menu]

sge.game.start_room = sge.Room(objects)


if __name__ == "__main__":
    sge.game.start()
