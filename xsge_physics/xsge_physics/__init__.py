# xSGE Physics Framework
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


__version__ = "0.13.2"
__all__ = ["Collider", "Wall", "SolidLeft", "SolidRight", "SolidTop",
           "SolidBottom", "Solid", "SlopeTopLeft", "SlopeTopRight",
           "SlopeBottomLeft", "SlopeBottomRight", "MobileWall"]


import math

import sge


NDIG = 6


class Collider(sge.dsp.Object):

    """
    Class for objects which have physics interactions.

    .. note::

       This class depends on use of :meth:`Collider.move_x` and
       :meth:`Collider.move_y` to handle physics interactions.
       :meth:`event_update_position` uses these methods, so speed
       attributes will work properly, but changing :attr:`x` and
       :attr:`y` manually will not cause any physics to occur.

    .. attribute:: nonstick_left
    .. attribute:: nonstick_right
    .. attribute:: nonstick_top
    .. attribute:: nonstick_bottom

       These attributes are used by certain wall classes to exclude the
       object from "sticking" to the wall.  See the documentation for
       the wall classes for more information.

       Default value: :const:`False`

    .. attribute:: slope_acceleration

       The factor by which the collider accelerates on slopes.  This is
       multiplied by the :attr:`slope_xacceleration` and
       :attr:`slope_yacceleration` values of any slopes the collider is
       touching and added to the use of :attr:`xacceleration` and
       :attr:`yacceleration` by :meth:`event_update_position`.

       Default value: ``0``
    """

    nonstick_left = False
    nonstick_right = False
    nonstick_top = False
    nonstick_bottom = False
    slope_acceleration = 0

    def move_x(self, move, absolute=False, do_events=True, exclude_events=()):
        """
        Move the object horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`x`.
        - ``absolute`` -- If set to :const:`True`, the distance moved
          horizontally is absolute, i.e. will not be reduced as a result
          of vertical movement caused by slopes.  Otherwise, any
          vertical movement caused by slopes will result in a reduction
          of horizontal movement.
        - ``do_events`` -- Whether or not physics collision events
          should be executed when appropriate.
        - ``exclude_events`` -- A set, list, or tuple of wall objects
          which should not cause collision events to be executed if
          collided with.
        """
        exclude_events = set(exclude_events)
        exclude_events.add(None)
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
        on_floor = None
        on_ceil = None

        def get_on_floor(on_floor, self=self, old_x=old_x, old_y=old_y):
            if on_floor is not None:
                return on_floor
            else:
                new_x = self.x
                new_y = self.y
                self.x = old_x
                self.y = old_y
                on_floor = (self.get_bottom_touching_wall() or
                            self.get_bottom_touching_slope())
                self.x = new_x
                self.y = new_y
                return on_floor

        def get_on_ceil(on_ceil, self=self, old_x=old_x, old_y=old_y):
            if on_ceil is not None:
                return on_ceil
            else:
                new_x = self.x
                new_y = self.y
                self.x = old_x
                self.y = old_y
                on_ceil = (self.get_top_touching_wall() or
                           self.get_top_touching_slope())
                self.x = new_x
                self.y = new_y
                return on_ceil

        if move > 0:
            if not self.nonstick_bottom:
                bbb = round(self.bbox_bottom, NDIG)
                for slope in self.collision(SlopeTopRight, y=(self.y + 1)):
                    if slope.xsticky_top:
                        y = round(slope.get_slope_y(self.bbox_left), NDIG)
                        if bbb == y:
                            sticky = 1
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_width / h
                            break
                        elif (self.bbox_left <= slope.bbox_left and
                              not self.collision(slope)):
                            sticky = 1
                            break
            if not sticky and not self.nonstick_top:
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

            slopes = self.collision(SlopeTopLeft)
            def key(s, self=self): return s.get_slope_x(self.bbox_bottom)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_y(y - self.bbox_bottom, do_events=do_events,
                                    exclude_events=exclude_events)
                        x = other.get_slope_x(self.bbox_bottom)
                        diff = self.bbox_right - x
                        if diff > 0:
                            self.bbox_right = x
                            if self.bbox_bottom == y:
                                self.move_x(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_floor = get_on_floor(on_floor)
                        if on_floor:
                            stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        stopper = other

            slopes = self.collision(SlopeBottomLeft)
            def key(s, self=self): return s.get_slope_x(self.bbox_top)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_y(y - self.bbox_top, do_events=do_events,
                                    exclude_events=exclude_events)
                        x = other.get_slope_x(self.bbox_top)
                        diff = self.bbox_right - x
                        if diff > 0:
                            self.bbox_right = x
                            if self.bbox_top == y:
                                self.move_x(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_ceil = get_on_ceil(on_ceil)
                        if on_ceil:
                            stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_right = min(self.bbox_right, other.bbox_left)
                        stopper = other

            for other in self.collision(SolidLeft):
                if not self.collision(other, x=old_x):
                    self.bbox_right = min(self.bbox_right, other.bbox_left)
                    stopper = other

            if do_events and stopper not in exclude_events:
                move_loss = max(0, abs(move) - abs(self.x - old_x))
                self.event_physics_collision_right(stopper, move_loss)
                stopper.event_physics_collision_left(self, 0)
                
        elif move < 0:
            if not self.nonstick_bottom:
                bbb = round(self.bbox_bottom, NDIG)
                for slope in self.collision(SlopeTopLeft, y=(self.y + 1)):
                    if slope.xsticky_top:
                        y = round(slope.get_slope_y(self.bbox_right), NDIG)
                        if bbb == y:
                            sticky = 1
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_width / h
                            break
                        elif (self.bbox_right >= slope.bbox_right and
                              not self.collision(slope)):
                            sticky = 1
                            break
            if not sticky and not self.nonstick_top:
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

            slopes = self.collision(SlopeTopRight)
            def key(s, self=self): return -s.get_slope_x(self.bbox_bottom)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_y(y - self.bbox_bottom, do_events=do_events,
                                    exclude_events=exclude_events)
                        x = other.get_slope_x(self.bbox_bottom)
                        diff = self.bbox_left - x
                        if diff < 0:
                            self.bbox_left = x
                            if self.bbox_bottom == y:
                                self.move_x(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_floor = get_on_floor(on_floor)
                        if on_floor:
                            stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        stopper = other

            slopes = self.collision(SlopeBottomRight)
            def key(s, self=self): return -s.get_slope_x(self.bbox_top)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_y(y - self.bbox_top, do_events=do_events,
                                    exclude_events=exclude_events)
                        x = other.get_slope_x(self.bbox_top)
                        diff = self.bbox_left - x
                        if diff < 0:
                            self.bbox_left = x
                            if self.bbox_top == y:
                                self.move_x(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_ceil = get_on_ceil(on_ceil)
                        if on_ceil:
                            stopper = other
                    elif not self.collision(other, x=old_x):
                        self.bbox_left = max(self.bbox_left, other.bbox_right)
                        stopper = other

            for other in self.collision(SolidRight):
                if not self.collision(other, x=old_x):
                    self.bbox_left = max(self.bbox_left, other.bbox_right)
                    stopper = other

            if do_events and stopper not in exclude_events:
                move_loss = max(0, abs(move) - abs(self.x - old_x))
                self.event_physics_collision_left(stopper, move_loss)
                stopper.event_physics_collision_right(self, 0)

        # Engage stickiness (same whether moving left or right)
        # 1 = sticking to the floor
        # 2 = sticking to the ceiling
        if sticky == 1:
            if (not self.get_bottom_touching_slope() and
                    not self.get_bottom_touching_wall()):
                new_bbox_bottom = None
                others = (
                    sge.game.current_room.get_objects_at(
                        self.bbox_left, self.bbox_top, self.bbox_width,
                        (sge.game.current_room.height - self.bbox_top +
                         sge.game.current_room.object_area_height)) |
                    sge.game.current_room.object_area_void)
                for other in others:
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
                others = (
                    sge.game.current_room.get_objects_at(
                        self.bbox_left, 0, self.bbox_width, self.bbox_bottom) |
                    sge.game.current_room.object_area_void)
                for other in others:
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

    def move_y(self, move, absolute=False, do_events=True, exclude_events=()):
        """
        Move the object vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        - ``absolute`` -- If set to :const:`True`, the distance moved
          vertically is absolute, i.e. will not be reduced as a result
          of horizontal movement caused by slopes.  Otherwise, any
          horizontal movement caused by slopes will result in a
          reduction of vertical movement.
        - ``do_events`` -- Whether or not physics collision events
          should be executed when appropriate.
        - ``exclude_events`` -- A set, list, or tuple of wall objects
          which should not cause collision events to be executed if
          collided with.
        """
        exclude_events = set(exclude_events)
        exclude_events.add(None)
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
        on_right = None
        on_left = None

        def get_on_right(on_right, self=self, old_x=old_x, old_y=old_y):
            if on_right is not None:
                return on_right
            else:
                new_x = self.x
                new_y = self.y
                self.x = old_x
                self.y = old_y
                on_right = (self.get_right_touching_wall() or
                            self.get_right_touching_slope())
                self.x = new_x
                self.y = new_y
                return on_right

        def get_on_left(on_left, self=self, old_x=old_x, old_y=old_y):
            if on_left is not None:
                return on_left
            else:
                new_x = self.x
                new_y = self.y
                self.x = old_x
                self.y = old_y
                on_left = (self.get_left_touching_wall() or
                           self.get_left_touching_slope())
                self.x = new_x
                self.y = new_y
                return on_left

        if move > 0:
            if not self.nonstick_right:
                bbr = round(self.bbox_right, NDIG)
                for slope in self.collision(SlopeBottomLeft, x=(self.x + 1)):
                    if slope.ysticky_left:
                        x = round(slope.get_slope_x(self.bbox_top), NDIG)
                        if bbr == x:
                            sticky = 1
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_height / h
                            break
                        elif (self.bbox_top <= slope.bbox_top and
                              not self.collision(slope)):
                            sticky = 1
                            break
            if not sticky and not self.nonstick_left:
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

            slopes = self.collision(SlopeTopLeft)
            def key(s, self=self): return s.get_slope_y(self.bbox_right)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_x(x - self.bbox_right, do_events=do_events,
                                    exclude_events=exclude_events)
                        y = other.get_slope_y(self.bbox_right)
                        diff = self.bbox_bottom - y
                        if diff > 0:
                            self.bbox_bottom = y
                            if self.bbox_right == x:
                                self.move_y(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_right = get_on_right(on_right)
                        if on_right:
                            stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        stopper = other

            slopes = self.collision(SlopeTopRight)
            def key(s, self=self): return s.get_slope_y(self.bbox_left)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_x(x - self.bbox_left, do_events=do_events,
                                    exclude_events=exclude_events)
                        y = other.get_slope_y(self.bbox_left)
                        diff = self.bbox_bottom - y
                        if diff > 0:
                            self.bbox_bottom = y
                            if self.bbox_left == x:
                                self.move_y(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_left = get_on_left(on_left)
                        if on_left:
                            stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_bottom = min(self.bbox_bottom,
                                               other.bbox_top)
                        stopper = other

            for other in self.collision(SolidTop):
                if not self.collision(other, y=old_y):
                    self.bbox_bottom = min(self.bbox_bottom, other.bbox_top)
                    stopper = other

            if do_events and stopper not in exclude_events:
                move_loss = max(0, abs(move) - abs(self.y - old_y))
                self.event_physics_collision_bottom(stopper, move_loss)
                stopper.event_physics_collision_top(self, 0)
                
        elif move < 0:
            if not self.nonstick_right:
                bbr = round(self.bbox_right, NDIG)
                for slope in self.collision(SlopeTopLeft, x=(self.x + 1)):
                    if slope.ysticky_left:
                        x = round(slope.get_slope_x(self.bbox_bottom), NDIG)
                        if bbr == x:
                            sticky = 1
                            if not absolute:
                                h = math.hypot(slope.bbox_width,
                                               slope.bbox_height)
                                move_mult = slope.bbox_height / h
                            break
                        elif (self.bbox_bottom >= slope.bbox_bottom and
                              not self.collision(slope)):
                            sticky = 1
                            break
            if not sticky and not self.nonstick_left:
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

            slopes = self.collision(SlopeBottomLeft)
            def key(s, self=self): return -s.get_slope_y(self.bbox_right)
            slopes.sort(key=key)
            for other in slopes:
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
                        self.move_x(x - self.bbox_right, do_events=do_events,
                                    exclude_events=exclude_events)
                        y = other.get_slope_y(self.bbox_right)
                        diff = self.bbox_top - y
                        if diff < 0:
                            self.bbox_top = y
                            if self.bbox_right == x:
                                self.move_y(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_right = get_on_right(on_right)
                        if on_right:
                            stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        stopper = other

            slopes = self.collision(SlopeBottomRight)
            def key(s, self=self): return -s.get_slope_y(self.bbox_left)
            slopes.sort(key=key)
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
                        self.move_x(x - self.bbox_left, do_events=do_events,
                                    exclude_events=exclude_events)
                        y = other.get_slope_y(self.bbox_left)
                        diff = self.bbox_top - y
                        if diff < 0:
                            self.bbox_top = y
                            if self.bbox_left == x:
                                self.move_y(diff, do_events=do_events,
                                            exclude_events=exclude_events)

                        on_left = get_on_left(on_left)
                        if on_left:
                            stopper = other
                    elif not self.collision(other, y=old_y):
                        self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                        stopper = other

            for other in self.collision(SolidBottom):
                if not self.collision(other, y=old_y):
                    self.bbox_top = max(self.bbox_top, other.bbox_bottom)
                    stopper = other

            if do_events and stopper not in exclude_events:
                move_loss = max(0, abs(move) - abs(self.y - old_y))
                self.event_physics_collision_top(stopper, move_loss)
                stopper.event_physics_collision_bottom(self, 0)

        # Engage stickiness (same whether moving left or right)
        # 1 = sticking to a wall on the right
        # 2 = sticking to a wall on the left
        if sticky == 1:
            if (not self.get_right_touching_slope() and
                    not self.get_right_touching_wall()):
                new_bbox_right = None
                others = (
                    sge.game.current_room.get_objects_at(
                        self.bbox_left, self.bbox_top,
                        (sge.game.current_room.width - self.bbox_left +
                         sge.game.current_room.object_area_width),
                        self.bbox_height) |
                    sge.game.current_room.object_area_void)
                for other in others:
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
                others = (
                    sge.game.current_room.get_objects_at(
                        0, self.bbox_top, self.bbox_right, self.bbox_height) |
                    sge.game.current_room.object_area_void)
                for other in others:
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

        See the documentation for :meth:`sge.dsp.Object.event_collision`
        for more information.
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

    def event_update_position(self, delta_mult):
        if delta_mult:
            xaccel = self.xacceleration
            yaccel = self.yacceleration
            if self.slope_acceleration:
                for slope in set(self.get_left_touching_slope() +
                                 self.get_right_touching_slope() +
                                 self.get_top_touching_slope() +
                                 self.get_bottom_touching_slope()):
                    xaccel += slope.slope_xacceleration * self.slope_acceleration
                    yaccel += slope.slope_yacceleration * self.slope_acceleration

            vi = self.xvelocity
            vf = vi + xaccel * delta_mult
            dc = abs(self.xdeceleration) * delta_mult
            if abs(vf) > dc:
                vf -= math.copysign(dc, vf)
            else:
                vf = 0
            self.xvelocity = vf
            self.move_x(((vi + vf) / 2) * delta_mult)

            vi = self.yvelocity
            vf = vi + yaccel * delta_mult
            dc = abs(self.ydeceleration) * delta_mult
            if abs(vf) > dc:
                vf -= math.copysign(dc, vf)
            else:
                vf = 0
            self.yvelocity = vf
            self.move_y(((vi + vf) / 2) * delta_mult)


class Wall(sge.dsp.Object):

    """
    Base class for all wall objects that :class:`Collider` objects
    interact with in some way.  It is functionally identical to its
    parent class, :class:`sge.dsp.Object`.
    """


class SolidLeft(Wall):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SolidRight(Wall):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the right.
    """

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SolidTop(Wall):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the top.
    """

    def event_physics_collision_top(self, other, move_loss):
        """
        Called when the top side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SolidBottom(Wall):

    """
    Class for walls which stop movement of :class:`Collider` objects
    from the bottom.
    """

    def event_physics_collision_bottom(self, other, move_loss):
        """
        Called when the bottom side of the wall collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class Solid(SolidLeft, SolidRight, SolidTop, SolidBottom):

    """
    Inherits :class:`SolidLeft`, :class:`SolidRight`, :class:`SolidTop`,
    and :class:`SolidBottom`.  Meant to be a convenient parent class for
    walls that should stop movement in all directions.
    """


class Slope(Wall):

    """
    Base class for all slopes.

    .. attribute:: slope_xacceleration

       Indicates the amount of horizontal acceleration to apply to any
       collider which is touching the slope.  It is multiplied by the
       affected colliders' :attr:`slope_acceleration` values and added
       to their use of :attr:`xacceleration` in
       :meth:`event_update_position`.

       Default value: ``0``

    .. attribute:: slope_yacceleration

       Indicates the amount of vertical acceleration to apply to any
       collider which is touching the slope.  It is multiplied by the
       affected colliders' :attr:`slope_acceleration` values and added
       to their use of :attr:`yacceleration` in
       :meth:`event_update_position`.

       Default value: ``0``
    """

    slope_xacceleration = 0
    slope_yacceleration = 0


class SlopeTopLeft(Slope):

    """
    A parent class for slopes which point in some direction upwards and
    to the left.

    Slopes of this type go from the bottom-left corner to the top-right
    corner of the bounding box.

    .. attribute:: xsticky_top

       If set to :const:`True`, a collider that moves to the left while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward, unless the
       collider's :attr:`nonstick_bottom` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: ysticky_left

       If set to :const:`True`, a collider that moves upward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right, unless the
       collider's :attr:`nonstick_right` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: slope_xacceleration

       See the documentation for :attr:`Slope.slope_xacceleration`.

    .. attribute:: slope_yacceleration

       See the documentation for :attr:`Slope.slope_yacceleration`.
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
        x = y / m + self.bbox_right
        return max(self.bbox_left, min(x, self.bbox_right))

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = -self.bbox_height / self.bbox_width
        x -= self.bbox_left
        y = m * x + self.bbox_bottom
        return max(self.bbox_top, min(y, self.bbox_bottom))

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
        """
        Called when the top side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SlopeTopRight(Slope):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky_top

       If set to :const:`True`, a collider that moves to the right while
       touching the top side of the slope will attempt to keep touching
       the top side of the slope by moving downward, unless the
       collider's :attr:`nonstick_bottom` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: ysticky_right

       If set to :const:`True`, a collider that moves upward while
       touching the right side of the slope will attempt to keep
       touching the right side of the slope by moving to the left,
       unless the collider's :attr:`nonstick_left` value is
       :const:`True`.

       Default value: :const:`False`

    .. attribute:: slope_xacceleration

       See the documentation for :attr:`Slope.slope_xacceleration`.

    .. attribute:: slope_yacceleration

       See the documentation for :attr:`Slope.slope_yacceleration`.
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
        x = y / m + self.bbox_left
        return max(self.bbox_left, min(x, self.bbox_right))

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        y = m * x + self.bbox_top
        return max(self.bbox_top, min(y, self.bbox_bottom))

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_top(self, other, move_loss):
        """
        Called when the top side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SlopeBottomLeft(Slope):

    """
    A parent class for slopes which point in some direction upwards and
    to the left.

    Slopes of this type go from the top-left corner to the bottom-right
    corner of the bounding box.

    .. attribute:: xsticky_bottom

       If set to :const:`True`, a collider that moves to the left while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward, unless
       the collider's :attr:`nonstick_top` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: ysticky_left

       If set to :const:`True`, a collider that moves downward while
       touching the left side of the slope will attempt to keep touching
       the left side of the slope by moving to the right, unless the
       collider's :attr:`nonstick_right` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: slope_xacceleration

       See the documentation for :attr:`Slope.slope_xacceleration`.

    .. attribute:: slope_yacceleration

       See the documentation for :attr:`Slope.slope_yacceleration`.
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
        x = y / m + self.bbox_left
        return max(self.bbox_left, min(x, self.bbox_right))

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = self.bbox_height / self.bbox_width
        x -= self.bbox_left
        y = m * x + self.bbox_top
        return max(self.bbox_top, min(y, self.bbox_bottom))

    def event_physics_collision_left(self, other, move_loss):
        """
        Called when the left side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
        """
        Called when the bottom side of the slope collides with a
        collider in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class SlopeBottomRight(Slope):

    """
    A parent class for slopes which point in some direction upwards and
    to the right.

    Slopes of this type go from the bottom-left corner to the top-right
    corner of the bounding box.

    .. attribute:: xsticky_bottom

       If set to :const:`True`, a collider that moves to the right while
       touching the bottom side of the slope will attempt to keep
       touching the bottom side of the slope by moving upward, unless
       the collider's :attr:`nonstick_top` value is :const:`True`.

       Default value: :const:`False`

    .. attribute:: ysticky_right

       If set to :const:`True`, a collider that moves downward while
       touching the right side of the slope will attempt to keep
       touching the right side of the slope by moving to the right,
       unless the collider's :attr:`nonstick_left` value is
       :const:`True`.

       Default value: :const:`False`

    .. attribute:: slope_xacceleration

       See the documentation for :attr:`Slope.slope_xacceleration`.

    .. attribute:: slope_yacceleration

       See the documentation for :attr:`Slope.slope_yacceleration`.
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
        x = y / m + self.bbox_right
        return max(self.bbox_left, min(x, self.bbox_right))

    def get_slope_y(self, x):
        """
        Get the corresponding y coordinate of a given x coordinate for
        the slope.
        """
        # y = mx + b [b is 0]
        m = -self.bbox_height / self.bbox_width
        x -= self.bbox_left
        y = m * x + self.bbox_bottom
        return max(self.bbox_top, min(y, self.bbox_bottom))

    def event_physics_collision_right(self, other, move_loss):
        """
        Called when the right side of the slope collides with a collider
        in the sense of the physics system, rather than in the sense of
        SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass

    def event_physics_collision_bottom(self, other, move_loss):
        """
        Called when the bottom side of the slope collides with a
        collider in the sense of the physics system, rather than in the
        sense of SGE collision detection.  See the documentation for
        :meth:`sge.dsp.Object.event_collision` for more information.
        """
        pass


class MobileWall(Wall):

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

    .. attribute:: push_left

       If set to :const:`True`, the wall will push any colliders
       collided with as a result of the wall's movement to the left.
       Otherwise, the wall will pass through such colliders.

       Default value: :const:`True`

    .. attribute:: push_right

       If set to :const:`True`, the wall will push any colliders
       collided with as a result of the wall's movement to the right.
       Otherwise, the wall will pass through such colliders.

       Default value: :const:`True`

    .. attribute:: push_up

       If set to :const:`True`, the wall will push any colliders
       collided with as a result of the wall's movement upwards.
       Otherwise, the wall will pass through such colliders.

       Default value: :const:`True`

    .. attribute:: push_down

       If set to :const:`True`, the wall will push any colliders
       collided with as a result of the wall's movement downwards.
       Otherwise, the wall will pass through such colliders.

       Default value: :const:`True`

    .. attribute:: sticky_left

       If set to :const:`True`, any colliders touching the left side of
       the wall will move along with it, regardless of the direction of
       movement, with the exception of colliders whose
       :attr:`nonstick_right` values are :const:`True`.

       Default value: :const:`False`

    .. attribute:: sticky_right

       If set to :const:`True`, any colliders touching the right side of
       the wall will move along with it, regardless of the direction of
       movement, with the exception of colliders whose
       :attr:`nonstick_left` values are :const:`True`.

       Default value: :const:`False`

    .. attribute:: sticky_top

       If set to :const:`True`, any colliders touching the top side of
       the wall will move along with it, regardless of the direction of
       movement, with the exception of colliders whose
       :attr:`nonstick_bottom` values are :const:`True`.

       Default value: :const:`False`

    .. attribute:: sticky_bottom

       If set to :const:`True`, any colliders touching the bottom side
       of the wall will move along with it, regardless of the direction
       of movement, with the exception of colliders whose
       :attr:`nonstick_top` values are :const:`True`.

       Default value: :const:`False`
    """

    push_left = True
    push_right = True
    push_up = True
    push_down = True
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
                    if not other.nonstick_right and not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider, x=(self.x - 1)):
                    x = self.get_slope_x(other.bbox_bottom)
                    if (not other.nonstick_right and other.bbox_right >= x and
                            (not self.collision(other) or
                             other.bbox_right - 1 < x)):
                        stuck.append(other)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider, x=(self.x - 1)):
                    x = self.get_slope_x(other.bbox_top)
                    if (not other.nonstick_right and other.bbox_right >= x and
                            (not self.collision(other) or
                             other.bbox_right - 1 < x)):
                        stuck.append(other)

        if self.sticky_right:
            if isinstance(self, SolidRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    if not other.nonstick_left and not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    x = self.get_slope_x(other.bbox_bottom)
                    if (not other.nonstick_left and other.bbox_left <= x and
                            (not self.collision(other) or
                             other.bbox_left + 1 > x)):
                        stuck.append(other)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider, x=(self.x + 1)):
                    x = self.get_slope_x(other.bbox_top)
                    if (not other.nonstick_left and other.bbox_left <= x and
                            (not self.collision(other) or
                             other.bbox_left + 1 > x)):
                        stuck.append(other)

        if self.sticky_top:
            if isinstance(self, SolidTop):
                for other in self.collision(Collider, y=(self.y - 1)):
                    if not other.nonstick_bottom and not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider, y=(self.y - 1)):
                    y = self.get_slope_y(other.bbox_right)
                    if (not other.nonstick_bottom and other.bbox_bottom >= y and
                            (not self.collision(other) or
                             other.bbox_bottom - 1 < y)):
                        stuck.append(other)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider, y=(self.y - 1)):
                    y = self.get_slope_y(other.bbox_left)
                    if (not other.nonstick_bottom and other.bbox_bottom >= y and
                            (not self.collision(other) or
                             other.bbox_bottom - 1 < y)):
                        stuck.append(other)

        if self.sticky_bottom:
            if isinstance(self, SolidBottom):
                for other in self.collision(Collider, y=(self.y + 1)):
                    if not other.nonstick_top and not self.collision(other):
                        stuck.append(other)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider, y=(self.y + 1)):
                    y = self.get_slope_y(other.bbox_right)
                    if (not other.nonstick_top and other.bbox_top <= y and
                            (not self.collision(other) or
                             other.bbox_top + 1 > y)):
                        stuck.append(other)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider, y=(self.y + 1)):
                    y = self.get_slope_y(other.bbox_left)
                    if (not other.nonstick_top and other.bbox_top <= y and
                            (not self.collision(other) or
                             other.bbox_top + 1 > y)):
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
                        if self.push_right:
                            other.move_x(self.bbox_right - other.bbox_left,
                                         True)
                        self.event_physics_collision_right(other, 0)
                        other.event_physics_collision_left(self, 0)
            if isinstance(self, SlopeTopRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            if self.push_right:
                                other.move_x(x - other.bbox_left, True)
                                if self.push_up:
                                    y = self.get_slope_y(other.bbox_left)
                                    other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
                        elif not self.collision(other, x=old_x):
                            if self.push_right:
                                other.move_x(self.bbox_right - other.bbox_left,
                                             True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_left < x:
                        if other.bbox_left >= x - move:
                            if self.push_right:
                                other.move_x(x - other.bbox_left, True)
                                if self.push_down:
                                    y = self.get_slope_y(other.bbox_left)
                                    other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)
                        elif not self.collision(other, x=old_x):
                            if self.push_right:
                                other.move_x(self.bbox_right - other.bbox_left,
                                             True)
                            self.event_physics_collision_right(other, 0)
                            other.event_physics_collision_left(self, 0)

        elif move < 0:
            if isinstance(self, SolidLeft):
                for other in self.collision(Collider):
                    if not self.collision(other, x=old_x):
                        if self.push_left:
                            other.move_x(self.bbox_left - other.bbox_right,
                                         True)
                        self.event_physics_collision_left(other, 0)
                        other.event_physics_collision_right(self, 0)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_bottom)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            if self.push_left:
                                other.move_x(x - other.bbox_right, True)
                                if self.push_up:
                                    y = self.get_slope_y(other.bbox_right)
                                    other.move_y(y - other.bbox_bottom, True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
                        elif not self.collision(other, x=old_x):
                            if self.push_left:
                                other.move_x(self.bbox_left - other.bbox_right,
                                             True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    x = self.get_slope_x(other.bbox_top)
                    if other.bbox_right > x:
                        if other.bbox_right <= x - move:
                            if self.push_left:
                                other.move_x(x - other.bbox_right, True)
                                if self.push_down:
                                    y = self.get_slope_y(other.bbox_right)
                                    other.move_y(y - other.bbox_top, True)
                            self.event_physics_collision_left(other, 0)
                            other.event_physics_collision_right(self, 0)
                        elif not self.collision(other, x=old_x):
                            if self.push_left:
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
                        if self.push_down:
                            other.move_y(self.bbox_bottom - other.bbox_top,
                                         True)
                        self.event_physics_collision_bottom(other, 0)
                        other.event_physics_collision_top(self, 0)
            if isinstance(self, SlopeBottomLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            if self.push_down:
                                other.move_y(y - other.bbox_top, True)
                                if self.push_left:
                                    x = self.get_slope_x(other.bbox_top)
                                    other.move_x(x - other.bbox_right, True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
                        elif not self.collision(other, y=old_y):
                            if self.push_down:
                                other.move_y(self.bbox_bottom - other.bbox_top,
                                             True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
            if isinstance(self, SlopeBottomRight):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_left)
                    if other.bbox_top < y:
                        if other.bbox_top >= y - move:
                            if self.push_down:
                                other.move_y(y - other.bbox_top, True)
                                if self.push_right:
                                    x = self.get_slope_x(other.bbox_top)
                                    other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)
                        elif not self.collision(other, y=old_y):
                            if self.push_down:
                                other.move_y(self.bbox_bottom - other.bbox_top,
                                             True)
                            self.event_physics_collision_bottom(other, 0)
                            other.event_physics_collision_top(self, 0)

        elif move < 0:
            if isinstance(self, SolidTop):
                for other in self.collision(Collider):
                    if not self.collision(other, y=old_y):
                        if self.push_up:
                            other.move_y(self.bbox_top - other.bbox_bottom,
                                         True)
                        self.event_physics_collision_top(other, 0)
                        other.event_physics_collision_bottom(self, 0)
            if isinstance(self, SlopeTopLeft):
                for other in self.collision(Collider):
                    y = self.get_slope_y(other.bbox_right)
                    if other.bbox_bottom > y:
                        if other.bbox_bottom <= y - move:
                            if self.push_up:
                                other.move_y(y - other.bbox_bottom, True)
                                if self.push_left:
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
                            if self.push_up:
                                other.move_y(y - other.bbox_bottom, True)
                                if self.push_right:
                                    x = self.get_slope_x(other.bbox_bottom)
                                    other.move_x(x - other.bbox_left, True)
                            self.event_physics_collision_top(other, 0)
                            other.event_physics_collision_bottom(self, 0)
                        elif not self.collision(other, y=old_y):
                            if self.push_up:
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

    def move_x(self, move, absolute=False, do_events=True, exclude_events=()):
        """
        Move the wall horizontally, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        """
        xprev = self.x
        Collider.move_x(self, move, absolute, do_events, exclude_events)
        real_move = self.x - xprev
        self.x = xprev
        MobileWall.move_x(self, real_move)

    def move_y(self, move, absolute=False, do_events=True, exclude_events=()):
        """
        Move the wall vertically, handling physics.

        Arguments:

        - ``move`` -- The amount to add to :attr:`y`.
        """
        yprev = self.y
        Collider.move_y(self, move, absolute, do_events, exclude_events)
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
