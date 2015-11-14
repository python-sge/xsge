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
xSGE is a collection of extensions for the SGE licensed under the GNU
General Public License.  They are designed to give additional features
to free/libre software games which aren't necessary, but are nice to
have.

xSGE extensions are not dependent on any particular SGE implementation.
They should work with any implementation that follows the specification.

This extension provides an easy-to-use framework for collision physics.
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

__version__ = "0.9.1a0"

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

    def _do_mxas(self, slope, move, xc, yc, slope_end_x, slope_end_y, absolute):
        # Return the point to arrive at on the slope with the given X
        # movement, and the movement remaining after doing this.
        x = slope.get_slope_x(yc)
        if round(x, NDIG) == round(xc, NDIG):
            if absolute:
                max_mv = slope_end_x - xc
            else:
                w_left = slope_end_x - xc
                h_left = slope_end_y - yc
                max_mv = math.copysign(math.hypot(w_left, h_left), w_left)

            if (max_mv < 0) == (move < 0):
                if abs(move) - abs(max_mv) > 1 / (10 ** NDIG):
                    mv = max_mv
                    move -= mv
                else:
                    mv = move if abs(move) < abs(max_mv) else max_mv
                    move = 0
            else:
                mv = 0

            if absolute:
                xc += mv
            else:
                h = math.hypot(slope.bbox_width, slope.bbox_height)
                xc += mv * slope.bbox_width / h

            yc = slope.get_slope_y(xc)
        else:
            mv = x - xc
            if (mv < 0) == (move < 0):
                if abs(mv) >= abs(move):
                    mv = move
                    move = 0
                else:
                    move -= mv
            else:
                mv = 0

            xc += mv

        return (move, xc, yc)

    def _do_myas(self, slope, move, xc, yc, slope_end_x, slope_end_y, absolute):
        # Return the point to arrive at on the slope with the given Y
        # movement, and the movement remaining after doing this.
        y = slope.get_slope_y(xc)
        if round(y, NDIG) == round(yc, NDIG):
            if absolute:
                max_mv = slope_end_y - yc
            else:
                w_left = slope_end_x - xc
                h_left = slope_end_y - yc
                max_mv = math.copysign(math.hypot(w_left, h_left), h_left)

            if (max_mv < 0) == (move < 0):
                if abs(move) - abs(max_mv) > 1 / (10 ** NDIG):
                    mv = max_mv
                    move -= mv
                else:
                    mv = move if abs(move) < abs(max_mv) else max_mv
                    move = 0
            else:
                mv = 0

            if absolute:
                yc += mv
            else:
                h = math.hypot(slope.bbox_width, slope.bbox_height)
                yc += mv * slope.bbox_height / h

            xc = slope.get_slope_x(yc)
        else:
            mv = y - yc
            if (mv < 0) == (move < 0):
                if abs(mv) >= abs(move):
                    mv = move
                    move = 0
                else:
                    move -= mv
            else:
                mv = 0

            yc += mv

        return (move, xc, yc)

    def _move_x_along_slope(self, slope, move, absolute):
        # Move along the given slope the given amount, if appropriate,
        # and return unused movement.
        if move > 0:
            if isinstance(slope, SlopeTopLeft):
                move, self.bbox_right, self.bbox_bottom = self._do_mxas(
                    slope, move, self.bbox_right, self.bbox_bottom,
                    slope.bbox_right, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeTopRight):
                if slope.xsticky_top:
                    move, self.bbox_left, self.bbox_bottom = self._do_mxas(
                        slope, move, self.bbox_left, self.bbox_bottom,
                        slope.bbox_right, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeBottomLeft):
                move, self.bbox_right, self.bbox_top = self._do_mxas(
                    slope, move, self.bbox_right, self.bbox_top,
                    slope.bbox_right, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeBottomRight):
                if slope.xsticky_bottom:
                    move, self.bbox_left, self.bbox_top = self._do_mxas(
                        slope, move, self.bbox_left, self.bbox_top,
                        slope.bbox_right, slope.bbox_top, absolute)
        elif move < 0:
            if isinstance(slope, SlopeTopLeft):
                if slope.xsticky_top:
                    move, self.bbox_right, self.bbox_bottom = self._do_mxas(
                        slope, move, self.bbox_right, self.bbox_bottom,
                        slope.bbox_left, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeTopRight):
                move, self.bbox_left, self.bbox_bottom = self._do_mxas(
                    slope, move, self.bbox_left, self.bbox_bottom,
                    slope.bbox_left, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeBottomLeft):
                if slope.xsticky_bottom:
                    move, self.bbox_right, self.bbox_top = self._do_mxas(
                        slope, move, self.bbox_right, self.bbox_top,
                        slope.bbox_left, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeBottomRight):
                move, self.bbox_left, self.bbox_top = self._do_mxas(
                    slope, move, self.bbox_left, self.bbox_top,
                    slope.bbox_left, slope.bbox_bottom, absolute)

        return move

    def _move_y_along_slope(self, slope, move, absolute):
        # Move along the given slope the given amount, if appropriate,
        # and return unused movement.
        if move > 0:
            if isinstance(slope, SlopeTopLeft):
                move, self.bbox_right, self.bbox_bottom = self._do_myas(
                    slope, move, self.bbox_right, self.bbox_bottom,
                    slope.bbox_left, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeTopRight):
                move, self.bbox_left, self.bbox_bottom = self._do_myas(
                    slope, move, self.bbox_left, self.bbox_bottom,
                    slope.bbox_right, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeBottomLeft):
                if slope.ysticky_left:
                    move, self.bbox_right, self.bbox_top = self._do_myas(
                        slope, move, self.bbox_right, self.bbox_top,
                        slope.bbox_right, slope.bbox_bottom, absolute)
            elif isinstance(slope, SlopeBottomRight):
                if slope.ysticky_right:
                    move, self.bbox_left, self.bbox_top = self._do_myas(
                        slope, move, self.bbox_left, self.bbox_top,
                        slope.bbox_left, slope.bbox_bottom, absolute)
        elif move < 0:
            if isinstance(slope, SlopeTopLeft):
                if slope.ysticky_left:
                    move, self.bbox_right, self.bbox_bottom = self._do_myas(
                        slope, move, self.bbox_right, self.bbox_bottom,
                        slope.bbox_right, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeTopRight):
                if slope.ysticky_right:
                    move, self.bbox_left, self.bbox_bottom = self._do_myas(
                        slope, move, self.bbox_left, self.bbox_bottom,
                        slope.bbox_left, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeBottomLeft):
                move, self.bbox_right, self.bbox_top = self._do_myas(
                    slope, move, self.bbox_right, self.bbox_top,
                    slope.bbox_left, slope.bbox_top, absolute)
            elif isinstance(slope, SlopeBottomRight):
                move, self.bbox_left, self.bbox_top = self._do_myas(
                    slope, move, self.bbox_left, self.bbox_top,
                    slope.bbox_right, slope.bbox_top, absolute)

        return move

    def _get_dslope_deepest(self, slope1, slope2):
        # Return the (x, y) coordinates to put the top-left of the
        # bounding box so that the object is as wedged between the two
        # slopes as possible.  If the slopes are parallel, this is
        # impossible, so return None instead.
        w = self.bbox_width
        h = self.bbox_height

        if ((isinstance(slope1, SlopeTopLeft) and
             isinstance(slope2, SlopeTopRight)) or
                (isinstance(slope1, SlopeBottomLeft) and
                 isinstance(slope2, SlopeBottomRight)) or
                (isinstance(slope1, SlopeTopRight) and
                 isinstance(slope2, SlopeTopLeft)) or
                (isinstance(slope1, SlopeBottomRight) and
                 isinstance(slope2, SlopeBottomLeft))):
            w = 0
        elif ((isinstance(slope1, SlopeTopLeft) and
               isinstance(slope2, SlopeBottomLeft)) or
              (isinstance(slope1, SlopeTopRight) and
               isinstance(slope2, SlopeBottomRight)) or
              (isinstance(slope1, SlopeBottomLeft) and
               isinstance(slope2, SlopeTopLeft)) or
              (isinstance(slope1, SlopeBottomRight) and
               isinstance(slope2, SlopeTopRight))):
            h = 0

        m1 = slope1.bbox_height / slope1.bbox_width
        m2 = slope2.bbox_height / slope2.bbox_width
        if isinstance(slope1, (SlopeTopLeft, SlopeBottomRight)):
            m1 *= -1
            b1 = slope1.bbox_top - m1 * slope1.bbox_right
        else:
            b1 = slope1.bbox_top - m1 * slope1.bbox_left
        if isinstance(slope2, (SlopeTopLeft, SlopeBottomRight)):
            m2 *= -1
            b2 = slope2.bbox_top - m2 * slope2.bbox_right - h
        else:
            b2 = slope2.bbox_top - m2 * slope2.bbox_left - h

        if m1 != m2:
            x = (b2 - b1) / (m1 - m2) - w
            y = slope1.get_slope_y(x)

            if isinstance(slope1, (SlopeTopLeft, SlopeBottomLeft)):
                x -= self.bbox_width
            if isinstance(slope1, (SlopeTopLeft, SlopeTopRight)):
                y -= self.bbox_height

            return (x, y)
        else:
            return None

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
        smv = move
        stopper = None

        while move:
            old_x = self.x
            old_y = self.y
            old_bbox_left = self.bbox_left
            old_bbox_right = self.bbox_right
            old_bbox_top = self.bbox_top
            old_bbox_bottom = self.bbox_bottom
            rold_bbox_left = round(old_bbox_left, NDIG)
            rold_bbox_right = round(old_bbox_right, NDIG)
            rold_bbox_top = round(old_bbox_top, NDIG)
            rold_bbox_bottom = round(old_bbox_bottom, NDIG)
            cmv = move

            for slope in (self.get_left_touching_slope() +
                          self.get_right_touching_slope() +
                          self.get_top_touching_slope() +
                          self.get_bottom_touching_slope()):
                mv = self._move_x_along_slope(slope, move, absolute)
                if mv != move:
                    current_slope = slope
                    move = mv
                    break
            else:
                current_slope = None
                self.x += move
                move = 0

            if smv > 0 and cmv > 0:
                for other in self.collision(SlopeTopLeft):
                    x = other.get_slope_x(self.bbox_bottom)
                    if self.collision(other) and self.bbox_right > x:
                        ox = round(other.get_slope_x(old_bbox_bottom), NDIG)
                        if rold_bbox_right <= ox:
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_right - x
                                self.bbox_right = x
                                stopper = other
                        elif not self.collision(other, x=old_x):
                            if current_slope is not None:
                                mv = other.bbox_left - self.bbox_right
                                self._move_x_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_right = other.bbox_left

                            move = 0
                            stopper = other

                for other in self.collision(SlopeBottomLeft):
                    x = other.get_slope_x(self.bbox_top)
                    if self.collision(other) and self.bbox_right > x:
                        ox = round(other.get_slope_x(old_bbox_top), NDIG)
                        if rold_bbox_right <= ox:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_right - x
                                self.bbox_right = x
                        elif not self.collision(other, x=old_x):
                            if current_slope is not None:
                                mv = other.bbox_left - self.bbox_right
                                self._move_x_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_right = other.bbox_left

                            move = 0
                            stopper = other

                for other in self.collision(SolidLeft):
                    if (self.collision(other) and
                            not self.collision(other, x=old_x)):
                        if current_slope is not None:
                            mv = other.bbox_left - self.bbox_right
                            self._move_x_along_slope(current_slope, mv, True)
                        else:
                            self.bbox_right = other.bbox_left

                        move = 0
                        stopper = other
            elif smv < 0 and cmv < 0:
                for other in self.collision(SlopeTopRight):
                    x = other.get_slope_x(self.bbox_bottom)
                    if self.collision(other) and self.bbox_left < x:
                        ox = round(other.get_slope_x(old_bbox_bottom), NDIG)
                        if rold_bbox_left >= ox:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_left - x
                                self.bbox_left = x
                        elif not self.collision(other, x=old_x):
                            if current_slope is not None:
                                mv = other.bbox_right - self.bbox_left
                                self._move_x_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_left = other.bbox_right

                            move = 0
                            stopper = other

                for other in self.collision(SlopeBottomRight):
                    x = other.get_slope_x(self.bbox_top)
                    if self.collision(other) and self.bbox_left < x:
                        ox = round(other.get_slope_x(old_bbox_top), NDIG)
                        if rold_bbox_left >= ox:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_left - x
                                self.bbox_left = x
                        elif not self.collision(other, x=old_x):
                            if current_slope is not None:
                                mv = other.bbox_right - self.bbox_left
                                self._move_x_along_slope(current_slope, mv,
                                                          True)
                            else:
                                self.bbox_left = other.bbox_right

                            move = 0
                            stopper = other

                for other in self.collision(SolidRight):
                    if (self.collision(other) and
                            not self.collision(other, x=old_x)):
                        if current_slope is not None:
                            mv = other.bbox_right - self.bbox_left
                            self._move_x_along_slope(current_slope, mv, True)
                        else:
                            self.bbox_left = other.bbox_right

                        move = 0
                        stopper = other

        if stopper is not None:
            move_loss = max(0, abs(smv) - abs(self.x - old_x))
            if smv > 0:
                self.event_physics_collision_right(stopper, move_loss)
                stopper.event_physics_collision_left(self, 0)
            elif smv < 0:
                self.event_physics_collision_left(stopper, move_loss)
                stopper.event_physics_collision_right(self, 0)

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
        smv = move
        stopper = None

        while move:
            old_x = self.x
            old_y = self.y
            old_bbox_left = self.bbox_left
            old_bbox_right = self.bbox_right
            old_bbox_top = self.bbox_top
            old_bbox_bottom = self.bbox_bottom
            rold_bbox_left = round(old_bbox_left, NDIG)
            rold_bbox_right = round(old_bbox_right, NDIG)
            rold_bbox_top = round(old_bbox_top, NDIG)
            rold_bbox_bottom = round(old_bbox_bottom, NDIG)
            cmv = move

            for slope in (self.get_left_touching_slope() +
                          self.get_right_touching_slope() +
                          self.get_top_touching_slope() +
                          self.get_bottom_touching_slope()):
                mv = self._move_y_along_slope(slope, move, absolute)
                if mv != move:
                    current_slope = slope
                    move = mv
                    break
            else:
                current_slope = None
                self.y += move
                move = 0

            if smv > 0 and cmv > 0:
                for other in self.collision(SlopeTopLeft):
                    y = other.get_slope_y(self.bbox_right)
                    if self.collision(other) and self.bbox_bottom > y:
                        oy = round(other.get_slope_y(old_bbox_right), NDIG)
                        if rold_bbox_bottom <= oy:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_bottom - y
                                self.bbox_bottom = y
                        elif not self.collision(other, y=old_y):
                            if current_slope is not None:
                                mv = other.bbox_top - self.bbox_bottom
                                self._move_y_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_bottom = other.bbox_top

                            move = 0
                            stopper = other

                for other in self.collision(SlopeTopRight):
                    y = other.get_slope_y(self.bbox_left)
                    if self.collision(other) and self.bbox_bottom > y:
                        oy = round(other.get_slope_y(old_bbox_left), NDIG)
                        if rold_bbox_bottom <= oy:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_bottom - y
                                self.bbox_bottom = y
                        elif not self.collision(other, y=old_y):
                            if current_slope is not None:
                                mv = other.bbox_top - self.bbox_bottom
                                self._move_y_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_bottom = other.bbox_top

                            move = 0
                            stopper = other

                for other in self.collision(SolidTop):
                    if (self.collision(other) and
                            not self.collision(other, y=old_y)):
                        if current_slope is not None:
                            mv = other.bbox_top - self.bbox_bottom
                            self._move_y_along_slope(current_slope, mv, True)
                        else:
                            self.bbox_bottom = other.bbox_top

                        move = 0
                        stopper = other
            elif smv < 0 and cmv < 0:
                for other in self.collision(SlopeBottomLeft):
                    y = other.get_slope_y(self.bbox_right)
                    if self.collision(other) and self.bbox_top < y:
                        oy = round(other.get_slope_y(old_bbox_right), NDIG)
                        if rold_bbox_top >= oy:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_top - y
                                self.bbox_top = y
                        elif not self.collision(other, y=old_y):
                            if current_slope is not None:
                                mv = other.bbox_bottom - self.bbox_top
                                self._move_y_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_top = other.bbox_bottom

                            move = 0
                            stopper = other

                for other in self.collision(SlopeBottomRight):
                    y = other.get_slope_y(self.bbox_left)
                    if self.collision(other) and self.bbox_top < y:
                        oy = round(other.get_slope_y(old_bbox_left), NDIG)
                        if rold_bbox_top >= oy:
                            stopper = other
                            if current_slope is not None:
                                r = self._get_dslope_deepest(current_slope,
                                                             other)
                                if r is not None:
                                    self.bbox_left, self.bbox_top = r
                            else:
                                move += self.bbox_top - y
                                self.bbox_top = y
                        elif not self.collision(other, y=old_y):
                            if current_slope is not None:
                                mv = other.bbox_bottom - self.bbox_top
                                self._move_y_along_slope(current_slope, mv,
                                                         True)
                            else:
                                self.bbox_top = other.bbox_bottom

                            move = 0
                            stopper = other

                for other in self.collision(SolidBottom):
                    if (self.collision(other) and
                            not self.collision(other, y=old_y)):
                        if current_slope is not None:
                            mv = other.bbox_bottom - self.bbox_top
                            self._move_y_along_slope(current_slope, mv, True)
                        else:
                            self.bbox_top = other.bbox_bottom

                        move = 0
                        stopper = other

        if stopper is not None:
            move_loss = max(0, abs(smv) - abs(self.y - old_y))
            if smv > 0:
                self.event_physics_collision_bottom(stopper, move_loss)
                stopper.event_physics_collision_top(self, 0)
            elif smv < 0:
                self.event_physics_collision_top(stopper, move_loss)
                stopper.event_physics_collision_bottom(self, 0)

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
                            not self.collision(slope)):
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

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.

        Arguments:

        - ``move_loss`` -- The amount of movement that was prevented by
          the collision in pixels.  For example, if the object would
          have moved 6 pixels, but only moved 2 pixels as a result of
          this collision, this value will be ``4``.  This can be used to
          undo such a reduction in movement.

        See the documentation for :meth:`sge.Object.event_collision` for
        more information.
        """
        pass

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`xsge_physics.Collider.event_physics_collision_left` for
        more information.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
        """
        Called when the top side of the collider collides with a wall or
        slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`xsge_physics.Collider.event_physics_collision_left` for
        more information.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
        """
        Called when the bottom side of the collider collides with a wall
        or slope in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`xsge_physics.Collider.event_physics_collision_left` for
        more information.
        """
        pass


class SolidLeft(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """

    def event_physics_collision_left(self, other, move_loss):
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

    def event_physics_collision_right(self, other, move_loss):
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

    def event_physics_collision_top(self, other, move_loss):
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

    def event_physics_collision_bottom(self, other, move_loss):
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

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
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
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_left

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_top

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
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
        Get the corresponding x coordinate of a given y coordinate for
        the slope.
        """
        # x = (y - b) / m [b is 0]
        m = self.bbox_height / self.bbox_width
        y -= self.bbox_top
        return y / m + self.bbox_left

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        return m * x + self.bbox_top

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
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

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
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
            other.move_x(move, True)

        if move > 0:
            if isinstance(self, SolidRight):
                for other in self.collision(Collider):
                    if not self.collision(other, x=old_x):
                        other.move_x(self.bbox_right - other.bbox_left, True)
                        self.event_physics_collision_right(other, 0)
                        other.event_physics_collision_left(self, 0)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            other.move_x(x - other.bbox_left, True)
                            y = self.get_slope_y(other.bbox_left)
                            other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_right - other.bbox_left,
                                         True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            other.move_x(x - other.bbox_left, True)
                            y = self.get_slope_y(other.bbox_left)
                            other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_right - other.bbox_left,
                                         True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)

        elif move < 0:
            if isinstance(self, SolidLeft):
                for other in self.collision(Collider):
                    if not self.collision(other, x=old_x):
                        other.move_x(self.bbox_left - other.bbox_right, True)
                        self.event_physics_collision_left(other, 0)
                        other.event_physics_collision_right(self, 0)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            other.move_x(x - other.bbox_right, True)
                            y = self.get_slope_y(other.bbox_right)
                            other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_left - other.bbox_right,
                                         True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            other.move_x(x - other.bbox_right, True)
                            y = self.get_slope_y(other.bbox_right)
                            other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
                        elif not self.collision(other, x=old_x):
                            other.move_x(self.bbox_left - other.bbox_right,
                                         True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)

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
                        self.event_physics_collision_bottom(other, 0)
                        other.event_physics_collision_top(self, 0)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            other.move_y(y - other.bbox_top, True)
                            x = self.get_slope_x(other.bbox_top)
                            other.move_x(x - other.bbox_right, True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_bottom - other.bbox_top,
                                         True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            other.move_y(y - other.bbox_top, True)
                            x = self.get_slope_x(other.bbox_top)
                            other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_bottom - other.bbox_top,
                                         True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)

        elif move < 0:
            if isinstance(self, SolidTop):
                for other in self.collision(Collider):
                    if not self.collision(other, y=old_y):
                        other.move_y(self.bbox_top - other.bbox_bottom, True)
                        self.event_physics_collision_top(other, 0)
                        other.event_physics_collision_bottom(self, 0)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_bottom > y:
                        if other.bbox_bottom <= y - move:
                            other.move_y(y - other.bbox_bottom, True)
                            x = self.get_slope_x(other.bbox_bottom)
                            other.move_x(x - other.bbox_right, True)
                            self.event_physics_collision_top(other, 0)
                            other.event_physics_collision_bottom(self, 0)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_top - other.bbox_bottom,
                                         True)
                            self.event_physics_collision_top(other, 0)
                            other.event_physics_collision_bottom(self, 0)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_bottom > y:
                        if other.bbox_bottom <= y - move:
                            other.move_y(y - other.bbox_bottom, True)
                            x = self.get_slope_x(other.bbox_bottom)
                            other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_top(other, 0)
                            other.event_physics_collision_bottom(self, 0)
                        elif not self.collision(other, y=old_y):
                            other.move_y(self.bbox_top - other.bbox_bottom,
                                         True)
                            self.event_physics_collision_top(other, 0)
                            other.event_physics_collision_bottom(self, 0)


class MobileColliderWall(MobileWall, Collider):

    """
    A parent class for mobile walls that are also colliders.  See the
    documentation for :class:`xsge_physics.Collider` and
    :class:`xsge_physics.MobileWall` for more information.

    .. note::

       Due to the way movement is implemented in this class, it is not
       safe to move this object during its collision events.  Doing so
       may cause colliders that should be stuck to this object to become
       un-stuck, or cause this object to pass through colliders it
       should be pushing.
    """

    def move_x(self, move, absolute=False):
        """
        Move the wall horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        """
        xprev = self.x
        Collider.move_x(self, move, absolute)
        real_move = self.x - xprev
        self.x = xprev
        MobileWall.move_x(self, real_move)

    def move_y(self, move, absolute=False):
        """
        Move the wall vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        """
        yprev = self.y
        Collider.move_y(self, move, absolute)
        real_move = self.y - yprev
        self.y = yprev
        MobileWall.move_y(self, real_move)

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the wall collides with a collider,
        wall, or slope in the sense of the physics system, rather than
        in the sense of SGE collision detection.  See the documentation
        for :meth:`xsge_physics.Collider.event_physics_collision_left`
        for more information.

        .. note::

           Due to the way movement is implemented in this class, it is
           not safe to move this object during this event.  Doing so may
           cause colliders that should be stuck to this object to become
           un-stuck, or cause this object to pass through colliders it
           should be pushing.
        """
        pass

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the wall collides with a collider,
        wall, or slope in the sense of the physics system, rather than
        in the sense of SGE collision detection.  See the documentation
        for :meth:`xsge_physics.Collider.event_physics_collision_left`
        for more information.

        .. note::

           Due to the way movement is implemented in this class, it is
           not safe to move this object during this event.  Doing so may
           cause colliders that should be stuck to this object to become
           un-stuck, or cause this object to pass through colliders it
           should be pushing.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
        """
        Called when the top side of the wall collides with a collider,
        wall, or slope in the sense of the physics system, rather than
        in the sense of SGE collision detection.  See the documentation
        for :meth:`xsge_physics.Collider.event_physics_collision_left`
        for more information.

        .. note::

           Due to the way movement is implemented in this class, it is
           not safe to move this object during this event.  Doing so may
           cause colliders that should be stuck to this object to become
           un-stuck, or cause this object to pass through colliders it
           should be pushing.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
        """
        Called when the bottom side of the wall collides with a
        collider, wall, or slope in the sense of the physics system,
        rather than in the sense of SGE collision detection.  See the
        documentation for
        :meth:`xsge_physics.Collider.event_physics_collision_left` for
        more information.

        .. note::

           Due to the way movement is implemented in this class, it is
           not safe to move this object during this event.  Doing so may
           cause colliders that should be stuck to this object to become
           un-stuck, or cause this object to pass through colliders it
           should be pushing.
        """
        pass
