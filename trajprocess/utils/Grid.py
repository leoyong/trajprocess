import geopandas
import pandas as pd
from shapely.geometry import Polygon, Point
import numpy as np

dic_epsg = {
    "4326": 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
}


class Grid:
    def __init__(self, xmin, ymin, xmax, ymax, xstep, ystep):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax 
        self.xstep = xstep
        self.ystep = ystep
        self.row_num = int(np.ceil((ymax - ymin) / ystep))
        self.col_num = int(np.ceil((xmax - xmin) / xstep))
        self.max_idx = self.row_num * self.col_num - 1
    
    def get_bound(self, i_row, j_col):
        """
        """
        assert i_row < self.row_num
        assert j_col < self.col_num
        xmin = self.xmin + j_col * self.xstep
        ymin = self.ymin + i_row * self.ystep
        return xmin, ymin, xmin + self.xstep, ymin + self.ystep
    
    def get_center(self, i_row, j_col):
        """
        """
        assert i_row < self.row_num
        assert j_col < self.col_num
        xmin = self.xmin + j_col * self.xstep
        ymin = self.ymin + i_row * self.ystep
        return xmin + self.xstep * 0.5, ymin + self.ystep * 0.5

    
    def get_idx(self, i_row, j_col):
        """
        """
        return i_row * self.col_num + j_col
    
    def coor_row_col(self, x, y):
        """
        """
        i_row = int((y - self.ymin) / self.ystep)
        j_col = int((x - self.xmin) / self.xstep)
        return i_row, j_col
    
    def coor_to_idx(self, x, y):
        """
        """
        i_row, j_col = self.coor_row_col(x, y)
        return self.get_idx(i_row, j_col)

    def batch_coor_to_idx(self, x, y):
        """
        x: pd.Series
        y: pd.Series
        """
        i_row = (y - self.ymin) / self.ystep
        j_col = (x - self.xmin) / self.xstep
        return self.get_idx(i_row.astype('int'), j_col.astype('int'))

    def to_gdf(self, epsg = None):
        """
        """
        list_geos = []
        for i in range(self.row_num):
            for j in range(self.col_num):
                idx = self.get_idx(i, j)
                xmin, ymin, xmax, ymax = self.get_bound(i, j)
                list_lng = [xmin, xmin, xmax, xmax]
                list_lat = [ymin, ymax, ymax, ymin]
                list_geos.append([idx, Polygon(zip(list_lng, list_lat))])
        df_geo = geopandas.GeoDataFrame(list_geos, columns = ["ZoneID", "geometry"])
        if epsg in dic_epsg.keys(): df_geo.crs = dic_epsg[epsg]
        return df_geo
    
    def to_gdf_point(self, epsg = None):
        """
        The center point of each cell 
        """
        list_geos = []
        for i in range(self.row_num):
            for j in range(self.col_num):
                idx = self.get_idx(i, j)
                xcent, ycent = self.get_center(i, j)
                list_geos.append([idx, Point(xcent, ycent)])
        df_geo = geopandas.GeoDataFrame(list_geos, columns = ["ZoneID", "geometry"])
        if epsg in dic_epsg.keys(): df_geo.crs = dic_epsg[epsg]
        return df_geo