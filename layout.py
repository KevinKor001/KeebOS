from kmk.keys import KC

def get_mappings():
    LEFT_COUNT = 42
    RIGHT_COUNT = 42

    left = list(range(0, LEFT_COUNT))
    right = list(range(LEFT_COUNT, LEFT_COUNT + RIGHT_COUNT))

    return left + right
