# Copyright (C) 2017 Julie Marchant <onpon4@riseup.net>
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

This extension provides particle effects for the SGE.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.1a0"

import six

import sge


__all__ = ["Emitter", "AnimationParticle", "TimedParticle"]


class Emitter(sge.dsp.Object):

    """
    Class for object emitters.  These are :class:`sge.dsp.Object`
    objects which create other :class:`sge.dsp.Object` objects of a
    specified class at a specified interval.

    To randomize the way particles are created, extend
    :meth:`event_create_particle` in a derived class.

    .. note::

       An alarm with the name ``"__emitter"`` is used to control the
       timing.

    .. attribute:: interval

       The number of frames to wait in between the creation of each
       particle (adjusted for delta timing).

    .. attribute:: particle_cls

       The class to use for the particles created.  Any class derived
       from :class:`sge.dsp.Object` will work.

    .. attribute:: particle_args

       The ordered arguments to pass to created particles' constructor
       methods.  If set to :const:`None`, an empty list is used.

    .. attribute:: particle_kwargs

       The keyword arguments to pass to created particles' constructor
       methods.  If set to :const:`None`, an empty dictionary is used.
    """

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value
        self.alarms["__emitter"] = min(value, self.alarms["__emitter"])

    def __init__(self, x, y, z=0, interval=1, particle_cls=sge.dsp.Object,
                 particle_args=None, particle_kwargs=None, tangible=False,
                 **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`Emitter` for more information.

        ``x``, ``y``, ``z``, ``tangible``, and all arguments passed to
        ``kwargs`` are passed as the corresponding arguments to the
        constructor method of :class:`sge.dsp.Object`.
        """
        self.__interval = interval
        self.particle_cls = particle_cls
        self.particle_args = particle_args
        self.particle_kwargs = particle_kwargs
        super(Emitter, self).__init__(x, y, z=z, tangible=tangible, **kwargs)
        self.alarms["__emitter"] = interval

    def event_alarm(self, alarm_id):
        if alarm_id == "__emitter":
            args = self.particle_args or []
            kwargs = self.particle_kwargs or {}
            particle = self.particle_cls.create(*args, **kwargs)
            self.event_create_particle(particle)
            self.alarms["__emitter"] = self.interval

    def event_create_particle(self, particle):
        """
        Called immediately after the emitter creates a particle.

        Arguments:

        - ``particle`` -- The particle object just created.
        """
        pass


class AnimationParticle(sge.dsp.Object):

    """
    Class for particle objects which animate once and are then
    destroyed.  It is otherwise identical to :class:`sge.dsp.Object`.
    """

    def event_animation_end(self):
        self.destroy()


class TimedParticle(sge.dsp.Object):

    """
    Class for particle objects which are destroyed after a designated
    amount of time.  It is otherwise identical to
    :class:`sge.dsp.Object`.

    .. note::

       An alarm with the name ``"__life"`` is used to control the
       timing.

    .. attribute:: life

       The number of frames (adjusted for delta timing) after which the
       particle is destroyed.  Setting this attribute resets the
       ``"__life"`` alarm to the given value.  Set to :const:`None` to
       disable timed destruction.
    """

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self, value):
        self.__life = value
        self.alarms["__life"] = value

    def __init__(self, x, y, z=0, life=None, tangible=False, **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`TimedParticle` for more
        information.

        ``x``, ``y``, ``z``, ``tangible``, and all arguments passed to
        ``kwargs`` are passed as the corresponding arguments to the
        constructor method of :class:`sge.dsp.Object`.
        """
        self.__life = life
        super(TimedParticle, self).__init__(x, y, z=z, tangible=tangible,
                                            **kwargs)
        self.alarms["__life"] = life
        

    def event_alarm(self, alarm_id):
        if alarm_id == "__life":
            self.destroy()

