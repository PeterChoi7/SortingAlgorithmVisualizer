import math
import pygame
import random

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    GREY = 128, 128, 128
    BLUE = 0, 0, 255
    background_color = BLACK

    GRADIENTS = [
        GREY,
        (168, 168, 168)
    ]

    FONT = pygame.font.SysFont('georgia', 15)
    LARGE_FONT = pygame.font.SysFont('georgia', 50)
    SIDE_PAD = 50
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)


    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name):
    draw_info.window.fill(draw_info.background_color)

    title = draw_info.FONT.render(algo_name, 1, draw_info.WHITE)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("C - Clear/ Reset | SPACE - Start Sorting", 1, draw_info.WHITE)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 35))

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort | S - Selection Sort | R - Radix Sort | M - Merge Sort | Q - Quick Sort", 1, draw_info.WHITE)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 55))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_position = {}, clear = False):
    lst = draw_info.lst

    if clear:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.background_color, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 2]

        if i in color_position:
            color = color_position[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []
    for i in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

def bubbleSort(draw_info):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if num1 > num2:
                lst[j], lst[j + 1] = lst[j + 1], lst [j]
                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst

def insertionSort(draw_info):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            sort = i > 0 and lst[i - 1] > current

            if not sort:
                break

            lst[i] = lst [i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True

    return lst

def selectionSort(draw_info):
    lst = draw_info.lst

    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j

        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, i - 1: draw_info.RED}, True)
        yield True

    return lst

def radixSort(draw_info):
    lst = draw_info.lst

    max1 = max(lst)
    exp = 1
    n = len(lst)

    while max1 / exp > 0:
        output = [0] * (n)
        count = [0] * (10)

        for i in range(0, n):
            index = (lst[i] / exp)
            count[int((index) % 10)] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (lst[i] / exp)
            output[count[int((index) % 10)] - 1] = lst[i]
            count[int((index) % 10)] -= 1
            i -= 1
        i = 0
        for i in range(0, len(lst)):
            lst[i] = output[i]
            yield True
        exp *= 10

    return lst

def mergeSort(draw_info, lst=None):
    if lst is None:
        lst = draw_info.lst
    
    if len(lst) > 1:
        mid = len(lst) // 2
        left_half = lst[:mid]
        right_half = lst[mid:]

        yield from mergeSort(draw_info, left_half)
        yield from mergeSort(draw_info, right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                lst[k] = left_half[i]
                i += 1
            else:
                lst[k] = right_half[j]
                j += 1
            k += 1
            draw_list(draw_info, {k-1: draw_info.RED}, True)
            yield True

        while i < len(left_half):
            lst[k] = left_half[i]
            i += 1
            k += 1
            draw_list(draw_info, {k-1: draw_info.RED}, True)
            yield True

        while j < len(right_half):
            lst[k] = right_half[j]
            j += 1
            k += 1
            draw_list(draw_info, {k-1: draw_info.RED}, True)
            yield True

    return lst

def quickSort(draw_info, lst=None, low=None, high=None):
    def partition(draw_info, lst, low, high):
        pivot = lst[high]
        i = low - 1

        for j in range(low, high):
            if lst[j] < pivot:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.RED, j: draw_info.BLUE}, True)

        lst[i+1], lst[high] = lst[high], lst[i+1]
        draw_list(draw_info, {i+1: draw_info.RED, high: draw_info.BLUE}, True)

        return i+1
    if lst is None:
        lst = draw_info.lst
    if low is None:
        low = 0
    if high is None:
        high = len(lst) - 1
    
    if low < high:
        pivot = partition(draw_info, lst, low, high)
        quickSort(draw_info, lst, low, pivot - 1)
        quickSort(draw_info, lst, pivot + 1, high)

    return lst


def partition(draw_info, lst, low, high):
    pivot = lst[high]
    i = low - 1

    for j in range(low, high):
        if lst[j] < pivot:
            i += 1
            lst[i], lst[j] = lst[j], lst[i]
            draw_list(draw_info, {i: draw_info.RED, j: draw_info.BLUE}, True)

    lst[i+1], lst[high] = lst[high], lst[i+1]
    draw_list(draw_info, {i+1: draw_info.RED, high: draw_info.BLUE}, True)

    return i+1


def main():
    run = True
    clock = pygame.time.Clock()

    n = 100
    min_val = 0
    max_val = 200

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)

    sorting = False

    sorting_algorithm = bubbleSort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    while run:
        clock.tick(300)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algorithm_name)

        draw(draw_info, sorting_algorithm_name)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_c:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info)
            elif event.key == pygame.K_b and sorting == False:
                sorting_algorithm = bubbleSort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_i and sorting == False:
                sorting_algorithm = insertionSort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_s and sorting == False:
                sorting_algorithm = selectionSort
                sorting_algorithm_name = "Selection Sort"
            elif event.key == pygame.K_r and sorting == False:
                sorting_algorithm = radixSort
                sorting_algorithm_name = "Radix Sort"
            elif event.key == pygame.K_m and sorting == False:
                sorting_algorithm = mergeSort
                sorting_algorithm_name = "Merge Sort"
            elif event.key == pygame.K_q and sorting == False:
                sorting_algorithm = quickSort
                sorting_algorithm_name = "Quick Sort"


    pygame.quit()

if __name__ == "__main__":
    main()