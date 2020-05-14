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


__version__ = "1.0"
__all__ = ["Particle", "AnimationParticle", "TimedParticle", "BubbleParticle",
           "AnimationBubbleParticle", "TimedBubbleParticle", "Emitter"]


import random

import sge


class Particle(sge.dsp.Object):

    """
    Base class for particles.  It is identical to
    :class:`sge.dsp.Object`, except that it is intangible by default.
    """

    def __init__(self, x, y, z=0, tangible=False, **kwargs):
        """
        ``x``, ``y``, ``z``, ``tangible``, and all arguments passed to
        ``kwargs`` are passed as the corresponding arguments to the
        constructor method of the parent class.
        """
        super().__init__(x, y, z=z, tangible=tangible, **kwargs)


class AnimationParticle(Particle):

    """
    Class for particle objects which animate once and are then
    destroyed.  It is otherwise identical to :class:`Particle`.

    .. note::

       :meth:`event_animation_end` is used to control the destruction.
    """

    def event_animation_end(self):
        super().event_animation_end()
        self.destroy()


class TimedParticle(Particle):

    """
    Class for particle objects which are destroyed after a designated
    amount of time.  It is otherwise identical to :class:`Particle`.

    .. note::

       An alarm with the name ``"__life"`` in :meth:`event_alarm` is
       used to control the timing.  It is initially set by
       :meth:`event_create`.

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
        constructor method of the parent class.
        """
        super().__init__(x, y, z=z, tangible=tangible, **kwargs)
        self.__life = life

    def event_create(self):
        super().event_create()
        self.alarms["__life"] = self.life
        

    def event_alarm(self, alarm_id):
        super().event_alarm(alarm_id)
        if alarm_id == "__life":
            self.destroy()


class BubbleParticle(Particle):

    """
    Class for particle objects which randomly change their move
    directions.

    .. note::

       :meth:`event_step` is used to control this behavior.
       :attr:`move_direction` is manipulated.

    .. attribute:: turn_factor

       The largest amount of rotation possible.

    .. attribute:: min_angle

       The lowest possible angle permitted.

    .. attribute:: max_angle

       The highest possible angle permitted.
    """

    def __init__(self, x, y, z=0, turn_factor=1, min_angle=180, max_angle=0,
                 tangible=False, **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`TimedParticle` for more
        information.

        ``x``, ``y``, ``z``, ``tangible``, and all arguments passed to
        ``kwargs`` are passed as the corresponding arguments to the
        constructor method of the parent class.
        """
        super().__init__(x, y, z=z, tangible=tangible, **kwargs)
        self.turn_factor = turn_factor
        self.min_angle = min_angle
        self.max_angle = max_angle

    def event_step(self, time_passed, delta_mult):
        super().event_step(time_passed, delta_mult)

        f = self.turn_factor * delta_mult
        self.move_direction += f * random.uniform(-1, 1)

        min_angle = self.min_angle % 360
        max_angle = self.max_angle % 360
        while max_angle < min_angle:
            max_angle += 360

        md = self.move_direction % 360
        while md < min_angle:
            md += 360

        if md > max_angle:
            if md - max_angle > (360 - (max_angle - min_angle)) / 2:
                self.move_direction = min_angle
            else:
                self.move_direction = max_angle


class AnimationBubbleParticle(AnimationParticle, BubbleParticle):

    """
    Inherits the features of both :class:`AnimationParticle` and
    :class:`BubbleParticle`.
    """


class TimedBubbleParticle(TimedParticle, BubbleParticle):

    """
    Inherits the features of both :class:`TimedParticle` and
    :class:`BubbleParticle`.
    """


class Emitter(sge.dsp.Object):

    """
    Class for object emitters.  These are :class:`sge.dsp.Object`
    objects which create other :class:`sge.dsp.Object` objects of a
    specified class at a specified interval.

    To randomize the way particles are created, extend
    :meth:`event_create_particle` in a derived class.

    .. note::

       An alarm with the name ``"__emitter"`` in :meth:`event_alarm` is
       used to control the timing.  It is initially set by
       :meth:`event_create`.

    .. attribute:: interval

       The number of frames to wait in between the creation of each
       particle (adjusted for delta timing).

    .. attribute:: chance

       The chance (out of 1) of a particle actually being created at
       each iteration.  This can be used to make particle generation
       uneven.

    .. attribute:: particle_cls

       The class to use for the particles created.  Any class derived
       from :class:`sge.dsp.Object` will work.

    .. attribute:: particle_args

       The ordered arguments to pass to created particles' constructor
       methods.  If set to :const:`None`, an empty list is used.

    .. attribute:: particle_kwargs

       The keyword arguments to pass to created particles' constructor
       methods.  If set to :const:`None`, an empty dictionary is used.

    .. attribute:: particle_lambda_args

       A list of functions which, when a particle is about to be
       created, are called and have the returned values passed to the
       particle's constructor method instead of the corresponding index
       of :attr:`particle_args`.  This emitter is passed to each of
       these functions as the first argument.

       Values in the list set to :const:`None` are ignored.  If this
       list is longer than :attr:`particle_args`, any arguments not set
       by either of these lists are set to :const:`None`.

       If set to :const:`None`, an empty list is used.

    .. attribute:: particle_lambda_kwargs

       A dictionary of functions which, when a particle is about to be
       created, are called and have the returned values passed to the
       particle's constructor method instead of the corresponding key of
       :attr:`particle_kwargs`.  This emitter is passed to each of these
       functions as the first argument.

       If set to :const:`None`, an empty dictionary is used.
    """

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, value):
        self.__interval = value
        self.alarms["__emitter"] = min(value, self.alarms["__emitter"])

    def __init__(self, x, y, z=0, interval=1, chance=1, particle_cls=Particle,
                 particle_args=None, particle_kwargs=None,
                 particle_lambda_args=None, particle_lambda_kwargs=None,
                 tangible=False, **kwargs):
        """
        Arguments set the respective initial attributes of the object.
        See the documentation for :class:`Emitter` for more information.

        ``x``, ``y``, ``z``, ``tangible``, and all arguments passed to
        ``kwargs`` are passed as the corresponding arguments to the
        constructor method of :class:`sge.dsp.Object`.
        """
        super().__init__(x, y, z=z, tangible=tangible, **kwargs)
        self.__interval = interval
        self.chance = chance
        self.particle_cls = particle_cls
        self.particle_args = particle_args
        self.particle_kwargs = particle_kwargs
        self.particle_lambda_args = particle_lambda_args
        self.particle_lambda_kwargs = particle_lambda_kwargs

    def event_create(self):
        super().event_create()
        self.alarms["__emitter"] = self.interval

    def event_alarm(self, alarm_id):
        if alarm_id == "__emitter":
            if random.random() < self.chance:
                args = (self.particle_args or [])[:]
                kwargs = (self.particle_kwargs or {}).copy()

                if self.particle_lambda_args:
                    while len(self.particle_lambda_args) > len(args):
                        args.append(None)

                    for i in range(len(self.particle_lambda_args)):
                        f = self.particle_lambda_args[i]
                        if f is not None:
                            args[i] = f(self)

                if self.particle_lambda_kwargs:
                    for i in self.particle_lambda_kwargs:
                        f = self.particle_lambda_kwargs[i]
                        kwargs[i] = f(self)

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

