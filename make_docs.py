#!/usr/bin/env python3
# This file has been dedicated to the public domain, to the extent
# possible under applicable law, via CC0. See
# http://creativecommons.org/publicdomain/zero/1.0/ for more
# information. This file is offered as-is, without any warranty.

import os
import subprocess


DIR = os.path.abspath(os.path.dirname(__file__))


for d in os.listdir(DIR):
    dirname = os.path.join(DIR, d)
    if os.path.isdir(dirname):
        os.chdir(dirname)
        if os.path.isdir("doc-src"):
            os.chdir("doc-src")
            subprocess.call(["make", "text", "html"])
