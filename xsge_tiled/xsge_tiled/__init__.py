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


__version__ = "1.0"
__all__ = ["load"]


import json
import os

import base64
import gzip
import sge
import xsge_path
import zlib


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


class Point(sge.dsp.Object):

    """
    Default class for point objects.  Identical to
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
        super().__init__(
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
        super().__init__(
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
        super().__init__(
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
    Load JSON tilemap ``fname`` and return a room of the class ``cls``.

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

      - Point objects default to :class:`Point`.
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
    if types is None:
        types = {}

    with open(fname, 'r') as f:
        tilemap = json.load(f)

    # Setting the default values of stuff here; other code below takes
    # advantage of this by forgoing use of get() and setdefault(), so
    # this must be retained and must be above everything else.
    room_width = (tilemap.setdefault("width", 1)
                  * tilemap.setdefault("tilewidth", 32))
    room_height = (tilemap.setdefault("height", 1)
                   * tilemap.setdefault("tileheight", 32))
    tilemap.setdefault("renderorder", "right-down")
    tilemap.setdefault("orientation", "orthogonal")

    c = tilemap.get("backgroundcolor")
    if c:
        color = t_get_color(c)
        background = sge.gfx.Background([], color)
    else:
        background = None

    tmdir = os.path.dirname(fname)

    tile_cls, tile_sprites, tile_kwargs = t_get_tilesets(tilemap, tmdir, types)

    objects = []
    views = []
    for layer in tilemap.get("layers", []):
        new_objects, new_views, z = t_parse_layer(
            layer, tilemap, tmdir, tile_cls, tile_sprites, tile_kwargs, types,
            z)
        objects.extend(new_objects)
        views.extend(new_views)

    room_kwargs = {
        "objects": objects, "width": room_width, "height": room_height,
        "views": views if views else None, "background": background}
    room_kwargs.update(t_get_properties(tilemap.get("properties", [])))

    return cls(**room_kwargs)


def t_get_tilesets(tilemap, tmdir, types):
    """
    Parse tilesets from loaded JSON data in ``tilemap``.  ``tmdir``
    indicates the directory that the data from ``tilemap`` is from.
    Returns a tuple containing the following:

    - A dictionary linking Tiled GID keys to classes found in ``types``.
    - A dictionary linking Tiled GID keys to SGE sprites.
    - A dictionary linking Tiled GID keys to keyword argument
      dictionaries based on the properties of the tileset and tiles.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
    tile_cls = {}
    tile_sprites = {}
    tile_kwargs = {}
    for tileset in tilemap.get("tilesets", []):
        # Must get this first because it's level data, not tileset data.
        firstgid = tileset.get("firstgid", 1)

        tsdir = tmdir
        if tileset.setdefault("source"):
            fname = os.path.join(tmdir, tileset["source"])
            tsdir = os.path.dirname(fname)
            with open(fname) as f:
                tileset = json.load(f)

        ts_kwargs = t_get_properties(tileset.get("properties", []))

        ts_cls = None
        if tileset.setdefault("name") in types:
            ts_cls = types[tileset["name"]]
        elif tileset.setdefault("type") in types:
            ts_cls = types[tileset["type"]]

        image = tileset.get("image")
        if image:
            image_fname = os.path.join(tsdir, image)
            margin = tileset.get("margin", 0)
            spacing = tileset.get("spacing", 0)
            tilewidth = tileset.get("tilewidth", tilemap["tilewidth"])
            tileheight = tileset.get("tileheight", tilemap["tileheight"])

            if "transparentcolor" in tileset:
                transparent = t_get_color(tileset["transparentcolor"])
            else:
                transparent = True

            name, ext = os.path.splitext(os.path.basename(image_fname))
            d = os.path.dirname(image_fname)
            raw_sprite = sge.gfx.Sprite(name, d)
            width = raw_sprite.width - 2*margin
            height = raw_sprite.height - 2*margin
            columns = int((width+spacing) / (tilewidth+spacing))
            rows = int((height+spacing) / (tileheight+spacing))

            ts_sprites = sge.gfx.Sprite.from_tileset(
                image_fname, x=margin, y=margin, columns=columns, rows=rows,
                xsep=spacing, ysep=spacing, width=tilewidth, height=tileheight,
                transparent=transparent).get_spritelist()

            for i in range(len(ts_sprites)):
                gid = firstgid + i
                tile_sprites[gid] = ts_sprites[i]
                if ts_cls:
                    tile_cls[gid] = ts_cls
                tile_kwargs[gid] = ts_kwargs.copy()

        for tile in tileset.get("tiles", []):
            gid = firstgid + tile.get("id", 0)

            if ts_cls and gid not in tile_cls:
                tile_cls[gid] = ts_cls
            if gid not in tile_kwargs:
                tile_kwargs[gid] = ts_kwargs.copy()

            animation = tile.get("animation", [])
            if animation:
                # Use average frame rate (since the SGE can't animate
                # different frames at different rates in an easy way)
                fps = (1000 * len(animation)
                       / sum([i.get("duration", 0) for i in animation]))

                sprite = sge.gfx.Sprite(width=1, height=1, fps=fps)
                while sprite.frames < len(animation):
                    sprite.append_frame()

                for i in range(len(animation)):
                    frame_gid = firstgid + animation[i].get("tileid", 0)
                    if frame_gid in tile_sprites:
                        frame_sprite = tile_sprites[frame_gid]
                        w = max(sprite.width, frame_sprite.width)
                        h = max(sprite.height, frame_sprite.height)
                        if w > sprite.width or height > sprite.height:
                            sprite.resize_canvas(w, h)
                        sprite.draw_sprite(frame_sprite, 0, 0, 0, frame=i)

                tile_sprites[gid] = sprite
            elif tile.setdefault("image"):
                image_fname = os.path.join(tsdir, tile["image"])
                name, ext = os.path.splitext(os.path.basename(image_fname))
                d = os.path.dirname(image_fname)
                tile_sprites[gid] = sge.gfx.Sprite(name, d)

            tile_kwargs[gid].update(
                t_get_properties(tile.get("properties", [])))

    return tile_cls, tile_sprites, tile_kwargs


def t_parse_layer(layer, tilemap, tmdir, tile_cls, tile_sprites, tile_kwargs,
                  types, z):
    """
    Parse a layer and return a tuple containing two values:

    - A list of objects retrieved by the layer.
    - A list of views retrieved by the layer.
    - The next z index to be used by another layer.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
    objects = []
    views = []

    type_ = layer.get("type")
    if type_ == "group":
        objects, views, z = t_parse_layer(
            layer.get("layers", []), tilemap, tmdir, tile_cls, tile_sprites,
            tile_kwargs, types, z)
    elif type_ == "tilelayer":
        default_cls = types.get(layer.get("name"), Decoration)
        default_kwargs = t_get_properties(layer.get("properties", []))

        objects.extend(t_parse_tilechunk(
            layer, tilemap, layer, tile_cls, tile_sprites, tile_kwargs,
            default_cls, default_kwargs, types, z))

        for chunk in layer.get("chunks", []):
            objects.extend(t_parse_tilechunk(
                chunk, tilemap, layer, tile_cls, tile_sprites, tile_kwargs,
                default_cls, default_kwargs, types, z))
    elif type_ == "objectgroup":
        # Note: unlike the others, we don't fall back to the Decoration
        # class here and instead leave it as None. This is because the
        # default default will depend on object type.
        default_cls = types.get(layer.get("name"))
        default_kwargs = t_get_properties(layer.get("properties", []))
        default_kwargs["z"] = z

        tx = layer.get("x", 0)
        xoffset = layer.get("offsetx", 0) + tx*tilemap["tilewidth"]
        ty = layer.get("y", 0)
        yoffset = layer.get("offsety", 0) + ty*tilemap["tileheight"]

        if layer.get("name") == "views":
            for obj in layer.get("objects", []):
                x = obj.get("x", 0) + xoffset
                y = obj.get("y", 0) + yoffset
                kwargs = default_kwargs.copy()
                kwargs.update(t_get_properties(obj.get("properties", [])))
                if obj.setdefault("width"):
                    kwargs["width"] = obj["width"]
                if obj.setdefault("height"):
                    kwargs["height"] = obj["height"]

                views.append(sge.dsp.View(x, y, **kwargs))
        else:
            c = layer.get("color")
            color = t_get_color(c) if c else None

            for obj in layer.get("objects", []):
                cls = types.get(obj.get("name"), types.get(obj.get("type")))
                kwargs = default_kwargs.copy()

                if obj.setdefault("rotation", 0) % 360:
                    kwargs["image_rotation"] = obj["rotation"]

                x = obj.get("x", 0)
                y = obj.get("y", 0)
                width = obj.get("width", 0)
                height = obj.get("height", 0)
                gid = obj.get("gid")
                if gid:
                    if cls is None:
                        cls = tile_cls.get(gid)
                    kwargs["sprite"] = tile_sprites.get(gid)
                    if kwargs["sprite"] is not None:
                        sw = kwargs["sprite"].width
                        sh = kwargs["sprite"].height
                        if not width:
                            width = sw
                        elif sw and width != sw:
                            kwargs["image_xscale"] = width / sw
                        if not height:
                            height = sh
                        elif sh and height != sh:
                            kwargs["image_yscale"] = height / sh

                    kwargs.update(tile_kwargs.get(gid, {}))

                # We do this here to ensure that non-gid objects get
                # asigned the default class if no other was picked.  We
                # do it down here to ensure that layer class doesn't
                # override gid class or object name/type class.
                if cls is None:
                    cls = default_cls

                # We do this after that other stuff to make sure
                # user-defined kwargs get priority over automatically
                # defined kwargs above, and priority over user-defined
                # tile kwargs.
                kwargs.update(t_get_properties(obj.get("properties", [])))

                if gid:
                    if cls is None:
                        cls = Decoration
                    if tilemap["orientation"] != "orthogonal":
                        x -= width / 2
                    y -= height
                    objects.append(cls(x + xoffset, y + yoffset, **kwargs))
                elif obj.get("point"):
                    if cls is None:
                        cls = Point
                    sprite = sge.gfx.Sprite(width=1, height=1)
                    sprite.draw_rectangle(0, 0, 1, 1, fill=color)
                    kwargs["sprite"] = sprite
                    objects.append(cls(x + xoffset, y + yoffset, **kwargs))
                elif obj.get("ellipse"):
                    if cls is None:
                        cls = Ellipse
                    sprite = sge.gfx.Sprite(width=width, height=height)
                    sprite.draw_ellipse(0, 0, width, height, fill=color)
                    kwargs["sprite"] = sprite
                    objects.append(cls(x + xoffset, y + yoffset, **kwargs))
                elif obj.setdefault("polygon"):
                    if cls is None:
                        cls = Polygon
                    first_point = obj["polygon"].pop(0)
                    base_x = first_point.get("x", 0)
                    base_y = first_point.get("y", 0)
                    points = []
                    for point in obj["polygon"]:
                        px = point.get("x", 0) - base_x
                        py = point.get("y", 0) - base_y
                        points.append((px, py))
                    kwargs["points"] = points
                    objects.append(cls(x + base_x + xoffset,
                                       y + base_y + yoffset, **kwargs))
                elif obj.setdefault("polyline"):
                    if cls is None:
                        cls = Polyline
                    first_point = obj["polyline"].pop(0)
                    base_x = first_point.get("x", 0)
                    base_y = first_point.get("y", 0)
                    points = []
                    for point in obj["polyline"]:
                        px = point.get("x", 0) - base_x
                        py = point.get("y", 0) - base_y
                        points.append((px, py))
                    kwargs["points"] = points
                    objects.append(cls(x + base_x + xoffset,
                                       y + base_y + yoffset, **kwargs))
                else:
                    if cls is None:
                        cls = Rectangle
                    sprite = sge.gfx.Sprite(width=width, height=height)
                    sprite.draw_rectangle(0, 0, width, height, fill=color)
                    kwargs["sprite"] = sprite
                    objects.append(cls(x + xoffset, y + yoffset, **kwargs))
    elif type_ == "imagelayer":
        cls = types.get(layer.get("name"), Decoration)
        kwargs = t_get_properties(layer.get("properties", []))
        kwargs["z"] = z

        tx = layer.get("x", 0)
        x = layer.get("offsetx", 0) + tx * tilemap["tilewidth"]
        ty = layer.get("y", 0)
        y = layer.get("offsety", 0) + ty * tilemap["tileheight"]
        image = layer.get("image")
        if image:
            fname = os.path.join(tmdir, image)
            name, ext = os.path.splitext(os.path.basename(image))
            d = os.path.dirname(fname)
            sprite = sge.gfx.Sprite(name, d)
        else:
            sprite = None

        objects.append(cls(x, y, z, sprite=sprite, **kwargs))

    z += 1
    return objects, views, z


def t_parse_tilechunk(chunk, tilemap, layer, tile_cls, tile_sprites,
                      tile_kwargs, default_cls, default_kwargs, types, z):
    """
    Parse a chunk of a layer and return a list of objects generated.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
    encoding = layer.get("encoding", "csv")
    compression = layer.get("compression")
    tiles = t_data_decode(chunk.get("data", []), encoding, compression)
    tx = chunk.get("x", 0) + layer.get("startx", 0)
    xoffset = layer.get("offsetx", 0) + tx*tilemap["tilewidth"]
    ty = chunk.get("y", 0) + layer.get("starty", 0)
    yoffset = layer.get("offsety", 0) + ty*tilemap["tileheight"]
    width = chunk.get("width", tilemap["width"])
    height = chunk.get("height", tilemap["height"])

    tile_grid_tiles = []
    objects = []

    for i in range(len(tiles)):
        if tiles[i]:
            gid, hflip, vflip, dflip = t_gid_parse(tiles[i])
            cls = tile_cls.get(gid, default_cls)
            kwargs = default_kwargs.copy()
            kwargs["z"] = z
            kwargs["sprite"] = tile_sprites.get(gid)
            if hflip:
                kwargs["image_xscale"] = -1
            if vflip:
                kwargs["image_yscale"] = -1
            if dflip:
                kwargs["image_yscale"] = -kwargs.get("image_yscale", 1)
                kwargs["image_rotation"] = 270

            if (cls == Decoration and kwargs["sprite"]
                    and kwargs["sprite"].width == tilemap["tilewidth"]
                    and kwargs["sprite"].height == tilemap["tileheight"]
                    and not tile_kwargs.setdefault(gid, {})):
                if hflip or vflip or dflip:
                    id_ = (gid, hflip, vflip, dflip)
                    sprite = tile_sprites.get(id_)
                    if sprite is None:
                        sprite = kwargs["sprite"].copy()
                        if kwargs.get("image_xscale", 1) < 0:
                            sprite.mirror()
                        if kwargs.get("image_yscale", 1) < 0:
                            sprite.flip()
                        if kwargs.setdefault("image_rotation", 0) % 360:
                            sprite.rotate(kwargs["image_rotation"])
                        tile_sprites[id_] = sprite
                else:
                    sprite = kwargs["sprite"]

                tile_grid_tiles.append(sprite)
            else:
                kwargs.update(tile_kwargs.get(gid, {}))
                x = (i % width) * tilemap["tilewidth"]
                y = (i // width) * tilemap["tileheight"]
                if kwargs["sprite"] is not None:
                    y += tilemap["tileheight"] - kwargs["sprite"].height

                obj = cls(x + xoffset, y + yoffset, **kwargs)
                objects.append(obj)

                tile_grid_tiles.append(None)
        else:
            tile_grid_tiles.append(None)

    if any(tile_grid_tiles):
        if tilemap["orientation"] == "staggered":
            render_method = "isometric"
        else:
            render_method = "orthogonal"

        tile_grid = sge.gfx.TileGrid(
            tile_grid_tiles, render_method=render_method, section_length=width,
            tile_width=tilemap["tilewidth"], tile_height=tilemap["tileheight"])
        objects.append(Decoration(xoffset, yoffset, z, sprite=tile_grid))

    return objects


def t_get_properties(properties):
    """
    Convert Tiled properties list ``properties`` into a dictionary of
    keyword arguments and return said dictionary.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
    kwargs = {}
    for property_ in properties:
        value = property_.get("value")
        type_ = property_.get("type")
        if type_ == "color":
            value = t_get_color(value)

        kwargs[property_.get("name")] = value
    return kwargs


def t_gid_parse(gid):
    """
    Parse the GID given and return a tuple with the following values:

    - The real GID without bitwise flags.
    - Whether or not the tile is horizontally flipped.
    - Whether or not the tile is vertically flipped.
    - Whether or not the tile is "diagonally" flipped.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
    rgid = (gid - (gid & 1<<31) - (gid & 1<<30) - (gid & 1<<29))
    hflip = bool(gid & 1<<31)
    vflip = bool(gid & 1<<30)
    dflip = bool(gid & 1<<29)
    return rgid, hflip, vflip, dflip


def t_get_color(value):
    """
    Return a sge.gfx.Color object corresponding to s, based on Tiled's
    color formatting.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
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


def t_data_decode(data, encoding, compression):
    """
    Decode encoded data and return a list of integers it represents.

    Arguments:

    - ``data`` -- The data to decode.
    - ``encoding`` -- The encoding of the data.  Can be ``"base64"``
      or ``"csv"``.
    - ``compression`` -- The compression method used.  Valid
      compression methods are ``"gzip"`` and ``"zlib"``.
      Set to ``None`` for no compression.

    This is a low-level function used internally by this library; you
    don't typically need to use it.
    """
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
                n = (ndata[i]  + ndata[i+1] * (2**8)
                     + ndata[i+2] * (2**16) + ndata[i+3] * (2**24))
                data.append(n)

            return data
        else:
            e = 'Encoding type "{}" not supported.'.format(encoding)
            raise ValueError(e)
    else:
        return data
