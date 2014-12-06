# xSGE Physics Framework
# Copyright (C) 2014 Julian Marchant <onpon4@riseup.net>
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
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge


__all__ = ["Collider", "SolidLeft", "SolidRight", "SolidTop", "SolidBottom",
           "Solid", "SlopeTopLeft", "SlopeTopRight", "SlopeBottomLeft",
           "SlopeBottomRight"]


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

    def move_x(self, move):
        """Move the object horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`x`.

        """
        sticky = False
        old_x = self.x
        old_y = self.y
        old_bbox_left = self.bbox_left
        old_bbox_right = self.bbox_right
        old_bbox_top = self.bbox_top
        old_bbox_bottom = self.bbox_bottom
        self.x += move

        if move > 0:
            for slope in self.collision(SlopeTopRight, x=(old_x - 1)):
                y = slope.get_slope_y(old_bbox_left)
                if (slope.xsticky and old_bbox_bottom >= y and
                        (not self.collision(slope, x=old_x) or
                         old_bbox_bottom - 1 < y)):
                    sticky = 1
                    break
            else:
                for slope in self.collision(SlopeBottomRight, x=(old_x - 1)):
                    y = slope.get_slope_y(old_bbox_left)
                    if (slope.xsticky and old_bbox_top <= y and
                            (not self.collision(slope, x=old_x) or
                             old_bbox_top + 1 > y)):
                        sticky = 2
                        break

            for other in self.collision(SolidLeft):
                if not self.collision(other, x=old_x):
                    self.bbox_right = min(self.bbox_right, other.bbox_left)
                    self.event_collision_right(other)
                    other.event_collision_left(self)

            for other in self.collision(SlopeTopLeft):
                oy = other.get_slope_y(old_bbox_right)
                y = other.get_slope_y(self.bbox_right)
                if self.bbox_bottom > y:
                    if old_bbox_bottom <= oy:
                        self.move_y(y - self.bbox_bottom)
                        x = other.get_slope_x(self.bbox_bottom)
                        self.bbox_right = min(self.bbox_right, x)
                        self.event_collision_right(other)
                        other.event_collision_left(self)
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        self.event_collision_right(other)
                        other.event_collision_left(self)

            for other in self.collision(SlopeBottomLeft):
                oy = other.get_slope_y(old_bbox_right)
                y = other.get_slope_y(self.bbox_right)
                if self.bbox_top < y:
                    if old_bbox_top >= oy:
                        self.move_y(y - self.bbox_top)
                        x = other.get_slope_x(self.bbox_top)
                        self.bbox_right = min(self.bbox_right, x)
                        self.event_collision_right(other)
                        other.event_collision_left(self)
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        self.event_collision_right(other)
                        other.event_collision_left(self)
                
        elif move < 0:
            for slope in self.collision(SlopeTopLeft, x=(old_x + 1)):
                y = slope.get_slope_y(old_bbox_right)
                if (slope.xsticky and old_bbox_bottom >= y and
                        (not self.collision(slope, x=old_x) or
                         old_bbox_bottom - 1 < y)):
                    sticky = 1
                    break
            else:
                for slope in self.collision(SlopeBottomLeft, x=(old_x + 1)):
                    y = slope.get_slope_y(old_bbox_right)
                    if (slope.xsticky and old_bbox_top <= y and
                            (not self.collision(slope, x=old_x) or
                             old_bbox_top + 1 > y)):
                        sticky = 2
                        break

            for other in self.collision(SolidRight):
                if not self.collision(other, x=old_x):
                    self.bbox_left = max(self.bbox_left, other.bbox_right)
                    self.event_collision_left(other)
                    other.event_collision_right(self)

            for other in self.collision(SlopeTopRight):
                oy = other.get_slope_y(old_bbox_left)
                y = other.get_slope_y(self.bbox_left)
                if self.bbox_bottom > y:
                    if old_bbox_bottom <= oy:
                        self.move_y(y - self.bbox_bottom)
                        x = other.get_slope_x(self.bbox_bottom)
                        self.bbox_right = max(self.bbox_right, x)
                        self.event_collision_left(other)
                        other.event_collision_right(self)
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        self.event_collision_left(other)
                        other.event_collision_right(self)

            for other in self.collision(SlopeBottomRight):
                oy = other.get_slope_y(old_bbox_left)
                y = other.get_slope_y(self.bbox_left)
                if self.bbox_top < y:
                    if old_bbox_top >= oy:
                        self.move_y(y - self.bbox_top)
                        x = other.get_slope_x(self.bbox_top)
                        self.bbox_left = max(self.bbox_left, x)
                        self.event_collision_left(other)
                        other.event_collision_right(self)
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        self.event_collision_left(other)
                        other.event_collision_right(self)

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

    def move_y(self, move):
        """Move the object vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.

        """
        sticky = False
        old_x = self.x
        old_y = self.y
        old_bbox_left = self.bbox_left
        old_bbox_right = self.bbox_right
        old_bbox_top = self.bbox_top
        old_bbox_bottom = self.bbox_bottom
        self.y += move

        if move > 0:
            for slope in self.collision(SlopeBottomLeft, y=(old_y - 1)):
                x = slope.get_slope_x(old_bbox_top)
                if (slope.ysticky and old_bbox_right >= x and
                        (not self.collision(slope, y=old_y) or
                         old_bbox_right - 1 < x)):
                    sticky = 1
                    break
            else:
                for slope in self.collision(SlopeBottomRight, y=(old_y - 1)):
                    x = slope.get_slope_x(old_bbox_top)
                    if (slope.ysticky and old_bbox_left <= x and
                            (not self.collision(slope, y=old_y) or
                             old_bbox_left + 1 > x)):
                        sticky = 2
                        break

            for other in self.collision(SolidTop):
                if not self.collision(other, y=old_y):
                    self.bbox_bottom = min(self.bbox_bottom, other.bbox_top)
                    self.event_collision_bottom(other)
                    other.event_collision_top(self)

            for other in self.collision(SlopeTopLeft):
                ox = other.get_slope_x(old_bbox_bottom)
                x = other.get_slope_x(self.bbox_bottom)
                if self.bbox_right > x:
                    if old_bbox_right <= ox:
                        self.move_x(x - self.bbox_right)
                        y = other.get_slope_y(self.bbox_right)
                        self.bbox_bottom = min(self.bbox_bottom, y)
                        self.event_collision_bottom(other)
                        other.event_collision_top(self)
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        self.event_collision_bottom(other)
                        other.event_collision_top(self)

            for other in self.collision(SlopeTopRight):
                ox = other.get_slope_x(old_bbox_bottom)
                x = other.get_slope_x(self.bbox_bottom)
                if self.bbox_left < x:
                    if old_bbox_left >= ox:
                        self.move_x(x - self.bbox_left)
                        y = other.get_slope_y(self.bbox_left)
                        self.bbox_bottom = min(self.bbox_bottom, y)
                        self.event_collision_bottom(other)
                        other.event_collision_top(self)
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        self.event_collision_bottom(other)
                        other.event_collision_top(self)
                
        elif move < 0:
            for slope in self.collision(SlopeTopLeft, y=(old_y + 1)):
                x = slope.get_slope_x(old_bbox_bottom)
                if (slope.ysticky and old_bbox_right >= x and
                        (not self.collision(slope, y=old_y) or
                         old_bbox_right - 1 < x)):
                    sticky = 1
                    break
            else:
                for slope in self.collision(SlopeTopRight, y=(old_y + 1)):
                    x = slope.get_slope_x(old_bbox_bottom)
                    if (slope.ysticky and old_bbox_left <= x and
                            (not self.collision(slope, y=old_y) or
                             old_bbox_left + 1 > x)):
                        sticky = 2
                        break

            for other in self.collision(SolidBottom):
                if not self.collision(other, y=old_y):
                    self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                    self.event_collision_top(other)
                    other.event_collision_bottom(self)

            for other in self.collision(SlopeBottomLeft):
                ox = other.get_slope_x(old_bbox_top)
                x = other.get_slope_x(self.bbox_top)
                if self.bbox_right > x:
                    if old_bbox_right <= ox:
                        self.move_x(x - self.bbox_right)
                        y = other.get_slope_y(self.bbox_right)
                        self.bbox_top = max(self.bbox_top, y)
                        self.event_collision_top(other)
                        other.event_collision_bottom(self)
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        self.event_collision_top(other)
                        other.event_collision_bottom(self)

            for other in self.collision(SlopeBottomRight):
                ox = other.get_slope_x(old_bbox_top)
                x = other.get_slope_x(self.bbox_top)
                if self.bbox_left < x:
                    if old_bbox_left >= ox:
                        self.move_x(x - self.bbox_left)
                        y = other.get_slope_y(self.bbox_left)
                        self.bbox_top = max(self.bbox_top, y)
                        self.event_collision_top(other)
                        other.event_collision_bottom(self)
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        self.event_collision_top(other)
                        other.event_collision_bottom(self)

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
        Return whether the left side of this object is touching the
        right side of a :class:`SolidRight` object.
        """
        for tile in self.collision(SolidRight, x=(self.x - 1)):
            if not self.collision(tile):
                return True

        return False

    def get_right_touching_wall(self):
        """
        Return whether the right side of this object is touching the
        right side of a :class:`SolidLeft` object.
        """
        for tile in self.collision(SolidLeft, x=(self.x + 1)):
            if not self.collision(tile):
                return True

        return False

    def get_top_touching_wall(self):
        """
        Return whether the top side of this object is touching the
        bottom side of a :class:`SolidBottom` object.
        """
        for tile in self.collision(SolidBottom, y=(self.y - 1)):
            if not self.collision(tile):
                return True

        return False

    def get_bottom_touching_wall(self):
        """
        Return whether the bottom side of this object is touching the
        top side of a :class:`SolidTop` object.
        """
        for tile in self.collision(SolidTop, y=(self.y + 1)):
            if not self.collision(tile):
                return True

        return False

    def get_left_touching_slope(self):
        """
        Return whether the left side of this object is touching the
        right side of a :class:`SlopeTopRight` or
        :class:`SlopeBottomRight` object.
        """
        for slope in self.collision(SlopeTopRight, x=(self.x - 1)):
            y = slope.get_slope_y(self.bbox_left)
            if self.bbox_bottom >= y and (not self.collision(slope) or
                                          self.bbox_bottom - 1 < y):
                return True
        else:
            for slope in self.collision(SlopeBottomRight, x=(self.x - 1)):
                y = slope.get_slope_y(self.bbox_left)
                if self.bbox_top <= y and (not self.collision(slope) or
                                           self.bbox_top + 1 > y):
                    return True

        return False

    def get_right_touching_slope(self):
        """
        Return whether the right side of this object is touching the
        left side of a :class:`SlopeTopLeft` or :class:`SlopeBottomLeft`
        object.
        """
        for slope in self.collision(SlopeTopLeft, x=(self.x + 1)):
            y = slope.get_slope_y(self.bbox_right)
            if self.bbox_bottom >= y and (not self.collision(slope) or
                                          self.bbox_bottom - 1 < y):
                return True
        else:
            for slope in self.collision(SlopeBottomLeft, x=(self.x + 1)):
                y = slope.get_slope_y(self.bbox_right)
                if self.bbox_top <= y and (not self.collision(slope) or
                                           self.bbox_top + 1 > y):
                    return True

        return False

    def get_top_touching_slope(self):
        """
        Return whether the top side of this object is touching the
        bottom side of a :class:`SlopeBottomLeft` or
        :class:`SlopeBottomRight` object.
        """
        for slope in self.collision(SlopeBottomLeft, y=(self.y - 1)):
            x = slope.get_slope_x(self.bbox_top)
            if self.bbox_right >= x and (not self.collision(slope) or
                                         self.bbox_right - 1 < x):
                return True
        else:
            for slope in self.collision(SlopeBottomRight, y=(self.y - 1)):
                x = slope.get_slope_x(self.bbox_top)
                if self.bbox_left <= x and (not self.collision(slope) or
                                            self.bbox_left + 1 > x):
                    return True

        return False

    def get_bottom_touching_slope(self):
        """
        Return whether the bottom side of this object is touching the
        top side of a :class:`SlopeTopLeft` or :class:`SlopeTopRight`
        object.
        """
        for slope in self.collision(SlopeTopLeft, y=(self.y + 1)):
            x = slope.get_slope_x(self.bbox_bottom)
            if self.bbox_right >= x and (not self.collision(slope) or
                                         self.bbox_right - 1 < x):
                return True
        else:
            for slope in self.collision(SlopeTopRight, y=(self.y + 1)):
                x = slope.get_slope_x(self.bbox_bottom)
                if self.bbox_left <= x and (not self.collision(slope) or
                                            self.bbox_left + 1 > x):
                    return True

        return False

    def event_update_position(self, delta_mult):
        xmove = self.xvelocity * delta_mult
        ymove = self.yvelocity * delta_mult
        self.move_x(xmove)
        self.move_y(ymove)


class SolidLeft(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """


class SolidRight(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the right.
    """


class SolidTop(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """


class SolidBottom(sge.Object):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the bottom.
    """


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

    .. attribute:: xsticky

       If set to :const:`True`, a collider that moves to the left while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward.

    .. attribute:: ysticky

       If set to :const:`True`, a collider that moves upward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right.
    """

    xsticky = False
    ysticky = False

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


class SlopeTopRight(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky

       If set to :const:`True`, a collider that moves to the right while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward.

    .. attribute:: ysticky

       If set to :const:`True`, a collider that moves upward while
       touching the right side of the slope will attempt to keep
       touching the right side of the slope by moving to the left.
    """

    xsticky = False
    ysticky = False

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


class SlopeBottomLeft(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the left.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky

       If set to :const:`True`, a collider that moves to the left while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward.

    .. attribute:: ysticky

       If set to :const:`True`, a collider that moves downward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right.
    """

    xsticky = False
    ysticky = False

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


class SlopeBottomRight(sge.Object):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the bottom-left corner to the top-right
    corner of the bounding box.

    .. attribute:: xsticky

       If set to :const:`True`, a collider that moves to the right while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward.

    .. attribute:: ysticky

       If set to :const:`True`, a collider that moves downward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right.
    """

    xsticky = False
    ysticky = False

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
