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

This extension provides support for loading the Tiled TMX format.  This
allows you to use Tiled to edit your game's world (e.g. levels), rather
than building a level editor yourself.
""".strip()

setup(name="xsge_tmx",
      version="1.1.2a0",
      description="xSGE TMX Library",
      long_description=long_description,
      author="Julie Marchant",
      author_email="onpon4@riseup.net",
      url="http://xsge.nongnu.org",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU General Public License",
      packages=["xsge_tmx"],
      package_dir={"xsge_tmx": "xsge_tmx"},
      package_data={"xsge_tmx": ["COPYING"]},
      requires=["sge (>=1.0, <2.0)", "six (>=1.4.0)", "tmx (>=1.9)",
                "xsge_path"],
      provides=["xsge_tmx"],
     )
