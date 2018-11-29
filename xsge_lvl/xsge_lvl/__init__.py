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

import sge


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

        - ``"meta"``: any value indicating the level's meta variables.
          These correspond to :attr:`Level.meta`.
        - ``"objects"``: an object with the level's objects as keys.
          Each value is an object indicating the following keys:

          - ``type``: Corresponds with :attr:`LevelObject.type`.
          - ``args``: Corresponds with :attr:`LevelObject.args`.
          - ``kwargs``: Corresponds with :attr:`LevelObject.kwargs`.
        """
        self = cls()
        data = json.load(fp)
        self.meta = data["meta"]
        for obj in data["objects"]:
            new_object = LevelObject()
            new_object.type = obj["type"]
            new_object.args = obj["args"]
            new_object.kwargs = obj["kwargs"]
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

        .. note::

           When saving SGE ASCII level files, keyword arguments are lost
           and ``args[0]`` and ``args[1]`` **must** be integers.
           Additionally, :attr:`meta` **must** be a list or other
           iterable value, and each value in the list **must** be a
           string.  Failure to follow these requirements may result in
           loss of data or otherwise cause saving to fail.
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
        """
        objects = []
        for obj in self.objects:
            T = str(obj.type)
            if len(T) == 1:
                x = int(round(obj.args[0]))
                y = int(round(obj.args[1]))
                while y >= len(objects):
                    objects.append([])
                while x >= len(objects[y]):
                    objects[y].append(" ")

                objects[y][x] = T
            else:
                raise ValueError("Object type must be a single character.")

        meta_data = [str(i) for i in self.meta]
        obj_data = [''.join(i) for i in objects]

        meta_text = '\n'.join(meta_data)
        obj_text = '\n'.join(obj_data)
        text = '\n\n'.join([meta_text, obj_text])

        fp.write(text)

    def spawn(self, types, room=None):
        """
        Spawn all level objects indicated by :attr:`objects` in the room
        indicated by ``room``.

        ``types`` is a dictionary with the type strings (from
        :attr:`LevelObject.type`) as keys and the actual classes of the
        corresponding types as values.

        If ``room`` is set to :const:`None`, the objects will be spawned
        in the current room (:attr:`sge.game.current_room`).
        """
        if room is None:
            room = sge.game.current_room

        for obj in self.objects:
            new_object = types[obj.type](*obj.args, **obj.kwargs)
            room.add(new_object)


class LevelObject(object):

    """
    Class used to store information about objects within a level.

    .. attribute:: type

       A string indicating the type (class) of the object.

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

    .. attribute:: grid_x

       The horizontal offset of the grid to the right in pixels.

    .. attribute:: grid_y

       The vertical offset of the grid downward in pixels.

    .. attribute:: grid_width

       The width of each column of the grid in pixels.

    .. attribute:: grid_height

       The height of each row of the grid in pixels.

    .. attribute:: grid_color

       A :class:`sge.gfx.Color` object indicating the color to display
       the grid as.  Set to :const:`None` for no display of the grid.

    .. attribute:: painting

       Whether or not painting is enabled.  While painting is enabled,
       objects of the type indicated by :attr:`paint_type` are added
       anywhere the mouse cursor goes.

    .. attribute:: paint_type

       A string indicating the type of object to paint while painting is
       enabled.

    .. attribute:: paint_args

       A list of the     
    """

    def __init__(self, *args, **kwargs):
        super(LevelEditor, self).__init__(*args, **kwargs)
        self.grid_x = 0
        self.grid_y = 0
        self.grid_width = 1
        self.grid_height = 1
        self.grid_color = None
        self.painting = False
        self.paint_type = None
        self.paint_args = []
        self.paint_kwargs = {}
        self.__paint_x = None
        self.__paint_y = None

    def place_object(type_, x, y, *args, **kwargs):
        """
        Create an object of the type ``type_`` at position
        (``x``, ``y``), passing ``args`` for the object's arguments and
        ``kwargs`` for the object's keyword arguments.

        Default behavior creates a :class:`LevelEditorObject` object,
        inserting ``x`` and ``y`` into the beginning of ``args``.
        """
        LevelEditorObject.create(type_, x, y, *args, **kwargs)


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
        object assigned to :attr:`lv_obj`.
        """
        super(LevelEditorObject, self).__init__(0, 0)
        self.lv_obj = LevelObject()
        self.lv_obj.type = type_
        self.lv_obj.args = args
        self.lv_obj.kwargs = kwargs
        self.update_obj()

    def update_obj(self):
        """
        Update this object based on changes to :attr:`lv_obj`.  Default
        behavior simply sets ``x`` and ``y`` as the first two values in
        ``lv_obj.args``, then assigns every value in ``lv_obj.kwargs``
        to the attribute with the same name as the corresponding key.
        """
        if len(self.lv_obj.args) >= 1:
            self.x = self.lv_obj.args[0]
            if len(self.lv_obj.args) >= 2:
                self.y = self.lv_obj.args[1]

        for i in self.lv_obj.kwargs:
            setattr(self, i, self.lv_obj.kwargs[i])

