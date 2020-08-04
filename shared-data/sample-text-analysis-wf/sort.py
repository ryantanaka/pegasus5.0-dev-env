#!/usr/bin/env python3
s = []
with open("wc.txt", "r") as _if, open("wc-sorted.txt", "w") as of:
    for l in _if:
        word, num = l.split()
        num = int(num)
        s.append((word, num))

    s = sorted(s, reverse=True, key=lambda i: i[1])

    for x in s:
        of.write("{} {}\n".format(x[0], x[1]))
