# xSGE TMX Library
# Copyright (c) 2014-2016 Julie Marchant <onpon4@riseup.net>
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

__version__ = "1.1"

import os

import sge
import six
import tmx
import xsge_path


__all__ = ["load"]


class Decoration(sge.dsp.Object):

    """
    Default class for tiles and image layers.  Identical to
    :class:`sge.dsp.Object`, except that it is intangible and doesn't
    check for collisions by default.
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
                 image_blend=None, image_blend_mode=None):
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
            image_alpha=image_alpha, image_blend=image_blend,
            image_blend_mode=image_blend_mode)


class Rectangle(sge.dsp.Object):

    """
    Default class for rectangle objects.  Identical to
    :class:`sge.dsp.Object`, except that it is invisible by default.
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
                 image_blend=None, image_blend_mode=None):
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
            image_alpha=image_alpha, image_blend=image_blend,
            image_blend_mode=image_blend_mode)


class Ellipse(sge.dsp.Object):

    """
    Default class for ellipse objects.  Identical to
    :class:`sge.dsp.Object`, except that it is invisible and uses
    ellipse collision detection by default.
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
                 image_blend=None, image_blend_mode=None):
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
            image_alpha=image_alpha, image_blend=image_blend,
            image_blend_mode=image_blend_mode)


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


def load(fname, cls=sge.dsp.Room, types=None, z=0):
    """
    Load the TMX file ``fname`` and return a room of the class ``cls``.

    The way the map generates the room, in general, is to convert all
    tiles, objects, and image layers into :class:`sge.dsp.Object`
    objects.  As a special exception, the object layer with the name
    "views" defines the views in the room; these objects are converted
    into :class:`sge.dsp.View` objects.

    Objects are given Z-axis positions based on the ordering of the
    layers in the TMX file: ``z`` is the Z-axis position of the first
    layer, and each subsequent layer's Z-axis position is the Z-axis
    position of the previous layer plus one.

    Except for views, all tiles, objects, and image layers can be
    defined to be converted into any class derived from
    :class:`sge.dsp.Object` via the ``types`` argument, which should be
    a dictionary matching strings to corresponding
    :class:`sge.dsp.Object` classes, or :const:`None`, which is
    equivalent to ``{}``.  Classes are determined in the following ways:

    - Tiles are converted to the class connected to, in order of
      preference, the name of the tileset or the name of the tile layer.
      If neither of these strings are valid keys in ``types``,
      :class:`xsge_tmx.Decoration` is used.

    - Objects are converted to the class connected to, in order of
      preference, the name of the object, the type of the object, the
      appropriate class for the respective tile if applicable (see
      above), or the name of the object group.  If none of these strings
      are valid keys in ``types``, the class used depends on what kind
      of object it is:

      - Rectangle objects default to :class:`xsge_tmx.Rectangle`.
      - Ellipse objects default to :class:`xsge_tmx.Ellipse`.
      - Polygon objects default to :class:`xsge_tmx.Polygon`.
      - Polyline objects default to :class:`xsge_tmx.Polyline`.
      - Tile objects default to :class:`xsge_tmx.Decoration`.

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
    for tileset in sorted(tilemap.tilesets, key=lambda T: T.firstgid):
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
            fs = sge.gfx.Sprite(n, d)
            fwidth = fs.width - tileset.margin
            fheight = fs.height - tileset.margin

            columns = int((fwidth - tileset.margin + tileset.spacing) /
                          (tileset.tilewidth + tileset.spacing))
            rows = int((fheight - tileset.margin + tileset.spacing) /
                       (tileset.tileheight + tileset.spacing))

            ts_sprite = sge.gfx.Sprite.from_tileset(
                source, x=tileset.margin, y=tileset.margin, columns=columns,
                rows=rows, xsep=tileset.spacing, ysep=tileset.spacing,
                width=tileset.tilewidth, height=tileset.tileheight)

            for i in six.moves.range(ts_sprite.frames):
                gid = tileset.firstgid + i
                if tileset.name in types:
                    tile_cls[gid] = types[tileset.name]
                elif gid in tile_cls:
                    del tile_cls[gid]
                if gid in tile_kwargs:
                    del tile_kwargs[gid]
                t_sprite = sge.gfx.Sprite(width=tileset.tilewidth,
                                          height=tileset.tileheight)
                t_sprite.draw_sprite(ts_sprite, i, 0, 0)
                tile_sprites[gid] = t_sprite

        tileset_kwargs = {}
        for prop in tileset.properties:
            tileset_kwargs[prop.name] = _nconvert(prop.value)

        for tile in tileset.tiles:
            i = tileset.firstgid + tile.id

            if tile.animation:
                # Use average frame rate (since the SGE can't animate
                # different frames at different rates in an easy way)
                fps = (1000 * len(tile.animation) /
                       sum([j.duration for j in tile.animation]))
                spr = sge.gfx.Sprite(width=1, height=1, fps=fps)

                while spr.frames < len(tile.animation):
                    spr.append_frame()

                for j in six.moves.range(len(tile.animation)):
                    frame = tile.animation[j]
                    frame_spr = tile_sprites[tileset.firstgid + frame.tileid]
                    w = max(spr.width, frame_spr.width)
                    h = max(spr.height, frame_spr.height)
                    if w > spr.width or h > spr.height:
                        spr.resize_canvas(w, h)
                    spr.draw_sprite(frame_spr, 0, 0, 0, frame=j)

                tile_sprites[i] = spr
                    
            elif tile.image is not None:
                if tile.image.source is not None:
                    source = tile.image.source
                else:
                    _file = tempfile.NamedTemporaryFile(
                        suffix=".{}".format(tile.image.format))
                    _file.write(tile.image.data)
                    source = _file.name

                n, e = os.path.splitext(os.path.basename(source))
                d = os.path.dirname(source)
                tile_sprites[i] = sge.gfx.Sprite(n, d)

            if tileset.name in types:
                tile_cls[i] = types[tileset.name]

            tile_kwargs[i] = tileset_kwargs.copy()
            for prop in tile.properties:
                tile_kwargs[i][prop.name] = _nconvert(prop.value)

    room_width = tilemap.width * tilemap.tilewidth
    room_height = tilemap.height * tilemap.tileheight

    c = tilemap.backgroundcolor
    if c is not None:
        color = sge.gfx.Color((c.red, c.green, c.blue))
        background = sge.gfx.Background([], color)
    else:
        background = None

    objects = []
    views = []
    for layer in tilemap.layers:
        if isinstance(layer, tmx.Layer):
            tile_grid_tiles = []

            default_cls = types.get(layer.name, Decoration)
            default_kwargs = {"z": z}

            offsetx = layer.offsetx
            offsety = layer.offsety

            for prop in layer.properties:
                default_kwargs[prop.name] = _nconvert(prop.value)

            row = []
            tile_row = []

            for i in six.moves.range(len(layer.tiles)):
                tile = layer.tiles[i]
                if tile.gid:
                    cls = tile_cls.get(tile.gid, default_cls)
                    kwargs = default_kwargs.copy()
                    kwargs["sprite"] = tile_sprites.get(tile.gid)
                    special = False
                    if tile.hflip:
                        kwargs["image_xscale"] = -1
                        special = True
                    if tile.vflip:
                        kwargs["image_yscale"] = -1
                        special = True
                    if tile.dflip:
                        kwargs["image_yscale"] = -kwargs.get("image_yscale", 1)
                        kwargs["image_rotation"] = 270
                        special = True

                    if (cls == Decoration and kwargs["sprite"] and
                            kwargs["sprite"].width == tilemap.tilewidth and
                            kwargs["sprite"].height == tilemap.tileheight and
                            not tile_kwargs.setdefault(tile.gid, {})):
                        if special:
                            id_ = (tile.gid, tile.hflip, tile.vflip, tile.dflip)
                            spr = tile_sprites.get(id_)
                            if spr is None:
                                spr = kwargs["sprite"].copy()
                                if kwargs["image_xscale"] < 0:
                                    spr.mirror()
                                if kwargs["image_yscale"] < 0:
                                    spr.flip()
                                if kwargs["image_rotation"] % 360:
                                    spr.rotate(kwargs["image_rotation"])
                                tile_sprites[id_] = spr
                        else:
                            spr = kwargs["sprite"]

                        if i % tilemap.width:
                            tile_row.append(spr)
                        else:
                            tile_grid_tiles.extend(tile_row)
                            if tilemap.renderorder.endswith("up"):
                                objects = row + objects
                            else:
                                objects.extend(row)

                            tile_row = [spr]
                            row = []
                    else:
                        for j in tile_kwargs.setdefault(tile.gid, {}):
                            kwargs[j] = tile_kwargs[tile.gid][j]

                        x = (i % tilemap.width) * tilemap.tilewidth
                        y = (i // tilemap.width) * tilemap.tileheight
                        y += tilemap.tileheight - kwargs["sprite"].height

                        obj = cls(x + offsetx, y + offsety, **kwargs)
                        objects.append(obj)
                        if i % tilemap.width:
                            tile_row.append(None)
                            if tilemap.renderorder.startswith("left"):
                                row.insert(0, obj)
                            else:
                                row.append(obj)
                        else:
                            tile_grid_tiles.extend(tile_row)
                            if tilemap.renderorder.endswith("up"):
                                objects = row + objects
                            else:
                                objects.extend(row)

                            tile_row = [None]
                            row = [obj]
                else:
                    if i % tilemap.width:
                        tile_row.append(None)
                    else:
                        tile_grid_tiles.extend(tile_row)
                        tile_row = [None]

            tile_grid_tiles.extend(tile_row)
            if tilemap.renderorder.endswith("up"):
                objects = row + objects
            else:
                objects.extend(row)

            if any(tile_grid_tiles):
                if tilemap.orientation == "staggered":
                    render_method = "isometric"
                else:
                    render_method = "orthogonal"

                tile_grid = sge.gfx.TileGrid(
                    tile_grid_tiles, render_method=render_method,
                    section_length=tilemap.width, tile_width=tilemap.tilewidth,
                    tile_height=tilemap.tileheight)
                objects.append(Decoration(0, 0, z, sprite=tile_grid))
                    
        elif isinstance(layer, tmx.ObjectGroup):
            default_kwargs = {"z": z}

            offsetx = layer.offsetx
            offsety = layer.offsety

            for prop in layer.properties:
                default_kwargs[prop.name] = _nconvert(prop.value)

            if layer.name == "views":
                for obj in layer.objects:
                    kwargs = default_kwargs.copy()
                    for prop in obj.properties:
                        kwargs[prop.name] = _nconvert(prop.value)

                    views.append(sge.dsp.View(obj.x + offsetx, obj.y + offsety,
                                              **kwargs))
            else:
                default_cls = types.get(layer.name)

                c = layer.color
                if c is not None:
                    color = sge.gfx.Color((c.red, c.green, c.blue))
                else:
                    color = None

                for obj in layer.objects:
                    cls = types.get(obj.name, types.get(obj.type))
                    kwargs = default_kwargs.copy()

                    if obj.rotation % 360:
                        kwargs["image_rotation"] = obj.rotation

                    for prop in obj.properties:
                        kwargs[prop.name] = _nconvert(prop.value)

                    if obj.gid is not None:
                        if cls is None:
                            cls = tile_cls.get(obj.gid)
                        kwargs["sprite"] = tile_sprites.get(obj.gid)
                        w = obj.width
                        h = obj.height

                        if kwargs["sprite"] is not None:
                            sw = kwargs["sprite"].width
                            sh = kwargs["sprite"].height
                            if not w:
                                w = sw
                            elif w != sw:
                                kwargs["image_xscale"] = w / sw
                            if not h:
                                h = sh
                            elif h != sh:
                                kwargs["image_yscale"] = h / sh

                        for i in tile_kwargs.setdefault(obj.gid, {}):
                            kwargs[i] = tile_kwargs[obj.gid][i]

                        # This is repetitive, but necessary to give
                        # object properties priority, and harmless.
                        for prop in obj.properties:
                            kwargs[prop.name] = _nconvert(prop.value)

                    if cls is None:
                        cls = default_cls

                    if obj.gid is not None:
                        if cls is None:
                            cls = Decoration

                        x = (obj.x if tilemap.orientation == "orthogonal" else
                             obj.x - (w / 2))
                        y = obj.y - h

                        objects.append(cls(x + offsetx, y + offsety, **kwargs))
                    elif obj.ellipse:
                        if cls is None:
                            cls = Ellipse
                        sprite = sge.gfx.Sprite(width=obj.width,
                                                height=obj.height)
                        sprite.draw_ellipse(0, 0, obj.width, obj.height,
                                            fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj.x + offsetx, obj.y + offsety,
                                           **kwargs))
                    elif obj.polygon:
                        if cls is None:
                            cls = Polygon
                        xoff, yoff = obj.polygon[0]
                        p = [(x - xoff, y - yoff) for x, y in obj.polygon[1:]]
                        kwargs["points"] = p
                        objects.append(cls(obj.x + xoff + offsetx,
                                           obj.y + yoff + offsety, **kwargs))
                    elif obj.polyline:
                        if cls is None:
                            cls = Polyline
                        xoff, yoff = obj.polyline[0]
                        p = [(x - xoff, y - yoff) for x, y in obj.polyline[1:]]
                        kwargs["points"] = p
                        objects.append(cls(obj.x + xoff + offsetx,
                                           obj.y + yoff + offsety, **kwargs))
                    else:
                        if cls is None:
                            cls = Rectangle
                        sprite = sge.gfx.Sprite(width=obj.width,
                                                height=obj.height)
                        sprite.draw_rectangle(0, 0, obj.width, obj.height,
                                              fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj.x + offsetx, obj.y + offsety,
                                           **kwargs))
        elif isinstance(layer, tmx.ImageLayer):
            cls = types.get(layer.name, Decoration)
            kwargs = {"z": z}

            for prop in layer.properties:
                kwargs[prop.name] = _nconvert(prop.value)

            if layer.image.source is not None:
                n, e = os.path.splitext(os.path.basename(layer.image.source))
                d = os.path.dirname(layer.image.source)
                sprite = sge.gfx.Sprite(n, d)
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
