from random import randint
import matplotlib.pyplot as plt

# Let there be a random list of 500 numbers.
x = [randint(0, 5) for _ in range(5)]


def bubble_sort(x):
    for i in range(len(x) - 1):
        for j in range(len(x) - 1 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
    return x

def insertion_sort(x):
    i = 1
    while i < len(x):
        j = i
        while j > 0 and x[j-1] > x[j]:
            x[j], x[j - 1] = x[j - 1], x[j]
            j -= 1
        i += 1

    return x



def selection_sort(x):
    for i in range(len(x)):
        min_value = i
        for j in range(i +1, len(x)):
            if x[j] < x[min_value]:
                min_value = j
        if min_value != i:
            x[i], x[min_value] = x[min_value], x[i]
    return x