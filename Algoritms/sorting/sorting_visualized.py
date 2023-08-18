from random import randint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
plt.style.use(['seaborn-v0_8-dark-palette'])


# Just a sandbox script to visualize sorting algoritms using matplotlib
values = [randint(0, 500) for _ in range(500)]

def bubble_sort_modified(x):
    iterations = []
    for i in range(len(x) - 1):
        for j in range(len(x) - 1 - i):
            if x[j] > x[j + 1]:
                x[j], x[j + 1] = x[j + 1], x[j]
            iterations.append(list(x))
    return iterations

def insertion_sort_modified(x):
    iterations = []
    i = 1
    while i < len(x):
        j = i
        while j > 0 and x[j-1] > x[j]:
            x[j], x[j - 1] = x[j - 1], x[j]
            j -= 1
        iterations.append(list(x))
        i += 1

    return iterations

def selection_sort_modified(x):
    iterations = []
    for i in range(len(x)):
        min_value = i
        for j in range(i +1, len(x)):
            if x[j] < x[min_value]:
                min_value = j
        if min_value != i:
            x[i], x[min_value] = x[min_value], x[i]
            iterations.append(list(x))
    return iterations

def sorting_animation(x, func):
    iterations = func(x)

    # Reduce the number of iterations for faster animation
    frames_to_display = 100
    step = len(iterations) // frames_to_display

    fig, ax = plt.subplots()
    bar_rects = ax.bar(range(len(x)), iterations[0], align="edge", width=1)

    def update_fig(i):
        for rect, val in zip(bar_rects, iterations[i]):
            rect.set_height(val)

    ani = FuncAnimation(
        fig, update_fig, frames=range(0, len(iterations), step), interval=10, repeat=False
    )

    return(plt.show())


sorting_animation(values, selection_sort_modified)