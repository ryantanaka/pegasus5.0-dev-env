#!/usr/bin/env python3

with open("hp.txt", "r") as _if, open("wc.txt", "w") as of:
    words = {}
    for l in _if:
        for w in l.split():
            if w in words:
                words[w] += 1
            else:
                words[w] = 1

    for k,v in words.items():
        of.write("{} {}\n".format(k,v))


