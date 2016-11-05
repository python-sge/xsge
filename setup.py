# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

import os
import sys
import subprocess

EXECUTABLE = sys.executable
DIR = os.path.abspath(os.path.dirname(__file__))


if EXECUTABLE:
    for d in os.listdir(DIR):
        dirname = os.path.join(DIR, d)
        if os.path.isdir(dirname):
            os.chdir(dirname)
            if os.path.isfile("setup.py"):
                subprocess.call([EXECUTABLE, "setup.py"] + sys.argv[1:])
else:
    print("Failed to determine the Python executable to use. Please edit")
    print("this script to define the Python binary explicitly, or otherwise")
    print("install each package individually.")
