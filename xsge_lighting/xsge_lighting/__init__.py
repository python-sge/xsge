# xSGE Lighting Library
# Copyright (c) 2015 Julian Marchant <onpon4@riseup.net>
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

This extension provides a simple interface for lighting.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.9a0"

import six
import sge


__all__ = ["project_light", "clear_lights", "project_darkness"]

_lights = []


def project_light(x, y, sprite, image=0):
    """
    Add a light to the current frame.  This must be called every frame
    :func:`xsge_lighting.project_darkness` is called to maintain the
    respective light.  This function should be called *before*
    :func:`xsge_lighting.project_darkness`.

    Arguments:

    - ``x`` -- The horizontal location of the light relative to the
      room.
    - ``y`` -- The vertical location of the light relative to the room.
    - ``sprite`` -- The sprite to use as the light.  Black pixels are
      ignored, and all other colors make the appropriate pixel 
    - ``image`` -- The frame of the sprite to use, where ``0`` is the
      first frame.
    """
    _lights.append((x, y, sprite, image))


def clear_lights():
    """
    Remove all lights that have been projected by
    :func:`xsge_lighting.project_light`.
    """
    global _lights
    _lights = []


def project_darkness(ambient_light=None):
    """
    This function must be called every frame to maintain darkness.  The
    darkness is projected to the game window, once in each of the
    current room's views, via :meth:`sge.Game.project_sprite`.  It is
    reduced appropriately by any lights added with
    :func:`xsge_lighting.project_light` since the last call of either
    this function or :func:`xsge_lighting.clear_lights`.

    .. note::

       Since window projection is used, any other window projections
       occurring before the darkness projection will be affected, while
       any other window projections occurring after the darkness
       projection will not be affected.

    Arguments:

    - ``ambient_light`` -- A :class:`sge.Color` object indicating the
      color that should be applied as lighting to the entirety of the
      darkness.  Set to :const:`None` for no ambient lighting.
    """
    global _lights

    if ambient_light is None:
        ambient_light = sge.Color("black")

    for view in sge.game.current_room.views:
        xscale = view.wport / view.width
        yscale = view.hport / view.height

        darkness = sge.Sprite(width=view.wport, height=view.hport)
        darkness.draw_lock()
        darkness.draw_rectangle(0, 0, view.wport, view.hport,
                                fill=ambient_light)
        for x, y, sprite, image in _lights:
            x -= view.x
            y -= view.y
            left = x - sprite.origin_x
            top = y - sprite.origin_y
            w = sprite.width * xscale
            h = sprite.height * yscale
            if (left + w > 0 and top + h > 0 and left < view.width and
                    top < view.height):
                if xscale != 1 or yscale != 1:
                    sprite = sprite.copy()
                    sprite.width = w
                    sprite.height = h
                darkness.draw_sprite(sprite, image, x * xscale, y * yscale,
                                     blend_mode=sge.BLEND_RGB_MAXIMUM)
        darkness.draw_unlock()

        sge.game.project_sprite(darkness, 0, view.xport, view.yport,
                                blend_mode=sge.BLEND_RGB_MULTIPLY)

    clear_lights()
