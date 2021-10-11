# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

import sys
from distutils.core import setup

long_description = """
xSGE is a collection of higher-level extensions for the SGE which
enhance the core functionality in an implementation-independent way.
Like the SGE itself, they are distribted under the terms of the GNU
Lesser General Public License.

This extension provides an easy-to-use framework for collision physics.
This is especially useful for platformers, though it can also be useful
for other types of games.
""".strip()

setup(name="xsge_physics",
      version="0.13.3",
      description="xSGE Physics Framework",
      long_description=long_description,
      author="The Diligent Circle",
      author_email="diligentcircle@riseup.net",
      url="https://python-sge.github.io",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU Lesser General Public License",
      packages=["xsge_physics"],
      package_dir={"xsge_physics": "xsge_physics"},
      package_data={"xsge_physics": ["COPYING", "COPYING.LESSER"]},
      requires=["sge (>=1.0, <3.0)"],
      provides=["xsge_physics"],
     )
