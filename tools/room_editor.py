#!/usr/bin/env python

# Stellar Room Editor
# Copyright (C) 2013 Julian Marchant <onpon4@lavabit.com>
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

"""Stellar Room Editor

A room editor for Stellar, written in SGE!

"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os
import ConfigParser as configparser
import json

import sge

DIRNAME = os.path.dirname(__file__)

SCREEN_SIZE = (1280, 960)

CURSOR_SIZE = (24, 34)
CURSOR_ORIGIN = (1, 0)

SIDE_BAR_SIZE = (74, 960)
TOP_BAR_SIZE = (1280, 74)

ICON_SIZE = (36, 36)
ICON_POS = (6, 6)

BUTTON_SIZE = (48, 48)
BUTTON_SAVE_POS = (8, 8)
BUTTON_SAVE_ALL_POS = (64, 8)
BUTTON_LOAD_POS = (120, 8)
BUTTON_GRID_POS = (232, 8)
BUTTON_SHIFT_POS = (552, 8)
BUTTON_RELOAD_RESOURCES_POS = (608, 8)
BUTTON_BACKGROUND_POS = (664, 8)
BUTTON_VIEWS_POS = (720, 8)
BUTTON_SETTINGS_POS = (776, 8)
BUTTON_ZOOM_RESET_POS = (888, 8)
BUTTON_ZOOM_OUT_POS = (944, 8)
BUTTON_ZOOM_IN_POS = (1000, 8)
BUTTON_PREVIOUS_ROOM_POS = (1112, 8)
BUTTON_NEXT_ROOM_POS = (1168, 8)
BUTTON_CLOSE_ROOM_POS = (1224, 8)
BUTTON_TOOL_POS = (8, 120)
BUTTON_CLASS_POS = (8, 232)
BUTTON_IMAGE_INDEX_POS = (8, 288)
BUTTON_IMAGE_ALPHA_POS = (8, 624)
BUTTON_IMAGE_BLEND_POS = (8, 680)
BUTTON_VISIBLE_POS = (8, 736)
BUTTON_ACTIVE_POS = (8, 798)
BUTTON_DETECTS_COLLISIONS_POS = (8, 848)
BUTTON_ARGS_POS = (8, 904)

TEXTBOX_SIZE = (60, 48)
TEXTBOX_GRID_XSIZE_POS = (288, 8)
TEXTBOX_GRID_YSIZE_POS = (388, 8)
TEXTBOX_Z_POS = (2, 344)
TEXTBOX_IMAGE_FPS_POS = (2, 400)
TEXTBOX_IMAGE_XSCALE_POS = (2, 456)
TEXTBOX_IMAGE_YSCALE_POS = (2, 512)
TEXTBOX_IMAGE_ANGLE_POS = (2, 568)

CHECKBOX_SIZE = (32, 32)
CHECKBOX_GRID_SNAP_POS = (464, 24)

sge.image_directories.append(os.path.join(DIRNAME, 'Sprites'))
sge.image_directories.append(os.path.join(DIRNAME, 'Backgrounds'))
sge.image_directories.append(os.path.join(DIRNAME, 'editor_data'))
sge.font_directories.append(os.path.join(DIRNAME, 'editor_data'))


class glob(object):

    button_sprites = {}
    text_entry_font = None
    tooltip_font = None
    tooltip_sprite = None

    sprites = []
    sprite_icons = {}
    defaults = {}


class Game(sge.Game):

    def event_game_start(self):
        self.events_active = True
        self.will_exit = False
        self.scale = 0

    def event_key_press(self, key):
        if self.events_active:
            if key == 'escape':
                self.close()

    def event_close(self):
        if self.events_active:
            self.close()

    def close(self):
        self.will_exit = True
        for room in self.rooms:
            if self.will_exit:
                room.close()
            else:
                break

        if self.will_exit:
            self.end()


class Object(sge.StellarClass):

    def __init__(self, cls, x, y, args, kwargs):
        self.cls = cls
        self.args = list(args)
        self.kwargs = kwargs
        self.defaults = glob.defaults.setdefault(cls, {})

        z = self.get_z()
        sprite = self.get_sprite()
        visible = self.get_visible()
        image_index = self.get_image_index()
        image_fps = self.get_image_fps()
        image_xscale = self.get_image_xscale()
        image_yscale = self.get_image_yscale()
        image_rotation = self.get_image_rotation()
        image_alpha = self.get_image_alpha()
        image_blend = self.get_image_blend()

        super(Object, self).__init__(
            x, y, z, sprite=sprite, active=False, detects_collisions=False,
            visible=visible, image_index=image_index, image_fps=image_fps,
            image_xscale=image_xscale, image_yscale=image_yscale,
            image_rotation=image_rotation, image_alpha=image_alpha,
            image_blend=image_blend)

    def refresh(self):
        self.sprite = self.get_sprite()
        self.image_index = self.get_image_index()
        self.image_fps = self.get_image_fps()
        self.image_xscale = self.get_image_xscale()
        self.image_yscale = self.get_image_yscale()
        self.image_rotation = self.get_image_rotation()
        self.image_alpha = self.get_image_alpha()
        self.image_blend = self.get_image_blend()

        if not self.get_visible():
            self.image_blend = 'black'
            self.image_alpha = 128

    def get_z(self):
        if 'z' in self.kwargs:
            return eval(self.kwargs['z'])
        elif 'z' in self.defaults:
            return eval(self.defaults['z'])
        else:
            return 0

    def get_sprite(self):
        if 'sprite' in self.kwargs:
            return eval(self.kwargs['sprite'])
        elif 'sprite' in self.defaults:
            return eval(self.defaults['sprite'])
        else:
            return 'stellar_room_editor_nosprite'

    def get_visible(self):
        if 'visible' in self.kwargs:
            return eval(self.kwargs['visible'])
        elif 'visible' in self.defaults:
            return eval(self.defaults['visible'])
        else:
            return True

    def get_image_index(self):
        if 'image_index' in self.kwargs:
            return eval(self.kwargs['image_index'])
        elif 'image_index' in self.defaults:
            return eval(self.defaults['image_index'])
        else:
            return 0

    def get_image_fps(self):
        if 'image_fps' in self.kwargs:
            return eval(self.kwargs['image_fps'])
        elif 'image_fps' in self.defaults:
            return eval(self.defaults['image_fps'])
        else:
            return None

    def get_image_xscale(self):
        if 'image_xscale' in self.kwargs:
            return eval(self.kwargs['image_xscale'])
        elif 'image_xscale' in self.defaults:
            return eval(self.defaults['image_xscale'])
        else:
            return 1

    def get_image_yscale(self):
        if 'image_yscale' in self.kwargs:
            return eval(self.kwargs['image_yscale'])
        elif 'image_yscale' in self.defaults:
            return eval(self.defaults['image_yscale'])
        else:
            return 1

    def get_image_rotation(self):
        if 'image_rotation' in self.kwargs:
            return eval(self.kwargs['image_rotation'])
        elif 'image_rotation' in self.defaults:
            return eval(self.defaults['image_rotation'])
        else:
            return 0

    def get_image_alpha(self):
        if 'image_alpha' in self.kwargs:
            return eval(self.kwargs['image_alpha'])
        elif 'image_alpha' in self.defaults:
            return eval(self.defaults['image_alpha'])
        else:
            return 255

    def get_image_blend(self):
        if 'image_blend' in self.kwargs:
            return eval(self.kwargs['image_blend'])
        elif 'image_blend' in self.defaults:
            return eval(self.defaults['image_blend'])
        else:
            return None


class Button(sge.StellarClass):

    def __init__(self, x, y, icon, tooltip):
        self.icon = icon
        self.tooltip = tooltip

        super(Button, self).__init__(x, y, sprite='stellar_room_editor_button',
                                     collision_precise=True)

    def do_effect(self):
        """Do the effect of pressing this button."""
        pass

    def event_create(self):
        self.pressed = False
        self.icon_object = sge.StellarClass.create(
            self.x + ICON_POS[0], self.y + ICON_POS[1], self.z + 1,
            sprite=self.icon)

    def event_step(self, time_passed):
        if self.pressed and self.collides(sge.game.mouse):
            self.image_index = 1
        else:
            self.image_index = 0

        self.icon_object.sprite = self.icon

    def event_mouse_move(self, x, y):
        pass

    def event_mouse_button_press(self, button):
        if button == 'left' and self.collides(sge.game.mouse):
            self.pressed = True

    def event_mouse_button_release(self, button):
        if button == 'left' and self.collides(sge.game.mouse):
            self.do_effect()


class Tooltip(sge.StellarClass):

    def __init__(self):
        super(Tooltip, self).__init__(0, 0, sprite=glob.tooltip_sprite)

    def event_step(self, time_passed):
        view = sge.game.current_room.views[0]
        self.bbox_right = view.x + view.width
        self.bbox_bottom = view.y + view.height

        if self.collides(sge.game.mouse):
            self.bbox_left = view.x


class Room(sge.Room):

    def __init__(self, *args, **kwargs):
        super(Room, self).__init__(*args, **kwargs)
        self.fname = None
        self.empty = True
        self.unchanged = True
        self.opened = True
        self.name = ""
        self.cls = "sge.Room"
        self.args = []
        self.kwargs = {}

    def save(self, fname):
        # Save settings to a file
        config = {'settings': {}, 'views': [], 'objects': []}
        config['settings']['class'] = self.cls
        config['settings']['name'] = self.name
        config['settings']['width'] = self.width
        config['settings']['height'] = self.height
        config['settings']['background'] = self.background.id
        config['settings']['background_x'] = self.background_x
        config['settings']['background_y'] = self.background_y
        config['settings']['args'] = self.args
        config['settings']['kwargs'] = self.kwargs

        for view in self.views:
            config['views'].append(
                {'x': view.x, 'y': view.y, 'xport': view.xport,
                 'yport': view.yport, 'width': view.width,
                 'height': view.height})

        for obj in self.objects:
            config['objects'].append(
                {'class': obj.cls, 'x': obj.x, 'y': obj.y, 'z': obj.z,
                 'args': obj.args, 'kwargs': obj.kwargs})

        if fname is None:
            fname = self.fname

        with open(fname, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

        self.unchanged = True

    def close(self):
        if self.unchanged:
            self.opened = False
            sge.game.room_goto_next()
        else:
            m = "Save changes to {0} before closing?".format(self.name)
            answer = sge.show_message(m, ("Cancel", "No", "Yes"), 2)
            if answer != 0:
                if answer == 2:
                    self.save(None)

                self.opened = False
                sge.game.room_goto_next()

    @classmethod
    def load(cls, fname):
        # Load settings from file and return the resulting room.
        config = {}
        with open(fname 'r') as f:
            config = json.load(f)

        settings = config.setdefault('settings', {})
        cls = settings.setdefault('class', 'sge.Room')
        name = settings.setdefault('name', '')
        width = settings.setdefault('width')
        height = settings.setdefault('height')
        background = settings.setdefault('background')
        background_x = settings.setdefault('background_x', 0)
        background_y = settings.setdefault('background_y', 0)
        args = settings.setdefault('args', [])
        kwargs = settings.setdefault('kwargs', {})

        view_settings = config.setdefault('views')
        if view_settings:
            views = []
            for view in view_settings:
                views.append(sge.View(
                    view.setdefault('x', 0), view.setdefault('y', 0),
                    view.setdefault('xport', 0), view.setdefault('yport', 0),
                    view.setdefault('width'), view.setdefault('height')))
        else:
            views = None

        object_settings = config.setdefault('objects', [])
        objects = []
        for obj in object_settings:
            objects.append(Object(
                obj.setdefault('class', sge.StellarClass),
                obj.setdefault('x', 0), obj.setdefault('y', 0),
                obj.setdefault('z', 0), obj.setdefault('args', []),
                obj.setdefault('kwargs', {})))

        if sge.game.current_room.empty:
            new_room = sge.game.current_room
        else:
            for room in sge.game.rooms:
                if room.name == name:
                    room.opened = True
                    return room

            new_room = cls(objects, width, height, views, background,
                           background_x, background_y)

        new_room.fname = fname
        new_room.cls = cls
        new_room.name = name
        new_room.empty = False
        new_room.opened = True

        return new_room


def set_tooltip(text):
    """Set the text of the tooltip.  Set to None for no tooltip."""
    glob.tooltip_sprite.draw_clear()
    if text:
        w, h = glob.tooltip_font.get_size(text)
        w += 4
        h += 4
        glob.tooltip_sprite.width = w
        glob.tooltip_sprite.height = h
        glob.tooltip_sprite.draw_rectangle(0, 0, w, h, "#C8AD7F", "black")
        glob.tooltip_sprite.draw_text(glob.tooltip_font, text, 2, 2)


def load_resources():
    """Load or reload the sprites, backgrounds, and objects."""
    # Load sprites
    sge.Sprite('save', width=ICON_HEIGHT, height=ICON_HEIGHT)
    sge.Sprite('folder', width=ICON_HEIGHT, height=ICON_HEIGHT)

    config_files = []
    for d in sge.image_directories:
        config_files.append(os.path.join(d, 'spriteconfig.ini'))

    sprites_config = configparser.ConfigParser()
    sprites_config.read(config_files)
    option_arguments = {'xorig': 'origin_x', 'yorig': 'origin_y'}

    for section in sprites_config.sections():
        kwargs = {'name': section}

        for option in sprite_config.options(section):
            value = sge.sprite_config.get(section, option)
            key = option_arguments.setdefault(option, option)
            kwargs['key'] = value

        try:
            sge.Sprite(**kwargs)
            sprite_name = kwargs['name']
            glob.sprites.append(sprite_name)
        except IOError:
            pass

    # Load backgrounds
    config_file = None
    for d in sge.image_directories:
        cfg = os.path.join(d, 'backgrounds.json')
        if os.path.isfile(cfg):
            config_file = cfg

    if config_file is not None:
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}

    config.setdefault('layers', {})
    config.setdefault('backgrounds', {})
    layers = {}
    filler = sge.Sprite()

    for i in config['layers']:
        layer = config['layers'][i]
        layers[i] = sge.BackgroundLayer(
            layer.setdefault('sprite', filler), layer.setdefault('x', 0),
            layer.setdefault('y', 0), layer.setdefault('z', 0),
            layer.setdefault('xscroll_rate', 1),
            layer.setdefault('yscroll_rate', 1),
            layer.setdefault('xrepeat', True),
            layer.setdefault('yrepeat', False))

    for i in config['backgrounds']:
        bg = config['backgrounds'][i]
        bg_layers = []
        for layer in bg['layers']:
            bg_layers.append(layers[layer])
        sge.Background(bg_layers, bg['color'], i)

    # Load class defaults
    glob.defaults = {}
    classes_dir = os.path.join(DIRNAME, 'Objects')
    if os.path.isdir(classes_dir):
        files = os.listdir(classes_dir)
        for fname in files:
            config = configparser.ConfigParser()
            success = config.read(os.path.join(classes_dir, fname))

            if success:
                try:
                    sprite = config.get('data', 'sprite')
                    if sprite == '<no sprite>':
                        sprite = None
                except (configparser.NoSectionError, configparser.NoOptionError):
                    sprite = None

                try:
                    z = config.get('data', 'z')
                except (configparser.NoSectionError, configparser.NoOptionError):
                    z = 0

                classname = os.path.splitext(fname)[0]
                glob.defaults[classname]


def main(*args):
    # Create Game object
    Game(*SCREEN_SIZE, scale=0.5, scale_smooth=True)

    # Load editor resources
    # Sprites
    sge.Sprite('stellar_room_editor_cursor', *CURSOR_SIZE,
               origin_x=CURSOR_ORIGIN[0], origin_y=CURSOR_ORIGIN[1])
    sge.Sprite('stellar_room_editor_panel_left', *SIDE_BAR_SIZE)
    sge.Sprite('stellar_room_editor_panel_top', *TOP_BAR_SIZE)
    sge.Sprite('stellar_room_editor_button', *BUTTON_SIZE, fps=0)
    sge.Sprite('stellar_room_editor_textbox', *TEXTBOX_SIZE)
    sge.Sprite('stellar_room_editor_checkbox', *CHECKBOX_SIZE, fps=0)
    sge.Sprite('stellar_room_editor_icon_active', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_args', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_background', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_close', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_grid', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_grid_isometric', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_image_settings', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_inactive', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_load', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_reload_resources', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_room_next', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_room_previous', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_save', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_save_all', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_settings', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_shift', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_solid', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_tool_fill', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_tool_line', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_tool_paintbrush', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_tool_pointer', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_unsolid', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_views', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_zoom_in', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_zoom_out', *ICON_SIZE)
    sge.Sprite('stellar_room_editor_icon_zoom_reset', *ICON_SIZE)
    glob.tooltip_sprite = sge.Sprite()

    # Fonts
    glob.text_entry_font = sge.Font('OSP-DIN.ttf', 20)
    glob.tooltip_font = sge.Font('OSP-DIN.ttf', 16)

    # Set mouse cursor
    sge.game.mouse.sprite = 'stellar_room_editor_cursor'

    # Load game resources
    load_resources()

    # Create rooms
    for arg in args[1:]:
        Room.load(arg)

    if not sge.game.rooms:
        Room()

    sge.game.start()


if __name__ == '__main__':
    main(*sys.argv)
