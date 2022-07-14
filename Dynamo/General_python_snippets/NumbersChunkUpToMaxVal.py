from numbers import Number


def chunk_upto_max(numbers, max_size):
    # type: (list[Number], Number) -> list[Number]
    """Takes a list of positive numbers and splits them
    into chunks not exceeding the maximum size"""
    assert max_size >= 0, "Max size should be positive"
    chunked_numbers = []
    for num in numbers:
        assert num >= 0, "Numbers should be positive"
        if num > max_size:
            multiplier = int(num / max_size)
            remainder = num - multiplier * max_size
            chunked_numbers.append(remainder)
            chunked_numbers.extend(max_size for i in range(multiplier))
        else:
            chunked_numbers.append(num)
    return chunked_numbers


chunk_upto_max([2, 5, 10], 7)  # -> [2, 5, 3, 7]
