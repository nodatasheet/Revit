"""Pack 1D items using First Fit Decreasing algorithm.
Supply: list of numbers, bin size (max number to fit into one bin)
Return: numbers packed in bins, bins qty, waste factor

first_fit_decreasing([2, 5, 3, 1], 6) -> [[5, 1], [3, 2]]
bins_qty -> 2
waste_factor -> 0.090909...
"""


def first_fit_decreasing(items, bin_size):
    # type: (list, int | float) -> list
    """Pack 1D items using First Fit Decreasing algorithm."""

    def catch_oversized(items, bin_size):
        # type: (list, int | float) -> None | ValueError
        """Assure there is no items with size bigger than bin.
        Otherwise raise an error with the list of oversized items."""
        oversized = {}
        for index, item in enumerate(items):
            if item > bin_size:
                oversized['index({})'.format(index)] = item
        if len(oversized) > 0:
            error_text = (
                'Following items are bigger than bin size:\n{}'.format(
                    oversized))
            raise ValueError(error_text)

    def first_fit(items, bin_size):
        # type: (list, int | float) -> list
        """First fit packing algorithm with unlimited qty of bins."""

        # move first item to first bin
        filled_space = [items[0]]
        bins = [[items[0]]]
        items.pop(0)

        # cycle by rest of items
        for item in items:
            is_bin_full = True
            for i in range(len(filled_space)):
                if (filled_space[i] + item <= bin_size):
                    bins[i].append(item)
                    filled_space[i] += item
                    is_bin_full = False
                    break
            if is_bin_full:
                bins.append([item])
                filled_space.append(item)
        return bins

    catch_oversized(items, bin_size)
    items_decreasing = sorted(items, reverse=True)
    bins = first_fit(items_decreasing, bin_size)
    return bins


items = IN[0]  # list of items to be packed
bin_size = IN[1]  # bin size

if items:
    packed = first_fit_decreasing(items, bin_size)
    bins_qty = len(packed)
    waste_factor = ((float(bins_qty * bin_size) / sum(items)) - 1)
else:
    packed = waste_factor = bins_qty = None

OUT = packed, bins_qty, waste_factor
