#!/usr/bin/env python3
import matplotlib.pyplot as plt

words = []
counts = []

with open("wc-sorted.txt", "r") as f:
    i = 0
    for l in f:
        if i > 25:
            break

        word, count = l.split()
        count = int(count)

        words.append(word)
        counts.append(count)
        i += 1

plt.title("Top 25 Used Words")
plt.bar(words, counts, width=0.7, color="burlywood")
plt.xticks(words, words, rotation=75)
plt.xlabel("words")
plt.ylabel("count")
#plt.show()
plt.savefig("plot.png")
