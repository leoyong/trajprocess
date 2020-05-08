from math import radians, cos, sin, asin, sqrt
from enum import Enum

# mean earth radius - https://en.wikipedia.org/wiki/Earth_radius#Mean_radius
_AVG_EARTH_RADIUS_KM = 6371.0088

class Unit(Enum):
    """
    Enumeration of supported units.
    The full list can be checked by iterating over the class; e.g.
    the expression `tuple(Unit)`.
    """

    KILOMETERS = 'km'
    METERS = 'm'
    MILES = 'mi'
    NAUTICAL_MILES = 'nmi'
    FEET = 'ft'
    INCHES = 'in'


# Unit values taken from http://www.unitconversion.org/unit_converter/length.html
_CONVERSIONS = {Unit.KILOMETERS:       1.0,
                Unit.METERS:           1000.0,
                Unit.MILES:            0.621371192,
                Unit.NAUTICAL_MILES:   0.539956803,
                Unit.FEET:             3280.839895013,
                Unit.INCHES:           39370.078740158}

def get_avg_earth_radius(unit):
    unit = Unit(unit)
    return _AVG_EARTH_RADIUS_KM * _CONVERSIONS[unit]


def haversine_pt(slng, slat, elng, elat, unit = Unit.KILOMETERS):
    """
    Default: km
    Code refer https://github.com/mapado/haversine/blob/master/haversine/haversine.py
    """
    if (slng == elng) and (slat == elat):
        return 0

    slng, slat, elng, elat = map(radians, (slng, slat, elng, elat))
    diffLng = elng - slng
    diffLat = elat - slat
    dis = sin(diffLat * 0.5) ** 2 + cos(slat) * cos(elat) * sin(diffLng * 0.5) ** 2
    return 2 * get_avg_earth_radius(unit) * asin(sqrt(dis))

def haversine(slng, slat, elng, elat, unit=Unit.KILOMETERS):
    """
    slng: list-like variable
    slat: list-like variable
    elng: list-like variable
    elat: list-like variable
    Reference: https://github.com/mapado/haversine/blob/master/haversine/haversine.py
    """
    try:
        import numpy as np
    except ModuleNotFoundError:
        return "Error, unable to import Numpy"

    # convert all latitudes/longitudes from decimal degrees to radians
    slng, slat, elng, elat = map(np.radians, (slng, slat, elng, elat))

    # calculate haversine
    lng = elng - slng
    lat = elat - slat
    d = (np.sin(lat * 0.5) ** 2 + np.cos(slat) * np.cos(elat) * np.sin(lng * 0.5) ** 2)

    return 2 * get_avg_earth_radius(unit) * np.arcsin(np.sqrt(d))