# ulvl - Universal Level Formats
# Copyright (c) 2014 Julie Marchant <onpon4@riseup.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This library reads and writes universal level formats.  These level
formats are generic enough to be used by any 2-D game.  Their purpose is
to unify level editing.
"""

__version__ = "0.4"


import json
import xml.etree.ElementTree as ET
import warnings


__all__ = ["ASCL", "JSL", "ULX", "LevelObject"]


class ASCL(object):

    """
    This class loads, stores, and saves ASCII Level (ASCL) files.  This
    format is based on a grid of plain text characters and generally has
    one of the following extensions: ".ascl", ".asc", ".txt".

    An ASCL file contains two main components: the meta variable
    definitions and the level object grid.

    Meta variables are defined simply at the top of the file: each line
    indicates the value of a different meta variable, always a string.
    Any number of meta variables can be defined.

    Everything after the first blank line in the ASCL file is considered
    to be part of the level object grid. Here, ASCII characters are used
    to represent level objects.  Any ASCII character can be used to
    represent an object except for ``" "``, which represents an empty
    tile.

    The width and height of the level is inferred from the number of
    columns and rows in the level object grid, respectively.

    .. attribute:: width

       The width of the level in tiles.

    .. attribute:: height

       The height of the level in tiles.

    .. attribute:: meta

       A list of the level's meta variables.

       .. note::

          The meta variables can be any value, but when the ASCL is
          saved, all meta variables will be automatically converted to
          strings.

    .. attribute:: objects

       A list of objects in the level as :class:`jsl.LevelObject`
       objects.  They must have single-character strings as types.
       Their positions are tile-based, and any meta-variables are
       ignored when saving.

       .. note::
       
          Due to the nature of this format, only integer positions are
          valid.  If an object's position attribute is not an integer,
          it will be rounded when the file is saved.

       .. note::

          Due to the nature of this format, only one object can be in
          any given tile position.  If two objects are in the same tile
          position, one will be arbitrarily lost when the file is saved.
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.meta = []
        self.objects = []

    @classmethod
    def load(cls, f):
        """
        Load the indicated file and return a :class:`ulvl.ASCL` object.
        """
        self = cls()

        data = f.read()

        grid = False
        y = 0
        for line in data.splitlines():
            if grid:
                self.width = max(self.width, len(line))
                self.height = max(self.height, y + 1)
                for x in range(len(line)):
                    char = line[x]
                    if char != " ":
                        obj = LevelObject(char, x, y)
                        self.objects.append(obj)
                y += 1
            elif line:
                self.meta.append(line)
            else:
                grid = True

        return self

    def save(self, f):
        """Save the object to the indicated file."""
        objects = [[' '] * self.width for i in range(self.height)]

        for obj in self.objects:
            T = str(obj.type)
            if len(T) == 1:
                x = int(round(obj.x))
                y = int(round(obj.y))
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

        f.write(text)


class JSL(object):

    """
    This class loads, stores, and saves JavaScript Level (JSL) files.
    This format is based on JSON and generally has one of the following
    extensions: ".jsl", ".json".

    A JSL file contains a top-level object with two keys:

    - ``"meta"``: an object indicating the level's meta variables.
      These can be any kind of value.
    - ``"objects"``: an object with the level's object types as keys.
      Each value is an array of objects in the level of the respective
      type, each individual object being an array with the following
      values:

      - The horizontal position of the object in the level.
      - The vertical position of the object in the level.
      - (Optional) An extra option for the object.  Can be any value.

    - ``"size"``: An array with the following values:

      - The width of the level.
      - The height of the level.

    .. attribute:: width

       The width of the level.  The unit of measurement used is
       arbitrary; pixels or tiles is recommended.

    .. attribute:: height

       The height of the level.  The unit of measurement used is
       arbitrary; pixels or tiles is recommended.

    .. attribute:: meta

       A dictionary of all of the level's meta variables.

    .. attribute:: objects

       A list of objects in the level as :class:`jsl.LevelObject`
       objects.
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.meta = {}
        self.objects = []

    @classmethod
    def load(cls, f):
        """
        Load the indicated file and return a :class:`ulvl.JSL` object.
        """
        self = cls()

        data = json.load(f)

        self.width, self.height = data.get("size", [0, 0])

        self.meta = data.get("meta", {})

        for t in data.setdefault("objects", {}):
            for o in data["objects"][t]:
                obj = LevelObject(t, *o)
                self.objects.append(obj)

        return self

    def save(self, f):
        """Save the object to the indicated file."""
        data = {"size": [self.width, self.height], "meta": self.meta,
                "objects": {}}

        for obj in self.objects:
            data["objects"].setdefault(obj.type, [])

            obj_list = [obj.x, obj.y]
            if obj.option is not None:
                obj_list.append(obj.option)

            data["objects"][obj.type].append(obj_list)

        json.dump(data, f, indent=4)


class ULX(object):

    """
    This class loads, stores, and saves Universal Level XML (ULX) files.
    This format is based on XML and generally has one of the following
    extensions: ".ulx", ".xml".

    A ULX file contains a root tree with the name "level" containing the
    following children:

    - ``width``: the width of the level.
    - ``height``: the height of the level.
    - ``meta``: contains one element for each of the level's meta
      variables.  Each element's tag indicates the name of the meta
      variable, while its text indicates the value.
    - ``objects``: contains ``object`` elements.  Each ``object``
      element has the following attributes:

      - ``"type"``: the object's type.
      - ``"x"``: the horizontal position of the object in the level.
      - ``"y"``: the vertical position of the object in the level.
      - ``"option"`` (optional): an extra option for the object.

    .. attribute:: width

       The width of the level.  The unit of measurement used is
       arbitrary; pixels or tiles is recommended.

    .. attribute:: height

       The height of the level.  The unit of measurement used is
       arbitrary; pixels or tiles is recommended.

    .. attribute:: meta

       A dictionary of all of the level's meta variables.

       .. note::

          The meta variables can be any value, but when the ULX is
          saved, all meta variables will be automatically converted to
          strings, since XML does not support any other type.

    .. attribute:: objects

       A list of objects in the level as :class:`jsl.LevelObject`
       objects.

       .. note::

          The extra options of the objects can be any value, but when
          the ULX is saved, any options which are not either strings or
          :const:`None` will be automatically converted to strings,
          since XML does not support any other type.
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.meta = {}
        self.objects = []

    @classmethod
    def load(cls, f):
        """
        Load the indicated file and return a :class:`ulvl.ULX` object.
        """
        self = cls()

        tree = ET.parse(f)
        root = tree.getroot()

        for child in root:
            if child.tag == "width":
                w = child.text
                self.width = float(w)
                if self.width == int(self.width):
                    self.width = int(self.width)
            elif child.tag == "height":
                h = child.text
                self.height = float(h)
                if self.height == int(self.height):
                    self.height = int(self.height)
            elif child.tag == "meta":
                for meta in child:
                    self.meta[meta.tag] = meta.text
            elif child.tag == "objects":
                for obj in child.findall("object"):
                    type_ = obj.attrib.get("type")
                    x = float(obj.attrib.get("x", "0"))
                    y = float(obj.attrib.get("y", "0"))
                    if x == int(x):
                        x = int(x)
                    if y == int(y):
                        y = int(y)
                    option = obj.attrib.get("option")
                    self.objects.append(LevelObject(type_, x, y, option))

        return self

    def save(self, f):
        """Save the object to the indicated file."""
        root = ET.Element("level")

        width_elem = ET.Element("width")
        width_elem.text = str(self.width)
        root.append(width_elem)

        height_elem = ET.Element("height")
        height_elem.text = str(self.height)
        root.append(height_elem)

        meta_elem = ET.Element("meta")
        for i in self.meta:
            elem = ET.Element(i)
            elem.text = str(self.meta[i])
            meta_elem.append(elem)

        root.append(meta_elem)

        objects_elem = ET.Element("objects")
        for obj in self.objects:
            if obj.x == int(obj.x):
                obj.x = int(obj.x)
            if obj.y == int(obj.y):
                obj.y = int(obj.y)
            attr = {"x": str(obj.x), "y": str(obj.y)}
            if obj.type is not None:
                attr["type"] = str(obj.type)
            if obj.option is not None:
                attr["option"] = str(obj.option)
            elem = ET.Element("object", attrib=attr)
            objects_elem.append(elem)

        root.append(objects_elem)

        tree = ET.ElementTree(root)
        tree.write(f, encoding="UTF-8", xml_declaration=True)


class LevelObject(object):

    """
    This class stores level objects.

    .. attribute:: type

       The type of object this is.  Can be any arbitrary value.

    .. attribute:: x

       The horizontal position of the object in the level.  The unit of
       measurement used is arbitrary; pixels or tiles is recommended.

    .. attribute:: y

       The vertical position of the object in the level.  The unit of
       measurement used is arbitrary; pixels or tiles is recommended.

    .. attribute:: option

       The option of the object; default is :const:`None`.  The meaning
       of this value is completely arbitrary; use it for any special
       variations level objects have.
    """

    def __init__(self, type_, x, y, option=None):
        self.type = type_
        self.x = x
        self.y = y
        self.option = option
