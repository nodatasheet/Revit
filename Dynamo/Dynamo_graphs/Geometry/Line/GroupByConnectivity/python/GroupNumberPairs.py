"""Method to group abstract unordered chunks of data
    based on their commonness, when there is no possibility of sorting them.

    Each pair of numbers represents a chunk. Connection represents commonness.
"""

from pprint import pprint
from random import shuffle, sample
import string


def connected(a, b):
    return a[0] == b[0] or a[1] == b[1] or a[0] == b[1] or a[1] == b[0]


def get_neighbors(pairs_dic):
    # type: (dict) -> list[set[dict.key]]
    """Gets all neighbors for each pair
    as list of sets of dictionary keys"""
    all_neighbours = []
    for i, pair in pairs_dic.items():
        sub_neighbours = {i}
        for j, pair in pairs_dic.items():
            if j != i and connected(pairs_dic[i], pair):
                sub_neighbours.add(j)
        all_neighbours.append(sub_neighbours)
    return all_neighbours


def merge_touching_sets(sets):
    # type: (list[set]) -> list[set]
    """Merges sets with common elements.
    Source: https://stackoverflow.com/a/9400562
    """
    new_group = []
    while len(new_group) != len(sets):
        new_group, sets = sets, []
        for set1 in new_group:
            for set2 in sets:
                if not set1.isdisjoint(set2):
                    set2.update(set1)
                    break
            else:
                sets.append(set1)
    return sets


pairs = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6],
         [10, 11], [11, 12], [12, 13], [13, 14]]

pairs = [tuple(sample(nums, len(nums))) for nums in pairs]
shuffle(pairs)
pprint(pairs)
print('')

pairs_dic = {string.ascii_lowercase[i]: v for i, v in enumerate(pairs)}
pprint(pairs_dic)
print('')

neighbours = get_neighbors(pairs_dic)
pprint(neighbours)
print('')

merged = merge_touching_sets(neighbours)
pprint(merged)
print('')

groupped = [[pairs_dic[k] for k in group] for group in merged]
pprint(groupped)
