# xSGE Tiled Library
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

This extension provides support for loading the JSON format of the
`Tiled Map Editor <http://www.mapeditor.org/>`_.  This allows you to use
Tiled to edit your game's world (e.g. levels), rather than building a
level editor yourself.

To load a tile map, simply use :func:`load`.  See the documentation for
this function for more information.
"""


__version__ = "0.1"
__all__ = ["load"]


import json
import os

import sge
import xsge_path


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


def load(f, cls=sge.dsp.Room, types=None, z=0):
    """
    Load JSON tilemap ``f`` and return a room of the class ``cls``.

    The way the map generates the room, in general, is to convert all
    tiles, objects, and image layers into :class:`sge.dsp.Object`
    objects.  As a special exception, the object layer with the name
    "views" defines the views in the room; these objects are converted
    into :class:`sge.dsp.View` objects.

    Objects are given Z-axis positions based on the ordering of the
    layers in the map file: ``z`` is the Z-axis position of the first
    layer, and each subsequent layer's Z-axis position is the Z-axis
    position of the previous layer plus one.

    Except for views, all tiles, objects, and image layers can be
    defined to be converted into any class derived from
    :class:`sge.dsp.Object` via the ``types`` argument, which should be
    a dictionary matching strings to corresponding
    :class:`sge.dsp.Object` classes, or :const:`None`, which is
    equivalent to ``{}``.  Classes are determined in the following ways:

    - Tiles are converted to the class connected to, in order of
      preference, the name of the tileset, the type of the tileset, or
      the name of the tile layer.  If none of these values are valid
      keys in ``types``, :class:`Decoration` is used.

    - Objects are converted to the class connected to, in order of
      preference, the name of the object, the type of the object, the
      appropriate class for the respective tile if applicable (see
      above), or the name of the object group.  If none of these strings
      are valid keys in ``types``, the class used depends on what kind
      of object it is:

      - Rectangle objects default to :class:`Rectangle`.
      - Ellipse objects default to :class:`Ellipse`.
      - Polygon objects default to :class:`Polygon`.
      - Polyline objects default to :class:`Polyline`.
      - Tile objects default to :class:`Decoration`.

    - Image layers are converted to the class connected to the image
      layer's name.  If the image layer's name is not a valid key in
      ``types``, :class:`Decoration` is used.

    Property lists are passed to objects as keyword arguments in the
    following ways:

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

    .. note::

       Currently zstd compression is **not** supported. Support for zstd
       will be added later either when it makes it into the Pyhton
       Standard Library or, if that doesn't happen, when it's clear what
       zstd library to use.
    """
    room_cls = cls
    if types is None:
        types = {}

    tilemap = json.load(f)
    tilemap_width = tilemap.get("width", 1)
    tilemap_height = tilemap.get("height", 1)
    tilemap_tilewidth = tilemap.get("tilewidth", 32)
    tilemap_tileheight = tilemap.get("tileheight", 32)

    tile_cls = {}
    tile_sprites = {}
    tile_kwargs = {}
    for tileset in sorted(tilemap.get("tilesets", []),
                          key=lambda T: T.firstgid):
        source = tileset.get("image")
        firstgid = tileset.get("firstgid", 1)
        if source is not None:
            margin = tileset.get("margin", 0)
            spacing = tileset.get("spacing", 0)
            tilewidth = tileset.get("tilewidth", tilemap_tilewidth)
            tileheight = tileset.get("tileheight", tilemap_tileheight)

            n, e = os.path.splitext(os.path.basename(source))
            d = os.path.dirname(source)
            fs = sge.gfx.Sprite(n, d)
            fwidth = fs.width - margin
            fheight = fs.height - margin

            columns = int((fwidth-margin + spacing) / (tilewidth+spacing))
            rows = int((fheight-margin + spacing) / (tileheight+spacing))

            ts_sprite = sge.gfx.Sprite.from_tileset(
                source, x=margin, y=margin, columns=columns, rows=rows,
                xsep=spacing, ysep=spacing, width=tilewidth, height=tileheight)

            for i in range(ts_sprite.frames):
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
        for prop in tileset.get("properties", {}):
            tileset_kwargs[prop.get("name")] = prop.get("value")

        for tile in tileset.get("tiles", {}):
            i = firstgid + tile.get("id", 0)

            animation = tile.get("animation", [])
            if animation:
                # Use average frame rate (since the SGE can't animate
                # different frames at different rates in an easy way)
                fps = (1000 * len(animation)
                       / sum([j.get("duration", 0) for j in animation]))
                spr = sge.gfx.Sprite(width=1, height=1, fps=fps)

                while spr.frames < len(animation):
                    spr.append_frame()

                for j in range(len(animation)):
                    frame = animation[j]
                    frame_spr = tile_sprites[firstgid + frame.get(tileid, 0)]
                    w = max(spr.width, frame_spr.width)
                    h = max(spr.height, frame_spr.height)
                    if w > spr.width or h > spr.height:
                        spr.resize_canvas(w, h)
                    spr.draw_sprite(frame_spr, 0, 0, 0, frame=j)

                tile_sprites[i] = spr
            elif "image" in tile:
                source = tile["image"]
                n, e = os.path.splitext(os.path.basename(source))
                d = os.path.dirname(source)
                tile_sprites[i] = sge.gfx.Sprite(n, d)

            if tileset.setdefault("name") in types:
                tile_cls[i] = types[tileset["name"]]
            elif tileset.setdefault("type") in types:
                tile_cls[i] = types[tileset["type"]]

            tile_kwargs[i] = tileset_kwargs.copy()
            for prop in tile.get("properties", []):
                tile_kwargs[i][prop.get("name")] = prop.get("value")

    room_width = tilemap_width * tilemap_tilewidth
    room_height = tilemap_height * tilemap_tileheight

    c = tilemap.get("backgroundcolor")
    if c is not None:
        color = _get_color(c)
        background = sge.gfx.Background([], color)
    else:
        background = None

    tilemap_orientation = tilemap.get("orientation", "orthogonal")
    tilemap_renderorder = tilemap.get("renderorder", "right-down")

    objects = []
    views = []
    for layer in tilemap.get("layers", []):
        if layer.get("type") == "tilelayer":
            tile_grid_tiles = []

            default_cls = types.get(layer.get("name"), Decoration)
            default_kwargs = {"z": z}

            offsetx = layer.get("x", 0)
            offsety = layer.get("y", 0)

            for prop in layer.get("properties", []):
                default_kwargs[prop.get("name")] = prop.get("value")

            row = []
            tile_row = []

            encoding = layer.get("encoding", "csv")
            compression = layer.get("compression")
            layer_tiles = _data_decode(layer.get("data", []), encoding,
                                       compression)

            for i in range(len(layer_tiles)):
                tile = layer_tiles[i]
                gid = (tile - (tile & 2**31) - (tile & 2**30) - (tile & 2**29))
                hflip = bool(tile & 2**31)
                vflip = bool(tile & 2**30)
                dflip = bool(tile & 2**29)
                if gid:
                    cls = tile_cls.get(gid, default_cls)
                    kwargs = default_kwargs.copy()
                    kwargs["sprite"] = tile_sprites.get(gid)
                    special = False
                    if hflip:
                        kwargs["image_xscale"] = -1
                        special = True
                    if vflip:
                        kwargs["image_yscale"] = -1
                        special = True
                    if dflip:
                        kwargs["image_yscale"] = -kwargs.get("image_yscale", 1)
                        kwargs["image_rotation"] = 270
                        special = True

                    if (cls == Decoration and kwargs["sprite"] and
                            kwargs["sprite"].width == tilemap_tilewidth and
                            kwargs["sprite"].height == tilemap_tileheight and
                            not tile_kwargs.setdefault(gid, {})):
                        if special:
                            id_ = (gid, hflip, vflip, dflip)
                            spr = tile_sprites.get(id_)
                            if spr is None:
                                spr = kwargs["sprite"].copy()
                                if kwargs.get("image_xscale", 1) < 0:
                                    spr.mirror()
                                if kwargs.get("image_yscale", 1) < 0:
                                    spr.flip()
                                if kwargs.setdefault("image_rotation", 0) % 360:
                                    spr.rotate(kwargs["image_rotation"])
                                tile_sprites[id_] = spr
                        else:
                            spr = kwargs["sprite"]

                        if i % tilemap_width:
                            tile_row.append(spr)
                        else:
                            tile_grid_tiles.extend(tile_row)
                            if tilemap_renderorder.endswith("up"):
                                objects = row + objects
                            else:
                                objects.extend(row)

                            tile_row = [spr]
                            row = []
                    else:
                        for j in tile_kwargs.setdefault(gid, {}):
                            kwargs[j] = tile_kwargs[gid][j]

                        x = (i % tilemap_width) * tilemap_tilewidth
                        y = (i // tilemap_width) * tilemap_tileheight
                        y += tilemap_tileheight - kwargs["sprite"].height

                        obj = cls(x + offsetx, y + offsety, **kwargs)
                        objects.append(obj)
                        if i % tilemap_width:
                            tile_row.append(None)
                            if tilemap_renderorder.startswith("left"):
                                row.insert(0, obj)
                            else:
                                row.append(obj)
                        else:
                            tile_grid_tiles.extend(tile_row)
                            if tilemap_renderorder.endswith("up"):
                                objects = row + objects
                            else:
                                objects.extend(row)

                            tile_row = [None]
                            row = [obj]
                else:
                    if i % tilemap_width:
                        tile_row.append(None)
                    else:
                        tile_grid_tiles.extend(tile_row)
                        tile_row = [None]

            tile_grid_tiles.extend(tile_row)
            if tilemap_renderorder.endswith("up"):
                objects = row + objects
            else:
                objects.extend(row)

            if any(tile_grid_tiles):
                if tilemap_orientation == "staggered":
                    render_method = "isometric"
                else:
                    render_method = "orthogonal"

                tile_grid = sge.gfx.TileGrid(
                    tile_grid_tiles, render_method=render_method,
                    section_length=tilemap_width, tile_width=tilemap_tilewidth,
                    tile_height=tilemap_tileheight)
                objects.append(Decoration(0, 0, z, sprite=tile_grid))
        elif layer.get("type") == "objectgroup":
            default_kwargs = {"z": z}

            offsetx = layer.get("x", 0)
            offsety = layer.get("y", 0)

            for prop in layer.get("properties", []):
                default_kwargs[prop.get("name")] = prop.get("value")

            if layer.get("name") == "views":
                for obj in layer.get("objects", []):
                    x = obj.get("x", 0) + offsetx
                    y = obj.get("y", 0) + offsety
                    kwargs = default_kwargs.copy()
                    for prop in obj.get("properties", []):
                        kwargs[prop.get("name")] = prop.get("value")

                    views.append(sge.dsp.View(x, y, **kwargs))
            else:
                default_cls = types.get(layer.get("name"))

                c = layer.get("tintcolor")
                if c is not None:
                    color = _get_color(c)
                else:
                    color = None

                for obj in layer.get("objects", []):
                    cls = types.get(obj.get("name"),
                                    types.get(obj.get("type")))
                    kwargs = default_kwargs.copy()

                    rotation = obj.get("rotation", 0) % 360
                    if rotation:
                        kwargs["image_rotation"] = rotation

                    if "gid" in obj:
                        gid = obj["gid"]
                        if cls is None:
                            cls = tile_cls.get(gid)
                        kwargs["sprite"] = tile_sprites.get(gid)
                        w = obj.get("width", 0)
                        h = obj.get("height", 0)

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

                        for i in tile_kwargs.setdefault(gid, {}):
                            kwargs[i] = tile_kwargs[gid][i]

                    # This is placed down here to give object properties
                    # priority over tile properties.
                    for prop in obj.get("properties", []):
                        kwargs[prop.get("name")] = prop.get("value")

                    if cls is None:
                        cls = default_cls

                    obj_x = obj.get("x", 0)
                    obj_y = obj.get("y", 0)

                    if "gid" in obj:
                        if cls is None:
                            cls = Decoration

                        x = obj_x
                        if tilemap_orientation != "orthogonal":
                            x -= w / 2
                        y = obj_y - h

                        objects.append(cls(x + offsetx, y + offsety, **kwargs))
                    elif obj.get("ellipse"):
                        if cls is None:
                            cls = Ellipse
                        width = obj.get("width", tilemap_tilewidth)
                        height = obj.get("height", tilemap_tileheight)
                        sprite = sge.gfx.Sprite(width=width, height=height)
                        sprite.draw_ellipse(0, 0, width, height, fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj_x + offsetx, obj_y + offsety,
                                           **kwargs))
                    elif obj.setdefault("polygon", []):
                        if cls is None:
                            cls = Polygon
                        polygon = obj["polygon"]
                        xoff = polygon[0].get("x", 0)
                        yoff = polygon[0].get("y", 0)
                        p = []
                        for point in polygon[1:]:
                            x = point.get("x", 0) - xoff
                            y = point.get("y", 0) - yoff
                            p.append((x, y))
                        kwargs["points"] = p
                        objects.append(cls(obj_x + xoff + offsetx,
                                           obj_y + yoff + offsety, **kwargs))
                    elif obj.setdefault("polyline", []):
                        if cls is None:
                            cls = Polyline
                        polyline = obj["polygon"]
                        xoff = polyline[0].get("x", 0)
                        yoff = polyline[0].get("y", 0)
                        p = []
                        for point in polyline[1:]:
                            x = point.get("x", 0) - xoff
                            y = point.get("y", 0) - yoff
                            p.append((x, y))
                        kwargs["points"] = p
                        objects.append(cls(obj_x + xoff + offsetx,
                                           obj_y + yoff + offsety, **kwargs))
                    else:
                        if cls is None:
                            cls = Rectangle
                        width = obj.get("width", tilemap_tilewidth)
                        height = obj.get("height", tilemap_tileheight)
                        sprite = sge.gfx.Sprite(width=width, height=height)
                        sprite.draw_rectangle(0, 0, width, height, fill=color)
                        kwargs["sprite"] = sprite
                        objects.append(cls(obj_x + offsetx, obj_y + offsety,
                                           **kwargs))
        elif layer.get("type") == "imagelayer":
            cls = types.get(layer.get("name"), Decoration)
            kwargs = {"z": z}

            for prop in layer.get("properties"):
                kwargs[prop.get("name")] = prop.get("value")

            if "image" in layer:
                n, e = os.path.splitext(os.path.basename(layer["image"]))
                d = os.path.dirname(layer["image"])
                sprite = sge.gfx.Sprite(n, d)
            else:
                sprite = None
            sobj = cls(layer.x, layer.y, z, sprite=sprite, **kwargs)
            objects.append(sobj)

        z += 1

    room_kwargs = {"objects": objects, "width": room_width,
                   "height": room_height, "views": views if views else None,
                   "background": background}

    for prop in tilemap.get("properties"):
        room_kwargs[prop.get("name")] = prop.get("value")

    return room_cls(**room_kwargs)


def _get_color(value):
    # Return a sge.gfx.Color object corresponding to s, based on Tiled's
    # color formatting.
    if value.startswith("#"):
        value = value[1:]

    if len(value) == 6:
        r, g, b = [int(value[i:(i + 2)], 16) for i in range(0, 6, 2)]
        return sge.gfx.Color((r, g, b))
    elif len(value) == 8:
        a, r, g, b = [int(value[i:(i + 2)], 16) for i in range(0, 8, 2)]
        return sge.gfx.Color((r, g, b, a))
    else:
        raise ValueError("Invalid color string.")


def _data_decode(data, encoding, compression):
    # Decode encoded data and return a list of integers it represents.
    #
    # Arguments:
    #
    # - ``data`` -- The data to decode.
    # - ``encoding`` -- The encoding of the data.  Can be ``"base64"``
    #   or ``"csv"``.
    # - ``compression`` -- The compression method used.  Valid
    #   compression methods are ``"gzip"`` and ``"zlib"``.
    #   Set to ``None`` for no compression.
    if isinstance(data, str):
        if encoding == "csv":
            return [int(i) for i in data.strip().split(",")]
        elif encoding == "base64":
            data = base64.b64decode(data.strip().encode("latin1"))

            if compression == "gzip":
                data = gzip.decompress(data)
            elif compression == "zlib":
                data = zlib.decompress(data)
            elif compression:
                e = 'Compression type "{}" not supported.'.format(compression)
                raise ValueError(e)

            ndata = [i for i in data]

            data = []
            for i in range(0, len(ndata), 4):
                n = (ndata[i]  + ndata[i + 1] * (2 ** 8) +
                     ndata[i + 2] * (2 ** 16) + ndata[i + 3] * (2 ** 24))
                data.append(n)

            return data
        else:
            e = 'Encoding type "{}" not supported.'.format(encoding)
            raise ValueError(e)
    else:
        return data
