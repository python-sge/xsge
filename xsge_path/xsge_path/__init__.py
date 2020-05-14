# xSGE Path
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

This extension provides paths for the SGE.  Paths are used to make
objects move in a certain way.
"""


__version__ = "1.0.2"
__all__ = ["Path"]


import math

import sge


class Path(sge.dsp.Object):

    """
    Class for paths: objects which define movement patterns for other
    objects.  Paths are defined as a series of points for an object to
    follow.

    This class is derived from :class:`sge.dsp.Object` and inherits all
    of that class's attributes and methods.

    .. note::

       :meth:`event_step` is used to implement path-following behavior.
       Keep this in mind if you derive a class from this one.

    .. attribute:: points

       A list of the points that make up the path relative to the
       position of the path in the room, excluding the first point.
       Each point should be a tuple in the form ``(x, y)``, where x is
       the horizontal location and y is the vertical location.  The
       first point is always ``(0, 0)``, which is why it is not included
       in this list.
    """

    def __init__(self, x, y, points=(), z=0, visible=False, tangible=False,
                 **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`Path` for more information.

        ``x``, ``y``, ``z``, ``visible``, ``tangible``, and all
        arguments passed to ``kwargs`` are passed as the corresponding
        arguments to the constructor method of the parent class.
        """
        super().__init__(x, y, z=z, visible=visible, tangible=tangible,
                         **kwargs)
        self.points = list(points)
        self.__objects = {}

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
        :const:`None`, the object will instead accelerate or decelerate,
        respectively, by that amount each frame on each segment of the
        path.

        ``loop`` indicates the number of times the object should follow
        the path after it does so the first time.  For example, if set
        to ``2``, the object will follow the path a total of 3 times.
        Set to :const:`None` to loop indefinitely.
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
        for i in list(self.__objects.keys()):
            (obj, speed, accel, decel, start_x, start_y, loop,
             dest) = self.__objects[i]

            dp = self.points[dest]
            dx = dp[0] + start_x
            dy = dp[1] + start_y

            if (delta_mult and
                    math.hypot(dx - obj.x,
                               dy - obj.y) / delta_mult < obj.speed):
                dest += 1
                obj.speed = 0
                obj.move_x(dx - obj.x)
                obj.move_y(dy - obj.y)

            if dest < len(self.points):
                dp = self.points[dest]
                dx = dp[0] + start_x
                dy = dp[1] + start_y
                xdist = dx - obj.x
                ydist = dy - obj.y
                dist = math.hypot(xdist, ydist)
                md = math.atan2(ydist, xdist)
                deceling = False

                if decel:
                    decel_dist = (obj.speed ** 2) / (2 * decel)
                    if dist <= decel_dist:
                        obj.xdeceleration = -(decel * math.cos(md))
                        obj.ydeceleration = -(decel * math.sin(md))
                        deceling = True
                    else:
                        obj.xdeceleration = 0
                        obj.ydeceleration = 0
                else:
                    obj.xdeceleration = 0
                    obj.ydeceleration = 0

                if not deceling:
                    if accel and obj.speed < speed:
                        obj.xacceleration = accel * math.cos(md)
                        obj.yacceleration = accel * math.sin(md)
                    else:
                        obj.speed = speed
                        obj.move_direction = math.degrees(md)
                        obj.xacceleration = 0
                        obj.yacceleration = 0
                else:
                    obj.xacceleration = 0
                    obj.yacceleration = 0

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


class PathLink(Path):

    """
    Class for path links.  Path links are just like normal paths, but
    can be linked to other path links or paths to form chains.

    By using a chain of path links, you can cause an object to move in
    different ways at different points of the path.  For example, you
    can cause the object to change its speed, or you can cause it to
    accelerate and decelerate only at particular points.

    .. note::

       :meth:`event_follow_end` is used to implement path linking.  Keep
       this in mind if you derive a class from this one.

    .. attribute:: next_path

       The next :class:`xsge_path.Path` object to be followed after this
       one.  If set to :const:`None`, no additional paths will be
       followed.

    .. attribute:: next_speed

       The value to pass on to the ``speed`` argument of the next path's
       :meth:`xsge_path.Path.follow_start` call.  If set to
       :const:`None`, the next path will not be followed.

    .. attribute:: next_accel

       The value to pass on to the ``accel`` argument of the next path's
       :meth:`xsge_path.Path.follow_start` call.

    .. attribute:: next_decel

       The value to pass on to the ``decel`` argument of the next path's
       :meth:`xsge_path.Path.follow_start` call.

    .. attribute:: next_loop

       The value to pass on to the ``loop`` argument of the next path's
       :meth:`xsge_path.Path.follow_start` call.
    """

    def __init__(self, x, y, points=(), next_path=None, next_speed=None,
                 next_accel=None, next_decel=None, next_loop=0, z=0,
                 visible=False, tangible=False, **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`Path` for more information.

        ``x``, ``y``, ``points``, ``z``, ``visible``, ``tangible``, and
        all arguments passed to ``kwargs`` are passed as the
        corresponding arguments to the constructor method of the parent
        class.
        """
        super().__init__(x, y, points=points, z=z, visible=visible,
                         tangible=tangible, **kwargs)
        self.next_path = next_path
        self.next_speed = next_speed
        self.next_accel = next_accel
        self.next_decel = next_decel
        self.next_loop = next_loop

    def event_follow_end(self, obj):
        if self.next_path is not None and self.next_speed is not None:
            self.next_path.follow_start(obj, self.next_speed, self.next_accel,
                                        self.next_decel, self.next_loop)
