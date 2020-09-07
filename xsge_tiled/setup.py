# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

import sys
from distutils.core import setup

long_description = """
xSGE is a collection of extensions for the SGE licensed under the GNU
General Public License.  They are designed to give additional features
to free/libre software games which aren't necessary, but are nice to
have.

xSGE extensions are not dependent on any particular SGE implementation.
They should work with any implementation that follows the specification.

This extension provides support for loading the JSON format of the
`Tiled Map Editor <http://www.mapeditor.org/>`_.  This allows you to use
Tiled to edit your game's world (e.g. levels), rather than building a
level editor yourself.
""".strip()

setup(name="xsge_tiled",
      version="1.0",
      description="xSGE Tiled Library",
      long_description=long_description,
      author="Layla Marchant",
      author_email="diligentcircle@riseup.net",
      url="https://python-sge.github.io",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU General Public License",
      packages=["xsge_tiled"],
      package_dir={"xsge_tiled": "xsge_tiled"},
      package_data={"xsge_tiled": ["COPYING"]},
      requires=["sge (>=1.0, <2.0)", "xsge_path (>=1.0, <2.0)"],
      provides=["xsge_tiled"],
     )
