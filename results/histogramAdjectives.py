import numpy as np

histogram = {}

with open("adjectives.txt", "r") as f:
    wordList = f.readline().strip().split(", ")

    for word in wordList:
        word = word.lower().strip()
        histogram[word] = histogram.get(word, 0) + 1

histogramSorted = sorted(histogram.items(), key=lambda kv: (kv[1], kv[0]))
histogramSorted.reverse()

with open("output.csv", "w") as f:
    for word, count in histogramSorted:
        print(f"{word},{count}", file=f)
