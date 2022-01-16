import math
import random
from numpy import random as rn


def generatePoisson(rate):
    res = random.randint(0, 100)/101.0

    a = -math.log(1.0-res)/(1-rate)

    return a


def weightedRandom(lb, ub, avg):
    x = []
    avg = ub if ub-avg < 0 else avg
    avg = lb if avg-lb < 0 else avg
    valid = False
    while not valid:
        if avg - lb > ub - avg:
            x = rn.normal(loc=avg, scale=(ub - avg) / 2, size=1)
        else:
            x = rn.normal(loc=avg, scale=(avg - lb) / 2, size=1)
        if lb <= x[0] <= ub:
            valid = True
    return round(x[0])
