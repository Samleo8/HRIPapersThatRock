import numpy as np

with open("adjectives.txt", "r") as f:
    wordList = f.readline().strip().split(", ")

    histogram = {}

    for word in wordList:
        word = word.lower().strip()
        histogram[word] = histogram.get(word, 0) + 1

    print(histogram)

with open("output.csv", "w") as f:
    for word in histogram:
        print(f"{word},{histogram[word]}", file=f)