import pandas as pd 
import shapely

from ..visualization import plotLink
import matplotlib.pyplot as plt


@pd.api.extensions.register_dataframe_accessor("Links")
class TripLinks:

    required_columns = ['stime', 'etime', 'slng', 'slat', 'elmg', 'elat']

    def __init__(self, df):
        self.df = df
    
    @staticmethod
    def _validate(df):
        if any([c not in df.columns for c in TripLinks.required_columns]):
            raise AttributeError("To process a DataFrame as a collection of triplegs, " \
                + "it must have the properties [%s], but it has [%s]." \
                % (', '.join(TripLinks.required_columns), ', '.join(df.columns)))
    
    def plot_duration(self, *args, **kwargs):
        if 'duration' not in self.df.columns:
            series = (self.df['etime'] - self.df['stime']).astype("int64") // 10 ** 9
        else:
            series = self.df['duration']
            
        plotLink.plot_time_density(series, *args, **kwargs)
        # plt.hist(series, range = (0, 3600), bins = int(3600 / 60), density = True)

    def plot_distance(self, *args, **kwargs):
        if "length" not in self.df.columns:
            return  
        
        plotLink.plot_dis_density(self.df['length'])
    
    def plot_hour(self, **kwargs):
        if 'hour' not in self.df.columns:
            series_hour = self.df['stime'].dt.hour
        else:
            series_hour = self.df['hour']

        plotLink.plot_hour(series_hour)

