# xSGE Menu Framework
# Copyright (c) 2015 Julian Marchant <onpon4@riseup.net>
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
This module provides a framework for menus navigated by the keyboard or
gamepad.

.. data:: joystick_threshold

   The amount of tilt on a joystick axis that is needed to change the
   menu selection.  Default is ``0.7``.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import six
import sge


__all__ = []


joystick_threshold = 0.7


class Menu(sge.Object):

    """
    Class for menus.

    Menus are objects which contain :class:`xsge.menu.Item` objects.
    The items can be cycled through with the up and down arrows, the
    second joystick axis, or the up and down directions on a joystick
    hat, and can be chosen with the Enter key or any button on the
    joystick.

    When a menu item is chosen, the menu item's :meth:`event_choose` is
    called, and the menu and all of its menu items are removed from the
    current room.

    .. attribute:: items

       A list of :class:`xsge.menu.Item` objects in this menu, from top
       to bottom.

       When the menu's create event is called, all menu items in this
       list are automatically added to the current room, if they haven't
       been added already.

    .. attribute:: selection

       The index in :attr:`items` of the currently selected menu item.
    """

    @property
    def selection(self):
        return self.__selection

    @selection.setter
    def selection(self, value):
        if self.items and value != self.__selection:
            self.items[self.__selection].event_deselect()
            self.__selection = value % len(self.items)
            self.items[self.__selection].event_select()
            self.event_change_selection()

    def __init__(self, x, y, items, selection=0, z=10000, sprite=None,
                 visible=True, active=True, checks_collisions=False,
                 tangible=False, bbox_x=None, bbox_y=None, bbox_width=None,
                 bbox_height=None, regulate_origin=False,
                 collision_ellipse=False, collision_precise=False, xvelocity=0,
                 yvelocity=0, image_index=0, image_origin_x=None,
                 image_origin_y=None, image_fps=None, image_xscale=1,
                 image_yscale=1, image_rotation=0, image_alpha=255,
                 image_blend=None):
        super(Menu, self).__init__(
            x, y, z=z, sprite=sprite, visible=visible, active=active,
            checks_collisions=checks_collisions, tangible=tangible,
            bbox_x=bbox_x, bbox_y=bbox_y, bbox_width=bbox_width,
            bbox_height=bbox_height, regulate_origin=regulate_origin,
            collision_ellipse=collision_ellipse,
            collision_precise=collision_precise, xvelocity=xvelocity,
            yvelocity=yvelocity, image_index=image_index,
            image_origin_x=image_origin_x, image_origin_y=image_origin_y,
            image_fps=image_fps, image_xscale=image_xscale,
            image_yscale=image_yscale, image_rotation=image_rotation,
            image_alpha=image_alpha, image_blend=image_blend)
        self.__axes = {}
        self.items = items
        self.__selection = selection
        if items:
            self.__selection %= len(items)
            items[self.__selection].event_select()

    def _choose(self):
        # Choose the current selection.
        self.items[self.selection].event_choose()
        self.destroy()
        for item in self.items:
            item.destroy()

    def event_create(self):
        for item in self.items:
            sge.game.current_room.add(item)

    def event_key_press(self, key, char):
        if self.items:
            if key == "up":
                self.selection -= 1
            elif key == "down":
                self.selection += 1
            elif key == "enter":
                self._choose()

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        if axis == 1:
            prev = self.__axes.get((js_id, axis), 0)
            self.__axes[(js_id, axis)] = value

            if prev > -joystick_threshold and value <= -joystick_threshold:
                self.selection -= 1
            elif prev < joystick_threshold and value >= joystick_threshold:
                self.selection += 1

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        if not x:
            self.selection += y

    def event_joystick_button_press(self, js_name, js_id, button):
        self._choose()

    def event_change_selection(self):
        """Called when :attr:`selection` changes."""
        pass


class Item(sge.Object):

    """
    Base class for menu items.  Mostly the same as :class:`Object`, but
    adds new event methods.
    """

    def __init__(self, x, y, z=10001, sprite=None, visible=True, active=True,
                 checks_collisions=False, tangible=False, bbox_x=None,
                 bbox_y=None, bbox_width=None, bbox_height=None,
                 regulate_origin=False, collision_ellipse=False,
                 collision_precise=False, xvelocity=0, yvelocity=0,
                 image_index=0, image_origin_x=None, image_origin_y=None,
                 image_fps=None, image_xscale=1, image_yscale=1,
                 image_rotation=0, image_alpha=255, image_blend=None):
        super(Item, self).__init__(
            x, y, z=z, sprite=sprite, visible=visible, active=active,
            checks_collisions=checks_collisions, tangible=tangible,
            bbox_x=bbox_x, bbox_y=bbox_y, bbox_width=bbox_width,
            bbox_height=bbox_height, regulate_origin=regulate_origin,
            collision_ellipse=collision_ellipse,
            collision_precise=collision_precise, xvelocity=xvelocity,
            yvelocity=yvelocity, image_index=image_index,
            image_origin_x=image_origin_x, image_origin_y=image_origin_y,
            image_fps=image_fps, image_xscale=image_xscale,
            image_yscale=image_yscale, image_rotation=image_rotation,
            image_alpha=image_alpha, image_blend=image_blend)

    def event_select(self):
        """Called when this item is selected."""
        pass

    def event_deselect(self):
        """Called when this item is deselected."""
        pass

    def event_choose(self):
        """Called when this item is chosen."""
        pass


class SimpleItem(Item):

    """
    Basic menu item class.  Has two sprites: one for when the item is
    selected, and one for when it is unselected.  When chosen, a
    function is called with a certain set of arguments.

    .. attribute:: sprite_selected

       The sprite shown when the item is selected.

    .. attribute:: sprite_unselected

       The sprite shown when the item is not selected.

    .. attribute:: action

       The function to call when the item is chosen.

    .. attribute:: action_args

       The positional arguments to pass to the call of :attr:`action`.

    .. attribute:: action_kwargs

       The keyword arguments to pass to the call of :attr:`action`.
    """

    def __init__(self, x, y, sprite_selected, sprite_unselected, z=10001,
                 action=None, action_args=None, action_kwargs=None):
        super(SimpleItem, self).__init__(x, y, z=z, sprite=sprite_unselected)
        self.sprite_selected = sprite_selected
        self.sprite_unselected = sprite_unselected
        self.action = action if action is not None else lambda: None
        self.action_args = action_args if action_args else []
        self.action_kwargs = action_kwargs if action_kwargs else {}

    def event_select(self):
        self.sprite = self.sprite_selected

    def event_deselect(self):
        self.sprite = self.sprite_unselected

    def event_choose(self):
        self.action(*self.action_args, **self.action_kwargs)


def get_text_menu(x, y, items, font=None, color=None, selected_font=None,
                  selected_color=None, background_color=None, height=None,
                  margin=0, halign="left", valign="top"):
    """
    Create a text-based menu.  The resulting menu will contain
    :class:`xsge.menu.SimpleItem` menu items.  You can then make the
    menu actually work by modifying the items' :attr:`action`,
    :attr:`action_args`, and :attr:`action_kwargs` values.

    Arguments:

    - ``x`` -- The horizontal location of the menu within the room.
    - ``y`` -- The vertical location of the menu within the room.
    - ``items`` -- A list of strings to use as menu items.
    - ``font`` -- The default font to use.
    - ``color`` -- The default color to use.
    - ``selected_font`` -- The font to use when an item is selected.  If
      set to :const:`None`, the font will not change when the item is
      selected.
    - ``selected_color`` -- The color to use when an item is selected.
      If set to :const:`None`, the color will not change when the item
      is selected.
    - ``background_color`` -- The color of the menu.  If set to
      :const:`None`, only the menu items will be displayed.
    - ``height`` -- The height of the menu.  If set to :const:`None`,
      the height will be the sum of the items' height.
    - ``margin`` -- The number of pixels that should surround the menu
      items.
    - ``halign`` -- The horizontal alignment of the menu.  See the
      documentation for :meth:`sge.Sprite.draw_text` for more
      information.
    - ``valign`` -- The vertical alignment of the menu.  See the
      documentation for :meth:`sge.Sprite.draw_text` for more
      information.
    """
    if selected_font is None: selected_font = font
    if selected_color is None: selected_color = color
    width = 0
    item_h = 0
    item_objs = []
    for item in items:
        un_spr = sge.Sprite.from_text(font, item, color=color,
                                      halign=halign, valign=valign)
        s_spr = sge.Sprite.from_text(selected_font, item,
                                     color=selected_color, halign=halign,
                                     valign=valign)
        width = max(width, un_spr.width, s_spr.width)
        item_h = max(item_h, un_spr.height, s_spr.height)
        item_objs.append(SimpleItem(x, y, s_spr, un_spr))

    if height is None:
        height = item_h * len(items)

    width += 2 * margin
    height += 2 * margin

    origin_x = {"left": 0, "right": width,
                "center": width / 2}.get(halign.lower(), 0)
    origin_y = {"top": 0, "bottom": height,
                "middle": height / 2}.get(valign.lower(), 0)

    ih = height - 2 * margin
    ih += ((height - margin - item_h) - ih *
           ((len(item_objs) - 1) / len(item_objs)))
    for i in six.moves.range(len(item_objs)):
        obj = item_objs[i]
        obj.y = y - origin_y + obj.sprite.origin_y + margin
        obj.y += ih * (i / len(item_objs))

    if background_color is not None:
        menu_sprite = sge.Sprite(width=width, height=height, origin_x=origin_x,
                                 origin_y=origin_y)
        menu_sprite.draw_rectangle(0, 0, width, height, fill=background_color)
    else:
        menu_sprite = None

    return Menu(x, y, item_objs, sprite=menu_sprite)
