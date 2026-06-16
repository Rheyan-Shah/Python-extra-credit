from utils.timer import measure

# Import both versions to compare
from problems.example.v1_basic import find_max as v1
from problems.example.v2_builtin import find_max as v2

data = [3, 1, 4, 1, 5, 9, 2, 6] * 1000

measure(v1, data)
measure(v2, data)
