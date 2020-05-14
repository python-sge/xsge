#!/usr/bin/env python3

# Lighting Example
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


import os
import random

import sge
import xsge_lighting


DATA = os.path.join(os.path.dirname(__file__), "data")

circles = []


class Game(sge.dsp.Game):

    def event_step(self, time_passed, delta_mult):
        xsge_lighting.project_darkness()
        self.project_line(self.width / 2, 0, self.width / 2, self.height,
                          sge.gfx.Color("#808080"), thickness=3)
        self.project_line(0, self.height / 2, self.width, self.height / 2,
                          sge.gfx.Color("#808080"), thickness=3)

    def event_paused_step(self, time_passed, delta_mult):
        self.event_step(time_passed, delta_mult)

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()
        elif key in ("p", "enter"):
            self.pause()

    def event_close(self):
        self.end()

    def event_paused_key_press(self, key, char):
        self.unpause()

    def event_paused_close(self):
        self.event_close()


class Circle(sge.dsp.Object):
    def __init__(self, x, y, player=0):
        super(Circle, self).__init__(x, y, tangible=False, bbox_x=-32,
                                     bbox_y=-32, bbox_width=64, bbox_height=64)
        self.player = player

    def light_up(self):
        s = [light_sprite, light_red_sprite, light_green_sprite,
             light_blue_sprite][self.player]
        xsge_lighting.project_light(self.x, self.y, s)

    def event_begin_step(self, time_passed, delta_mult):
        left_key = ['left', 'a', 'j', 'kp_4'][self.player]
        right_key = ['right', 'd', 'l', 'kp_6'][self.player]
        up_key = ['up', 'w', 'i', 'kp_8'][self.player]
        down_key = ['down', 's', 'k', 'kp_5'][self.player]
        self.xvelocity = (sge.keyboard.get_pressed(right_key) -
                          sge.keyboard.get_pressed(left_key))
        self.yvelocity = (sge.keyboard.get_pressed(down_key) -
                          sge.keyboard.get_pressed(up_key))

        # Limit the circles to inside the room.
        if self.bbox_left < 0:
            self.bbox_left = 0
        elif self.bbox_right >= sge.game.current_room.width:
            self.bbox_right = sge.game.current_room.width - 1
        if self.bbox_top < 0:
            self.bbox_top = 0
        elif self.bbox_bottom >= sge.game.current_room.height:
            self.bbox_bottom = sge.game.current_room.height - 1

        # Set view
        my_view = sge.game.current_room.views[self.player]
        my_view.x = self.x - (my_view.width // 2)
        my_view.y = self.y - (my_view.height // 2)

        self.light_up()

    def event_paused_step(self, time_passed, delta_mult):
        self.light_up()


def main():
    global light_sprite
    global light_red_sprite
    global light_green_sprite
    global light_blue_sprite

    # Create Game object
    Game(width=640, height=480, collision_events_enabled=False)

    # Load sprites
    light_sprite = sge.gfx.Sprite("light", DATA, origin_x=32, origin_y=32)
    light_red_sprite = sge.gfx.Sprite("light_red", DATA, origin_x=32,
                                      origin_y=32)
    light_green_sprite = sge.gfx.Sprite("light_green", DATA, origin_x=32,
                                        origin_y=32)
    light_blue_sprite = sge.gfx.Sprite("light_blue", DATA, origin_x=32,
                                       origin_y=32)
    fence = sge.gfx.Sprite('fence', DATA)

    # Load backgrounds
    layers = [sge.gfx.BackgroundLayer(fence, 0, 0, 0, repeat_left=True,
                                      repeat_right=True, repeat_up=True,
                                      repeat_down=True)]
    background = sge.gfx.Background(layers, sge.gfx.Color('white'))

    # Create objects
    objects = []
    for i in range(4):
        circle = Circle(64, 64, i)
        objects.append(circle)

    # Create views
    views = []
    for x in range(2):
        for y in range(2):
            views.append(sge.dsp.View(0, 0, 320 * x, 240 * y, 320, 240))

    # Create rooms
    sge.game.start_room = sge.dsp.Room(objects, 1280, 1024, views, background)

    sge.game.start()


if __name__ == '__main__':
    main()

