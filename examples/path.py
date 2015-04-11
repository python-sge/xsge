#!/usr/bin/env python3

# Physics example
# Written in 2014 by Julian Marchant <onpon4@riseup.net>
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
import xsge_path


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


def main():
    # Create Game object
    Game(800, 600)

    # Load sprites
    square_sprite = sge.Sprite(width=32, height=32)
    square_sprite.draw_rectangle(0, 0, 32, 32, fill=sge.Color("aqua"))

    # Load backgrounds
    background = sge.Background([], sge.Color("black"))

    # Create objects
    obj = sge.Object(400, 300, sprite=square_sprite)
    points = [(-100, -100), (0, -150), (100, -100), (100, 100), (-100, 100),
              (0, 0)]
    pth = xsge_path.Path(200, 150, points)
    pth.follow_start(obj, 5, 0.1, 0.1, loop=None)
    objects = [obj, pth]

    # Create room
    sge.game.start_room = sge.Room(objects, background=background)

    sge.game.start()


if __name__ == "__main__":
    main()
