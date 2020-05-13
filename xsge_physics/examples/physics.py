#!/usr/bin/env python3

# Physics example
#
# To the extent possible under law, the author(s) have dedicated all
# copyright and related and neighboring rights to this software to the
# public domain worldwide. This software is distributed without any
# warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
# along with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.


import sge
import xsge_physics


class Game(sge.dsp.Game):

    def event_key_press(self, key, char):
        if key == 'escape':
            self.end()

    def event_close(self):
        self.end()


class Player(xsge_physics.Collider):

    def event_step(self, time_passed, delta_mult):
        sge.game.window_text = "({}, {})".format(self.x, self.y)
        self.xvelocity = (sge.keyboard.get_pressed("right") -
                          sge.keyboard.get_pressed("left")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("down") -
                          sge.keyboard.get_pressed("up")) * 4


class Square(xsge_physics.Solid, xsge_physics.MobileWall):

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = (sge.keyboard.get_pressed("d") -
                          sge.keyboard.get_pressed("a")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("s") -
                          sge.keyboard.get_pressed("w")) * 4


class DiamondTopLeft(xsge_physics.SlopeTopLeft, xsge_physics.MobileWall):

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = (sge.keyboard.get_pressed("l") -
                          sge.keyboard.get_pressed("j")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("k") -
                          sge.keyboard.get_pressed("i")) * 4


class DiamondTopRight(xsge_physics.SlopeTopRight, xsge_physics.MobileWall):

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = (sge.keyboard.get_pressed("l") -
                          sge.keyboard.get_pressed("j")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("k") -
                          sge.keyboard.get_pressed("i")) * 4


class DiamondBottomLeft(xsge_physics.SlopeBottomLeft, xsge_physics.MobileWall):

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = (sge.keyboard.get_pressed("l") -
                          sge.keyboard.get_pressed("j")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("k") -
                          sge.keyboard.get_pressed("i")) * 4


class DiamondBottomRight(xsge_physics.SlopeBottomRight,
                         xsge_physics.MobileWall):

    def event_step(self, time_passed, delta_mult):
        self.xvelocity = (sge.keyboard.get_pressed("l") -
                          sge.keyboard.get_pressed("j")) * 4
        self.yvelocity = (sge.keyboard.get_pressed("k") -
                          sge.keyboard.get_pressed("i")) * 4


def main():
    # Create Game object
    Game(800, 600)

    # Load sprites
    square_sprite = sge.gfx.Sprite(width=32, height=32)
    square_sprite.draw_rectangle(0, 0, 32, 32, fill=sge.gfx.Color("aqua"))
    solid_sprite = sge.gfx.Sprite(width=16, height=16)
    solid_sprite.draw_rectangle(0, 0, 16, 16, fill=sge.gfx.Color("white"))
    slope1_sprite = sge.gfx.Sprite(width=32, height=16)
    slope1_sprite.draw_polygon([(0, 16), (32, 0), (32, 16)],
                               fill=sge.gfx.Color("white"))
    slope2_sprite = sge.gfx.Sprite(width=16, height=32)
    slope2_sprite.draw_polygon([(0, 0), (0, 32), (16, 32)],
                               fill=sge.gfx.Color("white"))
    slope3_sprite = sge.gfx.Sprite(width=16, height=16)
    slope3_sprite.draw_polygon([(0, 16), (16, 0), (0, 0)],
                               fill=sge.gfx.Color("white"))
    slope4_sprite = sge.gfx.Sprite(width=16, height=16)
    slope4_sprite.draw_polygon([(16, 16), (16, 0), (0, 0)],
                               fill=sge.gfx.Color("white"))
    sqwall_sprite = sge.gfx.Sprite(width=32, height=32)
    sqwall_sprite.draw_rectangle(0, 0, 32, 32, fill=sge.gfx.Color("red"))
    diamond_tl_sprite = sge.gfx.Sprite(width=16, height=16)
    diamond_tl_sprite.draw_polygon([(0, 16), (16, 16), (16, 0)],
                                   fill=sge.gfx.Color("red"))
    diamond_tr_sprite = sge.gfx.Sprite(width=16, height=16)
    diamond_tr_sprite.draw_polygon([(0, 0), (0, 16), (16, 16)],
                                   fill=sge.gfx.Color("red"))
    diamond_bl_sprite = sge.gfx.Sprite(width=16, height=16)
    diamond_bl_sprite.draw_polygon([(0, 0), (16, 0), (16, 16)],
                                   fill=sge.gfx.Color("red"))
    diamond_br_sprite = sge.gfx.Sprite(width=16, height=16)
    diamond_br_sprite.draw_polygon([(0, 0), (0, 16), (16, 0)],
                                   fill=sge.gfx.Color("red"))

    # Load backgrounds
    background = sge.gfx.Background([], sge.gfx.Color("black"))

    # Create objects
    player = Player(400, 300, 5, sprite=square_sprite)
    bottom_1 = xsge_physics.SolidTop(400, 500, 0, sprite=solid_sprite)
    bottom_2 = xsge_physics.SolidTop(416, 500, 0, sprite=solid_sprite)
    bottom_3 = xsge_physics.SolidTop(384, 500, 0, sprite=solid_sprite)
    top_1 = xsge_physics.SolidBottom(400, 100, 0, sprite=solid_sprite)
    top_2 = xsge_physics.SolidBottom(416, 100, 0, sprite=solid_sprite)
    top_3 = xsge_physics.SolidBottom(384, 100, 0, sprite=solid_sprite)
    left_1 = xsge_physics.SolidRight(100, 300, 0, sprite=solid_sprite)
    left_2 = xsge_physics.SolidRight(100, 316, 0, sprite=solid_sprite)
    left_3 = xsge_physics.SolidRight(100, 284, 0, sprite=solid_sprite)
    right_1 = xsge_physics.SolidLeft(700, 300, 0, sprite=solid_sprite)
    right_2 = xsge_physics.SolidLeft(700, 316, 0, sprite=solid_sprite)
    right_3 = xsge_physics.SolidLeft(700, 284, 0, sprite=solid_sprite)
    slope1_1 = xsge_physics.SlopeTopLeft(700, 500, 0, sprite=slope1_sprite)
    slope1_2 = xsge_physics.SlopeTopLeft(732, 484, 0, sprite=slope1_sprite)
    slope1_3 = xsge_physics.SlopeTopLeft(668, 516, 0, sprite=slope1_sprite)
    slope2_1 = xsge_physics.SlopeTopRight(100, 500, 0, sprite=slope2_sprite)
    slope2_2 = xsge_physics.SlopeTopRight(116, 532, 0, sprite=slope2_sprite)
    slope2_3 = xsge_physics.SlopeTopRight(84, 468, 0, sprite=slope2_sprite)
    slope3_1 = xsge_physics.SlopeBottomRight(100, 100, 0, sprite=slope3_sprite)
    slope3_2 = xsge_physics.SlopeBottomRight(116, 84, 0, sprite=slope3_sprite)
    slope3_3 = xsge_physics.SlopeBottomRight(84, 116, 0, sprite=slope3_sprite)
    slope4_1 = xsge_physics.SlopeBottomLeft(700, 100, 0, sprite=slope4_sprite)
    slope4_2 = xsge_physics.SlopeBottomLeft(716, 116, 0, sprite=slope4_sprite)
    slope4_3 = xsge_physics.SlopeBottomLeft(684, 84, 0, sprite=slope4_sprite)
    square = Square(10, 300, 0, sprite=sqwall_sprite)
    diamond_tl = DiamondTopLeft(700, 240, 0, sprite=diamond_tl_sprite)
    diamond_tr = DiamondTopRight(716, 240, 0, sprite=diamond_tr_sprite)
    diamond_bl = DiamondBottomLeft(700, 256, 0, sprite=diamond_bl_sprite)
    diamond_br = DiamondBottomRight(716, 256, 0, sprite=diamond_br_sprite)
    objects = [player, bottom_1, bottom_2, bottom_3, top_1, top_2, top_3,
               left_1, left_2, left_3, right_1, right_2, right_3,
               slope1_1, slope1_2, slope1_3, slope2_1, slope2_2, slope2_3,
               slope3_1, slope3_2, slope3_3, slope4_1, slope4_2, slope4_3,
               square, diamond_tl, diamond_tr, diamond_bl, diamond_br]

    # Create room
    sge.game.start_room = sge.dsp.Room(objects, background=background,
                                       object_area_width=64,
                                       object_area_height=64)

    sge.game.start()


if __name__ == "__main__":
    main()
