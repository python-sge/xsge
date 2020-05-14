#!/usr/bin/env python3

# Platformer example
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


import os

import ulvl

import sge
import xsge_physics


DATA = os.path.join(os.path.dirname(__file__), "data")

WALK_ACCEL = 0.5
WALK_SPEED = 5
FRICTION = 0.25
FALL_ACCEL = 0.25
FALL_SPEED = 10
JUMP_SPEED = 6
SLIDE_ACCEL = 1
SLIDE_SPEED = 2


class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Player(xsge_physics.Collider):

    on_floor = False
    on_slope = False

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("sprite", tile_sprites[1])
        kwargs["bbox_x"] = 4
        kwargs["bbox_width"] = 8
        super().__init__(*args, **kwargs)

    def event_step(self, time_passed, delta_mult):
        self.on_floor = self.get_bottom_touching_wall()
        self.on_slope = (not self.on_floor and self.get_bottom_touching_slope())

        self.xvelocity += (sge.keyboard.get_pressed("right") -
                           sge.keyboard.get_pressed("left")) * WALK_ACCEL

        if self.xvelocity > FRICTION:
            self.xvelocity -= FRICTION
        elif self.xvelocity < -FRICTION:
            self.xvelocity += FRICTION
        else:
            self.xvelocity = 0

        if self.xvelocity > WALK_SPEED:
            self.xvelocity = WALK_SPEED
        elif self.xvelocity < -WALK_SPEED:
            self.xvelocity = -WALK_SPEED

        if self.on_slope:
            if self.yvelocity > SLIDE_SPEED + SLIDE_ACCEL:
                self.yvelocity -= SLIDE_ACCEL
            elif self.yvelocity < SLIDE_SPEED - SLIDE_ACCEL:
                self.yvelocity += SLIDE_ACCEL
            else:
                self.yvelocity = SLIDE_SPEED
        elif not self.on_floor:
            self.yvelocity += FALL_ACCEL

            if self.yvelocity > FALL_SPEED:
                self.yvelocity = FALL_SPEED

    def event_key_press(self, key, char):
        if key == "up":
            if self.on_floor or self.on_slope:
                self.yvelocity = -JUMP_SPEED

    def event_physics_collision_left(self, other, move_loss):
        if isinstance(other, xsge_physics.SolidRight):
            self.xvelocity = 0

    def event_physics_collision_right(self, other, move_loss):
        if isinstance(other, xsge_physics.SolidLeft):
            self.xvelocity = 0

    def event_physics_collision_top(self, other, move_loss):
        if isinstance(other, (xsge_physics.SolidBottom,
                              xsge_physics.SlopeBottomLeft,
                              xsge_physics.SlopeBottomRight)):
            self.yvelocity = 0

    def event_physics_collision_bottom(self, other, move_loss):
        if isinstance(other, xsge_physics.SolidTop):
            self.yvelocity = 0


class Solid(xsge_physics.Solid):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


class SolidTop(xsge_physics.SolidTop):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


class SlopeTopLeft(xsge_physics.SlopeTopLeft):

    xsticky_top = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


class SlopeTopRight(xsge_physics.SlopeTopRight):

    xsticky_top = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


class SlopeBottomLeft(xsge_physics.SlopeBottomLeft):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


class SlopeBottomRight(xsge_physics.SlopeBottomRight):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("visible", False)
        kwargs.setdefault("checks_collisions", False)
        super().__init__(*args, **kwargs)


Game(640, 480)

types = {"player": Player, "solid": Solid, "unisolid": SolidTop,
         "slope_topleft": SlopeTopLeft, "slope_topright": SlopeTopRight,
         "slope_bottomleft": SlopeBottomLeft,
         "slope_bottomright": SlopeBottomRight}

tmx = ulvl.TMX.load(os.path.join(DATA, "level.tmx"))
tilewidth = tmx.meta["tilewidth"]
tileheight = tmx.meta["tileheight"]
width = tmx.meta["width"] * tilewidth
height = tmx.meta["height"] * tileheight
backgroundcolor = tmx.meta.get("backgroundcolor", "gray")

tile_sprites = sge.gfx.Sprite.from_tileset(
    os.path.join(DATA, "tiles.png"), x=2, y=2, columns=5, rows=4, xsep=1,
    ysep=1, width=16, height=16).get_spritelist()

layers = []
for dlayer in tmx.layers:
    tiles = []
    for i in range(len(dlayer.tiles)):
        tid = dlayer.tiles[i]
        if tid:
            tiles.append(tile_sprites[tid - 1])
        else:
            tiles.append(None)
    tilegrid = sge.gfx.TileGrid(tiles, section_length=dlayer.columns,
                                tile_width=tilewidth, tile_height=tileheight)
    layers.append(sge.gfx.BackgroundLayer(tilegrid, 0, 0))
background = sge.gfx.Background(layers, sge.gfx.Color(backgroundcolor))

objects = []
for obj in tmx.objects:
    cls = types[obj.type]
    x = obj.meta["x"]
    y = obj.meta["y"]
    if "gid" in obj.meta:
        x -= tilewidth - 2
        y -= tileheight
    width = obj.meta.get("width")
    height = obj.meta.get("height")
    objects.append(cls(x, y, bbox_x=0, bbox_y=0, bbox_width=width,
                       bbox_height=height))

sge.game.start_room = sge.dsp.Room(objects=objects, width=width, height=height,
                                   background=background)


if __name__ == "__main__":
    sge.game.start()
