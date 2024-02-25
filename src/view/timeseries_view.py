from cProfile import label
from textwrap import indent
from models.timeseries import Timeseries
import pandas as pd
import matplotlib.pyplot as plt


def visualize_timeseries(ts_dict: dict):
    plt.rcParams["figure.figsize"] = (10, 5)
    fig, ax = plt.subplots()
    for key, ts in ts_dict.items():
        # Add the time-series for "relative_temp" to the plot
        ax.plot(ts.pd_timeseries.index, ts.pd_timeseries, label=key)
    ax.legend()
    # Set the x-axis label
    ax.set_xlabel("Time")
