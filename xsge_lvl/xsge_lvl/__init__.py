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
             will be discarded.

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
    """

    def __init__(self, level, *args, **kwargs):
        super(LevelEditor, self).__init__(*args, **kwargs)
        self.level = level
        self.grid_x = 0
        self.grid_y = 0
        self.grid_width = 1
        self.grid_height = 1
        self.grid_color = None

    def load_meta(self):
        """
        Adjust the room to match the meta settings of :attr:`level`,
        such as size and background.

        Default behavior does nothing.  Override this method according
        to your needs.
        """
        pass

    def set_meta(self):
        """
        Adjust the meta settings of :attr:`level`, such as size and
        background, to match the room.

        Default behavior does nothing.  Override this method according
        to your needs.
        """
        pass

    def get_snap_x(self, x):
        """
        Return ``x`` "snapped" to the nearest horizontal grid cell.
        """
        return math.floor(x / self.grid_width) * self.grid_width

    def get_snap_y(self, y):
        """
        Return ``y`` "snapped" to the nearest vertical grid cell.
        """
        return math.floor(y / self.grid_height) * self.grid_height

    def place_object(self, type_, x, y, *args, **kwargs):
        """
        Create an object of the type ``type_`` at position
        (``x``, ``y``), passing ``args`` for the object's arguments and
        ``kwargs`` for the object's keyword arguments.

        Default behavior creates a :class:`LevelEditorObject` object,
        inserting ``x`` and ``y`` into the beginning of ``args``.
        """
        LevelEditorObject.create(type_, x, y, *args, **kwargs)

    def load(self):
        """
        Load the level indicated by :attr:`self.level`.

        Default behavior destroys all objects (if any), then uses
        :meth:`place_object` to place every object found in
        ``self.level.objects`` in the room as a level editor object.
        The first two values of the respective objects' :attr:`args`
        lists are used for ``x`` and ``y`` of :meth:`place_object`.
        """
        self.load_meta()

        for obj in self.objects[:]:
            self.remove(obj)

        for obj in self.level.objects:
            self.place_object(obj.type, *obj.args, **obj.kwargs)

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
        Create a LevelEditorObject object.  ``args`` and ``kwargs``
        are assigned to the corresponding attributes of the
        :class:`LevelObject` object assigned to :attr:`lv_obj`, after
        which :meth:`revert_obj` is called.
        """
        super(LevelEditorObject, self).__init__(0, 0)
        self.lv_obj = LevelObject()
        self.lv_obj.type = type_
        self.lv_obj.args = args
        self.lv_obj.kwargs = kwargs
        self.load_position()
        self.load_appearance()

    def load_position(self):
        """
        Adjust the position of this object to match the position
        settings of :attr:`lv_obj`.  This method can be extended or
        overridden if necessary.

        Default behavior sets :attr:`x` and :attr:`y` to the first two
        values of :attr:`lv_obj.args` if possible, or ``0`` otherwise.
        """
        if len(args) >= 2:
            self.x = args[0]
            self.y = args[1]
        elif len(args) >= 1:
            self.x = args[0]
            self.y = 0
        else:
            self.x = 0
            self.y = 0

    def load_appearance(self):
        """
        Adjust the appearance of this object to match the appearance
        settings of :attr:`lv_obj`.  This method can be extended or
        overridden if necessary.

        Default behavior sets the following attributes to the value with
        a key of the same name in :attr:`lv_obj.kwargs`:

          * :attr:`z`
          * :attr:`sprite`
          * :attr:`image_index`
          * :attr:`image_origin_x`
          * :attr:`image_origin_y`
          * :attr:`image_xscale`
          * :attr:`image_yscale`
          * :attr:`image_rotation`
          * :attr:`image_alpha`
          * :attr:`image_blend`
          * :attr:`image_blend_mode`
        """
        attrs = {
            "z", "sprite", "image_index", "image_origin_x", "image_origin_y",
            "image_xscale", "image_yscale", "image_rotation", "image_alpha",
            "image_blend", "image_blend_mode"}
        for i in attrs:
            setattr(self, i, self.lv_obj.kwargs[i])

    def set_position(self):
        """
        Adjust the position settings of :attr:`lv_obj` to match the
        position of this object.  This method can be extended or
        overridden if necessary.

        Default behavior sets :attr:`lv_obj.args` to
        ``[self.x, self.y]``.
        """
        self.lv_obj.args = [self.x, self.y]

    def set_appearance(self):
        """
        Adjust the appearance settings of :attr:`lv_obj` to match the
        appearance of this object.  This method can be extended or
        overridden if necessary.

        Default behavior assigns the following attributes to the keys of
        the same name in :attr:`lv_obj.kwargs`:

          * :attr:`z`
          * :attr:`sprite`
          * :attr:`image_index`
          * :attr:`image_origin_x`
          * :attr:`image_origin_y`
          * :attr:`image_xscale`
          * :attr:`image_yscale`
          * :attr:`image_rotation`
          * :attr:`image_alpha`
          * :attr:`image_blend`
          * :attr:`image_blend_mode`
        """
        attrs = {
            "z", "sprite", "image_index", "image_origin_x", "image_origin_y",
            "image_xscale", "image_yscale", "image_rotation", "image_alpha",
            "image_blend", "image_blend_mode"}
        for i in attrs:
            setattr(self, self.lv_obj.kwargs[i], i)

    def tile_paint(self, sprite, x, y):
        """
        If this object uses a :class:`sge.gfx.TileGrid` object as its
        sprite, paint ``sprite`` onto said tile grid in the space where
        the position (``x``, ``y``) relative to this object would be.
        If this object does not use a :class:`sge.gfx.TileGrid` object,
        or if the given position is not a valid tile position, this
        method does nothing.

        .. note::

           To erase a tile, set ``sprite`` to :const:`None`.
        """
        if isinstance(self.sprite, sge.gfx.TileGrid):
            spr = self.sprite
            if spr.render_method == "isometric":
                even_row = math.floor(y / spr.tile_height) * 2
                if (y % spr.tile_height) / spr.tile_height < 0.5:
                    odd_row = even_row - 1
                else:
                    odd_row = even_row + 1
                even_column = math.floor(x / spr.tile_width)
                odd_column = math.floor(x / spr.tile_width + 0.5)
                ec_x = even_column * spr.tile_width
                ec_y = odd_column * spr.tile_height

                # y=mx+b
                m = (spr.tile_height / 2) / (spr.tile_width / 2)
                if even_row > odd_row:
                    if even_column > odd_column:
                        b = ec_y + spr.tile_height / 2
                        m *= -1
                    else:
                        b = ec_y
                    if y >= m * x + b:
                        row = even_row
                        column = even_column
                    else:
                        row = odd_row
                        column = odd_column
                else:
                    if even_column > odd_column:
                        b = ec_y + spr.tile_height / 2
                    else:
                        b = ec_y + spr.tile_height
                        m *= -1
                    if y < m * x + b:
                        row = even_row
                        column = even_column
                    else:
                        row = odd_row
                        column = odd_column
                if (0 <= column < spr.section_length and
                        0 <= row < len(spr.tiles) / spr.section_length):
                    i = row * spr.section_length + column
                    if 0 <= i < len(spr.tiles):
                        spr.tiles[i] = sprite
            else: # spr.render_method == "orthogonal":
                row = math.floor(y / spr.tile_height)
                column = math.floor(x / spr.tile_width)
                if (0 <= column < spr.section_length and
                        0 <= row < len(spr.tiles) / spr.section_length):
                    i = row * spr.section_length + column
                    if 0 <= i < len(spr.tiles):
                        spr.tiles[i] = sprite

