# xSGE Path
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

"""
This module provides paths for the SGE.  Paths are used to make objects
move in a certain way.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import math

import sge


__all__ = ["Path"]


class Path(sge.Object):

    """
    Class for paths: objects which define movement patterns for other
    objects.  Paths are defined as a series of points for an object to
    follow.

    .. attribute:: points

       A list of the points that make up the path relative to the
       position of the path in the room, excluding the first point.
       Each point should be a tuple in the form ``(x, y)``, where x is
       the horizontal location and y is the vertical location.  The
       first point is always ``(0, 0)``, which is why it is not included
       in this list.
    """

    def __init__(self, x, y, points=()):
        super(Path, self).__init__(x, y, tangible=False)
        self.points = list(points)
        self.__objects = {}
        self.__delta = 0

    def follow_start(self, obj, speed, accel=None, decel=None, loop=0):
        """
        Cause ``obj`` to start following this path at the speed
        indicated by ``speed``.

        While path objects have a location within the room, this
        location has no bearing on how objects following the path move.
        Movement is determined relative to the location of the object
        following the path when it started, not the location of the
        path.

        By default, the object follows the path at a constant speed.
        If ``accel`` or ``decel`` is set to a value other than
        :const:`None` or ``0``, the object will instead accelerate or
        decelerate, respectively, by that amount each frame on each
        segment of the path.

        ``loop`` indicates the number of times the object should follow
        the path after it does so the first time.  For example, if set
        to ``2``, the object will follow the path a total of 3 times.
        Set to :const:`None` to loop indefinitely.

        .. note::

           Acceleration and deceleration does not work with delta
           timing.  This is a simple consequence of the way delta timing
           works; it is not possible to perfectly predict how much to
           accelerate or decelerate to achieve the desired effect, and
           to predict this even decently requires control over the
           actual movement, which paths don't have.
        """
        self.__objects[id(obj)] = [obj, speed, accel, decel, obj.x, obj.y,
                                   loop, 0]

    def follow_stop(self, obj):
        """Cause ``obj`` to stop following this path."""
        i = id(obj)
        if i in self.__objects:
            del self.__objects[i]

    def event_follow_end(self, obj):
        """
        Called when an object, indicated by ``obj``, finishes following
        the path.
        """
        pass

    def event_step(self, time_passed, delta_mult):
        self.__delta = (self.__delta % 1) + delta_mult
        for i in self.__objects.keys():
            (obj, speed, accel, decel, start_x, start_y, loop,
             dest) = self.__objects[i]

            p1 = (0, 0) if dest == 0 else self.points[dest - 1]
            p2 = self.points[dest]
            x1 = p1[0] + start_x
            y1 = p1[1] + start_y
            x2 = p2[0] + start_x
            y2 = p2[1] + start_y
            xprog = (obj.x - x1) / (x2 - x1)
            yprog = (obj.y - y1) / (y2 - y1)
            prog = math.hypot(xprog, yprog)

            if prog >= 1:
                dest += 1
                obj.speed = 0

            if dest < len(self.points):
                dx, dy = self.points[dest]
                dx += start_x
                dy += start_y
                xdist = dx - obj.x
                ydist = dy - obj.y
                dist = math.hypot(xdist, ydist)

                obj.move_direction = math.degrees(math.atan2(xdist, -ydist))
                deceling = False

                if decel:
                    d = obj.speed
                    decel_dist = 0
                    while d:
                        d -= decel
                        decel_dist += d

                    if dist <= decel_dist:
                        obj.speed = max(0, obj.speed - decel)
                        deceling = True

                if not deceling:
                    if accel and obj.speed < speed:
                        obj.speed = min(speed, obj.speed + accel)
                    else:
                        obj.speed = speed

                self.__objects[i] = [obj, speed, accel, decel, start_x,
                                     start_y, loop, dest]
            else:
                self.follow_stop(obj)

                if loop is None:
                    self.follow_start(obj, speed, accel, decel, None)
                elif loop > 0:
                    self.follow_start(obj, speed, accel, decel, loop - 1)
                else:
                    self.event_follow_end(obj)
