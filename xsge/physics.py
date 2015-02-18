# xSGE Physics Framework
# Copyright (C) 2014, 2015 Julian Marchant <onpon4@riseup.net>
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

"""
This module provides an easy-to-use framework for collision physics.
This is especially useful for platformers, though it can also be useful
for other types of games.

.. note::

   This collision system supports plain rectangle-based collision
   detection ONLY.  Attempting to use precise or ellipse collision
   detection will not work as you expect, and may often not even work at
   all.  This is because implementing support for such mask-based
   collision detection would be guaranteed to be slow, unreliable, and
   needlessly complicated; it's not worth it.

   If you must use precise collision detection, consider doing so with
   a separate object that follows the appropriate :class:`Collider`
   object.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math

import sge


__all__ = ["Collider", "SolidLeft", "SolidRight", "SolidTop", "SolidBottom",
           "Solid", "SlopeTopLeft", "SlopeTopRight", "SlopeBottomLeft",
           "SlopeBottomRight", "MobileWall"]


NDIG = 6


class Collider(sge.Object):

    """
    Class for objects which have physics interactions.

    .. note::

       This class depends on use of :meth:`Collider.move_x` and
       :meth:`Collider.move_y` to handle physics interactions.
       :meth:`event_update_position` uses these methods, so speed
       attributes will work properly, but changing :attr:`x` and
       :attr:`y` manually will not cause any physics to occur.
    """

    def move_x(self, move, absolute=False):
        """
        Move the object horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`x`.
        - ``absolute`` -- If set to :const:`True`, the distance moved
          horizontally is absolute, i.e. will not be reduced as a result
          of vertical movement caused by slopes.  Otherwise, any
          vertical movement caused by slopes will result in a reduction
          of horizontal movement.
        """
        sticky = False
        move_mult = 1
        old_x = self.x
        old_y = self.y
        old_bbox_left = self.bbox_left
        old_bbox_right = self.bbox_right
        old_bbox_top = self.bbox_top
        old_bbox_bottom = self.bbox_bottom
        rold_bbox_top = round(old_bbox_top, NDIG)
        rold_bbox_bottom = round(old_bbox_bottom, NDIG)

        if move > 0:
            bbb = round(self.bbox_bottom, NDIG)
            for slope in self.collision(SlopeTopRight, y=(self.y + 1)):
                if slope.xsticky_top:
                    y = round(slope.get_slope_y(self.bbox_left), NDIG)
                    if bbb == y:
                        sticky = 1
                        if not absolute:
                            h = math.hypot(slope.bbox_width, slope.bbox_height)
                            move_mult = slope.bbox_width / h
                        break
                    elif (self.bbox_left <= slope.bbox_left and
                          not self.collision(slope)):
                        sticky = 1
                        break
            else:
                bbt = round(self.bbox_top, NDIG)
                for slope in self.collision(SlopeBottomRight, y=(self.y - 1)):
                    if slope.xsticky_bottom:
                        y = round(slope.get_slope_y(self.bbox_left), NDIG)
                        if bbt == y:
                            sticky = 2
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_width / h
                            break
                        elif (self.bbox_left <= slope.bbox_left and
                              not self.collision(slope)):
                            sticky = 2
                            break

            self.x += move * move_mult

            stopper = None

            for other in self.collision(SlopeTopLeft):
                y = other.get_slope_y(self.bbox_right)
                if self.bbox_bottom > y:
                    oy = round(other.get_slope_y(old_bbox_right), NDIG)
                    if rold_bbox_bottom <= oy:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_width / h
                            if m < move_mult:
                                self.x -= move * (move_mult - m)
                                move_mult = m
                                y = other.get_slope_y(self.bbox_right)
                        self.move_y(y - self.bbox_bottom)
                        x = other.get_slope_x(self.bbox_bottom)
                        self.bbox_right = min(self.bbox_right, x)
                        stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        stopper = other

            for other in self.collision(SlopeBottomLeft):
                y = other.get_slope_y(self.bbox_right)
                if self.bbox_top < y:
                    oy = round(other.get_slope_y(old_bbox_right), NDIG)
                    if rold_bbox_top >= oy:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_width / h
                            if m < move_mult:
                                self.x -= move * (move_mult - m)
                                move_mult = m
                                y = other.get_slope_y(self.bbox_right)
                        self.move_y(y - self.bbox_top)
                        x = other.get_slope_x(self.bbox_top)
                        self.bbox_right = min(self.bbox_right, x)
                        stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        stopper = other

            for other in self.collision(SolidLeft):
                if not self.collision(other, x=old_x):
                    self.bbox_right = min(self.bbox_right, other.bbox_left)
                    stopper = other

            if stopper is not None:
                self.event_physics_collision_right(stopper)
                stopper.event_physics_collision_left(self)
                
        elif move < 0:
            bbb = round(self.bbox_bottom, NDIG)
            for slope in self.collision(SlopeTopLeft, y=(self.y + 1)):
                if slope.xsticky_top:
                    y = round(slope.get_slope_y(self.bbox_right), NDIG)
                    if bbb == y:
                        sticky = 1
                        if not absolute:
                            h = math.hypot(slope.bbox_width, slope.bbox_height)
                            move_mult = slope.bbox_width / h
                        break
                    elif (self.bbox_right >= slope.bbox_right and
                          not self.collision(slope)):
                        sticky = 1
                        break
            else:
                bbt = round(self.bbox_top, NDIG)
                for slope in self.collision(SlopeBottomLeft, y=(self.y - 1)):
                    if slope.xsticky_bottom:
                        y = round(slope.get_slope_y(self.bbox_right), NDIG)
                        if bbt == y:
                            sticky = 2
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_width / h
                            break
                        elif (self.bbox_right >= slope.bbox_right and
                              not self.collision(slope)):
                            sticky = 2
                            break

            self.x += move * move_mult

            stopper = None

            for other in self.collision(SlopeTopRight):
                y = other.get_slope_y(self.bbox_left)
                if self.bbox_bottom > y:
                    oy = round(other.get_slope_y(old_bbox_left), NDIG)
                    if rold_bbox_bottom <= oy:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_width / h
                            if m < move_mult:
                                self.x -= move * (move_mult - m)
                                move_mult = m
                                y = other.get_slope_y(self.bbox_left)
                        self.move_y(y - self.bbox_bottom)
                        x = other.get_slope_x(self.bbox_bottom)
                        self.bbox_left = max(self.bbox_left, x)
                        stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        stopper = other

            for other in self.collision(SlopeBottomRight):
                y = other.get_slope_y(self.bbox_left)
                if self.bbox_top < y:
                    oy = round(other.get_slope_y(old_bbox_left), NDIG)
                    if rold_bbox_top >= oy:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_width / h
                            if m < move_mult:
                                self.x -= move * (move_mult - m)
                                move_mult = m
                                y = other.get_slope_y(self.bbox_left)
                        self.move_y(y - self.bbox_top)
                        x = other.get_slope_x(self.bbox_top)
                        self.bbox_left = max(self.bbox_left, x)
                        stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        stopper = other

            for other in self.collision(SolidRight):
                if not self.collision(other, x=old_x):
                    self.bbox_left = max(self.bbox_left, other.bbox_right)
                    stopper = other

            if stopper is not None:
                self.event_physics_collision_left(stopper)
                stopper.event_physics_collision_right(self)

        # Engage stickiness (same whether moving left or right)
        # 1 = sticking to the floor
        # 2 = sticking to the ceiling
        if sticky == 1:
            if (not self.get_bottom_touching_slope() and
                    not self.get_bottom_touching_wall()):
                new_bbox_bottom = None
                for other in sge.game.current_room.objects:
                    if (other.bbox_left >= self.bbox_right or
                            other.bbox_right <= self.bbox_left):
                        continue

                    if isinstance(other, SolidTop):
                        y = other.bbox_top
                    elif isinstance(other, SlopeTopLeft):
                        y = other.get_slope_y(self.bbox_right)
                    elif isinstance(other, SlopeTopRight):
                        y = other.get_slope_y(self.bbox_left)
                    else:
                        continue

                    if (y >= self.bbox_bottom and
                            (new_bbox_bottom is None or
                             y < new_bbox_bottom)):
                        new_bbox_bottom = y

                if new_bbox_bottom is not None:
                    self.bbox_bottom = new_bbox_bottom
        elif sticky == 2:
            if (not self.get_top_touching_slope() and
                    not self.get_top_touching_wall()):
                new_bbox_top = None
                for other in sge.game.current_room.objects:
                    if (other.bbox_left >= self.bbox_right or
                            other.bbox_right <= self.bbox_left):
                        continue

                    if isinstance(other, SolidBottom):
                        y = other.bbox_bottom
                    elif isinstance(other, SlopeBottomLeft):
                        y = other.get_slope_y(self.bbox_right)
                    elif isinstance(other, SlopeBottomRight):
                        y = other.get_slope_y(self.bbox_left)
                    else:
                        continue

                    if y <= self.bbox_top and (new_bbox_top is None or
                                               y > new_bbox_top):
                        new_bbox_top = y

                if new_bbox_top is not None:
                    self.bbox_top = new_bbox_top

    def move_y(self, move, absolute=False):
        """
        Move the object vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        - ``absolute`` -- If set to :const:`True`, the distance moved
          vertically is absolute, i.e. will not be reduced as a result
          of horizontal movement caused by slopes.  Otherwise, any
          horizontal movement caused by slopes will result in a
          reduction of vertical movement.
        """
        sticky = False
        move_mult = 1
        old_x = self.x
        old_y = self.y
        old_bbox_left = self.bbox_left
        old_bbox_right = self.bbox_right
        rold_bbox_left = round(old_bbox_left, NDIG)
        rold_bbox_right = round(old_bbox_right, NDIG)
        old_bbox_top = self.bbox_top
        old_bbox_bottom = self.bbox_bottom

        if move > 0:
            bbr = round(self.bbox_right, NDIG)
            for slope in self.collision(SlopeBottomLeft, x=(self.x + 1)):
                if slope.ysticky_left:
                    x = round(slope.get_slope_x(self.bbox_top), NDIG)
                    if bbr == x:
                        sticky = 1
                        if not absolute:
                            h = math.hypot(slope.bbox_width, slope.bbox_height)
                            move_mult = slope.bbox_height / h
                        break
                    elif (self.bbox_top <= slope.bbox_top and
                          not self.collision(slope)):
                        sticky = 1
                        break
            else:
                bbl = round(self.bbox_left, NDIG)
                for slope in self.collision(SlopeBottomRight, x=(self.x - 1)):
                    if slope.ysticky_right:
                        x = round(slope.get_slope_x(self.bbox_top), NDIG)
                        if bbl == x:
                            sticky = 2
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_height / h
                            break
                        elif (self.bbox_top <= slope.bbox_top and
                              not self.collision(slope)):
                            sticky = 2
                            break

            self.y += move * move_mult

            stopper = None

            for other in self.collision(SlopeTopLeft):
                x = other.get_slope_x(self.bbox_bottom)
                if self.bbox_right > x:
                    ox = round(other.get_slope_x(old_bbox_bottom), NDIG)
                    if rold_bbox_right <= ox:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_height / h
                            if m < move_mult:
                                self.y -= move * (move_mult - m)
                                move_mult = m
                                x = other.get_slope_x(self.bbox_bottom)
                        self.move_x(x - self.bbox_right)
                        y = other.get_slope_y(self.bbox_right)
                        self.bbox_bottom = min(self.bbox_bottom, y)
                        stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        stopper = other

            for other in self.collision(SlopeTopRight):
                x = other.get_slope_x(self.bbox_bottom)
                if self.bbox_left < x:
                    ox = round(other.get_slope_x(old_bbox_bottom), NDIG)
                    if rold_bbox_left >= ox:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_height / h
                            if m < move_mult:
                                self.y -= move * (move_mult - m)
                                move_mult = m
                                x = other.get_slope_x(self.bbox_bottom)
                        self.move_x(x - self.bbox_left)
                        y = other.get_slope_y(self.bbox_left)
                        self.bbox_bottom = min(self.bbox_bottom, y)
                        stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        stopper = other

            for other in self.collision(SolidTop):
                if not self.collision(other, y=old_y):
                    self.bbox_bottom = min(self.bbox_bottom, other.bbox_top)
                    stopper = other

            if stopper is not None:
                self.event_physics_collision_bottom(stopper)
                stopper.event_physics_collision_top(self)
                
        elif move < 0:
            bbr = round(self.bbox_right, NDIG)
            for slope in self.collision(SlopeTopLeft, x=(self.x + 1)):
                if slope.ysticky_left:
                    x = round(slope.get_slope_x(self.bbox_bottom), NDIG)
                    if bbr == x:
                        sticky = 1
                        if not absolute:
                            h = math.hypot(slope.bbox_width, slope.bbox_height)
                            move_mult = slope.bbox_height / h
                        break
                    elif (self.bbox_bottom >= slope.bbox_bottom and
                          not self.collision(slope)):
                        sticky = 1
                        break
            else:
                bbl = round(self.bbox_left, NDIG)
                for slope in self.collision(SlopeTopRight, x=(self.x - 1)):
                    if slope.ysticky_right:
                        x = round(slope.get_slope_x(self.bbox_bottom), NDIG)
                        if bbl == x:
                            sticky = 2
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_height / h
                            break
                        elif (self.bbox_bottom >= slope.bbox_bottom and
                              not self.collision(slope)):
                            sticky = 2
                            break

            self.y += move * move_mult

            stopper = None

            for other in self.collision(SlopeBottomLeft):
                x = other.get_slope_x(self.bbox_top)
                if self.bbox_right > x:
                    ox = round(other.get_slope_x(old_bbox_top), NDIG)
                    if rold_bbox_right <= ox:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_height / h
                            if m < move_mult:
                                self.y -= move * (move_mult - m)
                                move_mult = m
                                x = other.get_slope_x(self.bbox_top)
                        self.move_x(x - self.bbox_right)
                        y = other.get_slope_y(self.bbox_right)
                        self.bbox_top = max(self.bbox_top, y)
                        stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        stopper = other

            for other in self.collision(SlopeBottomRight):
                x = other.get_slope_x(self.bbox_top)
                if self.bbox_left < x:
                    ox = round(other.get_slope_x(old_bbox_top), NDIG)
                    if rold_bbox_left >= ox:
                        if not absolute:
                            h = math.hypot(other.bbox_width, other.bbox_height)
                            m = other.bbox_height / h
                            if m < move_mult:
                                self.y -= move * (move_mult - m)
                                move_mult = m
                                x = other.get_slope_x(self.bbox_top)
                        self.move_x(x - self.bbox_left)
                        y = other.get_slope_y(self.bbox_left)
                        self.bbox_top = max(self.bbox_top, y)
                        stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        stopper = other

            for other in self.collision(SolidBottom):
                if not self.collision(other, y=old_y):
                    self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                    stopper = other

            if stopper is not None:
                self.event_physics_collision_top(stopper)
                stopper.event_physics_collision_bottom(self)

        # Engage stickiness (same whether moving left or right)
        # 1 = sticking to a wall on the right
        # 2 = sticking to a wall on the left
        if sticky == 1:
            if (not self.get_right_touching_slope() and
                    not self.get_right_touching_wall()):
                new_bbox_right = None
                for other in sge.game.current_room.objects:
                    if (other.bbox_top >= self.bbox_bottom or
                            other.bbox_bottom <= self.bbox_top):
                        continue

                    if isinstance(other, SolidLeft):
                        x = other.bbox_left
                    elif isinstance(other, SlopeTopLeft):
                        x = other.get_slope_x(self.bbox_bottom)
                    elif isinstance(other, SlopeBottomLeft):
                        x = other.get_slope_x(self.bbox_top)
                    else:
                        continue

                    if x >= self.bbox_right and (new_bbox_right is None or
                                                 x < new_bbox_right):
                        new_bbox_right = x

                if new_bbox_right is not None:
                    self.bbox_right = new_bbox_right
        elif sticky == 2:
            if (not self.get_left_touching_slope() and
                    not self.get_left_touching_wall()):
                new_bbox_left = None
                for other in sge.game.current_room.objects:
                    if (other.bbox_top >= self.bbox_bottom or
                            other.bbox_bottom <= self.bbox_top):
                        continue

                    if isinstance(other, SolidRight):
                        x = other.bbox_right
                    elif isinstance(other, SlopeTopRight):
                        x = other.get_slope_x(self.bbox_bottom)
                    elif isinstance(other, SlopeBottomRight):
                        x = other.get_slope_x(self.bbox_top)
                    else:
                        continue

                    if x <= self.bbox_left and (new_bbox_left is None or
                                                x > new_bbox_left):
                        new_bbox_left = x

                if new_bbox_left is not None:
                    self.bbox_left = new_bbox_left

    def get_left_touching_wall(self):
        """
        Return a list of :class:`SolidRight` objects whose right sides
        are touching the left side of this object.
        """
        r = []
        for tile in self.collision(SolidRight, x=(self.x - 1)):
            if not self.collision(tile):
                r.append(tile)
        return r

    def get_right_touching_wall(self):
        """
        Return a list of :class:`SolidLeft` objects whose left sides are
        touching the right side of this object.
        """
        r = []
        for tile in self.collision(SolidLeft, x=(self.x + 1)):
            if not self.collision(tile):
                r.append(tile)
        return r

    def get_top_touching_wall(self):
        """
        Return a list of :class:`SolidTop` objects whose top sides are
        touching the bottom side of this object.
        """
        r = []
        for tile in self.collision(SolidBottom, y=(self.y - 1)):
            if not self.collision(tile):
                r.append(tile)
        return r

    def get_bottom_touching_wall(self):
        """
        Return a list of :class:`SolidBottom` objects whose bottom sides
        are touching the top side of this object.
        """
        r = []
        for tile in self.collision(SolidTop, y=(self.y + 1)):
            if not self.collision(tile):
                r.append(tile)
        return r

    def get_left_touching_slope(self):
        """
        Return a list of :class:`SlopeTopRight` and
        :class:`SlopeBottomRight` objects whose right sides are touching
        the left side of this object.
        """
        r = []

        bbb = round(self.bbox_bottom, NDIG)
        for slope in self.collision(SlopeTopRight, x=(self.x - 1)):
            y = round(slope.get_slope_y(self.bbox_left), NDIG)
            if bbb == y or (self.bbox_bottom >= slope.bbox_bottom and
                            not self.collision(slope)):
                r.append(slope)

        bbt = round(self.bbox_top, NDIG)
        for slope in self.collision(SlopeBottomRight, x=(self.x - 1)):
            y = round(slope.get_slope_y(self.bbox_left), NDIG)
            if bbt == y or (self.bbox_top <= slope.bbox_top and
                            not self.collision(sope)):
                r.append(slope)

        return r

    def get_right_touching_slope(self):
        """
        Return a list of :class:`SlopeTopLeft` and
        :class:`SlopeBottomLeft` objects whose left sides are touching
        the right side of this object.
        """
        r = []

        bbb = round(self.bbox_bottom, NDIG)
        for slope in self.collision(SlopeTopLeft, x=(self.x + 1)):
            y = round(slope.get_slope_y(self.bbox_right), NDIG)
            if bbb == y or (self.bbox_bottom >= slope.bbox_bottom and
                            not self.collision(slope)):
                r.append(slope)

        bbt = round(self.bbox_top, NDIG)
        for slope in self.collision(SlopeBottomLeft, x=(self.x + 1)):
            y = round(slope.get_slope_y(self.bbox_right), NDIG)
            if bbt == y or (self.bbox_top <= slope.bbox_top and
                            not self.collision(slope)):
                r.append(slope)

        return r

    def get_top_touching_slope(self):
        """
        Return a list of :class:`SlopeBottomLeft` and
        :class:`SlopeBottomRight` objects whose bottom sides are
        touching the top side of this object.
        """
        r = []

        bbr = round(self.bbox_right, NDIG)
        for slope in self.collision(SlopeBottomLeft, y=(self.y - 1)):
            x = round(slope.get_slope_x(self.bbox_top), NDIG)
            if bbr == x or (self.bbox_right >= slope.bbox_right and
                            not self.collision(slope)):
                r.append(slope)

        bbl = round(self.bbox_left, NDIG)
        for slope in self.collision(SlopeBottomRight, y=(self.y - 1)):
            x = round(slope.get_slope_x(self.bbox_top), NDIG)
            if bbl == x or (self.bbox_left <= slope.bbox_left and
                            not self.collision(slope)):
                r.append(slope)

        return r

    def get_bottom_touching_slope(self):
        """
        Return a list of :class:`SlopeTopLeft` and
        :class:`SlopeTopRight` objects whose top sides are touching the
        bottom side of this object.
        """
        r = []

        bbr = round(self.bbox_right, NDIG)
        for slope in self.collision(SlopeTopLeft, y=(self.y + 1)):
            x = round(slope.get_slope_x(self.bbox_bottom), NDIG)
            if bbr == x or (self.bbox_right >= slope.bbox_right and
                            not self.collision(slope)):
                r.append(slope)

        bbl = round(self.bbox_left, NDIG)
        for slope in self.collision(SlopeTopRight, y=(self.y + 1)):
            x = round(slope.get_slope_x(self.bbox_bottom), NDIG)
            if bbl == x or (self.bbox_left <= slope.bbox_left and
                            not self.collision(slope)):
                r.append(slope)

        return r

    def event_physics_collision_left(self, other):
        """
        Called when the left side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_right(self, other):
        """
        Called when the right side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other):
        """
        Called when the top side of the collider collides with a wall or
        slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other):
        """
        Called when the bottom side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_update_position(self, delta_mult):
        xdecel = (self.xdeceleration and self.xvelocity and
                  (self.xdeceleration < 0) != (self.xvelocity < 0))
        ydecel = (self.ydeceleration and self.yvelocity and
                  (self.ydeceleration < 0) != (self.yvelocity < 0))

        if (self.xacceleration + self.xdeceleration and
                (self.xacceleration or xdecel)):
            vi = self.xvelocity
            a = self.xacceleration * delta_mult
            self.xvelocity += a

            if xdecel:
                if abs(self.xvelocity) > abs(self.xdeceleration):
                    a += self.xdeceleration * delta_mult
                    self.xvelocity += self.xdeceleration * delta_mult
                else:
                    a -= self.xvelocity
                    self.xvelocity = 0

            d = ((self.xvelocity ** 2) - (vi ** 2)) / (2 * a)
            self.move_x(math.copysign(d, self.xvelocity))
        else:
            self.move_x(self.xvelocity * delta_mult)

        if (self.yacceleration + self.ydeceleration and
                (self.yacceleration or ydecel)):
            vi = self.yvelocity
            a = self.yacceleration * delta_mult
            self.yvelocity += a

            if ydecel:
                if abs(self.yvelocity) > abs(self.ydeceleration):
                    a += self.ydeceleration * delta_mult
                    self.yvelocity += self.ydeceleration * delta_mult
                else:
                    a -= self.yvelocity
                    self.yvelocity = 0

            d = ((self.yvelocity ** 2) - (vi ** 2)) / (2 * a)
            self.move_y(math.copysign(d, self.yvelocity))
        else:
            self.move_y(self.yvelocity * delta_mult)


class SolidLeft(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """

    def event_physics_collision_left(self, other):
        """
        Called when the left side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SolidRight(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the right.
    """

    def event_physics_collision_right(self, other):
        """
        Called when the right side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SolidTop(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """

    def event_physics_collision_top(self, other):
        """
        Called when the top side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SolidBottom(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the bottom.
    """

    def event_physics_collision_bottom(self, other):
        """
        Called when the bottom side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class Solid(SolidLeft, SolidRight, SolidTop, SolidBottom):

    """
    Inherits :class:`SolidLeft`, :class:`SolidRight`, :class:`SolidTop`,
    and :class:`SolidBottom`.  Meant to be a convenient parent class for
    walls that should stop movement in all directions.
    """


class SlopeTopLeft(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the left.

    Slopes of this type go from the bottom-left corner to the top-right
    corner of the bounding box.

    .. attribute:: xsticky_top

       If set to :const:`True`, a collider that moves to the left while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward.

    .. attribute:: ysticky_left

       If set to :const:`True`, a collider that moves upward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right.
    """

    xsticky_top = False
    ysticky_left = False

    def get_slope_x(self, y):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = -self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_right

    def get_slope_y(self, x):
        """
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = -self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_bottom

    def event_physics_collision_left(self, other):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other):
        """
        Called when the top side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SlopeTopRight(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky_top

       If set to :const:`True`, a collider that moves to the right while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward.

    .. attribute:: ysticky_right

       If set to :const:`True`, a collider that moves upward while
       touching the right side of the slope will attempt to keep
       touching the right side of the slope by moving to the left.
    """

    xsticky_top = False
    ysticky_right = False

    def get_slope_x(self, y):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_left

    def get_slope_y(self, x):
        """
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_top

    def event_physics_collision_right(self, other):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other):
        """
        Called when the top side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SlopeBottomLeft(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the left.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky_bottom

       If set to :const:`True`, a collider that moves to the left while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward.

    .. attribute:: ysticky_left

       If set to :const:`True`, a collider that moves downward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right.
    """

    xsticky_bottom = False
    ysticky_left = False

    def get_slope_x(self, y):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_left

    def get_slope_y(self, x):
        """
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_top

    def event_physics_collision_left(self, other):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other):
        """
        Called when the bottom side of the slope collides with a
        collider in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class SlopeBottomRight(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the bottom-left corner to the top-right
    corner of the bounding box.

    .. attribute:: xsticky_bottom

       If set to :const:`True`, a collider that moves to the right while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward.

    .. attribute:: ysticky_right

       If set to :const:`True`, a collider that moves downward while
       touching the right side of the slope will attempt to keep
       touching the right side of the slope by moving to the right.
    """

    xsticky_bottom = False
    ysticky_right = False

    def get_slope_x(self, y):
        """
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = -self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_right

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = -self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_bottom

    def event_physics_collision_right(self, other):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other):
        """
        Called when the bottom side of the slope collides with a
        collider in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass


class MobileWall(sge.Object):

    """
    A parent class for walls and slopes that can move.  When an object
    of this class moves, it "pushes" any appropriate colliders, as a
    real wall might be expected to do.

    .. note::

       For classes derived from this class to be useful, they also need
       to inherit one or more of the other wall classes.  Objects of
       this class that are not also objects of other classes will
       naturally not collide.

    .. note::

       This class depends on use of :meth:`MobileWall.move_x` and
       :meth:`MobileWall.move_y` to handle physics interactions.
       :meth:`event_update_position` uses these methods, so speed
       attributes will work properly, but changing :attr:`x` and
       :attr:`y` manually will not cause any physics to occur.

    .. attribute:: sticky_left

       If set to :const:`True`, any colliders touching the left side of
       the wall will move along with it, regardless of the direction of
       movement.

    .. attribute:: sticky_right

       If set to :const:`True`, any colliders touching the right side of
       the wall will move along with it, regardless of the direction of
       movement.

    .. attribute:: sticky_top

       If set to :const:`True`, any colliders touching the top side of
       the wall will move along with it, regardless of the direction of
       movement.

    .. attribute:: sticky_left

       If set to :const:`True`, any colliders touching the bottom side
       of the wall will move along with it, regardless of the direction
       of movement.
    """

    sticky_left = False
    sticky_right = False
    sticky_top = False
    sticky_bottom = False

    def get_stuck_colliders(self):
        """
        Return a list of :class:`Collider` objects which are "stuck" to
        this wall (i.e. will move along with the wall regardless of
        direction).
        """
        stuck = []

        if self.sticky_left:
            if isinstance(self, SolidLeft):
                for other in self.collision(Collider, x=(self.x - 1)):
                    if not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider, x=(self.x - 1)):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_right >= x and (not self.collision(other) or
                                                  other.bbox_right - 1 < x):
                        stuck.append(other)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider, x=(self.x - 1)):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_right >= x and (not self.collision(other) or
                                                  other.bbox_right - 1 < x):
                        stuck.append(other)

        if self.sticky_right:
            if isinstance(self, SolidRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    if not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_left <= x and (not self.collision(other) or
                                                 other.bbox_left + 1 > x):
                        stuck.append(other)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_left <= x and (not self.collision(other) or
                                                 other.bbox_left + 1 > x):
                        stuck.append(other)

        if self.sticky_top:
            if isinstance(self, SolidTop):
                for other in self.collision(Collider, y=(self.y - 1)):
                    if not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider, y=(self.y - 1)):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_bottom >= y and (not self.collision(other) or
                                                   other.bbox_bottom - 1 < y):
                        stuck.append(other)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider, y=(self.y - 1)):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_bottom >= y and (not self.collision(other) or
                                                   other.bbox_bottom - 1 < y):
                        stuck.append(other)

        if self.sticky_bottom:
            if isinstance(self, SolidBottom):
                for other in self.collision(Collider, y=(self.y + 1)):
                    if not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider, y=(self.y + 1)):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_top <= y and (not self.collision(other) or
                                                other.bbox_top + 1 > y):
                        stuck.append(other)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider, y=(self.y + 1)):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_top <= y and (not self.collision(other) or
                                                other.bbox_top + 1 > y):
                        stuck.append(other)

        return stuck

    def move_x(self, move):
        """
        Move the wall horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`x`.
        """
        stuck = self.get_stuck_colliders()
        old_x = self.x
        self.x += move
        for other in stuck:
            other.move_y(move, True)

        if move > 0:
            if isinstance(self, SolidRight):
                for other in self.collision(Collider):
                    if not self.collision(other, x=old_x):
                        other.move_x(self.bbox_right - other.bbox_left, True)
                        self.event_physics_collision_right(other)
                        other.event_physics_collision_left(self)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            other.move_x(x - other.bbox_left, True)
                            y = self.get_slope_y(other.bbox_left)
                            other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_right(other)
                            other.event_physics_collision_left(self)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_right - other.bbox_left,
                                         True)
                            self.event_physics_collision_right(other)
                            other.event_physics_collision_left(self)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            other.move_x(x - other.bbox_left, True)
                            y = self.get_slope_y(other.bbox_left)
                            other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_right(other)
                            other.event_physics_collision_left(self)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_right - other.bbox_left,
                                         True)
                            self.event_physics_collision_right(other)
                            other.event_physics_collision_left(self)

        elif move < 0:
            if isinstance(self, SolidLeft):
                for other in self.collision(Collider):
                    if not self.collision(other, x=old_x):
                        other.move_x(self.bbox_left - other.bbox_right, True)
                        self.event_physics_collision_left(other)
                        other.event_physics_collision_right(self)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            other.move_x(x - other.bbox_right, True)
                            y = self.get_slope_y(other.bbox_right)
                            other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_left(other)
                            other.event_physics_collision_right(self)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_left - other.bbox_right,
                                         True)
                            self.event_physics_collision_left(other)
                            other.event_physics_collision_right(self)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            other.move_x(x - other.bbox_right, True)
                            y = self.get_slope_y(other.bbox_right)
                            other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_left(other)
                            other.event_physics_collision_right(self)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_left - other.bbox_right,
                                         True)
                            self.event_physics_collision_left(other)
                            other.event_physics_collision_right(self)

    def move_y(self, move):
        """
        Move the wall vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        """
        stuck = self.get_stuck_colliders()
        old_y = self.y
        self.y += move
        for other in stuck:
            other.move_y(move, True)

        if move > 0:
            if isinstance(self, SolidBottom):
                for other in self.collision(Collider):
                    if not self.collision(other, y=old_y):
                        other.move_y(self.bbox_bottom - other.bbox_top, True)
                        self.event_physics_collision_bottom(other)
                        other.event_physics_collision_top(self)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            other.move_y(y - other.bbox_top, True)
                            x = self.get_slope_x(other.bbox_top)
                            other.move_x(x - other.bbox_right, True)
                            self.event_physics_collision_bottom(other)
                            other.event_physics_collision_top(self)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_bottom - other.bbox_top,
                                         True)
                            self.event_physics_collision_bottom(other)
                            other.event_physics_collision_top(self)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            other.move_y(y - other.bbox_top, True)
                            x = self.get_slope_x(other.bbox_top)
                            other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_bottom(other)
                            other.event_physics_collision_top(self)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_bottom - other.bbox_top,
                                         True)
                            self.event_physics_collision_bottom(other)
                            other.event_physics_collision_top(self)

        elif move < 0:
            if isinstance(self, SolidTop):
                for other in self.collision(Collider):
                    if not self.collision(other, y=old_y):
                        other.move_y(self.bbox_top - other.bbox_bottom, True)
                        self.event_physics_collision_top(other)
                        other.event_physics_collision_bottom(self)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_bottom > y:
                        if other.bbox_bottom <= y - move:
                            other.move_y(y - other.bbox_bottom, True)
                            x = self.get_slope_x(other.bbox_bottom)
                            other.move_x(x - other.bbox_right, True)
                            self.event_physics_collision_top(other)
                            other.event_physics_collision_bottom(self)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_top - other.bbox_bottom,
                                         True)
                            self.event_physics_collision_top(other)
                            other.event_physics_collision_bottom(self)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_bottom > y:
                        if other.bbox_bottom <= y - move:
                            other.move_y(y - other.bbox_bottom, True)
                            x = self.get_slope_x(other.bbox_bottom)
                            other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_top(other)
                            other.event_physics_collision_bottom(self)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_top - other.bbox_bottom,
                                         True)
                            self.event_physics_collision_top(other)
                            other.event_physics_collision_bottom(self)

    def event_update_position(self, delta_mult):
        xdecel = (self.xdeceleration and self.xvelocity and
                  (self.xdeceleration < 0) != (self.xvelocity < 0))
        ydecel = (self.ydeceleration and self.yvelocity and
                  (self.ydeceleration < 0) != (self.yvelocity < 0))

        if (self.xacceleration + self.xdeceleration and
                (self.xacceleration or xdecel)):
            vi = self.xvelocity
            a = self.xacceleration * delta_mult
            self.xvelocity += a

            if xdecel:
                if abs(self.xvelocity) > abs(self.xdeceleration):
                    a += self.xdeceleration * delta_mult
                    self.xvelocity += self.xdeceleration * delta_mult
                else:
                    a -= self.xvelocity
                    self.xvelocity = 0

            d = ((self.xvelocity ** 2) - (vi ** 2)) / (2 * a)
            self.move_x(math.copysign(d, self.xvelocity))
        else:
            self.move_x(self.xvelocity * delta_mult)

        if (self.yacceleration + self.ydeceleration and
                (self.yacceleration or ydecel)):
            vi = self.yvelocity
            a = self.yacceleration * delta_mult
            self.yvelocity += a

            if ydecel:
                if abs(self.yvelocity) > abs(self.ydeceleration):
                    a += self.ydeceleration * delta_mult
                    self.yvelocity += self.ydeceleration * delta_mult
                else:
                    a -= self.yvelocity
                    self.yvelocity = 0

            d = ((self.yvelocity ** 2) - (vi ** 2)) / (2 * a)
            self.move_y(math.copysign(d, self.yvelocity))
        else:
            self.move_y(self.yvelocity * delta_mult)
