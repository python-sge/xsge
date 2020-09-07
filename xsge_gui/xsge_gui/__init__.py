# xSGE GUI Toolkit
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

This extension provides a simple toolkit for adding GUIs to a SGE game
as well as support for modal dialog boxes.

To use this extension, you must call :func:`xsge_gui.init` sometime
between the creation of the :class:`sge.dsp.Game` object and the start
of the game.

.. data:: window_background_color
          keyboard_focused_box_color
          text_color
          button_text_color
          textbox_text_color
          textbox_text_selected_color
          textbox_highlight_color
          title_text_color

   The colors used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.

.. data:: default_font
          button_font
          textbox_font
          title_font

   The fonts used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.

.. data:: button_sprite
          button_left_sprite
          button_right_sprite
          button_pressed_sprite
          button_pressed_left_sprite
          button_pressed_right_sprite
          button_selected_sprite
          button_selected_left_sprite
          button_selected_right_sprite
          checkbox_off_sprite
          checkbox_on_sprite
          progressbar_sprite
          progressbar_left_sprite
          progressbar_right_sprite
          progressbar_container_sprite
          progressbar_container_left_sprite
          progressbar_container_right_sprite
          radiobutton_off_sprite
          radiobutton_on_sprite
          textbox_sprite
          textbox_left_sprite
          textbox_right_sprite
          window_border_left_sprite
          window_border_right_sprite
          window_border_bottom_sprite
          window_border_bottomleft_sprite
          window_border_bottomright_sprite
          window_border_top_sprite
          window_border_topleft_sprite
          window_border_topright_sprite

   The sprites used by this module.  They can be safely changed, but be
   sure to call :meth:`redraw` on all windows and widgets that would be
   affected; some changes might not become visible until you do.

.. data:: next_window_keys

   A list of keys which, when pressed, will give keyboard focus to the
   next available window.

   Default value: ``[]``

.. data:: previous_window_keys

   A list of keys which, when pressed, will give keyboard focus to the
   previous available window.

   Default value: ``[]``

.. data:: next_widget_keys

   A list of keys which, when pressed, will give keyboard focus to the
   next available widget on the window which has keyboard focus.

   Default value: ``["tab"]``

.. data:: previous_widget_keys

   A list of keys which, when pressed, will give keyboard focus to the
   previous available widget on the window which has keyboard focus.

   Default value: ``[]``

.. data:: left_keys

   A list of keys to treat as left arrows.

   Default value: ``["left"]``

.. data:: right_keys

   A list of keys to treat as right arrows.

   Default value: ``["right"]``

.. data:: up_keys

   A list of keys to treat as up arrows.

   Default value: ``["up"]``

.. data:: down_keys

   A list of keys to treat as down arrows.

   Default value: ``["down"]``

.. data:: enter_keys

   A list of keys to treat as Enter keys.

   Default value: ``["enter", "kp_enter"]``

.. data:: escape_keys

   A list of keys to treat as Escape keys.

   Default value: ``["escape"]``

.. data:: next_window_joystick_events

   A list of tuples indicating joystick events which will give keyboard
   focus to the next available window.

   The tuples should contain, in order, the following values:

   1. The number of the joystick, where ``0`` is the first joystick.

   2. The type of event.  See the documentation for
      :class:`sge.input.JoystickEvent` for more information.

   3. The number of the joystick control, where ``0`` is the first
      control of its type on the joystick.

   Default value: ``[]``

.. data:: previous_window_joystick_events

   A list of tuples indicating joystick events which will give keyboard
   focus to the previous available window.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[]``

.. data:: next_widget_joystick_events

   A list of tuples indicating joystick events which will give keyboard
   focus to the next available widget on the window which has keyboard
   focus.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "button", 8)]``

.. data:: previous_widget_joystick_events

   A list of tuples indicating joystick events which will give keyboard
   focus to the previous available widget on the window which has
   keyboard focus.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[]``

.. data:: left_joystick_events

   A list of tuples indicating joystick events to treat as left arrows.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "axis-", 0), (0, "hat_left", 0)]``

.. data:: right_joystick_events

   A list of tuples indicating joystick events to treat as right arrows.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "axis+", 0), (0, "hat_right", 0)]``

.. data:: up_joystick_events

   A list of tuples indicating joystick events to treat as up arrows.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "axis-", 1), (0, "hat_up", 0)]``

.. data:: down_joystick_events

   A list of tuples indicating joystick events to treat as down arrows.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "axis+", 1), (0, "hat_down", 0)]``

.. data:: enter_joystick_events

   A list of tuples indicating joystick events to treat as Enter keys.

   See the documentation for :attr:`next_window_joystick_events` for
   more information.

   Default value: ``[(0, "button", 9)]``

.. data:: escape_joystick_events

   A list of tuples indicating joystick events to treat as Escape keys.

   Default value: ``[]``

.. data:: joystick_threshold

   The amount of tilt on a joystick that should be considered
   "triggered" for the purpose of navigating menus.
"""


__version__ = "1.2"
__all__ = ["Handler", "Window", "Dialog", "Widget", "DecorativeWidget",
           "Label", "Button", "CheckBox", "RadioButton", "ProgressBar",
           "TextBox", "MenuItem", "MenuWindow", "MenuDialog", "MessageDialog",
           "TextEntryDialog", "init", "show_message", "get_text_entry",
           "get_menu_selection"]


import os
import weakref

try:
    from tkinter import Tk
except ImportError:
    class Tk(object):
        def withdraw(self): pass
        def clipboard_clear(self): pass
        def clipboard_append(self, *args, **kwargs): pass
        def selection_get(self, *args, **kwargs): return ''
        def destroy(self): pass

import sge


DATA = os.path.join(os.path.dirname(__file__), "data")
TEXTBOX_MIN_EDGE = 4
TEXTBOX_CURSOR_BLINK_TIME = 500
DIALOG_PADDING = 8

window_background_color = sge.gfx.Color("#A4A4A4")
keyboard_focused_box_color = sge.gfx.Color((0, 0, 0, 170))
text_color = sge.gfx.Color("black")
button_text_color = sge.gfx.Color("black")
textbox_text_color = sge.gfx.Color("black")
textbox_text_selected_color = sge.gfx.Color("white")
textbox_highlight_color = sge.gfx.Color("blue")
title_text_color = sge.gfx.Color("white")
default_font = None
button_font = None
textbox_font = None
title_font = None
button_sprite = None
button_left_sprite = None
button_right_sprite = None
button_pressed_sprite = None
button_pressed_left_sprite = None
button_pressed_right_sprite = None
button_selected_sprite = None
button_selected_left_sprite = None
button_selected_right_sprite = None
checkbox_off_sprite = None
checkbox_on_sprite = None
progressbar_sprite = None
progressbar_left_sprite = None
progressbar_right_sprite = None
progressbar_container_sprite = None
progressbar_container_left_sprite = None
progressbar_container_right_sprite = None
radiobutton_off_sprite = None
radiobutton_on_sprite = None
textbox_sprite = None
textbox_left_sprite = None
textbox_right_sprite = None
window_border_left_sprite = None
window_border_right_sprite = None
window_border_bottom_sprite = None
window_border_bottomleft_sprite = None
window_border_bottomright_sprite = None
window_border_top_sprite = None
window_border_topleft_sprite = None
window_border_topright_sprite = None
next_window_keys = []
previous_window_keys = []
next_widget_keys = ["tab"]
previous_widget_keys = []
left_keys = ["left"]
right_keys = ["right"]
up_keys = ["up"]
down_keys = ["down"]
enter_keys = ["enter", "kp_enter"]
escape_keys = ["escape"]
next_window_joystick_events = []
previous_window_joystick_events = []
next_widget_joystick_events = [(0, "button", 8)]
previous_widget_joystick_events = []
left_joystick_events = [(0, "axis-", 0), (0, "hat_left", 0)]
right_joystick_events = [(0, "axis+", 0), (0, "hat_right", 0)]
up_joystick_events = [(0, "axis-", 1), (0, "hat_up", 0)]
down_joystick_events = [(0, "axis+", 1), (0, "hat_down", 0)]
enter_joystick_events = [(0, "button", 9)]
escape_joystick_events = []
joystick_threshold = 0.7


class Handler(sge.dsp.Object):

    """
    An object of this class needs to exist in any room where windows are
    to be used.  It feeds SGE events to the windows so they can react to
    user input.  It also refreshes all windows every frame.

    .. attribute:: windows

       A list of all windows that are currently handled by this handler.

       You don't need to modify this list manually.  Instead, use
       :meth:`xsge_gui.Window.show` and :meth:`xsge_gui.Window.hide` to
       add and remove windows from this list, respectively.

    .. attribute:: keyboard_focused_window

       The window that currently has keyboard focus, or :const:`None` if
       no window has focus.
    """

    def __init__(self):
        super().__init__(0, 0, visible=False, tangible=False)
        self.windows = []
        self.keyboard_focused_window = None
        self.__joystick_prev = {}

    def _kb_focus_move(self, n):
        if self.windows:
            if self.keyboard_focused_window in self.windows:
                i = self.windows.index(self.keyboard_focused_window) + n
                i %= len(self.windows)
            else:
                i = 0 if n > 0 else -1

            self.keyboard_focused_window = self.windows[i]

    def get_mouse_focused_window(self):
        """
        Return the window that currently has mouse focus.  The window
        with mouse focus is the one which is closest to the front that
        is touching the mouse cursor.

        Return :const:`None` if no window has focus.
        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        for window in reversed(self.windows):
            border_x = window.x
            border_y = window.y
            if window.border:
                border_x -= window_border_left_sprite.width
                border_y -= window_border_top_sprite.height

            if (border_x <= x < border_x + window.sprite.width and
                    border_y <= y < border_y + window.sprite.height):
                return window

        return None

    def event_step(self, time_passed, delta_mult):
        if self.windows and self.keyboard_focused_window not in self.windows:
            self.keyboard_focused_window = self.windows[-1]

        for window in self.windows[:]:
            window.event_step(time_passed, delta_mult)
            for widget in window.widgets:
                widget.event_step(time_passed, delta_mult)
            window.refresh()

    def event_key_press(self, key, char):
        if key in next_window_keys:
            self._kb_focus_move(1)
        if key in previous_window_keys:
            self._kb_focus_move(-1)

        window = self.keyboard_focused_window
        if window is not None:
            window.event_key_press(key, char)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_press(key, char)

        for window in self.windows[:]:
            window.event_global_key_press(key, char)
            for widget in window.widgets:
                widget.event_global_key_press(key, char)

    def event_key_release(self, key):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_key_release(key)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_key_release(key)

        for window in self.windows[:]:
            window.event_global_key_release(key)
            for widget in window.widgets:
                widget.event_global_key_release(key)

    def event_mouse_button_press(self, button):
        window = self.get_mouse_focused_window()
        if window is not None:
            self.keyboard_focused_window = window
            window.move_to_front()
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_press(button)
            else:
                window.event_mouse_button_press(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_press(button)

        for window in self.windows[:]:
            window.event_global_mouse_button_press(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_press(button)

    def event_mouse_button_release(self, button):
        window = self.get_mouse_focused_window()
        if window is not None:
            if window.get_mouse_on_titlebar():
                window.event_titlebar_mouse_button_release(button)
            else:
                window.event_mouse_button_release(button)
                widget = window.get_mouse_focused_widget()
                if widget is not None:
                    widget.event_mouse_button_release(button)

        for window in self.windows[:]:
            window.event_global_mouse_button_release(button)
            for widget in window.widgets:
                widget.event_global_mouse_button_release(button)

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick_axis_move(js_name, js_id, axis, value)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick_axis_move(js_name, js_id, axis, value)

        for window in self.windows[:]:
            window.event_global_joystick_axis_move(js_name, js_id, axis, value)
            for widget in window.widgets:
                widget.event_global_joystick_axis_move(js_name, js_id, axis,
                                                       value)

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick_hat_move(js_name, js_id, hat, x, y)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick_hat_move(js_name, js_id, hat, x, y)

        for window in self.windows[:]:
            window.event_global_joystick_hat_move(js_name, js_id, hat, x, y)
            for widget in window.widgets:
                widget.event_global_joystick_hat_move(js_name, js_id, hat, x, y)

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick_trackball_move(js_name, js_id, ball, x, y)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick_trackball_move(js_name, js_id, ball, x, y)

        for window in self.windows[:]:
            window.event_global_joystick_trackball_move(js_name, js_id, ball,
                                                        x, y)
            for widget in window.widgets:
                widget.event_global_joystick_trackball_move(js_name, js_id,
                                                            ball, x, y)

    def event_joystick_button_press(self, js_name, js_id, button):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick_button_press(js_name, js_id, button)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick_button_press(js_name, js_id, button)

        for window in self.windows[:]:
            window.event_global_joystick_button_press(js_name, js_id, button)
            for widget in window.widgets:
                widget.event_global_joystick_button_press(js_name, js_id,
                                                          button)

    def event_joystick_button_release(self, js_name, js_id, button):
        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick_button_release(js_name, js_id, button)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick_button_release(js_name, js_id, button)

        for window in self.windows[:]:
            window.event_global_joystick_button_release(js_name, js_id, button)
            for widget in window.widgets:
                widget.event_global_joystick_button_release(js_name, js_id,
                                                            button)

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        js = (js_id, input_type, input_id)
        prev = self.__joystick_prev.get(js, 0)
        self.__joystick_prev[js] = value
        if value >= joystick_threshold and prev < joystick_threshold:
            if js in next_window_joystick_events:
                self._kb_focus_move(1)
            if js in previous_window_joystick_events:
                self._kb_focus_move(-1)

        window = self.keyboard_focused_window
        if window is not None:
            window.event_joystick(js_name, js_id, input_type, input_id, value)
            widget = window.keyboard_focused_widget
            if widget is not None:
                widget.event_joystick(js_name, js_id, input_type, input_id,
                                      value)

        for window in self.windows[:]:
            window.event_global_joystick(js_name, js_id, input_type, input_id,
                                         value)
            for widget in window.widgets:
                widget.event_global_joystick(js_name, js_id, input_type,
                                             input_id, value)


class Window(object):

    """
    Window objects are used to contain widgets.  They can be moved
    around the game window by the user.

    .. attribute:: parent

       A weak reference to this window's parent handler object, which is
       used to display it when it is supposed to be visible.

       If a strong reference is assigned to this attribute, it will
       automatically be changed to a weak reference.

    .. attribute:: x

       The horizontal position of the window relative to the game
       window.

    .. attribute:: y

       The vertical position of the window relative to the game window.

    .. attribute:: width

       The width of the window.

    .. attribute:: height

       The height of the window.

    .. attribute:: title

       The text that shows up in the title bar of the window.

    .. attribute:: background_color

       The color of this window's background.  If set to :const:`None`,
       it becomes the same value as
       :data:`xsge_gui.window_background_color`.

    .. attribute:: border

       Whether or not the window has a border.  If this is
       :const:`False`, the window cannot be moved or resized by the
       user, and :attr:`title` will not be displayed.

    .. attribute:: widgets

       A list of this window's widgets.

    .. attribute:: keyboard_focused_widget

       The widget which currently has keyboard focus within this window,
       or :const:`None` if no widget has keyboard focus within this
       window.

    .. attribute:: sprite

       The sprite this window currently displays as itself.
    """

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        if isinstance(value, weakref.ref):
            self.__parent = value
        else:
            self.__parent = weakref.ref(value)

    @property
    def background_color(self):
        return self.__background_color

    @background_color.setter
    def background_color(self, value):
        if value is not None:
            self.__background_color = value
        else:
            self.__background_color = window_background_color

    def __init__(self, parent, x, y, width, height, title="",
                 background_color=None, border=True):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.title = title
        self.background_color = background_color
        self.border = border
        self.widgets = []
        self.keyboard_focused_widget = None
        self._border_grab = None
        self._close_button_pressed = False
        self.__joystick_prev = {}

        self.sprite = sge.gfx.Sprite(width=1, height=1)
        self.redraw()

    def _kb_focus_move(self, d):
        assert d
        if self.widgets:
            try:
                i = self.widgets.index(self.keyboard_focused_widget)
            except ValueError:
                i = -1 if d > 0 else 0

            for _ in range(len(self.widgets)):
                i += d
                i %= len(self.widgets)
                if self.widgets[i].tab_focus:
                    self.keyboard_focused_widget = self.widgets[i]
                    self.event_change_keyboard_focus()
                    break

    def show(self):
        """Add this window to its parent handler."""
        parent = self.parent()
        if parent is not None:
            if self not in parent.windows:
                parent.windows.append(self)
            else:
                self.move_to_front()

    def hide(self):
        """Remove this window from its parent handler."""
        parent = self.parent()
        if parent is not None:
            while self in parent.windows:
                parent.windows.remove(self)
            if self is parent.keyboard_focused_window:
                parent.keyboard_focused_window = None

    def move_to_front(self):
        """Move this window in front of all other windows."""
        parent = self.parent()
        if parent is not None:
            if self in parent.windows:
                i = parent.windows.index(self)
                parent.windows.append(parent.windows.pop(i))

    def move_to_back(self):
        """Move this window behind all other windows."""
        parent = self.parent()
        if parent is not None:
            if self in parent.windows:
                i = parent.windows.index(self)
                parent.windows.insert(0, parent.windows.pop(i))

    def destroy(self):
        """An alias for :meth:`xsge_gui.Window.hide`."""
        self.hide()

    def redraw(self):
        """
        Re-draw this window's sprite.

        Call this method if you change any variables that should affect
        this window's appearance. For performance reasons, the changes
        won't show up in an existing window until this method is called.
        """
        if self.border:
            self.sprite.width = (self.width + window_border_left_sprite.width +
                                 window_border_right_sprite.width)
            self.sprite.height = (self.height +
                                  window_border_top_sprite.height +
                                  window_border_bottom_sprite.height)
            self.sprite.draw_lock()
            self.sprite.draw_clear()

            self.sprite.draw_rectangle(window_border_left_sprite.width,
                                       window_border_top_sprite.height,
                                       self.width, self.height,
                                       fill=self.background_color)

            start = window_border_topleft_sprite.width
            end = self.sprite.width - window_border_topright_sprite.width
            for i in range(start, end, window_border_top_sprite.width):
                self.sprite.draw_sprite(window_border_top_sprite, 0, i, 0)

            start = window_border_bottomleft_sprite.width
            end = self.sprite.width - window_border_bottomright_sprite.width
            y = self.sprite.height - window_border_bottom_sprite.height
            for i in range(start, end, window_border_bottom_sprite.width):
                self.sprite.draw_sprite(window_border_bottom_sprite, 0, i, y)

            start = window_border_topleft_sprite.height
            end = self.sprite.height - window_border_bottomleft_sprite.height
            for i in range(start, end, window_border_left_sprite.height):
                self.sprite.draw_sprite(window_border_left_sprite, 0, 0, i)

            start = window_border_topright_sprite.height
            end = self.sprite.height - window_border_bottomright_sprite.height
            x = self.sprite.width - window_border_right_sprite.width
            for i in range(start, end, window_border_right_sprite.height):
                self.sprite.draw_sprite(window_border_right_sprite, 0, x, i)

            self.sprite.draw_sprite(window_border_topleft_sprite, 0, 0, 0)
            x = self.sprite.width - window_border_topright_sprite.width
            self.sprite.draw_sprite(window_border_topright_sprite, 0, x, 0)
            y = self.sprite.height - window_border_bottomleft_sprite.height
            self.sprite.draw_sprite(window_border_bottomleft_sprite, 0, 0, y)
            x = self.sprite.width - window_border_bottomright_sprite.width
            y = self.sprite.height - window_border_bottomright_sprite.height
            self.sprite.draw_sprite(window_border_bottomright_sprite, 0, x, y)

            x = self.sprite.width / 2
            y = window_border_top_sprite.height / 2
            self.sprite.draw_text(title_font, self.title, x, y,
                                  width=self.sprite.width,
                                  height=window_border_top_sprite.height,
                                  color=title_text_color,
                                  halign="center", valign="middle")

            self.sprite.draw_unlock()
        else:
            self.sprite.width = self.width
            self.sprite.height = self.height
            self.sprite.draw_clear()
            self.sprite.draw_rectangle(0, 0, self.width, self.height,
                                       fill=self.background_color)

    def refresh(self):
        """
        Project this window onto the game window.

        This method must be called every frame for the window to be
        visible.
        """
        if self.border:
            target_width = (self.width + window_border_left_sprite.width +
                            window_border_right_sprite.width)
            target_height = (self.height + window_border_top_sprite.height +
                             window_border_bottom_sprite.height)
        else:
            target_width = self.width
            target_height = self.height

        if self._border_grab is not None:
            self.x = sge.mouse.get_x() + self._border_grab[0]
            self.y = sge.mouse.get_y() + self._border_grab[1]

        if (self.sprite.width != target_width or
                self.sprite.height != target_height):
            self.redraw()

        if self.border:
            x = self.x - window_border_left_sprite.width
            y = self.y - window_border_top_sprite.height
        else:
            x = self.x
            y = self.y

        if x < 0:
            x = 0
        elif x + self.sprite.width >= sge.game.width:
            x = sge.game.width - self.sprite.width
        if y < 0:
            y = 0
        elif y + self.sprite.height >= sge.game.height:
            y = sge.game.height - self.sprite.height

        if self.border:
            self.x = x + window_border_left_sprite.width
            self.y = y + window_border_top_sprite.height
        else:
            self.x = x
            self.y = y

        sge.game.project_sprite(self.sprite, 0, x, y)

        for widget in self.widgets:
            widget.refresh()

    def get_mouse_on_titlebar(self):
        """Return whether or not the mouse is on the title bar."""
        if self.border:
            mouse_x = sge.mouse.get_x()
            mouse_y = sge.mouse.get_y()
            border_x = self.x - window_border_left_sprite.width
            border_y = self.y - window_border_top_sprite.height
            return (border_x <= mouse_x < border_x + self.sprite.width and
                    border_y <= mouse_y < self.y)
        else:
            return False

    def get_mouse_focused_widget(self):
        """
        Return the widget in this window with mouse focus.  The widget
        with mouse focus is the one which is closest to the front that
        is touching the mouse cursor.

        Return :const:`None` if no widget has focus.
        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        for widget in self.widgets[::-1]:
            widget_x = self.x + widget.x
            widget_y = self.y + widget.y
            if (widget_x <= x < widget_x + widget.sprite.width and
                    widget_y <= y < widget_y + widget.sprite.height):
                return widget

        return None

    def event_step(self, time_passed, delta_mult):
        """
        Called once every frame, before refreshing.  See the
        documentation for :meth:`sge.dsp.Game.event_step` for more
        information.
        """
        pass

    def event_change_keyboard_focus(self):
        """
        Called when :attr:`keyboard_focused_widget` changes as a result
        of a key or joystick event being pressed.
        """
        pass

    def event_key_press(self, key, char):
        """
        Called when a key is pressed while this window has keyboard
        focus.  See the documentation for :class:`sge.input.KeyPress`
        for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        next_widget_keys_ = next_widget_keys
        previous_widget_keys_ = previous_widget_keys
        left_keys_ = left_keys
        right_keys_ = right_keys
        up_keys_ = up_keys
        down_keys_ = down_keys
        enter_keys_ = enter_keys
        escape_keys_ = escape_keys

        if key in next_widget_keys_:
            self._kb_focus_move(1)
        if key in previous_widget_keys_:
            self._kb_focus_move(-1)
        if key in left_keys_:
            self.event_press_left()
        if key in right_keys_:
            self.event_press_right()
        if key in up_keys_:
            self.event_press_up()
        if key in down_keys_:
            self.event_press_down()
        if key in enter_keys_:
            self.event_press_enter()
        if key in escape_keys_:
            self.event_press_escape()

    def event_key_release(self, key):
        """
        Called when a key is released while this window has keyboard
        focus.  See the documentation for :class:`sge.input.KeyRelease`
        for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        left_keys_ = left_keys
        right_keys_ = right_keys
        up_keys_ = up_keys
        down_keys_ = down_keys
        enter_keys_ = enter_keys
        escape_keys_ = escape_keys

        if key in left_keys_:
            self.event_release_left()
        if key in right_keys_:
            self.event_release_right()
        if key in up_keys_:
            self.event_release_up()
        if key in down_keys_:
            self.event_release_down()
        if key in enter_keys_:
            self.event_release_enter()
        if key in escape_keys_:
            self.event_release_escape()

    def event_mouse_button_press(self, button):
        """
        Called when a mouse button is pressed while this window has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.
        """
        pass

    def event_mouse_button_release(self, button):
        """
        Called when a mouse button is released while this window has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.
        """
        pass

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        Called when a joystick axis is moved while this window has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickAxisMove` for more information.
        """
        pass

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        Called when a joystick hat is moved while this window has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickHatMove` for more information.
        """
        pass

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        Called when a joystick trackball is moved while this window has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_joystick_button_press(self, js_name, js_id, button):
        """
        Called when a joystick button is pressed while this window has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonPress` for more information.
        """
        pass

    def event_joystick_button_release(self, js_name, js_id, button):
        """
        Called when a joystick button is released while this window has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        """
        Called when a joystick event occurs while this window has
        keyboard focus.  See the documentation for
        :class:`sge.inputJoystickEvent` for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        next_widget_joystick_events_ = next_widget_joystick_events
        previous_widget_joystick_events_ = previous_widget_joystick_events
        left_joystick_events_ = left_joystick_events
        right_joystick_events_ = right_joystick_events
        up_joystick_events_ = up_joystick_events
        down_joystick_events_ = down_joystick_events
        enter_joystick_events_ = enter_joystick_events
        escape_joystick_events_ = escape_joystick_events

        js = (js_id, input_type, input_id)
        prev = self.__joystick_prev.get(js, 0)
        self.__joystick_prev[js] = value
        if value >= joystick_threshold and prev < joystick_threshold:
            if js in next_widget_joystick_events_:
                self._kb_focus_move(1)
            if js in previous_widget_joystick_events_:
                self._kb_focus_move(-1)
            if js in left_joystick_events_:
                self.event_press_left()
            if js in right_joystick_events_:
                self.event_press_right()
            if js in up_joystick_events_:
                self.event_press_up()
            if js in down_joystick_events_:
                self.event_press_down()
            if js in enter_joystick_events_:
                self.event_press_enter()
            if js in escape_joystick_events_:
                self.event_press_escape()
        elif value < joystick_threshold and prev >= joystick_threshold:
            if js in left_joystick_events_:
                self.event_release_left()
            if js in right_joystick_events_:
                self.event_release_right()
            if js in up_joystick_events_:
                self.event_release_up()
            if js in down_joystick_events_:
                self.event_release_down()
            if js in enter_joystick_events_:
                self.event_release_enter()
            if js in escape_joystick_events_:
                self.event_release_escape()

    def event_press_left(self):
        """
        Called when a key in :data:`left_keys` or a joystick event in
        :data:`left_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_press_right(self):
        """
        Called when a key in :data:`right_keys` or a joystick event in
        :data:`right_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_press_up(self):
        """
        Called when a key in :data:`up_keys` or a joystick event in
        :data:`up_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_press_down(self):
        """
        Called when a key in :data:`down_keys` or a joystick event in
        :data:`down_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_press_enter(self):
        """
        Called when a key in :data:`enter_keys` or a joystick event in
        :data:`enter_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_press_escape(self):
        """
        Called when a key in :data:`escape_keys` or a joystick event in
        :data:`enter_joystick_events` is pressed while this window has
        keyboard focus.
        """
        pass

    def event_release_left(self):
        """
        Called when a key in :data:`left_keys` or a joystick event in
        :data:`left_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_release_right(self):
        """
        Called when a key in :data:`right_keys` or a joystick event in
        :data:`right_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_release_up(self):
        """
        Called when a key in :data:`up_keys` or a joystick event in
        :data:`up_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_release_down(self):
        """
        Called when a key in :data:`down_keys` or a joystick event in
        :data:`down_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_release_enter(self):
        """
        Called when a key in :data:`enter_keys` or a joystick event in
        :data:`enter_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_release_escape(self):
        """
        Called when a key in :data:`escape_keys` or a joystick event in
        :data:`enter_joystick_events` is released while this window has
        keyboard focus.
        """
        pass

    def event_titlebar_mouse_button_press(self, button):
        """
        Called when a mouse button is pressed on top of this window's
        title bar (top border).  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.
        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        border_x = self.x - window_border_left_sprite.width
        close_button_w = window_border_topright_sprite.width
        close_button_x = (border_x + self.sprite.width - close_button_w)
        if close_button_x <= x < close_button_x + close_button_w:
            if button == "left":
                self._close_button_pressed = True
        else:
            if button == "left":
                self._border_grab = (self.x - x, self.y - y)
            elif button == "middle":
                self.move_to_back()

    def event_titlebar_mouse_button_release(self, button):
        """
        Called when a mouse button is released on top of this window's
        title bar (top border).  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.
        """
        x = sge.mouse.get_x()
        y = sge.mouse.get_y()
        border_x = self.x - window_border_left_sprite.width
        close_button_w = window_border_topright_sprite.width
        close_button_x = (border_x + self.sprite.width - close_button_w)
        if close_button_x <= x < close_button_x + close_button_w:
            if button == "left":
                if self._close_button_pressed:
                    self.event_close()
        else:
            if button == "left":
                if self._border_grab is not None:
                    self.x = x + self._border_grab[0]
                    self.y = y + self._border_grab[1]

        self.event_global_mouse_button_release(button)

    def event_global_key_press(self, key, char):
        """
        Called when a key is pressed, regardless of which window has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyPress` for more information.
        """
        pass

    def event_global_key_release(self, key):
        """
        Called when a key is released, regardless of which window has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyRelease` for more information.
        """
        pass

    def event_global_mouse_button_press(self, button):
        """
        Called when a mouse button is pressed, regardless of which
        window has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.
        """
        pass

    def event_global_mouse_button_release(self, button):
        """
        Called when a mouse button is released, regardless of which
        window has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.
        """
        if button == "left":
            self._close_button_pressed = False
            self._border_grab = None

    def event_global_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        Called when a joystick axis is moved, regardless of which window
        has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickAxisMove` for more information.
        """
        pass

    def event_global_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        Called when a joystick hat is moved, regardless of which window
        has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickHatMove` for more information.
        """
        pass

    def event_global_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        Called when a joystick trackball is moved, regardless of which
        window has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_global_joystick_button_press(self, js_name, js_id, button):
        """
        Called when a joystick button is pressed, regardless of which
        window has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonPress` for more information.
        """
        pass

    def event_global_joystick_button_release(self, js_name, js_id, button):
        """
        Called when a joystick button is released, regardless of which
        window has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    def event_global_joystick(self, js_name, js_id, input_type, input_id,
                              value):
        """
        Called when a joystick event occurs, regardless of which window
        has keyboard focus.  See the documentation for
        :class:`sge.inputJoystickEvent` for more information.
        """
        pass

    def event_close(self):
        """
        Called when the "X" button in the top-right corner of the window
        is pressed.

        By default, this calls :meth:`xsge_gui.Window.destroy`.
        """
        self.destroy()


class Dialog(Window):

    """Dialog class.

    Dialogs are windows with their own loops, also called modal windows.
    They are used for tasks that must be completed before the main
    program continues, such as pop-up messages.

    See the documentation for :class:`xsge_gui.Window` for more
    information.

    """

    def show(self):
        """Show this dialog and start its loop.

        Like :meth:`xsge_gui.Window.show`, this method adds the dialog
        to its parent.  It then starts this dialog's loop.  Call
        :meth:`xsge_gui.Dialog.hide` on this dialog to end the loop.

        """
        try:
            parent = self.parent()
            if parent is not None:
                screenshot = sge.gfx.Sprite.from_screenshot()
                super().show()
                parent.keyboard_focused_window = self
                while self in parent.windows:
                    self.move_to_front()

                    # Input events
                    sge.game.pump_input()
                    while sge.game.input_events:
                        event = sge.game.input_events.pop(0)

                        if isinstance(event, sge.input.KeyPress):
                            self.event_key_press(event.key, event.char)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_key_press(event.key, event.char)
                            self.event_global_key_press(event.key, event.char)
                            for widget in self.widgets:
                                widget.event_global_key_press(event.key,
                                                              event.char)
                        elif isinstance(event, sge.input.KeyRelease):
                            self.event_key_release(event.key)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_key_release(event.key)
                            self.event_global_key_release(event.key)
                            for widget in self.widgets:
                                widget.event_global_key_release(event.key)
                        elif isinstance(event, sge.input.MouseButtonPress):
                            if parent.get_mouse_focused_window() is self:
                                if self.get_mouse_on_titlebar():
                                    self.event_titlebar_mouse_button_press(
                                        event.button)
                                else:
                                    self.event_mouse_button_press(event.button)
                                    widget = self.get_mouse_focused_widget()
                                    if widget is not None:
                                        widget.event_mouse_button_press(
                                            event.button)

                            self.event_global_mouse_button_press(event.button)
                            for widget in self.widgets:
                                widget.event_global_mouse_button_press(
                                    event.button)
                        elif isinstance(event, sge.input.MouseButtonRelease):
                            if parent.get_mouse_focused_window() is self:
                                if self.get_mouse_on_titlebar():
                                    self.event_titlebar_mouse_button_release(
                                        event.button)
                                else:
                                    self.event_mouse_button_release(event.button)
                                    widget = self.get_mouse_focused_widget()
                                    if widget is not None:
                                        widget.event_mouse_button_release(
                                            event.button)

                            self.event_global_mouse_button_release(event.button)
                            for widget in self.widgets:
                                widget.event_global_mouse_button_release(
                                    event.button)
                        elif isinstance(event, sge.input.JoystickAxisMove):
                            self.event_joystick_axis_move(
                                event.js_name, event.js_id, event.axis,
                                event.value)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_joystick_axis_move(
                                    event.js_name, event.js_id, event.axis,
                                    event.value)
                            self.event_global_joystick_axis_move(
                                event.js_name, event.js_id, event.axis,
                                event.value)
                            for widget in self.widgets:
                                widget.event_global_joystick_axis_move(
                                    event.js_name, event.js_id, event.axis,
                                    event.value)
                        elif isinstance(event, sge.input.JoystickHatMove):
                            self.event_joystick_hat_move(
                                event.js_name, event.js_id, event.hat, event.x,
                                event.y)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_joystick_hat_move(
                                    event.js_name, event.js_id, event.hat,
                                    event.x, event.y)
                            self.event_global_joystick_hat_move(
                                event.js_name, event.js_id, event.hat, event.x,
                                event.y)
                            for widget in self.widgets:
                                widget.event_global_joystick_hat_move(
                                    event.js_name, event.js_id, event.hat,
                                    event.x, event.y)
                        elif isinstance(event, sge.input.JoystickButtonPress):
                            self.event_joystick_button_press(
                                event.js_name, event.js_id, event.button)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_joystick_button_press(
                                    event.js_name, event.js_id, event.button)
                            self.event_global_joystick_button_press(
                                event.js_name, event.js_id, event.button)
                            for widget in self.widgets:
                                widget.event_global_joystick_button_press(
                                    event.js_name, event.js_id, event.button)
                        elif isinstance(event, sge.input.JoystickButtonRelease):
                            self.event_joystick_button_release(
                                event.js_name, event.js_id, event.button)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_joystick_button_release(
                                    event.js_name, event.js_id, event.button)
                            self.event_global_joystick_button_release(
                                event.js_name, event.js_id, event.button)
                            for widget in self.widgets:
                                widget.event_global_joystick_button_release(
                                    event.js_name, event.js_id, event.button)
                        elif isinstance(event, sge.input.JoystickEvent):
                            self.event_joystick(event.js_name, event.js_id,
                                                event.input_type,
                                                event.input_id, event.value)
                            widget = self.keyboard_focused_widget
                            if widget is not None:
                                widget.event_joystick(
                                    event.js_name, event.js_id,
                                    event.input_type, event.input_id,
                                    event.value)
                            self.event_global_joystick(
                                event.js_name, event.js_id, event.input_type,
                                event.input_id, event.value)
                            for widget in self.widgets:
                                widget.event_global_joystick(
                                    event.js_name, event.js_id,
                                    event.input_type, event.input_id,
                                    event.value)
                        elif isinstance(event, sge.input.QuitRequest):
                            sge.game.input_events.insert(0, event)
                            self.hide()
                            return

                    # Regulate speed
                    time_passed = sge.game.regulate_speed()

                    if sge.game.delta:
                        t = min(time_passed, 1000 / sge.game.delta_min)
                        delta_mult = t / (1000 / sge.game.fps)
                    else:
                        delta_mult = 1

                    # Project screenshot
                    sge.game.project_sprite(screenshot, 0, 0, 0)

                    # Project windows
                    self.event_step(time_passed, delta_mult)
                    for widget in self.widgets:
                        widget.event_step(time_passed, delta_mult)

                    for window in parent.windows[:]:
                        window.refresh()

                    # Refresh
                    sge.game.refresh()

                sge.game.pump_input()
                sge.game.input_events = []
        except RuntimeError:
            # Recursion is possible in some cases due to the way this
            # works. This will prevent exceeding recursion depth from
            # crashing the entire game.
            print("Recursion depth exceeded! Dialog canceled.")


class MenuWindow(Window):

    """
    Meant to  be used with :class:`xsge_gui.MenuItem` widgets to create
    keyboard-navigated menus.  Has no border by default.  If one of the
    keys in :data:`enter_keys` or one of the joystick events in
    :data:`enter_joystick_events` is pressed, :attr:`choice` is set to
    the index within :attr:`widgets` of the widget which currently has
    keyboard focus, the window is closed, and :meth:`event_choose` is
    called.  If one of the keys in :data:`escape_keys` or one of the
    joystick events in :data:`escape_joystick_events` is pressed, the
    window is closed and :meth:`event_choose` is called.

    .. attribute:: choice

       The menu item chosen.  If no menu item has been chosen, it is set
       to :const:`None`.

    See the documentation for :class:`xsge_gui.Window` for more
    information.
    """

    def __init__(self, parent, x, y, width, height, title="",
                 background_color=sge.gfx.Color("#0000"), border=False):
        super().__init__(parent, x, y, width, height, title, background_color,
                         border)
        self.choice = None

    def event_step(self, time_passed, delta_mult):
        if self.keyboard_focused_widget is None and self.widgets:
            self.keyboard_focused_widget = self.widgets[0]

    def event_press_enter(self):
        try:
            self.choice = self.widgets.index(self.keyboard_focused_widget)
        except ValueError:
            pass

        self.destroy()
        sge.game.refresh()
        self.event_choose()

    def event_press_escape(self):
        self.destroy()
        sge.game.refresh()
        self.event_choose()

    def event_choose(self):
        """Called when a menu item is chosen."""
        pass

    @classmethod
    def from_text(cls, parent, x, y, items, font_normal=None,
                  color_normal=None, font_selected=None, color_selected=None,
                  background_color=sge.gfx.Color("#0000"), height=None,
                  margin=0, halign="left", valign="top", outline_normal=None,
                  outline_selected=None, outline_thickness_normal=0,
                  outline_thickness_selected=0, selection_prefix="",
                  selection_suffix=""):
        """
        Return a menu created automatically from a list of strings.

        Arguments:

        - ``x`` -- The horizontal location of the window within the
          room.  Affected by ``halign``.
        - ``y`` -- The vertical location of the window within the room.
          Affected by ``valign``.
        - ``items`` -- A list of strings to use as the menu's items.
        - ``font_normal`` -- The default font to use.
        - ``color_normal`` -- The default color to use.
        - ``font_selected`` -- The font to use for the currently
          selected item.  If set to :const:`None`, the default font will
          be used.
        - ``color_selected`` -- The color to use for the currently
          selected item.  If set to :const:`None`, the default color
          will be used.
        - ``height`` -- The height of the menu.  If set to
          :const:`None`, it will be the sum of the items' height.
        - ``margin`` -- The size of the margin around the menu.
        - ``halign`` -- The horizontal alignment of the menu.  See the
          documentation for :meth:`sge.gfx.Sprite.draw_text` for more
          information.
        - ``valign`` -- The vertical alignment of the menu.  See the
          documentation for :meth:`sge.gfx.Sprite.draw_text` for more
          information.
        - ``outline_normal`` -- The default outline color to use.  See
          the documentation for :meth:`sge.gfx.Sprite.draw_text` for
          more information.
        - ``outline_selected`` -- The outline color to use for the
          currently selected item.  See the documentation for
          :meth:`sge.gfx.Sprite.draw_text` for more information.
        - ``outline_thickness_normal`` -- The default outline thickness
          to use. See the documentation for
          :meth:`sge.gfx.Sprite.draw_text` for more information.
        - ``outline_thickness_selected`` -- The outline thickness to use
          for the currently selected item. See the documentation for
          :meth:`sge.gfx.Sprite.draw_text` for more information.
        - ``selection_prefix`` -- A prefix to prepend to the text of the
          current selection.  Useful for colorblind accessibility.
        - ``selection_suffix`` -- A suffix to append to the text of the
          current selection.  Useful for colorblind accessibility.
        """
        if font_selected is None: font_selected = font_normal
        if color_selected is None: color_selected = color_normal
        width = 0
        item_h = 0
        item_sprites = []
        for item in items:
            item_selected = "".join([selection_prefix, item, selection_suffix])
            n_spr = sge.gfx.Sprite.from_text(
                font_normal, item, color=color_normal, halign=halign,
                valign=valign, outline=outline_normal,
                outline_thickness=outline_thickness_normal)
            s_spr = sge.gfx.Sprite.from_text(
                font_selected, item_selected, color=color_selected,
                halign=halign, valign=valign, outline=outline_selected,
                outline_thickness=outline_thickness_selected)
            width = max(width, n_spr.width, s_spr.width)
            item_h = max(item_h, n_spr.height, s_spr.height)
            item_sprites.append((n_spr, s_spr))

        if height is None:
            height = item_h * len(items)

        width += 2 * margin
        height += 2 * margin

        origin_x = {"left": 0, "right": width,
                    "center": width / 2}.get(halign.lower(), 0)
        origin_y = {"top": 0, "bottom": height,
                    "middle": height / 2}.get(valign.lower(), 0)

        x -= origin_x
        y -= origin_y

        self = cls(parent, x, y, width, height,
                   background_color=background_color)

        ih = height - 2 * margin
        for i in range(len(item_sprites)):
            n_spr, s_spr = item_sprites[i]
            iy = n_spr.origin_y + margin + ih * i / len(item_sprites)
            MenuItem(self, origin_x, iy, i, sprite_normal=n_spr,
                     sprite_selected=s_spr)

        return self


class MenuDialog(MenuWindow, Dialog):

    """
    Inherits both :class:`MenuWindow` and :class:`Dialog`.

    See the documentation for :class:`xsge_gui.Dialog` for more
    information.
    """

    pass


class MessageDialog(Dialog):

    """
    This dialog shows a message box and accepts button input.  All
    buttons cause the dialog to close and set :attr:`choice` to the
    button pressed.

    .. attribute:: choice

       The button clicked.  If a button hasn't been clicked (i.e. the
       dialog hasn't yet been closed or was closed by clicking on the
       close button), it is set to :const:`None`.

    See the documentation for :class:`xsge_gui.Dialog` for more
    information.
    """

    def __init__(self, parent, message="", title="Message", buttons=("Ok",),
                 default=-1, width=320, height=None):
        """See :func:`xsge_gui.show_message`."""
        button_w = max(1, round((width - DIALOG_PADDING*(len(buttons) + 1))
                                / len(buttons)))
        button_h = button_sprite.height
        label_w = max(1, width - DIALOG_PADDING * 2)

        if height is None:
            height = (default_font.get_height(message, width=label_w) +
                      button_h + DIALOG_PADDING * 3)

        x = sge.game.width / 2 - width / 2
        y = sge.game.height / 2 - height / 2
        super().__init__(parent, x, y, width, height, title=title)
        label_h = max(1, height - button_h - DIALOG_PADDING * 3)
        Label(self, DIALOG_PADDING, DIALOG_PADDING, 0, message, width=label_w,
              height=label_h)

        y = height - button_h - DIALOG_PADDING
        for i in range(len(buttons)):
            x = i * (button_w + DIALOG_PADDING) + DIALOG_PADDING
            button = Button(self, x, y, 0, buttons[i], width=button_w)

            def event_press(self=button, x=i):
                parent = self.parent()
                if parent is not None:
                    parent._return_button(x)

            button.event_press = event_press

            if i in (default, len(buttons) + default):
                self.keyboard_focused_widget = button

        self.choice = None

    def _return_button(self, x):
        # Return button with index ``x``.
        self.choice = x
        self.destroy()

    def event_press_escape(self):
        self.destroy()


class TextEntryDialog(Dialog):

    """
    This dialog shows a message and has the user enter some text.  Two
    buttons are shown: a "Cancel" button that closes the dialog, and an
    "Ok" button that sets :attr:`text` to the text entered and then
    closes the dialog.

    .. attribute:: text

       The text entered after the "Ok" button is clicked.  If the "Ok"
       button hasn't been clicked, this is :const:`None`.

    See the documentation for :class:`xsge_gui.Dialog` for more
    information.
    """

    def __init__(self, parent, message="", title="Text Entry", text="",
                 width=320, height=None):
        """See :func:`xsge_gui.get_text_entry`."""
        button_w = max(1, (width - DIALOG_PADDING * 3) / 2)
        button_h = button_sprite.height
        textbox_w = max(1, width - DIALOG_PADDING * 2)
        textbox_h = textbox_sprite.height
        label_w = textbox_w

        if height is None:
            height = (default_font.get_height(message, width=label_w) +
                      button_h + textbox_h + DIALOG_PADDING * 4)

        x = sge.game.width / 2 - width / 2
        y = sge.game.height / 2 - height / 2
        super().__init__(parent, x, y, width, height, title=title)
        label_h = max(1, height - button_h - textbox_h - DIALOG_PADDING * 4)

        x = DIALOG_PADDING
        y = DIALOG_PADDING
        Label(self, x, y, 0, message, width=label_w, height=label_h)

        y = label_h + DIALOG_PADDING * 2
        self.textbox = TextBox(self, x, y, 0, width=textbox_w, text=text)
        if text:
            self.textbox._selected = (0, len(text))

        def event_key_press(key, char, self=self.textbox):
            if key in ("enter", "kp_enter"):
                parent = self.parent()
                if parent is not None:
                    parent._return_text(self.text)
            else:
                TextBox.event_key_press(self, key, char)

        self.textbox.event_key_press = event_key_press

        y = height - button_h - DIALOG_PADDING
        x = DIALOG_PADDING
        button = Button(self, x, y, 0, "Cancel", width=button_w)

        def event_press(self=button):
            parent = self.parent()
            if parent is not None:
                parent.destroy()

        button.event_press = event_press

        x = button_w + DIALOG_PADDING * 2
        button = Button(self, x, y, 0, "Ok", width=button_w)

        def event_press(self=button):
            parent = self.parent()
            if parent is not None:
                parent._return_text(parent.textbox.text)

        button.event_press = event_press

        self.text = None
        self.keyboard_focused_widget = self.textbox

    def _return_text(self, s):
        # Return ``s`` as this dialog's text.
        self.text = s
        self.destroy()

    def event_press_escape(self):
        self.destroy()


class Widget(object):

    """
    Widget objects are things like controls and decorations that exist
    on windows.

    .. attribute:: parent

       A weak reference to this widget's parent window.

       If a strong reference is assigned to this attribute, it will
       automatically be changed to a weak reference.

    .. attribute:: x

       The horizontal position of the widget relative to its parent
       window.

    .. attribute:: y

       The vertical position of the widget relative to its parent
       window.

    .. attribute:: z

       The Z-axis position of the widget.  Widgets with a higher Z-axis
       value are in front of widgets with a lower Z-axis value.  This
       value is not connected in any way to Z-axis values in the SGE.

    .. attribute:: sprite

       The sprite this widget displays as itself.

    .. attribute:: index

       Indicates the "position" this widget is in for the purposes of
       tab-focusing.  Smaller indexes are first on the window's list of
       widgets.  Set to :const:`None` to use :attr:`z` for this purpose.
       Widgets with smaller indexes are inserted earlier in the parent
       window's :attr:`widgets` list, and this positioning is what
       actually determines the ordering of tab-focusing.

       .. note::

          This attribute does not *precisely* control the index of the
          widget within the parent widget's :attr:`widgets` list. It
          only controls where the widget is in the list relative to
          other widgets.

    .. attribute:: tab_focus

       Class attribute indicating whether or not the widget should be
       considered for focusing when the Tab key is pressed.

       Default value: :const:`True`
    """

    tab_focus = True

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        parent = self.parent()
        if parent is not None:
            if self in parent.widgets:
                parent.widgets.remove(self)

        if isinstance(value, weakref.ref):
            self.__parent = value
        else:
            self.__parent = weakref.ref(value)

        parent = self.__parent()
        if parent is not None:
            i = 0
            while (i < len(parent.widgets) and
                   parent.widgets[i].index <= self.index):
                i += 1

            parent.widgets.insert(i, self)

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, value):
        if value is None:
            value = self.z

        self.__index = value

        parent = self.parent()
        if parent is not None:
            if self in parent.widgets:
                parent.widgets.remove(self)

            i = 0
            while i < len(parent.widgets) and parent.widgets[i].index <= value:
                i += 1

            parent.widgets.insert(i, self)

    def __init__(self, parent, x, y, z, sprite=None, index=None):
        if isinstance(parent, weakref.ref):
            self.__parent = parent
        else:
            self.__parent = weakref.ref(parent)
        self.x = x
        self.y = y
        self.z = z
        self.index = index
        if sprite is not None:
            self.sprite = sprite
        else:
            self.sprite = sge.gfx.Sprite(width=1, height=1)
        self.__joystick_prev = {}

    def destroy(self):
        """Destroy this widget."""
        parent = self.parent()
        if parent is not None and self in parent.widgets:
            parent.widgets.remove(self)

    def redraw(self):
        """
        Re-draw this widget's sprite.

        Call this method if you change any variables that should affect
        this widget's appearance.  This method automatically makes any
        changes necessary to :attr:`self.sprite`.
        """
        pass

    def refresh(self):
        """
        Project this widget onto the game window.

        This method must be called every frame for the widget to be
        visible.
        """
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)
            if parent.keyboard_focused_widget is self:
                sge.game.project_rectangle(
                    parent.x + self.x, parent.y + self.y, self.sprite.width,
                    self.sprite.height, outline=keyboard_focused_box_color)
        else:
            self.destroy()

    def event_step(self, time_passed, delta_mult):
        """
        Called once every frame, before refreshing.  See the
        documentation for :meth:`sge.dsp.Game.event_step` for more
        information.
        """
        pass

    def event_key_press(self, key, char):
        """
        Called when a key is pressed while this widget has keyboard
        focus.  See the documentation for :class:`sge.input.KeyPress`
        for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        left_keys_ = left_keys
        right_keys_ = right_keys
        up_keys_ = up_keys
        down_keys_ = down_keys
        enter_keys_ = enter_keys
        escape_keys_ = escape_keys

        if key in left_keys_:
            self.event_press_left()
        if key in right_keys_:
            self.event_press_right()
        if key in up_keys_:
            self.event_press_up()
        if key in down_keys_:
            self.event_press_down()
        if key in enter_keys_:
            self.event_press_enter()
        if key in escape_keys_:
            self.event_press_escape()

    def event_key_release(self, key):
        """
        Called when a key is released while this widget has keyboard
        focus.  See the documentation for :class:`sge.input.KeyRelease`
        for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        left_keys_ = left_keys
        right_keys_ = right_keys
        up_keys_ = up_keys
        down_keys_ = down_keys
        enter_keys_ = enter_keys
        escape_keys_ = escape_keys

        if key in left_keys_:
            self.event_release_left()
        if key in right_keys_:
            self.event_release_right()
        if key in up_keys_:
            self.event_release_up()
        if key in down_keys_:
            self.event_release_down()
        if key in enter_keys_:
            self.event_release_enter()
        if key in escape_keys_:
            self.event_release_escape()

    def event_mouse_button_press(self, button):
        """
        Called when a mouse button is pressed while this widget has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.
        """
        pass

    def event_mouse_button_release(self, button):
        """
        Called when a mouse button is released while this widget has
        mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.
        """
        pass

    def event_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        Called when a joystick axis is moved while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickAxisMove` for more information.
        """
        pass

    def event_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        Called when a joystick hat is moved while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickHatMove` for more information.
        """
        pass

    def event_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        Called when a joystick trackball is moved while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_joystick_button_press(self, js_name, js_id, button):
        """
        Called when a joystick button is pressed while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonPress` for more information.
        """
        pass

    def event_joystick_button_release(self, js_name, js_id, button):
        """
        Called when a joystick button is released while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    def event_joystick(self, js_name, js_id, input_type, input_id, value):
        """
        Called when a joystick event occurs while this widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.JoystickEvent` for more information.
        """
        # Localize these variables so that changes made during this
        # event don't screw everything up.
        left_joystick_events_ = left_joystick_events
        right_joystick_events_ = right_joystick_events
        up_joystick_events_ = up_joystick_events
        down_joystick_events_ = down_joystick_events
        enter_joystick_events_ = enter_joystick_events
        escape_joystick_events_ = escape_joystick_events

        js = (js_id, input_type, input_id)
        prev = self.__joystick_prev.get(js, 0)
        self.__joystick_prev[js] = value
        if value >= joystick_threshold and prev < joystick_threshold:
            if js in left_joystick_events_:
                self.event_press_left()
            if js in right_joystick_events_:
                self.event_press_right()
            if js in up_joystick_events_:
                self.event_press_up()
            if js in down_joystick_events_:
                self.event_press_down()
            if js in enter_joystick_events_:
                self.event_press_enter()
            if js in escape_joystick_events_:
                self.event_press_escape()
        elif value < joystick_threshold and prev >= joystick_threshold:
            if js in left_joystick_events_:
                self.event_release_left()
            if js in right_joystick_events_:
                self.event_release_right()
            if js in up_joystick_events_:
                self.event_release_up()
            if js in down_joystick_events_:
                self.event_release_down()
            if js in enter_joystick_events_:
                self.event_release_enter()
            if js in escape_joystick_events_:
                self.event_release_escape()

    def event_press_left(self):
        """
        Called when a key in :data:`left_keys` or a joystick event in
        :data:`left_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_press_right(self):
        """
        Called when a key in :data:`right_keys` or a joystick event in
        :data:`right_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_press_up(self):
        """
        Called when a key in :data:`up_keys` or a joystick event in
        :data:`up_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_press_down(self):
        """
        Called when a key in :data:`down_keys` or a joystick event in
        :data:`down_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_press_enter(self):
        """
        Called when a key in :data:`enter_keys` or a joystick event in
        :data:`enter_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_press_escape(self):
        """
        Called when a key in :data:`escape_keys` or a joystick event in
        :data:`enter_joystick_events` is pressed while this widget has
        keyboard focus.
        """
        pass

    def event_release_left(self):
        """
        Called when a key in :data:`left_keys` or a joystick event in
        :data:`left_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_release_right(self):
        """
        Called when a key in :data:`right_keys` or a joystick event in
        :data:`right_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_release_up(self):
        """
        Called when a key in :data:`up_keys` or a joystick event in
        :data:`up_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_release_down(self):
        """
        Called when a key in :data:`down_keys` or a joystick event in
        :data:`down_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_release_enter(self):
        """
        Called when a key in :data:`enter_keys` or a joystick event in
        :data:`enter_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_release_escape(self):
        """
        Called when a key in :data:`escape_keys` or a joystick event in
        :data:`enter_joystick_events` is released while this widget has
        keyboard focus.
        """
        pass

    def event_global_key_press(self, key, char):
        """
        Called when a key is pressed, regardless of which widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyPress` for more information.
        """
        pass

    def event_global_key_release(self, key):
        """
        Called when a key is released, regardless of which widget has
        keyboard focus.  See the documentation for
        :class:`sge.input.KeyRelease` for more information.
        """
        pass

    def event_global_mouse_button_press(self, button):
        """
        Called when a mouse button is pressed, regardless of which
        widget has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonPress` for more information.
        """
        pass

    def event_global_mouse_button_release(self, button):
        """
        Called when a mouse button is released, regardless of which
        widget has mouse focus.  See the documentation for
        :class:`sge.input.MouseButtonRelease` for more information.
        """
        pass

    def event_global_joystick_axis_move(self, js_name, js_id, axis, value):
        """
        Called when a joystick axis is moved, regardless of which widget
        has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickAxisMove` for more information.
        """
        pass

    def event_global_joystick_hat_move(self, js_name, js_id, hat, x, y):
        """
        Called when a joystick hat is moved, regardless of which widget
        has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickHatMove` for more information.
        """
        pass

    def event_global_joystick_trackball_move(self, js_name, js_id, ball, x, y):
        """
        Called when a joystick trackball is moved, regardless of which
        widget has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickTrackballMove` for more information.
        """
        pass

    def event_global_joystick_button_press(self, js_name, js_id, button):
        """
        Called when a joystick button is pressed, regardless of which
        widget has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonPress` for more information.
        """
        pass

    def event_global_joystick_button_release(self, js_name, js_id, button):
        """
        Called when a joystick button is released, regardless of which
        widget has keyboard focus.  See the documentation for
        :class:`sge.input.JoystickButtonRelease` for more information.
        """
        pass

    def event_global_joystick(self, js_name, js_id, input_type, input_id,
                              value):
        """
        Called when a joystick event occurs, regardless of which window
        has keyboard focus.  See the documentation for
        :class:`sge.inputJoystickEvent` for more information.
        """
        pass


class DecorativeWidget(Widget):

    """
    Identical to :class:`Widget`, except that :attr:`tab_focus` is
    :const:`False` by default.
    """

    tab_focus = False


class Label(DecorativeWidget):

    """
    This widget simply displays some text.

    .. attribute:: text

       The text this label should display.

    .. attribute:: font

       The font this label's text should be rendered with.  If set to
       :const:`None`, the value of :data:`xsge_gui.default_font` is
       used.

    .. attribute:: width

       The width of the imaginary rectangle the text is drawn in.  See
       the documentation for :meth:`sge.gfx.Sprite.draw_text` for more
       information.

    .. attribute:: height

       The height of the imaginary rectangle the text is drawn in.  See
       the documentation for :meth:`sge.gfx.Sprite.draw_text` for more
       information.

    .. attribute:: halign

       The horizontal alignment of the text.  See the documentation for
       :meth:`sge.gfx.Sprite.draw_text` for more information.

    .. attribute:: valign

       The vertical alignment of the text.  See the documentation for
       :meth:`sge.gfx.Sprite.draw_text` for more information.

    See the documentation for :class:`xsge_gui.Widget` for more
    information.
    """

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, value):
        self.__font = value if value is not None else default_font

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value if value is not None else text_color

    def __init__(self, parent, x, y, z, text, font=None, width=None,
                 height=None, color=None, halign="left", valign="top"):
        super().__init__(parent, x, y, z)
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        self.color = color
        self.halign = halign
        self.valign = valign

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_text(self.font, self.text, parent.x + self.x,
                                  parent.y + self.y, width=self.width,
                                  height=self.height, color=self.color,
                                  halign=self.halign, valign=self.valign)
        else:
            self.destroy()


class ProgressiveLabel(Label):

    """
    This widget is a version of :class:`xsge_gui.Label` which
    progressively builds :attr:`text` one character at a time, making it
    look like the text is being typed in real-time.

    .. attribute:: full_text

       The value that :attr:`text` progressively becomes.

    .. attribute:: rate

       The rate at which :attr:`text` is built in characters per minute.
    """

    def __init__(self, parent, x, y, z, full_text, font=None, width=None,
                 height=None, color=None, halign="left", valign="top",
                 rate=1000):
        self.full_text = full_text
        self.rate = rate
        self.__time_passed = 0
        super().__init__(
            parent, x, y, z, "", font=font, width=width, height=height,
            color=color, halign=halign, valign=valign)

    def event_step(self, time_passed, delta_mult):
        if len(self.text) < len(self.full_text):
            self.__time_passed += time_passed
            delay = 60000 / self.rate
            while self.__time_passed >= delay:
                self.__time_passed -= delay
                i = len(self.text)
                if i < len(self.full_text):
                    self.text += self.full_text[i]
                    self.event_add_character()

    def event_add_character(self):
        """Called when a character is added to :attr:`text`."""
        pass


class Button(Widget):

    """
    This widget contains some text and can be clicked on by the user.

    .. attribute:: text

       The text contained in the button.

    .. attribute:: width

       The width of the button.  If set to :const:`None`, the width is
       chosen based on the width of the rendered text.

    .. attribute:: halign

       The horizontal alignment of the text.  See the documentation for
       :meth:`sge.gfx.Sprite.draw_text` for more information.

    See the documentation for :class:`xsge_gui.Widget` for more
    information.
    """

    def __init__(self, parent, x, y, z, text, width=None, halign="center"):
        super().__init__(parent, x, y, z)
        self.text = text
        self.width = width
        self.halign = halign
        self.__pressed = False
        self.sprite_normal = None
        self.sprite_selected = None
        self.sprite_pressed = None
        self.redraw()

    def redraw(self):
        h = button_sprite.height
        if self.width is None:
            w = round(button_font.get_width(self.text, height=h))
            sprite_w = w + button_left_sprite.width + button_right_sprite.width
        else:
            sprite_w = round(self.width)
            w = sprite_w - button_left_sprite.width - button_right_sprite.width

        left = button_left_sprite.width
        right = sprite_w - button_right_sprite.width
        self.sprite_normal = sge.gfx.Sprite(width=sprite_w, height=h)
        self.sprite_normal.draw_lock()
        for i in range(left, right, button_sprite.width):
            self.sprite_normal.draw_sprite(button_sprite, 0, i, 0)
        self.sprite_normal.draw_sprite(button_left_sprite, 0, 0, 0)
        self.sprite_normal.draw_sprite(button_right_sprite, 0, right, 0)
        self.sprite_normal.draw_text(button_font, self.text, sprite_w / 2,
                                     h / 2, width=w, height=h,
                                     color=button_text_color,
                                     halign=self.halign, valign="middle")
        self.sprite_normal.draw_unlock()

        sprite_w = (w + button_selected_left_sprite.width +
                    button_selected_right_sprite.width)
        left = button_selected_left_sprite.width
        right = sprite_w - button_selected_right_sprite.width
        self.sprite_selected = sge.gfx.Sprite(width=sprite_w, height=h)
        self.sprite_selected.draw_lock()
        for i in range(left, right, button_selected_sprite.width):
            self.sprite_selected.draw_sprite(button_selected_sprite, 0, i, 0)
        self.sprite_selected.draw_sprite(button_selected_left_sprite, 0, 0, 0)
        self.sprite_selected.draw_sprite(button_selected_right_sprite, 0,
                                         right, 0)
        self.sprite_selected.draw_text(button_font, self.text, sprite_w / 2,
                                       h / 2, width=w, height=h,
                                       color=button_text_color,
                                       halign=self.halign, valign="middle")
        self.sprite_selected.draw_unlock()

        sprite_w = (w + button_pressed_left_sprite.width +
                    button_pressed_right_sprite.width)
        left = button_pressed_left_sprite.width
        right = sprite_w - button_pressed_right_sprite.width
        self.sprite_pressed = sge.gfx.Sprite(width=sprite_w, height=h)
        self.sprite_pressed.draw_lock()
        for i in range(left, right, button_pressed_sprite.width):
            self.sprite_pressed.draw_sprite(button_pressed_sprite, 0, i, 0)
        self.sprite_pressed.draw_sprite(button_pressed_left_sprite, 0, 0, 0)
        self.sprite_pressed.draw_sprite(button_pressed_right_sprite, 0, right,
                                        0)
        self.sprite_pressed.draw_text(button_font, self.text, sprite_w / 2,
                                      h / 2, width=w, height=h,
                                      color=button_text_color,
                                      halign=self.halign, valign="middle")
        self.sprite_pressed.draw_unlock()

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)
        else:
            self.destroy()

    def event_step(self, time_passed, delta_mult):
        parent = self.parent()
        if parent is not None:
            handler = parent.parent()
            if (handler is not None and
                ((handler.keyboard_focused_window is parent and
                  parent.keyboard_focused_widget is self) or
                 (handler.get_mouse_focused_window() is parent and
                  parent.get_mouse_focused_widget() is self))):
                if self.__pressed:
                    self.sprite = self.sprite_pressed
                else:
                    self.sprite = self.sprite_selected
            else:
                self.sprite = self.sprite_normal

    def event_mouse_button_press(self, button):
        if button == "left":
            self.__pressed = True

    def event_mouse_button_release(self, button):
        if button == "left":
            if self.__pressed:
                self.event_press()

    def event_press_enter(self):
        self.event_press()

    def event_global_mouse_button_release(self, button):
        if button == "left":
            self.__pressed = False

    def event_press(self):
        """
        Called when this button is clicked on, or when the Enter key is
        pressed while this button is selected.
        """
        pass


class CheckBox(Widget):

    """
    This widget can be toggled "on" or "off" by clicking on it.

    .. attribute:: enabled

       Whether or not the checkbox is on.

    See the documentation for :class:`xsge_gui.Widget` for more
    information.
    """

    def __init__(self, parent, x, y, z, enabled=False):
        super().__init__(parent, x, y, z)
        self.enabled = enabled
        self.__pressed = False

    def event_step(self, time_passed, delta_mult):
        if self.enabled:
            self.sprite = checkbox_on_sprite
        else:
            self.sprite = checkbox_off_sprite

    def event_mouse_button_press(self, button):
        if button == "left":
            self.__pressed = True

    def event_mouse_button_release(self, button):
        if button == "left":
            if self.__pressed:
                self.event_press_enter()

    def event_press_enter(self):
        self.enabled = not self.enabled
        self.event_toggle()

    def event_global_mouse_button_release(self, button):
        if button == "left":
            self.__pressed = False

    def event_toggle(self):
        """
        Called when the state of the checkbox is toggled by the user.
        """
        pass


class RadioButton(CheckBox):

    """
    This widget is mostly like :class:`xsge_gui.CheckBox`, but clicking
    on it while it is on will not turn it off, and only one radio button
    can be on at any given time (i.e. enabling one radio button on a
    window will disable all others on the same window).

    See the documentation for :class:`xsge_gui.CheckBox` for more
    information.
    """

    def event_step(self, time_passed, delta_mult):
        if self.enabled:
            self.sprite = radiobutton_on_sprite
        else:
            self.sprite = radiobutton_off_sprite

    def event_press_enter(self):
        # Enable the radiobutton, disable any others, and call
        # event_toggle.
        if not self.enabled:
            self.enabled = True
            parent = self.parent()
            if parent is not None:
                for widget in parent.widgets:
                    if widget is not self and isinstance(widget, RadioButton):
                        if widget.enabled:
                            widget.enabled = False
                            widget.event_toggle()

            self.event_toggle()

    def event_toggle(self):
        """
        Called when the state of the radiobutton is toggled by the user.
        """
        pass


class ProgressBar(DecorativeWidget):

    """
    This widget displays a bar which can be used to show progress (e.g.
    of some task being done).

    .. attribute:: width

       The width of the progress bar.

    .. attribute:: progress

       The progress indicated by the progress bar as a factor (i.e.
       ``0`` is no completion, ``1`` is full completion, and ``0.5`` is
       half completion).
    """

    def __init__(self, parent, x, y, z, width=128, progress=0):
        super().__init__(parent, x, y, z, sge.gfx.Sprite(width=1, height=1))
        self.width = width
        self.progress = progress
        self.redraw()

    def redraw(self):
        self.progress = max(0, min(self.progress, 1))
        self.sprite.width = self.width
        self.sprite.height = progressbar_container_sprite.height
        left = progressbar_container_left_sprite.width
        right = self.width - progressbar_container_right_sprite.width
        y = round((progressbar_container_sprite.height
                   - progressbar_sprite.height) / 2)
        pixels = round(self.progress * (right-left))

        self.sprite.draw_lock()
        self.sprite.draw_clear()

        self.sprite.draw_sprite(progressbar_container_left_sprite, 0, 0, 0)

        for x in range(left, right,
                                 progressbar_container_sprite.width):
            self.sprite.draw_sprite(progressbar_container_sprite, 0, x, 0)

        for x in range(left, left + pixels,
                                 progressbar_sprite.width):
            self.sprite.draw_sprite(progressbar_sprite, 0, x, y)

        self.sprite.draw_erase(right, 0, self.sprite.width - right,
                               self.sprite.height)
        self.sprite.draw_sprite(progressbar_container_right_sprite, 0, right,
                                0)
        self.sprite.draw_sprite(progressbar_left_sprite, 0,
                                left - progressbar_left_sprite.width, y)
        self.sprite.draw_sprite(progressbar_right_sprite, 0, left + pixels, y)

        self.sprite.draw_unlock()


class TextBox(Widget):

    """
    This widget provides a place for the user to enter text.

    .. attribute:: width

       The width of the text box.

    .. attribute:: text

       The text in the text box.

    .. attribute:: text_limit

       The maximum number of characters allowed in the text box.

    See the documentation for :class:`xsge_gui.Widget` for more
    information.
    """

    def __init__(self, parent, x, y, z, width=32, text="", text_limit=1000):
        super().__init__(parent, x, y, z, sge.gfx.Sprite(width=1, height=1))
        self.width = width
        self.text = text
        self.text_limit = text_limit
        self._cursor_pos = 0
        self._clicked_pos = None
        self._selected = None
        self._text_x = 0
        self._cursor_shown = True
        self._cursor_blink_time = TEXTBOX_CURSOR_BLINK_TIME
        self.redraw()

    def redraw(self):
        self.sprite.width = self.width
        self.sprite.height = textbox_sprite.height
        self._cursor_h = textbox_font.get_height("|")
        left = textbox_left_sprite.width
        right = self.width - textbox_right_sprite.width

        self.sprite.draw_lock()
        self.sprite.draw_clear()

        self.sprite.draw_sprite(textbox_left_sprite, 0, 0, 0)

        for i in range(left, right, textbox_sprite.width):
            self.sprite.draw_sprite(textbox_sprite, 0, i, 0)

        self.sprite.draw_erase(right, 0, self.sprite.width - right,
                               self.sprite.height)
        self.sprite.draw_sprite(textbox_right_sprite, 0, right, 0)

        self.sprite.draw_unlock()

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            sge.game.project_sprite(self.sprite, 0, parent.x + self.x,
                                    parent.y + self.y)

            self._cursor_pos = max(0, min(self._cursor_pos, len(self.text)))

            text_area_w = (self.width - textbox_right_sprite.width -
                           textbox_left_sprite.width)

            tl = self._cursor_pos
            # The first loop is necessary because sometimes the cursor
            # is not within the visible area for a brief moment.  This
            # accounts for that.
            while (tl < len(self.text) and
                   self._text_x + textbox_font.get_width(self.text[:tl]) < 0):
                tl += 1
            while (tl > 0 and
                   self._text_x + textbox_font.get_width(self.text[:tl]) >= 0):
                tl -= 1

            text_x = self._text_x + textbox_font.get_width(self.text[:tl])

            tr = tl
            while (tr < len(self.text) and
                   (text_x + textbox_font.get_width(self.text[tl:tr]) <=
                    text_area_w)):
                tr += 1

            text_y = textbox_sprite.height / 2
            cursor_x = textbox_font.get_width(self.text[:self._cursor_pos])
            cursor_y = text_y - self._cursor_h / 2

            if 0 < self._cursor_pos < len(self.text):
                min_edge = TEXTBOX_MIN_EDGE
            else:
                min_edge = 0

            if self._text_x + cursor_x < min_edge:
                self._text_x = min_edge - cursor_x
            elif self._text_x + cursor_x > text_area_w - min_edge:
                self._text_x = text_area_w - min_edge - cursor_x

            text_sprite = sge.gfx.Sprite(width=text_area_w,
                                         height=textbox_sprite.height)
            text_sprite.draw_lock()

            text_sprite.draw_text(textbox_font, self.text[tl:tr], text_x,
                                  text_y, color=textbox_text_color,
                                  valign="middle")

            if self._selected is None:
                if (self._cursor_shown and
                        parent.keyboard_focused_widget is self):
                    text_sprite.draw_line(cursor_x + self._text_x, cursor_y,
                                          cursor_x + self._text_x,
                                          cursor_y + self._cursor_h,
                                          textbox_text_color)
            else:
                a, b = self._selected
                a = max(a, tl)
                b = min(b, tr)
                x = textbox_font.get_width(self.text[:a])
                w = textbox_font.get_width(self.text[a:b])
                y = text_y - self._cursor_h / 2
                text_sprite.draw_rectangle(x + self._text_x, y, w,
                                           self._cursor_h,
                                           fill=textbox_highlight_color)
                text_sprite.draw_text(textbox_font, self.text[a:b],
                                      x + self._text_x, text_y,
                                      color=textbox_text_selected_color,
                                      valign="middle")

            text_sprite.draw_unlock()

            sge.game.project_sprite(
                text_sprite, 0, parent.x + self.x + textbox_left_sprite.width,
                parent.y + self.y)
        else:
            self.destroy()

    def _show_cursor(self):
        # Forcibly show the cursor (restarting the animation).
        self._cursor_shown = True
        self._cursor_blink_time = TEXTBOX_CURSOR_BLINK_TIME

    def _get_previous_word(self):
        # Return the index of the start of the previous or current word.
        i = max(0, self._cursor_pos - 1)
        while i > 0 and not self.text[i].isalnum():
            i -= 1

        while i > 0 and self.text[i].isalnum():
            i -= 1

        return i

    def _get_next_word(self):
        # Return the index of the end of the next or current word.
        i = min(self._cursor_pos + 1, len(self.text))
        while i < len(self.text) and not self.text[i].isalnum():
            i += 1

        while i < len(self.text) and self.text[i].isalnum():
            i += 1

        return i

    def _move_selection(self, pos):
        # Move the selection so that the cursor is at ``pos``.
        if self._selected is not None:
            if self._selected[0] == self._cursor_pos:
                fixed_pos = self._selected[1]
            else:
                fixed_pos = self._selected[0]

            if fixed_pos > pos:
                self._selected = (pos, fixed_pos)
            elif pos > fixed_pos:
                self._selected = (fixed_pos, pos)
            else:
                self._selected = None
        else:
            if self._cursor_pos > pos:
                self._selected = (pos, self._cursor_pos)
            elif pos > self._cursor_pos:
                self._selected = (self._cursor_pos, pos)
            else:
                self._selected = None

        self._cursor_pos = pos

    def _delete_selection(self):
        # Delete the currently selected text.
        if self._selected is not None:
            a, b = self._selected
            self._cursor_pos = a
            self.text = ''.join([self.text[:a], self.text[b:]])
            self._selected = None

    def _insert_text(self, text):
        # Insert the indicated text at the current cursor position.  If
        # text is selected, it is deleted first.
        self._delete_selection()

        if len(self.text) + len(text) <= self.text_limit:
            i = self._cursor_pos
            self.text = ''.join([self.text[:i], text, self.text[i:]])
            self._cursor_pos += len(text)

        self._show_cursor()

    def _get_cursor_position(self):
        # Get the cursor position from mouse position ``x``.
        parent = self.parent()
        if parent is not None:
            x = (sge.mouse.get_x() - parent.x - self.x - self._text_x -
                 textbox_left_sprite.width)
            i = 0
            while (i < len(self.text) and
                   textbox_font.get_width(self.text[:i]) < x):
                i += 1

            # FIXME: This feels inaccurate, but I can't think of any way
            # to reliably make it better.  Leaving it as-is for now.
            return i

        return 0

    def _update_selection(self):
        # Update the selection, for use when the mouse button is held
        # down.
        self._cursor_pos = self._get_cursor_position()
        if self._cursor_pos > self._clicked_pos:
            self._selected = (self._clicked_pos, self._cursor_pos)
        elif self._cursor_pos < self._clicked_pos:
            self._selected = (self._cursor_pos, self._clicked_pos)
        else:
            self._selected = None

    def event_step(self, time_passed, delta_mult):
        self._cursor_blink_time -= time_passed
        if self._cursor_blink_time <= 0:
            self._cursor_shown = not self._cursor_shown
            self._cursor_blink_time += TEXTBOX_CURSOR_BLINK_TIME

        if self._clicked_pos is not None:
            self._update_selection()

    def event_key_press(self, key, char):
        if sge.keyboard.get_modifier("ctrl"):
            if key == "left":
                if sge.keyboard.get_modifier("shift"):
                    self._move_selection(self._get_previous_word())
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    else:
                        self._cursor_pos = self._get_previous_word()

                    self._show_cursor()
            elif key == "right":
                if sge.keyboard.get_modifier("shift"):
                    self._move_selection(self._get_next_word())
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    else:
                        self._cursor_pos = self._get_next_word()

                    self._show_cursor()
            elif key == 'a':
                self._selected = (0, len(self.text))
                self._cursor_pos = len(self.text)
            elif key == 'x':
                if self._selected is not None:
                    a, b = self._selected
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(self.text[a:b])
                    r.destroy()
                    self._delete_selection()
            elif key == 'c':
                if self._selected is not None:
                    a, b = self._selected
                    r = Tk()
                    r.withdraw()
                    r.clipboard_clear()
                    r.clipboard_append(self.text[a:b])
                    r.destroy()
            elif key == 'v':
                r = Tk()
                r.withdraw()
                new_text = r.selection_get(selection="CLIPBOARD")
                r.destroy()
                self._insert_text(new_text.replace('\n', ' '))
        else:
            if key == "left":
                if sge.keyboard.get_modifier("shift"):
                    pos = max(0, self._cursor_pos - 1)
                    self._move_selection(pos)
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[0]
                        self._selected = None
                    elif self._cursor_pos > 0:
                        self._cursor_pos -= 1

                    self._show_cursor()
            elif key == "right":
                if sge.keyboard.get_modifier("shift"):
                    pos = min(self._cursor_pos + 1, len(self.text))
                    self._move_selection(pos)
                else:
                    if self._selected is not None:
                        self._cursor_pos = self._selected[1]
                        self._selected = None
                    elif self._cursor_pos < len(self.text):
                        self._cursor_pos += 1

                    self._show_cursor()
            elif key == "home":
                self._cursor_pos = 0
                self._selected = None
                self._show_cursor()
            elif key == "end":
                self._cursor_pos = len(self.text)
                self._selected = None
                self._show_cursor()
            elif key == "backspace":
                if self._selected is None and self._cursor_pos > 0:
                    self._selected = (self._cursor_pos - 1, self._cursor_pos)

                self._delete_selection()
                self._show_cursor()
            elif key == "delete":
                if (self._selected is None and
                        self._cursor_pos < len(self.text)):
                    self._selected = (self._cursor_pos, self._cursor_pos + 1)

                self._delete_selection()
                self._show_cursor()
            elif char and char not in ('\n', '\t', '\b', '\r', '\a', '\f',
                                       '\v', '\x1b'):
                self._insert_text(char)

    def event_mouse_button_press(self, button):
        if button == "left":
            parent = self.parent()
            if parent is not None:
                parent.keyboard_focused_widget = self
                self._clicked_pos = self._get_cursor_position()
                self._show_cursor()

    def event_global_mouse_button_release(self, button):
        if button == "left":
            if self._clicked_pos is not None:
                self._update_selection()
                self._clicked_pos = None

    def event_change_text(self):
        """Change text event.

        Called when the user changes the text in the textbox.

        """
        pass


class MenuItem(Widget):

    """
    This widget has two sprites: one for when it is selected, and one
    for when it is unselected.  Meant to be used with
    :class:`xsge_gui.MenuWindow` or :class:`xsge_gui.MenuDialog`.

    .. attribute:: sprite_normal

       The sprite to use as :attr:`sprite` when this widget is
       unselected.

    .. attribute:: sprite_selected

       The sprite to use as :attr:`sprite` when this widget is selected.

    See the documentation for :class:`xsge_gui.Widget` for more
    information.
    """

    def __init__(self, parent, x, y, z, sprite_normal=None,
                 sprite_selected=None):
        super().__init__(parent, x, y, z, sprite=sprite_normal)
        self.sprite_normal = self.sprite
        if sprite_selected is not None:
            self.sprite_selected = sprite_selected
        else:
            self.sprite_selected = self.sprite
        self.__frame = 0

    def refresh(self):
        parent = self.parent()
        if parent is not None:
            if parent.keyboard_focused_widget is self:
                spr = self.sprite_selected
            else:
                spr = self.sprite_normal

            sge.game.project_sprite(spr, round(self.__frame),
                                    parent.x + self.x, parent.y + self.y)
        else:
            self.destroy()

    def event_step(self, time_passed, delta_mult):
        self.__frame += delta_mult


def init():
    """
    Prepare this module for use.  This function in particular creates
    the sprites and fonts it uses for windows and widgets.  Because of
    this, it must not be called until after a :class:`sge.dsp.Game`
    object has been created.
    """
    global default_font
    global button_font
    global textbox_font
    global title_font
    global button_sprite
    global button_left_sprite
    global button_right_sprite
    global button_pressed_sprite
    global button_pressed_left_sprite
    global button_pressed_right_sprite
    global button_selected_sprite
    global button_selected_left_sprite
    global button_selected_right_sprite
    global checkbox_off_sprite
    global checkbox_on_sprite
    global progressbar_sprite
    global progressbar_left_sprite
    global progressbar_right_sprite
    global progressbar_container_sprite
    global progressbar_container_left_sprite
    global progressbar_container_right_sprite
    global radiobutton_off_sprite
    global radiobutton_on_sprite
    global textbox_sprite
    global textbox_left_sprite
    global textbox_right_sprite
    global window_border_left_sprite
    global window_border_right_sprite
    global window_border_bottom_sprite
    global window_border_bottomleft_sprite
    global window_border_bottomright_sprite
    global window_border_bottomright_resizable_sprite
    global window_border_top_sprite
    global window_border_topleft_sprite
    global window_border_topright_sprite

    default_font = sge.gfx.Font([os.path.join(DATA, "DroidSans.ttf"),
                                 "Droid Sans"], size=12)
    button_font = sge.gfx.Font([os.path.join(DATA, "DroidSans-Bold.ttf"),
                                "Droid Sans"], size=12)
    textbox_font = default_font
    title_font = sge.gfx.Font([os.path.join(DATA, "DroidSans-Bold.ttf"),
                               "Droid Sans"], size=14)

    try:
        button_sprite = sge.gfx.Sprite("button", DATA)
        button_left_sprite = sge.gfx.Sprite("button_left", DATA)
        button_right_sprite = sge.gfx.Sprite("button_right", DATA)
        button_pressed_sprite = sge.gfx.Sprite("button_pressed", DATA)
        button_pressed_left_sprite = sge.gfx.Sprite("button_pressed_left",
                                                    DATA)
        button_pressed_right_sprite = sge.gfx.Sprite("button_pressed_right",
                                                     DATA)
        button_selected_sprite = sge.gfx.Sprite("button_selected", DATA)
        button_selected_left_sprite = sge.gfx.Sprite("button_selected_left",
                                                     DATA)
        button_selected_right_sprite = sge.gfx.Sprite("button_selected_right",
                                                      DATA)
        checkbox_off_sprite = sge.gfx.Sprite("checkbox_off", DATA)
        checkbox_on_sprite = sge.gfx.Sprite("checkbox_on", DATA)
        progressbar_sprite = sge.gfx.Sprite("progressbar", DATA)
        progressbar_left_sprite = sge.gfx.Sprite("progressbar_left", DATA)
        progressbar_right_sprite = sge.gfx.Sprite("progressbar_right", DATA)
        progressbar_container_sprite = sge.gfx.Sprite("progressbar_container",
                                                      DATA)
        progressbar_container_left_sprite = sge.gfx.Sprite(
            "progressbar_container_left", DATA)
        progressbar_container_right_sprite = sge.gfx.Sprite(
            "progressbar_container_right", DATA)
        radiobutton_off_sprite = sge.gfx.Sprite("radiobutton_off", DATA)
        radiobutton_on_sprite = sge.gfx.Sprite("radiobutton_on", DATA)
        textbox_sprite = sge.gfx.Sprite("textbox", DATA)
        textbox_left_sprite = sge.gfx.Sprite("textbox_left", DATA)
        textbox_right_sprite = sge.gfx.Sprite("textbox_right", DATA)
        window_border_left_sprite = sge.gfx.Sprite("window_border_left", DATA)
        window_border_right_sprite = sge.gfx.Sprite("window_border_right",
                                                    DATA)
        window_border_bottom_sprite = sge.gfx.Sprite("window_border_bottom",
                                                     DATA)
        window_border_bottomleft_sprite = sge.gfx.Sprite(
            "window_border_bottomleft", DATA)
        window_border_bottomright_sprite = sge.gfx.Sprite(
            "window_border_bottomright", DATA)
        window_border_top_sprite = sge.gfx.Sprite("window_border_top", DATA)
        window_border_topleft_sprite = sge.gfx.Sprite("window_border_topleft",
                                                      DATA)
        window_border_topright_sprite = sge.gfx.Sprite(
            "window_border_topright", DATA)
    except IOError:
        black = sge.gfx.Color("black")
        white = sge.gfx.Color("white")
        button_sprite = sge.gfx.Sprite(width=1, height=24)
        button_sprite.draw_rectangle(0, 0, 1, 24, fill=black)
        button_sprite.draw_rectangle(0, 1, 1, 22, fill=white)
        button_left_sprite = sge.gfx.Sprite(width=10, height=24)
        button_left_sprite.draw_rectangle(0, 0, 10, 24, fill=black)
        button_right_sprite = button_left_sprite
        button_selected_sprite = sge.gfx.Sprite(width=1, height=24)
        button_selected_sprite.draw_rectangle(0, 0, 1, 24, fill=black)
        button_selected_sprite.draw_rectangle(0, 1, 1, 22,
                                              fill=sge.gfx.Color("aqua"))
        button_selected_left_sprite = button_left_sprite
        button_selected_right_sprite = button_right_sprite
        button_pressed_sprite = button_selected_sprite
        button_pressed_left_sprite = button_selected_left_sprite
        button_pressed_right_sprite = button_selected_right_sprite
        checkbox_off_sprite = sge.gfx.Sprite(width=16, height=16)
        checkbox_off_sprite.draw_rectangle(0, 0, 16, 16, fill=white,
                                           outline=black)
        checkbox_on_sprite = sge.gfx.Sprite(width=16, height=16)
        checkbox_on_sprite.draw_sprite(checkbox_off_sprite, 0, 0, 0)
        checkbox_on_sprite.draw_line(0, 0, 15, 15, black)
        checkbox_on_sprite.draw_line(0, 15, 15, 0, black)
        progressbar_sprite = sge.gfx.Sprite(width=1, height=18)
        progressbar_sprite.draw_rectangle(0, 0, 1, 18, fill=white)
        progressbar_left_sprite = sge.gfx.Sprite(width=2, height=18)
        progressbar_left_sprite.draw_rectangle(0, 0, 2, 18, fill=white)
        progressbar_right_sprite = progressbar_left_sprite
        progressbar_container_sprite = sge.gfx.Sprite(width=1, height=24)
        progressbar_container_sprite.draw_rectangle(0, 0, 1, 24, fill=black)
        progressbar_container_left_sprite = sge.gfx.Sprite(width=5, height=24)
        progressbar_container_left_sprite.draw_rectangle(0, 0, 5, 24,
                                                         fill=black)
        progressbar_container_right_sprite = progressbar_container_left_sprite
        radiobutton_off_sprite = checkbox_off_sprite
        radiobutton_on_sprite = checkbox_on_sprite
        textbox_sprite = button_sprite
        textbox_left_sprite = sge.gfx.Sprite(width=4, height=24)
        textbox_left_sprite.draw_rectangle(0, 0, 4, 24, fill=black)
        textbox_right_sprite = textbox_left_sprite
        window_border_left_sprite = sge.gfx.Sprite(width=4, height=1)
        window_border_left_sprite.draw_rectangle(0, 0, 4, 1, fill=black)
        window_border_right_sprite = window_border_left_sprite
        window_border_bottom_sprite = sge.gfx.Sprite(width=1, height=4)
        window_border_bottom_sprite.draw_rectangle(0, 0, 1, 4, fill=black)
        window_border_bottomleft_sprite = sge.gfx.Sprite(width=4, height=4)
        window_border_bottomleft_sprite.draw_rectangle(0, 0, 4, 4, fill=black)
        window_border_bottomright_sprite = window_border_bottomleft_sprite
        window_border_top_sprite = sge.gfx.Sprite(width=1, height=28)
        window_border_top_sprite.draw_rectangle(0, 0, 1, 28, fill=black)
        window_border_topleft_sprite = sge.gfx.Sprite(width=11, height=28)
        window_border_topleft_sprite.draw_rectangle(0, 0, 11, 28, fill=black)
        window_border_topright_sprite = sge.gfx.Sprite(width=23, height=28)
        window_border_topright_sprite.draw_rectangle(0, 0, 23, 28, fill=black)
        window_border_topright_sprite.draw_line(0, 0, 23, 23,
                                                sge.gfx.Color("red"))
        window_border_topright_sprite.draw_line(0, 23, 23, 0,
                                                sge.gfx.Color("red"))


def show_message(parent=None, message="", title="Message", buttons=("Ok",),
                 default=-1, width=320, height=None):
    """
    Show a message and return the button pressed.

    Arguments:

    - ``parent`` -- The parent handler of the
      :class:`xsge_gui.MessageDialog` object created.  Set to
      :const:`None` to create a new handler and then destroy it after
      the dialog is shown.
    - ``message`` -- The message shown to the user.
    - ``title`` -- The window title of the
      :class:`xsge_gui.MessageDialog` object created.
    - ``buttons`` -- A list of strings to put inside the buttons, from
      left to right.
    - ``default`` -- The index of the default button selected by the
      keyboard (i.e. the default choice).
    - ``width`` -- The width of the :class:`xsge_gui.MessageDialog`
      object created.
    - ``height`` -- The height of the :class:`xsge_gui.MessageDialog`
      object created.  If set to :const:`None`, set the height
      automatically based on the space needed for the text.

    Value returned is the index of the button pressed, where ``0`` is
    the leftmost button, or :const:`None` if no button was pressed (i.e.
    the close button on the window frame was pressed instead).

    See the documentation for :class:`xsge_gui.MessageDialog` for more
    information.
    """
    if parent is None:
        parent = Handler.create()
        destroy_parent = True
    else:
        destroy_parent = False

    w = MessageDialog(parent, message=message, title=title, buttons=buttons,
                      default=default, width=width, height=height)
    w.show()
    w.destroy()

    if destroy_parent:
        parent.destroy()

    return w.choice


def get_text_entry(parent=None, message="", title="Text Entry", text="",
                   width=320, height=None):
    """
    Return text entered by the user.

    Arguments:

    - ``parent`` -- The parent handler of the
      :class:`xsge_gui.MessageDialog` object created.  Set to
      :const:`None` to create a new handler and then destroy it after
      the dialog is shown.
    - ``message`` -- The message shown to the user.
    - ``title`` -- The window title of the
      :class:`xsge_gui.TextEntryDialog` object created.
    - ``text`` -- The text in the text box by default.
    - ``width`` -- The width of the :class:`xsge_gui.TextEntryDialog`
      object created.
    - ``height`` -- The height of the :class:`xsge_gui.TextEntryDialog`
      object created.  If set to :const:`None`, set the height
      automatically based on the space needed for the text.

    Value returned is the text entered if the "Ok" button is pressed, or
    :const:`None` otherwise.

    See the documentation for :class:`xsge_gui.TextEntryDialog` for more
    information.
    """
    if parent is None:
        parent = Handler.create()
        destroy_parent = True
    else:
        destroy_parent = False

    w = TextEntryDialog(parent, message=message, title=title, text=text,
                        width=width, height=height)
    w.show()
    w.destroy()

    if destroy_parent:
        parent.destroy()

    return w.text


def get_menu_selection(x, y, items, parent=None, default=0, font_normal=None,
                       color_normal=None, font_selected=None,
                       color_selected=None,
                       background_color=sge.gfx.Color("#0000"), height=None,
                       margin=0, halign="left", valign="top",
                       outline_normal=None, outline_selected=None,
                       outline_thickness_normal=0,
                       outline_thickness_selected=0, selection_prefix="",
                       selection_suffix=""):
    """
    Show a menu and return the index of the menu item selected.

    Arguments:

    - ``parent`` -- The parent handler of the
      :class:`xsge_gui.TextMenuDialog` object created.  Set to
      :const:`None` to create a new handler and then destroy it after
      the dialog is shown.
    - ``default`` -- The index of the item to select by default.

    See the documentation for :class:`xsge_gui.MenuWindow.from_text` for
    more information.
    """
    if items:
        if parent is None:
            parent = Handler.create()
            destroy_parent = True
        else:
            destroy_parent = False

        w = MenuDialog.from_text(
            parent, x, y, items, font_normal=font_normal,
            color_normal=color_normal, font_selected=font_selected,
            color_selected=color_selected, background_color=background_color,
            height=height, margin=margin, halign=halign, valign=valign,
            outline_normal=outline_normal, outline_selected=outline_selected,
            outline_thickness_normal=outline_thickness_normal,
            outline_thickness_selected=outline_thickness_selected,
            selection_prefix=selection_prefix,
            selection_suffix=selection_suffix)
        default %= len(w.widgets)
        w.keyboard_selected_widget = w.widgets[default]
        w.show()
        w.destroy()

        if destroy_parent:
            parent.destroy()

        return w.choice
    else:
        return None
