#!/usr/bin/env python3

# Copyright (c) 2014 Julian Marchant <onpon4@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
FALL_ACCEL = 0.35
FALL_SPEED = 10
WALL_DECEL = 0.4
JUMP_SPEED = 8


class Game(sge.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Player(physics.Collider):

    on_floor = False

    def event_step(self, time_passed, delta_mult):
        self.xvelocity += (sge.keyboard.get_pressed("right") -
                           sge.keyboard.get_pressed("left")) * WALK_ACCEL

        if self.xvelocity > FRICTION:
            self.xvelocity -= FRICTION
        elif self.xvelocity < -FRICTION:
            self.xvelocity += FRICTION
        else:
            self.xvelocity = 0

        self.yvelocity += FALL_ACCEL

        if self.xvelocity > WALK_SPEED:
            self.xvelocity = WALK_SPEED
        elif self.xvelocity < -WALK_SPEED:
            self.xvelocity = -WALK_SPEED

        if self.yvelocity > FALL_SPEED:
            self.yvelocity = FALL_SPEED

        self.on_floor = (self.get_bottom_touching_wall() or
                         self.get_bottom_touching_slope())

    def event_key_press(self, key, char):
        if key == "up":
            if self.on_floor:
                self.yvelocity = -JUMP_SPEED

    def event_physics_collision_left(self, other):
        if isinstance(other, physics.SolidRight):
            self.xvelocity = 0

    def event_physics_collision_right(self, other):
        if isinstance(other, physics.SolidLeft):
            self.xvelocity = 0

    def event_physics_collision_top(self, other):
        if isinstance(other, physics.SolidBottom):
            self.yvelocity = 0

    def event_physics_collision_bottom(self, other):
        if isinstance(other, physics.SolidTop):
            self.yvelocity = 0


class Solid(physics.Solid):

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(Solid, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class SolidTop(physics.SolidTop):

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(SolidTop, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class SlopeTopLeft(physics.SlopeTopLeft):

    xsticky_top = True

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(SlopeTopLeft, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class SlopeTopRight(physics.SlopeTopRight):

    xsticky_top = True

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(SlopeTopRight, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class SlopeBottomLeft(physics.SlopeBottomLeft):

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(SlopeBottomLeft, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class SlopeBottomRight(physics.SlopeBottomRight):

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=False, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(SlopeBottomRight, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


Game(640, 480)

types = {"player": Player, "solid": Solid, "unisolid": SolidTop,
         "slope_topleft": SlopeTopLeft, "slope_topright": SlopeTopRight,
         "slope_bottomleft": SlopeBottomLeft,
         "slope_bottomright": SlopeBottomRight}
sge.game.start_room = tmx.load(os.path.join(DATA, "level.tmx"), types=types)


if __name__ == "__main__":
    sge.game.start()
