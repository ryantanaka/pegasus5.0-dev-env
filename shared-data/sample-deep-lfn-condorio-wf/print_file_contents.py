#!/usr/bin/env python3
from glob import glob

for path in glob("**/*.txt", recursive=True):
    with open(path, "r") as f:
        print("{}: {}".format(path, f.read()))

