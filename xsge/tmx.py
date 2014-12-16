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
import tmx
import six


__all__ = ["load"]


def load(fname, cls=sge.Room, types=None, z=0):
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
            n, d, x=tileset.margin, y=tileset.margin, columns=columns,
            rows=rows, xsep=tileset.spacing, ysep=tileset.spacing,
            width=tileset.tilewidth, height=tileset.tileheight)

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
            for tile in layer.tiles:
                # TODO
                pass
        elif isinstance(layer, tmx.ObjectGroup):
            if layer.name == "views":
                for obj in layer.objects:
                    x = (obj.x if tilemap.orientation == "orthogonal" else
                         obj.x + obj.width)
                    y = obj.y - obj.height
                    xport = 0
                    yport = 0
                    wport = None
                    hport = None
                    for prop in obj.properties:
                        if prop.name == "xport":
                            xport = float(prop.value)
                        elif prop.name == "yport":
                            yport = float(prop.value)
                        elif prop.name == "wport":
                            wport = float(prop.value)
                        elif prop.name == "hport":
                            hport = float(prop.value)
                    views.append(sge.View(x, y, xport=xport, yport=yport,
                                          width=obj.width, height=obj.height,
                                          wport=wport, hport=hport))
            else:
                default_cls = types.get(layer.name, sge.Object)
                default_kwargs = {}

                if not layer.visible:
                    default_kwargs["visible"] = False

                if layer.opacity != 1:
                    default_kwargs["image_alpha"] = layer.opacity * 255

                for prop in layer.properties:
                    if prop.value.isdigit():
                        default_kwargs[prop.name] = int(prop.value)
                    else:
                        try:
                            default_kwargs[prop.name] = float(prop.value)
                        except ValueError:
                            default_kwargs[prop.name] = prop.value

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
                        if prop.value.isdigit():
                            kwargs[prop.name] = int(prop.value)
                        else:
                            try:
                                kwargs[prop.name] = float(prop.value)
                            except ValueError:
                                kwargs[prop.name] = prop.value

                    if obj.gid is not None:
                        kwargs["sprite"] = tile_sprites.get(obj.gid)
                    elif obj.ellipse:
                        sprite = sge.Sprite(width=obj.width, height=obj.height)
                        sprite.draw_ellipse(0, 0, obj.width, obj.height,
                                            outline=color)
                        kwargs["sprite"] = sprite
                    elif obj.polygon:
                        # TODO
                        pass
                    elif obj.polyline:
                        # TODO
                        pass
                    else:
                        sprite = sge.Sprite(width=obj.width, height=obj.height)
                        sprite.draw_rectangle(0, 0, obj.width, obj.height,
                                              outline=color)
                        kwargs["sprite"] = sprite
        elif isinstance(layer, tmx.ImageLayer):
            cls = types.get(layer.name, sge.Object)
            kwargs = {}

            if cls is sge.Object:
                kwargs["tangible"] = False
                kwargs["checks_collisions"] = False

            if not layer.visible:
                kwargs["visible"] = False

            if layer.opacity != 1:
                kwargs["image_alpha"] = layer.opacity * 255

            for prop in layer.properties:
                if prop.value.isdigit():
                    kwargs[prop.name] = int(prop.value)
                else:
                    try:
                        kwargs[prop.name] = float(prop.value)
                    except ValueError:
                        kwargs[prop.name] = prop.value

            sprite = sge.Sprite(layer.image.source)
            sobj = sge.Object(layer.x, layer.y, z, sprite=sprite, **kwargs)
            objects.append(sobj)

        z += 1

    return cls(objects=objects, width=room_width, height=room_height,
               views=views, background=background)
