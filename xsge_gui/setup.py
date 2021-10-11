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

This extension provides a simple toolkit for adding GUIs to a SGE game
as well as support for modal dialog boxes.
""".strip()

setup(name="xsge_gui",
      version="2.0",
      description="xSGE GUI Toolkit",
      long_description=long_description,
      author="The Diligent Circle",
      author_email="diligentcircle@riseup.net",
      url="https://python-sge.github.io",
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "License :: DFSG approved",
                   "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development"],
      license="GNU Lesser General Public License",
      packages=["xsge_gui"],
      package_dir={"xsge_gui": "xsge_gui"},
      package_data={"xsge_gui": ["COPYING", "COPYING.LESSER", "data/*"]},
      requires=["sge (>=2.0, <3.0)"],
      provides=["xsge_gui"],
     )
