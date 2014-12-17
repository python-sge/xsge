# xSGE Path
# Copyright (c) 2014 Julian Marchant <onpon4@riseup.net>
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
This module provides paths for the SGE.  Paths are used to make objects
move in a certain way.
"""

from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sge


__all__ = ["Path"]


class Path(sge.Object):

    """
    Class for paths: objects which define movement patterns for other
    objects.  Paths are defined as a series of points for an object to
    follow.

    .. attribute:: points

       A list of the points that make up the path.  Each point should be
       a tuple in the form ``(x, y)``, where x is the horizontal
       location and y is the vertical location.
    """

    def __init__(self, points):
        x, y = points[0] if points else (0, 0)
        super(Path, self).__init__(x, y, tangible=False)
        self.points = points
