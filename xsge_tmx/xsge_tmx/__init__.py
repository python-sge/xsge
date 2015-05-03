# xSGE TMX Library
# Copyright (c) 2014, 2015 Julian Marchant <onpon4@riseup.net>
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

This extension provides support for loading the `Tiled
<http://www.mapeditor.org/>`_ TMX format.  This allows you to use Tiled
to edit your game's world (e.g. levels), rather than building a level
editor yourself.

To load a TMX map, simply use :func:`xsge_tmx.load`.  See the
documentation for this function for more information.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.8.1a0"

import os

import sge
import six
import tmx
import xsge_path


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
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None):
        super(Decoration, self).__init__(
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
            image_alpha=image_alpha, image_blend=image_blend)


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
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None):
        super(Rectangle, self).__init__(
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
            image_alpha=image_alpha, image_blend=image_blend)


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
                 xacceleration=0, yacceleration=0, xdeceleration=0,
                 ydeceleration=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None):
        super(Ellipse, self).__init__(
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
            image_alpha=image_alpha, image_blend=image_blend)


class Polygon(xsge_path.Path):

    """
    Default class for polygon objects.  Identical to
    :class:`xsge_path.Path`.
    """


class Polyline(xsge_path.Path):

    """
    Default class for polyline objects.  Identical to
    :class:`xsge_path.Path`.
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

    Except for views, all tiles, objects, and image layers can be
    defined to be converted into any class derived from
    :class:`sge.Object` via the ``types`` argument, which should be a
    dictionary matching strings to corresponding :class:`sge.Object`
    classes, or :const:`None`, which is equivalent to ``{}``.  Classes
    are determined in the following ways:

    - Tiles are converted to the class connected to, in order of
      preference, the name of the tileset or the name of the tile layer.
      If neither of these strings are valid keys in ``types``,
      :class:`xsge_tmx.Decoration` is used.

    - Objects are converted to the class connected to, in order of
      preference, the name of the object, the type of the object, or the
      name of the object group.  If none of these strings are valid keys
      in ``types``, the class used depends on what kind of object it is:

      - Rectangle objects default to :class:`xsge_tmx.Rectangle`.
      - Ellipse objects default to :class:`xsge_tmx.Ellipse`.
      - Polygon objects default to :class:`xsge_tmx.Polygon`.
      - Polyline objects default to :class:`xsge_tmx.Polyline`.
      - Tile objects default to the appropriate class for the given
        tile (see above).

    - Image layers are converted to the class connected to the image
      layer's name.  If the image layer's name is not a valid key in
      ``types``, :class:`xsge_tmx.Decoration` is used.

    Property lists, converted to integers or floats if possible, are
    passed to objects as keyword arguments in the following ways:

    - Tiles have their properties, the properties of their tilesets, and
      the properties of their layers applied to them.  Tileset properties
      override layer properties, and tile properties override tileset
      properties.

    - Tile objects have their properties, the properties of their tiles,
      the properties of their tiles' tilesets, and the properties of
      their object groups applied to them.  Object properties override
      tile properties, tile properties override tileset properties, and
      tileset properties override object group properties.

    - Other objects have their properties and the properties of their
      object groups applied to them.  Object properties override object
      group properties.

    - Image layers have their properties applied to them.
    """
    room_cls = cls
    if types is None:
        types = {}

    tilemap = tmx.TileMap.load(fname)

    tile_cls = {}
    tile_sprites = {}
    tile_kwargs = {}
    for tileset in tilemap.tilesets:
        if tileset.image is not None:
            if tileset.image.source is not None:
                source = tileset.image.source
            else:
                _file = tempfile.NamedTemporaryFile(
                    suffix=".{}".format(tileset.image.format))
                _file.write(tileset.image.data)
                source = _file.name

            n, e = os.path.splitext(os.path.basename(source))
            d = os.path.dirname(source)
            fs = sge.Sprite(n, d)
            fwidth = fs.width - tileset.margin
            fheight = fs.height - tileset.margin

            columns = int((fwidth - tileset.margin + tileset.spacing) /
                          (tileset.tilewidth + tileset.spacing))
            rows = int((fheight - tileset.margin + tileset.spacing) /
                       (tileset.tileheight + tileset.spacing))

            ts_sprite = sge.Sprite.from_tileset(
                source, x=tileset.margin, y=tileset.margin, columns=columns,
                rows=rows, xsep=tileset.spacing, ysep=tileset.spacing,
                width=tileset.tilewidth, height=tileset.tileheight)

            for i in six.moves.range(ts_sprite.frames):
                if tileset.name in types:
                    tile_cls[tileset.firstgid + i] = types[tileset.name]
                t_sprite = sge.Sprite(width=tileset.tilewidth,
                                      height=tileset.tileheight)
                t_sprite.draw_sprite(ts_sprite, i, 0, 0)
                tile_sprites[tileset.firstgid + i] = t_sprite

        tileset_kwargs = {}
        for prop in tileset.properties:
            tileset_kwargs[prop.name] = _nconvert(prop.value)

        for tile in tileset.tiles:
            i = tileset.firstgid + tile.id

            if tile.image is not None:
                if tile.image.source is not None:
                    source = tile.image.source
                else:
                    _file = tempfile.NamedTemporaryFile(
                        suffix=".{}".format(tile.image.format))
                    _file.write(tile.image.data)
                    source = _file.name

                n, e = os.path.splitext(os.path.basename(source))
                d = os.path.dirname(source)
                tile_sprites[i] = sge.Sprite(n, d)

            if tileset.name in types:
                tile_cls[i] = types[tileset.name]

            tile_kwargs[i] = tileset_kwargs.copy()
            for prop in tile.properties:
                tile_kwargs[i][prop.name] = _nconvert(prop.value)

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
            default_cls = types.get(layer.name, Decoration)
            default_kwargs = {"z": z}

            for prop in layer.properties:
                default_kwargs[prop.name] = _nconvert(prop.value)

            for i in six.moves.range(len(layer.tiles)):
                tile = layer.tiles[i]
                if tile.gid:
                    cls = tile_cls.get(tile.gid, default_cls)
                    kwargs = default_kwargs.copy()
                    kwargs["sprite"] = tile_sprites.get(tile.gid)
                    if tile.hflip:
                        kwargs["image_xscale"] = -1
                    if tile.vflip:
                        kwargs["image_yscale"] = -1
                    if tile.dflip:
                        kwargs["image_yscale"] = -kwargs.get("image_yscale", 1)
                        kwargs["image_rotation"] = 90

                    for j in tile_kwargs.setdefault(tile.gid, {}):
                        kwargs[j] = tile_kwargs[tile.gid][j]

                    x = i % tilemap.width
                    y = i // tilemap.width
                    if tilemap.renderorder.startswith("left"):
                        x = tilemap.width - x - 1
                    if tilemap.renderorder.endswith("up"):
                        y = tilemap.height - y - 1

                    x *= tilemap.tilewidth
                    y *= tilemap.tileheight
                    y += tilemap.tileheight - kwargs["sprite"].height
                    objects.append(cls(x, y, **kwargs))
                    
        elif isinstance(layer, tmx.ObjectGroup):
            default_kwargs = {"z": z}

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

                if layer.color is not None:
                    if not layer.color.startswith("#"):
                        layer.color = "#" + layer.color
                    color = sge.Color(layer.color)
                else:
                    color = None

                for obj in layer.objects:
                    cls = types.get(obj.name, types.get(obj.type, default_cls))
                    kwargs = default_kwargs.copy()

                    if obj.rotation % 360:
                        kwargs["image_rotation"] = -obj.rotation

                    for prop in obj.properties:
                        kwargs[prop.name] = _nconvert(prop.value)

                    if obj.gid is not None:
                        if cls is None:
                            cls = tile_cls.get(obj.gid, Decoration)
                        kwargs["sprite"] = tile_sprites.get(obj.gid)
                        if kwargs["sprite"] is not None:
                            w = kwargs["sprite"].width
                            h = kwargs["sprite"].height
                        else:
                            w = 0
                            h = 0
                        x = (obj.x if tilemap.orientation == "orthogonal" else
                             obj.x - (w / 2))
                        y = obj.y - h

                        for i in tile_kwargs.setdefault(obj.gid, {}):
                            kwargs[i] = tile_kwargs[obj.gid][i]

                        # This is repetitive, but necessary to give
                        # object properties priority, and harmless.
                        for prop in obj.properties:
                            kwargs[prop.name] = _nconvert(prop.value)

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
                        xoff, yoff = obj.polygon[0]
                        p = [(x - xoff, y - yoff) for x, y in obj.polygon[1:]]
                        kwargs["points"] = p
                        objects.append(cls(obj.x + xoff, obj.y + yoff,
                                           **kwargs))
                    elif obj.polyline:
                        if cls is None:
                            cls = Polyline
                        xoff, yoff = obj.polyline[0]
                        p = [(x - xoff, y - yoff) for x, y in obj.polyline[1:]]
                        kwargs["points"] = p
                        objects.append(cls(obj.x + xoff, obj.y + yoff,
                                           **kwargs))
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
            kwargs = {"z": z}

            for prop in layer.properties:
                kwargs[prop.name] = _nconvert(prop.value)

            if layer.image.source is not None:
                n, e = os.path.splitext(os.path.basename(layer.image.source))
                d = os.path.dirname(layer.image.source)
                sprite = sge.Sprite(n, d)
            else:
                sprite = None
            sobj = cls(layer.x, layer.y, z, sprite=sprite, **kwargs)
            objects.append(sobj)

        z += 1

    room_kwargs = {"objects": objects, "width": room_width,
                   "height": room_height, "views": views if views else None,
                   "background": background}

    for prop in tilemap.properties:
        room_kwargs[prop.name] = _nconvert(prop.value)

    return room_cls(**room_kwargs)


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
