from tools import *

wac = WeightedAverageCalculator()

for x in range(0, 2000):
    print(wac.feed(x))