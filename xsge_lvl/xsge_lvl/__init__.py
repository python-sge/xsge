# xSGE Level Library
# Copyright (c) 2018 Julie Marchant <onpon4@riseup.net>
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

This extension provides support for loading standardized xSGE level
files and a skeleton for the creation of a level editor.

TODO
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

__version__ = "0.1"

import json
import math

import sge
import six


__all__ = ["Level", "LevelObject"]


class Level(object):

    """
    Class used to store, save, and load level information.  Use
    :meth:`Level.load` to load a level, and use :meth:`Level.save` to
    save a level.  Use :meth:`Level.generate` to generate the actual
    level from the level data.

    .. attribute:: meta

       Meta-information about the level. Can be any arbitrary value as
       long as it is supported by the JSON format.

    .. attribute:: objects

       A list of :class:`LevelObject` files indicating the objects in
       the room.
    """

    def __init__(self):
        self.meta = None
        self.objects = []

    @classmethod
    def load_json(cls, fp):
        """
        Load ``fp`` (a ``.read()``-supporting file-like object) as a
        SGE JSON level file and create a new :class:`Level` object from
        it.

        A SGE JSON file contains a top-level object with two keys:

        - ``"meta"``: Any value indicating the level's meta variables.
          These correspond to :attr:`Level.meta`.
        - ``"objects"``: A list of the level's objects.  Each value is
          an object indicating the following keys:

          - ``type``: Corresponds with :attr:`LevelObject.type`.
          - ``args``: Corresponds with :attr:`LevelObject.args`.
          - ``kwargs``: Corresponds with :attr:`LevelObject.kwargs`.
        """
        self = cls()
        data = json.load(fp)
        self.meta = data.get("meta")
        for obj in data.get("objects", []):
            new_object = LevelObject()
            new_object.type = obj.get("type")
            new_object.args = obj.get("args", [])
            new_object.kwargs = obj.get("kwargs", {})
            self.objects.append(new_object)

    @classmethod
    def load_ascii(cls, fp):
        """
        Load ``fp`` (a ``.read()``-supporting file-like object) as a
        SGE ASCII level file and create a new :class:`Level` object from
        it.

        A SGE ASCII file contains two main components: the meta variable
        definitions and the level object grid.

        Meta variables are defined simply at the top of the file: each
        line indicates the value of a different meta variable, always a
        string.  Any number of meta variables can be defined. Meta
        variable defintions end when a completely blank line is
        encountered.  The meta variables are assigned to :attr:`meta` as
        a list.

        Everything after the first blank line in the file is considered
        to be part of the level object grid. Here, text characters are
        used to represent level objects.  Any character can be used to
        represent an object except for ``" "``, which represents empty
        space.

        Each level object passes the character that represents it to
        :attr:`LevelObject.type`. :attr:`LevelObject.args` is set to a
        list with two values: the column (horizontal position) of the
        character (where ``0`` is the leftmost column), and the row
        (vertical position) of the character  (where ``0`` is the
        topmost row).
        """
        self = cls()
        self.meta = []

        data = fp.read()

        grid = False
        y = 0
        for line in data.splitlines():
            if grid:
                for x in range(len(line)):
                    char = line[x]
                    if char != " ":
                        obj = LevelObject()
                        obj.type = char
                        obj.args = [x, y]
                        self.objects.append(obj)
                y += 1
            elif line:
                self.meta.append(line)
            else:
                grid = True

        return self

    def save_json(self, fp):
        """
        Save the level to ``fp`` (a ``.write()``-supporting file-like
        object) as a SGE JSON level file.

        See the documentation for :meth:`Level.load_json` for more
        information.
        """
        objects = []
        for obj in self.objects:
            objects.append({"type": obj.type, "args": obj.args,
                            "kwargs": obj.kwargs})
        data = {"meta": self.meta, "objects": objects}
        json.dump(data, fp)

    def save_ascii(self, fp):
        """
        Save the level to ``fp`` (a ``.write()``-supporting file-like
        object) as a SGE ASCII level file.

        See the documentation for :meth:`Level.ascii_json` for more
        information.

        .. note::

           This format has several limitations:

           - A level object's type must be a string containing a single
             character, which cannot be ``" "``.  If the string form of
             any object's type does not contain exactly one character,
             or if the character is ``" "``, :exc:`ValueError` is
             raised.

           - The first two values of ``args`` for each object are used
             to determine their position. These values must be defined
             as integers, and only one object can exist in any given
             location.  If the values do not exist or cannot be
             converted into integers, :exc:`TypeError` is raised.  If
             two objects share the same location, :exc:`ValueError` is
             raised. Any arguments beyond the first two for an object
             will be discarded

           - Level objects cannot have keyword arguments.  Any keyword
             arguments defined for an object will be discarded.

           - :attr:`meta` must be a list or other iterable object. All
             values within will be converted into strings automatically.
        """
        objects = []
        for obj in self.objects:
            T = str(obj.type)
            if len(T) == 1 and T != " ":
                try:
                    sx = obj.args[0]
                    sy = obj.args[1]
                except (TypeError, IndexError):
                    e = 'Required position args undefined in "{}" object.'.format(T)
                    raise TypeError(e)
                else:
                    try:
                        x = int(sx)
                        y = int(sy)
                    except (TypeError, ValueError):
                        e = 'Failed to convert position objects "{}" and "{}" to integers for "{}" object.'.format(sx, sy, T)
                        raise TypeError(e)
                    else:
                        while y >= len(objects):
                            objects.append([])
                        while x >= len(objects[y]):
                            objects[y].append(" ")

                        if objects[y][x] == " ":
                            objects[y][x] = T
                        else:
                            e = 'Position ({},{}) occupied by both "{}" object and "{}" object.'.format(objects[y][x], T)
                            raise ValueError(e)
            else:
                raise ValueError('Invalid object type "{}".'.format(T))

        meta_data = [str(i) for i in self.meta]
        obj_data = [''.join(i) for i in objects]

        meta_text = '\n'.join(meta_data)
        obj_text = '\n'.join(obj_data)
        text = '\n\n'.join([meta_text, obj_text])

        fp.write(text)

    def spawn(self, types, room=None, default_type=None):
        """
        Spawn all level objects indicated by :attr:`objects` in the room
        indicated by ``room``.

        ``types`` is a dictionary with the type strings (from
        :attr:`LevelObject.type`) as keys and the actual classes of the
        corresponding types as values.

        If ``room`` is set to :const:`None`, the objects will be spawned
        in the current room (:attr:`sge.game.current_room`).

        ``default_type`` indicates the type to use for objects with a
        type not found in ``types``.  If set to :const:`None`,
        :class:`sge.dsp.Object` is used.
        """
        if room is None:
            room = sge.game.current_room
        if default_type is None:
            default_type = sge.dsp.Object

        for obj in self.objects:
            new_object = types.get(obj.type, default_type)(*obj.args, **obj.kwargs)
            room.add(new_object)


class LevelObject(object):

    """
    Class used to store information about objects within a level.

    .. attribute:: type

       The type (class) of the object.  Can be any arbitrary value.

    .. attribute:: args

       A list of the positional arguments passed to the object upon
       creation within the game.

    .. attribute:: kwargs

       A dictionary of the keyword arguments passed to the object upon
       creation within the game.
    """

    def __init__(self):
        self.type = None
        self.args = []
        self.kwargs = {}


class LevelEditor(sge.dsp.Room):

    """
    Base class for constructing a level editor, with features useful for
    the purpose.

    .. note::

       Some of this class's functionality is implemented by
       :meth:`event_step`.


    .. attribute:: level

       The :class:`Level` file which represents the level currently
       being edited.

    .. attribute:: grid_x

       The horizontal offset of the grid to the right in pixels.

       Default value: ``0``

    .. attribute:: grid_y

       The vertical offset of the grid downward in pixels.

       Default value: ``0``

    .. attribute:: grid_width

       The width of each column of the grid in pixels.

       Default value: ``1``

    .. attribute:: grid_height

       The height of each row of the grid in pixels.

       Default value: ``1``

    .. attribute:: grid_color

       A :class:`sge.gfx.Color` object indicating the color to display
       the grid as.  Set to :const:`None` for no display of the grid.

       Default value: :const:`None`

    .. attribute:: painting

       Whether or not painting is enabled.  While painting is enabled,
       objects of the type indicated by :attr:`paint_type` are added
       anywhere the mouse cursor goes, using :meth:`place_object`.

       Default value: :const:`False`

    .. attribute:: paint_type

       The value assigned to the ``type_`` argument of
       :meth:`place_object` when painting.

       Default value: :const:`None`

    .. attribute:: paint_args

       A list assigned to the ``args`` argument of :meth:`place_object`
       when painting.

       Default value: ``[]``

    .. attribute:: paint_kwargs

       A dictionary assigned to the ``kwargs`` argument of
       :meth:`place_object` when painting.

       Default value: ``{}``
    """

    def __init__(self, level, *args, **kwargs):
        super(LevelEditor, self).__init__(*args, **kwargs)
        self.level = level
        self.grid_x = 0
        self.grid_y = 0
        self.grid_width = 1
        self.grid_height = 1
        self.grid_color = None
        self.grid_snap = True
        self.painting = False
        self.paint_type = None
        self.paint_args = []
        self.paint_kwargs = {}
        self.__paint_x = None
        self.__paint_y = None

    def place_object(self, type_, x, y, *args, **kwargs):
        """
        Create an object of the type ``type_`` at position
        (``x``, ``y``), passing ``args`` for the object's arguments and
        ``kwargs`` for the object's keyword arguments.

        Default behavior creates a :class:`LevelEditorObject` object,
        inserting ``x`` and ``y`` into the beginning of ``args``.
        """
        LevelEditorObject.create(type_, x, y, *args, **kwargs)

    def event_step(self, time_passed, delta_mult):
        if self.grid_color:
            for view in self.views:
                view_xfactor = view.wport / view.width
                view_yfactor = view.hport / view.height

                if self.grid_width >= 2 * view.width / view.wport:
                    x = math.ceil(view.x / self.grid_width) * self.grid_width
                    while x < view.x + view.width:
                        dsp_x = view.xport + view_xfactor * (x - view.x)
                        sge.game.project_line(
                            dsp_x, view.yport, dsp_x, view.yport + view.hport,
                            self.grid_color)
                        x += self.grid_width

                if self.grid_height >= 2 * view.height / view.hport:
                    y = math.ceil(view.y / self.grid_height) * self.grid_height
                    while y < view.y + view.height:
                        dsp_y = view.yport + view_yfactor * (y - view.y)
                        sge.game.project_line(
                            view.xport, dsp_y, view.xport + view.wport, dsp_y,
                            self.grid_color)
                        y += self.grid_height


class LevelEditorObject(sge.dsp.Object):

    """
    Base class for level editor representations of level objects.

    .. attribute:: lv_obj

       The :class:`LevelObject` object represented.
    """

    def __init__(self, type_, *args, **kwargs):
        """
        Create a LevelEditorObject object.  All arguments are assigned
        to the corresponding attributes of the :class:`LevelObject`
        object assigned to :attr:`lv_obj`, after which
        :meth:`revert_obj` is called.
        """
        super(LevelEditorObject, self).__init__(0, 0)
        self.lv_obj = LevelObject()
        self.lv_obj.type = type_
        self.lv_obj.args = args
        self.lv_obj.kwargs = kwargs
        self.revert_obj()

    def revert_obj(self):
        """
        Revert the condition of this object to that of :attr:`lv_obj`.
        Default behavior simply sets :attr:`x` and :attr:`y` to the
        first two values in ``lv_obj.args``, then assigns every value in
        ``lv_obj.kwargs`` to the attribute with the same name as the
        corresponding key.  Override or extend this method if you need
        :attr:`lv_obj` to be used in some different way.
        """
        if len(self.lv_obj.args) >= 1:
            self.x = self.lv_obj.args[0]
            if len(self.lv_obj.args) >= 2:
                self.y = self.lv_obj.args[1]

        for i in self.lv_obj.kwargs:
            setattr(self, i, self.lv_obj.kwargs[i])

    def update_obj(self):
        """
        Update :attr:`lv_obj` to match the current state of this object.
        Default behavior simply sets ``lv_obj.args`` to
        ``[self.x, self.y]``, and sets ``lv_obj.kwargs`` to the values
        of all non-default attributes that can be set by
        :meth:`sge.dsp.Object.__init__`.  Override or extend this method
        if you need :attr:`lv_obj` to be set in some different way.
        """
        self.lv_obj.args = [self.x, self.y]
        self.lv_obj.kwargs = {}

        # Default values of ``0``
        for i in {"z", "xvelocity", "yvelocity", "xacceleration",
                  "yacceleration", "image_index", "image_rotation"}:
            v = getattr(self, i, 0)
            if v != 0:
                self.lv_obj.kwargs[i] = v

        # Default values of ``True``
        for i in {"visible", "active", "checks_collisions", "tangible"}:
            v = getattr(self, i, True)
            if not v:
                self.lv_obj.kwargs[i] = False

        # Default values of ``False``
        for i in {"regulate_origin", "collision_ellipse", "collision_precise"}:
            v = getattr(self, i, False)
            if v:
                self.lv_obj.kwargs[i] = True

        # Image-related properties (case-by-case)
        if self.sprite is not None:
            self.lv_obj.kwargs["sprite"] = self.sprite
            if self.bbox_x != self.sprite.bbox_x:
                self.lv_obj.kwargs["bbox_x"] = self.bbox_x
            if self.bbox_y != self.sprite.bbox_y:
                self.lv_obj.kwargs["bbox_y"] = self.bbox_y
            if self.image_index != 0:
                self.lv_obj.kwargs["image_index"] = self.image_index
            if self.image_origin_x != self.sprite.origin_x:
                self.lv_obj.kwargs["image_origin_x"] = self.image_origin_x
            if self.image_origin_y != self.sprite.origin_y:
                self.lv_obj.kwargs["image_origin_y"] = self.image_origin_y
            if self.image_fps != self.sprite.fps:
                self.lv_obj.kwargs["image_fps"] = self.image_fps
            for i in {"image_xscale", "image_yscale"}:
                v = getattr(self, i, 1)
                if v != 1:
                    self.lv_obj.kwargs[i] = v
            if self.image_rotation != 0:
                self.lv_obj.kwargs["image_rotation"] = self.image_rotation
            if self.image_alpha != 255:
                self.lv_obj.kwargs["image_alpha"] = self.image_alpha
            for i in {"image_blend", "image_blend_mode"}:
                v = getattr(self, i, None)
                if v is not None:
                    self.lv_obj.kwargs[i] = v
        else:
            for i in {"bbox_x", "bbox_y"}:
                v = getattr(self, i, 0)
                if v != 0:
                    self.lv_obj.kwargs[i] = v
            for i in {"bbox_width", "bbox_height"}:
                v = getattr(self, i, 1)
                if v != 1:
                    self.lv_obj.kwargs[i] = v

