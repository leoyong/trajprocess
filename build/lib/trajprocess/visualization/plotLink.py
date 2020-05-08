
import pandas as pd 
import matplotlib.pyplot as plt

def plot_time_density(series, **kwargs):
    """
    """
    plt.hist(series, range=(0, 3600), bins = int(3600 / 60), density = True)

def plot_dis_density(series, **kwargs):
    """
    """
    # plt.plot(series, )
    pass

def plot_hour(series, **kwargs):
    """
    """
    value_counts = series.value_counts(sort=False)
    value_counts = value_counts.sort_index()
    plt.plot(series.index, series.values)
    pass