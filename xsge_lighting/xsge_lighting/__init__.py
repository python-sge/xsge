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

__version__ = "0.8.1a0"

import six
import sge


__all__ = ["project_light", "project_darkness"]

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


def project_darkness(z=100000):
    """
    This function must be called every frame to maintain darkness.

    Arguments:

    - ``z`` -- The Z-axis position of the darkness in the room.
      Anything with a higher Z-axis value will not be affected.
    """
    global _lights

    groups = []
    for view in sge.game.current_room.views:
        my_groups = []
        for i in six.moves.range(len(groups)):
            for member in groups[i]:
                if (view.x + view.width > member.x and
                        view.x < member.x + member.width and
                        view.y + view.height > member.y and
                        view.y < member.y + member.height):
                    my_groups.append(i)
                    break

        if my_groups:
            g = my_groups[0]
            groups[g].append(view)
            for i in my_groups[1:]:
                groups[g].extend(groups[i])
                del groups[i]
        else:
            groups.append([view])

    for group in groups:
        dx = sge.game.current_room.width
        dy = sge.game.current_room.height
        dx2 = 0
        dy2 = 0
        for view in group:
            dx = min(dx, view.x)
            dy = min(dy, view.y)
            dx2 = max(dx2, view.x + view.width)
            dy2 = max(dy2, view.y + view.height)
        width = dx2 - dx
        height = dy2 - dy

        darkness = sge.Sprite(width=width, height=height)

        darkness.draw_lock()
        darkness.draw_rectangle(0, 0, width, height, fill=sge.Color("black"))
        for x, y, sprite, image in _lights:
            darkness.draw_sprite(sprite, image, x - dx, y - dy,
                                 blend_mode=sge.BLEND_RGB_MAXIMUM)
        darkness.draw_unlock()

        sge.game.current_room.project_sprite(darkness, 0, dx, dy, z,
                                             blend_mode=sge.BLEND_RGB_MULTIPLY)

    _lights = []
