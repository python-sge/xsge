#!/usr/bin/env python3

# Platformer example
# Written in 2014, 2015 by Julian Marchant <onpon4@riseup.net>
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

import os

import sge
from xsge import physics, tmx


DATA = os.path.join(os.path.dirname(__file__), "data")

WALK_ACCEL = 0.5
WALK_SPEED = 5
FRICTION = 0.25
FALL_ACCEL = 0.25
FALL_SPEED = 10
JUMP_SPEED = 6
SLIDE_ACCEL = 1
SLIDE_SPEED = 2


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Player(physics.Collider):

    on_floor = False
    on_slope = False

    def event_step(self, time_passed, delta_mult):
        self.on_floor = self.get_bottom_touching_wall()
        self.on_slope = (not self.on_floor and self.get_bottom_touching_slope())

        self.xvelocity += (sge.keyboard.get_pressed("right") -
                           sge.keyboard.get_pressed("left")) * WALK_ACCEL

        if self.xvelocity > FRICTION:
            self.xvelocity -= FRICTION
        elif self.xvelocity < -FRICTION:
            self.xvelocity += FRICTION
        else:
            self.xvelocity = 0

        if self.xvelocity > WALK_SPEED:
            self.xvelocity = WALK_SPEED
        elif self.xvelocity < -WALK_SPEED:
            self.xvelocity = -WALK_SPEED

        if self.on_slope:
            if self.yvelocity > SLIDE_SPEED + SLIDE_ACCEL:
                self.yvelocity -= SLIDE_ACCEL
            elif self.yvelocity < SLIDE_SPEED - SLIDE_ACCEL:
                self.yvelocity += SLIDE_ACCEL
            else:
                self.yvelocity = SLIDE_SPEED
        elif not self.on_floor:
            self.yvelocity += FALL_ACCEL

            if self.yvelocity > FALL_SPEED:
                self.yvelocity = FALL_SPEED

    def event_key_press(self, key, char):
        if key == "up":
            if self.on_floor or self.on_slope:
                self.yvelocity = -JUMP_SPEED

    def event_physics_collision_left(self, other):
        if isinstance(other, physics.SolidRight):
            self.xvelocity = 0

    def event_physics_collision_right(self, other):
        if isinstance(other, physics.SolidLeft):
            self.xvelocity = 0

    def event_physics_collision_top(self, other):
        if isinstance(other, (physics.SolidBottom, physics.SlopeBottomLeft,
                              physics.SlopeBottomRight)):
            self.yvelocity = 0

    def event_physics_collision_bottom(self, other):
        if isinstance(other, physics.SolidTop):
            self.yvelocity = 0


class Solid(physics.Solid):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(Solid, self).__init__(*args, **kwargs)


class SolidTop(physics.SolidTop):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(SolidTop, self).__init__(*args, **kwargs)


class SlopeTopLeft(physics.SlopeTopLeft):

    xsticky_top = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(SlopeTopLeft, self).__init__(*args, **kwargs)


class SlopeTopRight(physics.SlopeTopRight):

    xsticky_top = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(SlopeTopRight, self).__init__(*args, **kwargs)


class SlopeBottomLeft(physics.SlopeBottomLeft):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(SlopeBottomLeft, self).__init__(*args, **kwargs)


class SlopeBottomRight(physics.SlopeBottomRight):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super(SlopeBottomRight, self).__init__(*args, **kwargs)


Game(640, 480)

types = {"player": Player, "solid": Solid, "unisolid": SolidTop,
         "slope_topleft": SlopeTopLeft, "slope_topright": SlopeTopRight,
         "slope_bottomleft": SlopeBottomLeft,
         "slope_bottomright": SlopeBottomRight}
sge.game.start_room = tmx.load(os.path.join(DATA, "level.tmx"), types=types)


if __name__ == "__main__":
    sge.game.start()
