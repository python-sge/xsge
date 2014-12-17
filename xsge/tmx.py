# xSGE TMX Library
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
This module provides support for loading the `Tiled
<http://www.mapeditor.org/>`_ TMX format.  This allows you to use Tiled
to edit your game's world (e.g. levels), rather than building a level
editor yourself.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import sge
import six
import tmx

from xsge import path


__all__ = ["load"]


class Decoration(sge.Object):

    """
    Default class for tiles and image layers.  Identical to
    :class:`sge.Object`, except that it is intangible and doesn't check
    for collisions by default.
    """

    def __init__(self, x, y, z=0, sprite=None, visible=True, active=False,
                 checks_collisions=False, tangible=False, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(Decoration, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class Rectangle(sge.Object):

    """
    Default class for rectangle objects.  Identical to
    :class:`sge.Object`, except that it is invisible by default.
    """

    def __init__(self, x, y, z=0, sprite=None, visible=False, active=True,
                 checks_collisions=True, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(Decoration, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class Ellipse(sge.Object):

    """
    Default class for ellipse objects.  Identical to
    :class:`sge.Object`, except that it is invisible and uses ellipse
    collision detection by default.
    """

    def __init__(self, x, y, z=0, sprite=None, visible=True, active=True,
                 checks_collisions=True, tangible=True, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=True,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(Decoration, self).__init__(
            x, y, z, sprite, visible, active, checks_collisions, tangible,
            bbox_x, bbox_y, bbox_width, bbox_height, regulate_origin,
            collision_ellipse, collision_precise, xvelocity, yvelocity,
            image_index, image_origin_x, image_origin_y, image_fps,
            image_xscale, image_yscale, image_rotation, image_alpha,
            image_blend)


class Polygon(path.Path):

    """
    Default class for polygon objects.  Identical to
    :class:`xsge.path.Path`.
    """


class Polyline(path.Path):

    """
    Default class for polyline objects.  Identical to
    :class:`xsge.path.Path`.
    """


def load(fname, cls=sge.Room, types=None, z=0):
    """
    Load the TMX file ``fname`` and return a room of the class ``cls``.

    The way the map generates the room, in general, is to convert all
    tiles, objects, and image layers into :class:`sge.Object` objects.
    As a special exception, the object layer with the name "views"
    defines the views in the room; these objects are converted into
    :class:`sge.View` objects.

    Objects are given Z-axis positions based on the ordering of the
    layers in the TMX file: ``z`` is the Z-axis position of the first
    layer, and each subsequent layer's Z-axis position is the Z-axis
    position of the previous layer plus one.

    Except for views, all objects can be defined to be converted into
    any class derived from :class:`sge.Object` via the ``types``
    argument, which should be a dictionary matching strings to
    corresponding :class:`sge.Object` classes, or :const:`None`, which
    is equivalent to ``{}``.  Classes are determined in the following
    ways:

    - Tiles are converted to the class connected to, in order of
      preference, the name of the tileset or the name of the tile layer.
      If neither of these strings are valid keys in ``types``,
      :class:`Decoration` is used.

    - Objects are converted to the class connected to, in order of
      preference, the name of the object, the type of the object, or the
      name of the object group.  If none of these strings are valid keys
      in ``types``, the class used depends on what kind of object it is:

      - Rectangle objects default to :class:`Rectangle`.
      - Ellipse objects default to :class:`Ellipse`.
      - Polygon objects default to :class:`Polygon`.
      - Polyline objects default to :class:`xsge.path.Path`.

      Polygon and polyline objects have lists of points passed to their
      constructors, as is expected for :class:`xsge.path.Path`, instead
      of the usual x and y coordinates.  Keep this in mind when defining
      different classes for these types of objects.

    - Image layers are converted to the class connected to the image
      layer's name.  If the image layer's name is not a valid key in
      ``types``, :class:`Decoration` is used.

    Property lists, converted to integers or floats if possible, are
    passed to objects as keyword arguments in the following ways:

    - Tiles have the properties of their tilesets and the properties of
      their layers applied to them.  Tileset properties override layer
      properties.

    - Objects have their properties and the properties of their
      object groups applied to them.  Object properties override object
      group properties.

    - Image layers have their properties applied to them.
    """
    if types is None:
        types = {}

    tilemap = tmx.TileMap.load(fname)

    tile_sprites = {}
    for tileset in tilemap.tilesets:
        n = os.path.basename(tileset.source)
        d = os.path.dirname(tileset.source)
        fs = sge.Sprite(n, d)
        fwidth = fs.width - tileset.margin
        fheight = fs.height - tileset.margin

        columns = int((fwidth - tileset.margin +
                       tileset.spacing) / tileset.tilewidth)
        rows = int((fheight - tileset.margin +
                    tileset.spacing) / tileset.tileheight)

        ts_sprite = sge.Sprite.from_tileset(
            tileset.source, x=tileset.margin, y=tileset.margin,
            columns=columns, rows=rows, xsep=tileset.spacing,
            ysep=tileset.spacing, width=tileset.tilewidth,
            height=tileset.tileheight)

        for i in six.moves.range(ts_sprite.frames):
            t_sprite = sge.Sprite(width=tileset.tilewidth,
                                  height=tileset.tileheight)
            t_sprite.draw_sprite(ts_sprite, i, 0, 0)
            tile_sprites[tileset.firstgid + i] = t_sprite

    room_width = tilemap.width * tilemap.tilewidth
    room_height = tilemap.height * tilemap.tileheight

    if tilemap.backgroundcolor is not None:
        if not tilemap.backgroundcolor.startswith("#"):
            tilemap.backgroundcolor = "#" + tilemap.backgroundcolor
        color = sge.Color(tilemap.backgroundcolor)
        background = sge.Background([], color)
    else:
        background = None

    objects = []
    views = []
    for layer in tilemap.layers:
        if isinstance(layer, tmx.Layer):
            cls = types.get(layer.name, Decoration)
            kwargs = {}

            if not layer.visible:
                kwargs["visible"] = False

            if layer.opacity != 1:
                kwargs["image_alpha"] = layer.opacity * 255

            for prop in layer.properties:
                kwargs[prop.name] = _nconvert(prop.value)

            for i in six.moves.range(len(layer.tiles)):
                tile = layer.tiles[i]
                if tile:
                    kwargs["sprite"] = tile_sprites.get(tile)
                    x = i % tileset.width
                    if tileset.renderorder.startswith("left"):
                        x = tileset.width - x - 1
                    y = i // tileset.height
                    if tileset.renderorder.endswith("up"):
                        y = tileset.height - y - 1

                    x *= tileset.tilewidth
                    y *= tileset.tileheight
                    objects.append(cls(x, y, **kwargs))
                    
        elif isinstance(layer, tmx.ObjectGroup):
            default_kwargs = {}

            if not layer.visible:
                default_kwargs["visible"] = False

            if layer.opacity != 1:
                default_kwargs["image_alpha"] = layer.opacity * 255

            for prop in layer.properties:
                default_kwargs[prop.name] = _nconvert(prop.value)

            if layer.name == "views":
                for obj in layer.objects:
                    kwargs = default_kwargs.copy()
                    for prop in obj.properties:
                        kwargs[prop.name] = _nconvert(prop.value)

                    views.append(sge.View(obj.x, obj.y, **kwargs))
            else:
                default_cls = types.get(layer.name)

                if not layer.color.startswith("#"):
                    layer.color = "#" + layer.color
                color = sge.Color(layer.color)

                for obj in layer.objects:
                    cls = types.get(obj.name, types.get(obj.type, default_cls))
                    kwargs = default_kwargs.copy()

                    if obj.rotation % 360:
                        kwargs["image_rotation"] = -obj.rotation

                    if obj.visible != layer.visible:
                        kwargs["visible"] = obj.visible

                    for prop in obj.properties:
                        kwargs[prop.name] = _nconvert(prop.value)

                    if obj.gid is not None:
                        if cls is None:
                            cls = Decoration
                        kwargs["sprite"] = tile_sprites.get(obj.gid)
                        x = (obj.x if tilemap.orientation == "orthogonal" else
                             obj.x - (obj.width / 2))
                        y = obj.y - obj.height
                        objects.append(cls(x, y, **kwargs))
                    elif obj.ellipse:
                        if cls is None:
                            cls = Ellipse
                        sprite = sge.Sprite(width=obj.width, height=obj.height)
                        sprite.draw_ellipse(0, 0, obj.width, obj.height,
                                            fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj.x, obj.y, **kwargs))
                    elif obj.polygon:
                        if cls is None:
                            cls = Polygon
                        pt = [(x + obj.x, y + obj.y) for x, y in obj.polygon]
                        objects.append(cls(pt, **kwargs))
                    elif obj.polyline:
                        if cls is None:
                            cls = Polyline
                        pt = [(x + obj.x, y + obj.y) for x, y in obj.polyline]
                        objects.append(cls(pt, **kwargs))
                    else:
                        if cls is None:
                            cls = Rectangle
                        sprite = sge.Sprite(width=obj.width, height=obj.height)
                        sprite.draw_rectangle(0, 0, obj.width, obj.height,
                                              fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj.x, obj.y, **kwargs))
        elif isinstance(layer, tmx.ImageLayer):
            cls = types.get(layer.name, Decoration)
            kwargs = {}

            if cls is sge.Object:
                kwargs["tangible"] = False
                kwargs["checks_collisions"] = False

            if not layer.visible:
                kwargs["visible"] = False

            if layer.opacity != 1:
                kwargs["image_alpha"] = layer.opacity * 255

            for prop in layer.properties:
                kwargs[prop.name] = _nconvert(prop.value)

            sprite = sge.Sprite(layer.image.source)
            sobj = cls(layer.x, layer.y, z, sprite=sprite, **kwargs)
            objects.append(sobj)

        z += 1

    return cls(objects=objects, width=room_width, height=room_height,
               views=(views if views else None), background=background)


def _nconvert(s):
    # Convert ``s`` to an int or float if possible.
    try:
        r = float(s)
    except ValueError:
        return s
    else:
        if r == int(r):
            r = int(r)

        return r
