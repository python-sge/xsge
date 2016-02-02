# setup.py alias
# Copyright (C) 2015 onpon4 <onpon4@riseup.net>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
