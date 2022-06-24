from itertools import repeat
import math


def chunk_upto_max(numbers, max_size):
    # type: (list, float) -> list
    """Takes a list of numbers and splits them
    into values not exceeding the maximum size"""
    chunked_lengths = []
    for num in numbers:
        if num > max_size:
            denominator = math.floor(num / max_size)
            remainder = num - denominator * max_size
            chunked_lengths.append(remainder)
            chunked_lengths.extend(repeat(max_size, denominator))
        else:
            chunked_lengths.append(num)
    return chunked_lengths


chunked_lengths = chunk_upto_max([2, 5, 10], 7)  # -> [2, 5, 3, 7]
