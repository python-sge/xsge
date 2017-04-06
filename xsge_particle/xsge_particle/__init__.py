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


__all__ = []


class Emitter(sge.dsp.Object):

    """
    Class for object emitters.  These are :class:`sge.dsp.Object`
    objects which create other :class:`sge.dsp.Object` objects of a
    specified class at a specified interval.

    To randomize the way particles are created, use
    :attr:`particle_args_replace` and :attr:`particle_kwargs_replace`.

    .. attribute:: interval

       The number of frames to wait in between the creation of each
       particle (adjusted for delta timing).

    .. attribute:: particle_cls

       The class to use for the particles created.  Any class derived
       from :class:`sge.dsp.Object` will work.

       If set to :const:`None`, :class:`sge.dsp.Object` will be used.

    .. attribute:: particle_args

       The ordered arguments to pass to created particles' constructor
       methods.

       If set to :const:`None`, ``[]`` will be used.

    .. attribute:: particle_args_replace

       A list.  Before any particle is created, every value in this list
       which is not :const:`None` is called as a function, and the
       returned value replaces the corresponding value of
       :attr:`particle_args` as the argument passed to the particle's
       constructor method.

       If set to :const:`None`, ``[]`` will be used.

    .. attribute:: particle_kwargs

       The keyword arguments to pass to created particles' constructor
       methods.

       If set to :const:`None`, ``{}`` will be used.

    .. attribute:: particle_args_replace

       A dictionary.  Before any particle is created, every value in
       this dictionary which is not :const:`None` is called as a
       function, and the returned value replaces the corresponding
       value of :attr:`particle_kwargs` as the argument passed to the
       particle's constructor method.

       If set to :const:`None`, ``{}`` will be used.
    """

    def __init__(self, x, y, interval=1, particle_cls=None, particle_args=None,
                 particle_kwargs=None, particle_args_replace=None,
                 particle_kwargs_replace=None, z=0, sprite=None, visible=True,
                 active=True, checks_collisions=True, tangible=True,
                 bbox_x=None, bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None, image_blend_mode=None):
        self.interval = interval
        self.particle_cls = particle_cls
        self.particle_args = particle_args
        self.particle_kwargs = particle_kwargs
        self.particle_args_replace = particle_args_replace
        self.particle_kwargs_replace = particle_kwargs_replace
        super(Emitter, self).__init__(
            x, y, z=z, sprite=sprite, visible=visible, active=active,
            checks_collisions=checks_collisions, tangible=tangible,
            bbox_x=bbox_x, bbox_y=bbox_y, bbox_width=bbox_width,
            bbox_height=bbox_height, regulate_origin=regulate_origin,
            collision_ellipse=collision_ellipse,
            collision_precise=collision_precise, xvelocity=xvelocity,
            yvelocity=yvelocity, xacceleration=xacceleration,
            yacceleration=yacceleration, xdeceleration=xdeceleration,
            ydeceleration=ydeceleration, image_index=image_index,
            image_origin_x=image_origin_x, image_origin_y=image_origin_y,
            image_fps=image_fps, image_xscale=image_xscale,
            image_yscale=image_yscale, image_rotation=image_rotation,
            image_alpha=image_alpha, image_blend=image_blend,
            image_blend_mode=image_blend_mode)

    def event_create(self):
        self.alarms["emit"] = self.interval

    def event_alarm(self, alarm_id):
        if alarm_id == "emit":
            cls = self.particle_cls or sge.dsp.Object
            args = (self.particle_args or [])[:]
            kwargs = (self.particle_kwargs or {}).copy()

            for i in six.move.range(
                    min(len(args), len(self.particle_args_replace))):
                value = self.particle_args_replace[i]
                if value is not None:
                    args[i] = value()

            for i in self.particle_kwargs_replace:
                value = self.particle_kwargs_replace[i]
                if value is not None:
                    kwargs[i] = value()

            cls.create(*args, **kwargs)

            self.alarms["emit"] = self.interval


class AnimationParticle(sge.dsp.Object):

    """
    Class for particle objects which animate once and are then
    destroyed.  It is otherwise identical to :class:`sge.dsp.Object`.
    """

    def event_animation_end(self):
        self.destroy()


class TimedParticle(sge.dsp.Object):

    """
    Class for particle objects which are destroyed when the
    ``"particle_timer"`` alarm goes off.  It is otherwise identical to
    :class:`sge.dsp.Object`.
    """

    def event_alarm(self, alarm_id):
        if alarm_id == "particle_timer":
            self.destroy()

