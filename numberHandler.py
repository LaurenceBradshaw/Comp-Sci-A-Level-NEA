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


def coordsToDistance(lon1, lon2, lat1, lat2):
    # R = 3959.87433 for distance in miles.  For Earth radius in kilometers use 6372.8 km
    R = 6372.8
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    a = math.sin(dLat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dLon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return R * c
