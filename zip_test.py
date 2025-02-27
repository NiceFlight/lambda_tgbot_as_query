import itertools
import json

# aa = [1, 2, 3, 4, 5, 6, 7]

# for a, b in itertools.zip_longest(aa[::2], aa[1::2], fillvalue=None):
#     print(a, b)


def load_locations():
    with open('as_code.json', 'r', encoding='utf-8') as f:
        return json.load(f)

locations = load_locations()
print(locations['台北市'].values())
