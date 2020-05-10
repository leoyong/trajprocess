import math
import numpy as np
from .base import isnumbrer
# https://github.com/wandergis/coordTransform_py/blob/master/coordTransform_utils.py

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方


def transformLat_pt(x, y):
    """
    """
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * math.pi) + 40.0 * math.sin(y / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * math.pi) + 320 * math.sin(y * math.pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLat(x_vec, y_vec):
    """
    """
    try:
        import numpy as np
    except:
        return "Error, unable to import Numpy"

    ret = -100.0 + 2.0 * x_vec + 3.0 * y_vec + 0.2 * y_vec * y_vec + 0.1 * x_vec * y_vec + 0.2 * np.sqrt(np.abs(x_vec))
    ret += (20.0 * np.sin(6.0 * x_vec * pi) + 20.0 * np.sin(2.0 * x_vec * pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(y_vec * pi) + 40.0 * np.sin(y_vec / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * np.sin(y_vec / 12.0 * pi) + 320 * np.sin(y_vec * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLon_pt(x, y):
    """
    """
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * math.pi) + 20.0 * math.sin(2.0 * x * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * math.pi) + 40.0 * math.sin(x / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * math.pi) + 300.0 * math.sin(x / 30.0 * math.pi)) * 2.0 / 3.0
    return ret

def transformLon(x_vec, y_vec):
    """
    """
    try:
        import numpy as np
    except:
        return "Error, unable to import Numpy"

    ret = 300.0 + x_vec + 2.0 * y_vec + 0.1 * x_vec * x_vec + 0.1 * x_vec * y_vec + 0.1 * np.sqrt(np.abs(x_vec))
    ret += (20.0 * np.sin(6.0 * x_vec * pi) + 20.0 * np.sin(2.0 * x_vec * pi)) * 2.0 / 3.0
    ret += (20.0 * np.sin(x_vec * pi) + 40.0 * np.sin(x_vec / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * np.sin(x_vec / 12.0 * pi) + 300.0 * np.sin(x_vec / 30.0 * pi)) * 2.0 / 3.0
    return ret

def outOfChina(lng, lat):
    """
    """
    if lng < 72.004 or lng > 137.8347:
        return True
    
    if lat < 0.8293 or lat > 55.8271:
        return True
    
    return False

def _WGSToGC02_pt(lng, lat):
    """
    lng:
    lat:
    """
    if outOfChina(lng, lat):
        return lng, lat

    dLat = transformLat(lng - 105.0, lat - 35.0)
    dLng = transformLon(lng - 105.0, lat - 35.0)

    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)

    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLng = (dLng * 180.0) / (a / sqrtMagic * math.cos(radLat) * math.pi)

    mgLat = lat + dLat
    mgLng = lng + dLng
    return mgLng, mgLat

def WGSToGC02(lng, lat):
    """
    Transfer WGS84 to GCJ-02
    lng_vec: 
    """
    if isnumbrer(lng) and isnumbrer(lat):
        return _WGSToGC02_pt(lng, lat)
    
    try:
        import numpy as np
    except:
        return "Error, unable to import Numpy"

    dLat = transformLat(lng - 105.0, lat - 35.0)
    dLng = transformLon(lng - 105.0, lat - 35.0)

    radLat = lat / 180.0 * pi
    magic = np.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = np.sqrt(magic)

    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLng = (dLng * 180.0) / (a / sqrtMagic * np.cos(radLat) * pi)

    mgLat = lat + dLat
    mgLng = lng + dLng
    return mgLng, mgLat

def _GC02ToWGS_pt(lng, lat):
    """
    GCJ02 to WGS84
    lng: GCJ02 lontitude
    lat: GCJ02 latitude
    """
    if outOfChina(lng, lat):
        return lng, lat
    
    dlat = transformLat(lng - 105.0, lat - 35.0)
    dlng = transformLon(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * math.pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dlng = (dlng * 180.0) / (a / sqrtMagic * math.cos(radlat) * math.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat

def GC02ToWGS(lng, lat):
    """
    GCJ02 to WGS84
    lng_vec: longitude vector
    lat_vec: latitude vector
    """
    if isnumbrer(lng) and isnumbrer(lat):
        return _GC02ToWGS_pt(lng, lat)

    try:
        import numpy as np
    except:
        return "Error, unable to import Numpy"
    
    dlat = transformLat(lng - 105.0, lat - 35.0)
    dlng = transformLon(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = np.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtMagic = np.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtMagic * np.cos(radlat) * np.pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return lng * 2 - mglng, lat * 2 - mglat
