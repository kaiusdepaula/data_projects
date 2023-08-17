from random import randint
import matplotlib.pyplot as plt

# Let there be a random list of 500 numbers.
values = [randint(0, 500) for _ in range(500)]


def bubble_sort(x):
    for i in range(len(x) - 1):
        for j in range(len(x) - 1 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
    return x


