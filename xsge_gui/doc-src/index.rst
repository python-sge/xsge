****************
xSGE GUI Toolkit
****************

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

.. automodule:: xsge_gui

xsge_gui Classes
================

xsge_gui.Handler
----------------

.. autoclass:: xsge_gui.Handler

xsge_gui.Handler Methods
~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_gui.Handler.get_mouse_focused_window

xsge_gui.Window
---------------

.. autoclass:: xsge_gui.Window

xsge_gui.Window Methods
~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_gui.Window.show

.. automethod:: xsge_gui.Window.hide

.. automethod:: xsge_gui.Window.move_to_front

.. automethod:: xsge_gui.Window.move_to_back

.. automethod:: xsge_gui.Window.destroy

.. automethod:: xsge_gui.Window.redraw

.. automethod:: xsge_gui.Window.refresh

.. automethod:: xsge_gui.Window.get_mouse_on_titlebar

.. automethod:: xsge_gui.Window.get_mouse_focused_widget

xsge_gui.Window Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_gui.Window.event_step

.. automethod:: xsge_gui.Window.event_change_keyboard_focus

.. automethod:: xsge_gui.Window.event_key_press

.. automethod:: xsge_gui.Window.event_key_release

.. automethod:: xsge_gui.Window.event_mouse_button_press

.. automethod:: xsge_gui.Window.event_mouse_button_release

.. automethod:: xsge_gui.Window.event_joystick_axis_move

.. automethod:: xsge_gui.Window.event_joystick_hat_move

.. automethod:: xsge_gui.Window.event_joystick_trackball_move

.. automethod:: xsge_gui.Window.event_joystick_button_press

.. automethod:: xsge_gui.Window.event_joystick_button_release

.. automethod:: xsge_gui.Window.event_joystick

.. automethod:: xsge_gui.Window.event_press_left

.. automethod:: xsge_gui.Window.event_press_right

.. automethod:: xsge_gui.Window.event_press_up

.. automethod:: xsge_gui.Window.event_press_down

.. automethod:: xsge_gui.Window.event_press_enter

.. automethod:: xsge_gui.Window.event_press_escape

.. automethod:: xsge_gui.Window.event_release_left

.. automethod:: xsge_gui.Window.event_release_right

.. automethod:: xsge_gui.Window.event_release_up

.. automethod:: xsge_gui.Window.event_release_down

.. automethod:: xsge_gui.Window.event_release_enter

.. automethod:: xsge_gui.Window.event_release_escape

.. automethod:: xsge_gui.Window.event_titlebar_mouse_button_press

.. automethod:: xsge_gui.Window.event_titlebar_mouse_button_release

.. automethod:: xsge_gui.Window.event_global_key_press

.. automethod:: xsge_gui.Window.event_global_key_release

.. automethod:: xsge_gui.Window.event_global_mouse_button_press

.. automethod:: xsge_gui.Window.event_global_mouse_button_release

.. automethod:: xsge_gui.Window.event_global_joystick_axis_move

.. automethod:: xsge_gui.Window.event_global_joystick_hat_move

.. automethod:: xsge_gui.Window.event_global_joystick_trackball_move

.. automethod:: xsge_gui.Window.event_global_joystick_button_press

.. automethod:: xsge_gui.Window.event_global_joystick_button_release

.. automethod:: xsge_gui.Window.event_global_joystick

.. automethod:: xsge_gui.Window.event_close

xsge_gui.Dialog
---------------

.. autoclass:: xsge_gui.Dialog

xsge_gui.Dialog Methods
~~~~~~~~~~~~~~~~~~~~~~~

In addition to methods inherited from :class:`xsge_gui.Window`, the
following methods are also available:

.. automethod:: xsge_gui.Dialog.show

xsge_gui.MenuWindow
-------------------

.. autoclass:: xsge_gui.MenuWindow

xsge_gui.MenuWindow Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the methods inherited from :class:`xsge_gui.Window`, the
following methods are also available:

.. automethod:: xsge_gui.MenuWindow.from_text

xsge_gui.MenuWindow Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Window`, the following event methods are also
available:

.. automethod:: xsge_gui.MenuWindow.event_choose

xsge_gui.MenuDialog
-------------------

.. autoclass:: xsge_gui.MenuDialog

xsge_gui.MessageDialog
----------------------

.. autoclass:: xsge_gui.MessageDialog

xsge_gui.TextEntryDialog
------------------------

.. autoclass:: xsge_gui.TextEntryDialog

xsge_gui.Widget
---------------

.. autoclass:: xsge_gui.Widget

xsge_gui.Widget Methods
~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_gui.Widget.destroy

.. automethod:: xsge_gui.Widget.redraw

.. automethod:: xsge_gui.Widget.refresh

xsge_gui.Widget Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_gui.Widget.event_step

.. automethod:: xsge_gui.Widget.event_key_press

.. automethod:: xsge_gui.Widget.event_key_release

.. automethod:: xsge_gui.Widget.event_mouse_button_press

.. automethod:: xsge_gui.Widget.event_mouse_button_release

.. automethod:: xsge_gui.Widget.event_joystick_axis_move

.. automethod:: xsge_gui.Widget.event_joystick_hat_move

.. automethod:: xsge_gui.Widget.event_joystick_trackball_move

.. automethod:: xsge_gui.Widget.event_joystick_button_press

.. automethod:: xsge_gui.Widget.event_joystick_button_release

.. automethod:: xsge_gui.Widget.event_joystick

.. automethod:: xsge_gui.Widget.event_press_left

.. automethod:: xsge_gui.Widget.event_press_right

.. automethod:: xsge_gui.Widget.event_press_up

.. automethod:: xsge_gui.Widget.event_press_down

.. automethod:: xsge_gui.Widget.event_press_enter

.. automethod:: xsge_gui.Widget.event_press_escape

.. automethod:: xsge_gui.Widget.event_release_left

.. automethod:: xsge_gui.Widget.event_release_right

.. automethod:: xsge_gui.Widget.event_release_up

.. automethod:: xsge_gui.Widget.event_release_down

.. automethod:: xsge_gui.Widget.event_release_enter

.. automethod:: xsge_gui.Widget.event_release_escape

.. automethod:: xsge_gui.Widget.event_global_key_press

.. automethod:: xsge_gui.Widget.event_global_key_release

.. automethod:: xsge_gui.Widget.event_global_mouse_button_press

.. automethod:: xsge_gui.Widget.event_global_mouse_button_release

.. automethod:: xsge_gui.Widget.event_global_joystick_axis_move

.. automethod:: xsge_gui.Widget.event_global_joystick_hat_move

.. automethod:: xsge_gui.Widget.event_global_joystick_trackball_move

.. automethod:: xsge_gui.Widget.event_global_joystick_button_press

.. automethod:: xsge_gui.Widget.event_global_joystick_button_release

xsge_gui.DecorativeWidget
-------------------------

.. autoclass:: xsge_gui.DecorativeWidget

xsge_gui.Label
--------------

.. autoclass:: xsge_gui.Label

xsge_gui.ProgressiveLabel
-------------------------

.. autoclass:: xsge_gui.ProgressiveLabel

xsge_gui.ProgressiveLabel Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Widget`, the following event methods are also
available:

.. automethod:: xsge_gui.ProgressiveLabel.event_add_character

xsge_gui.Button
---------------

.. autoclass:: xsge_gui.Button

xsge_gui.Button Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Widget`, the following event methods are also
available:

.. automethod:: xsge_gui.Button.event_press

xsge_gui.CheckBox
-----------------

.. autoclass:: xsge_gui.CheckBox

xsge_gui.CheckBox Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Widget`, the following event methods are also
available:

.. automethod:: xsge_gui.CheckBox.event_toggle

xsge_gui.RadioButton
--------------------

.. autoclass:: xsge_gui.RadioButton

xsge_gui.RadioButton Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Widget`, the following event methods are also
available:

.. automethod:: xsge_gui.RadioButton.event_toggle

xsge_gui.ProgressBar
--------------------

.. autoclass:: xsge_gui.ProgressBar

xsge_gui.TextBox
----------------

.. autoclass:: xsge_gui.TextBox

xsge_gui.TextBox Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In addition to the event methods inherited from
:class:`xsge_gui.Widget`, the following event methods are also
available:

.. automethod:: xsge_gui.TextBox.event_change_text

xsge_gui.MenuItem
-----------------

.. autoclass:: xsge_gui.MenuItem

xsge_gui Functions
==================

.. autofunction:: xsge_gui.init

.. autofunction:: xsge_gui.show_message

.. autofunction:: xsge_gui.get_text_entry

.. autofunction:: xsge_gui.get_menu_selection
