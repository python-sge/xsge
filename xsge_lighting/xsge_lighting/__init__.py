# xSGE Lighting Library
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

__version__ = "1.0.2"
__all__ = ["project_light", "clear_lights", "project_darkness"]


import sge


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


def project_darkness(z=100000, ambient_light=None, buffer=0):
    """
    This function must be called every frame to maintain darkness.

    Arguments:

    - ``z`` -- The Z-axis position of the darkness in the room.
      Anything with a higher Z-axis value will not be affected.
    - ``ambient_light`` -- A :class:`sge.gfx.Color` object indicating
      the color that should be applied as lighting to the entirety of
      the darkness.  Set to :const:`None` for no ambient lighting.
    - ``buffer`` -- An extra portion of the room, in addition to what is
      covered by the room's views, to cover with darkness.  This can be
      used to prevent situations where movement of a view at the wrong
      time causes part of the view to not be properly covered in
      darkness.  To ensure maximum efficiency, this should be the
      smallest number possible, i.e. the maximum amount of view movement
      that can happen in a single frame.
    """
    global _lights

    if ambient_light is None:
        ambient_light = sge.gfx.Color("black")

    groups = []
    for view in sge.game.current_room.views:
        my_groups = []
        for i in range(len(groups)):
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
        rw = sge.game.current_room.width
        rh = sge.game.current_room.height
        dx = rw
        dy = rh
        dx2 = 0
        dy2 = 0
        for view in group:
            dx = min(dx, max(0, view.x - buffer))
            dy = min(dy, max(0, view.y - buffer))
            dx2 = max(dx2, min(view.x + view.width + buffer, rw))
            dy2 = max(dy2, min(view.y + view.height + buffer, rh))
        width = dx2 - dx
        height = dy2 - dy

        darkness = sge.gfx.Sprite(width=width, height=height)
        darkness.draw_lock()
        darkness.draw_rectangle(0, 0, width, height, fill=ambient_light)
        for x, y, sprite, image in _lights:
            darkness.draw_sprite(sprite, image, x - dx, y - dy,
                                 blend_mode=sge.BLEND_RGB_MAXIMUM)
        darkness.draw_unlock()

        sge.game.current_room.project_sprite(darkness, 0, dx, dy, z,
                                             blend_mode=sge.BLEND_RGB_MULTIPLY)

    clear_lights()
