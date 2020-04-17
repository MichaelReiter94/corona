import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates
from matplotlib.animation import FuncAnimation
import random

def getData(list_of_countries, plotting_data):
    check_csv = pd.read_csv('Austria.csv')
    dates = np.array(check_csv['date'])

    data_length = len(dates)
    plotting_array = np.zeros([data_length, len(list_of_countries)])
    if type(list_of_countries) is not list:
        list_of_countries = [list_of_countries]

    for index, country_name in enumerate(list_of_countries):
        file_name = country_name + '.csv'
        data = pd.read_csv(file_name)
        plotting_array[:, index] = np.array(data[plotting_data])

    return plotting_array, dates


def animate(it, plotting_array, list_of_countries, dates, color_array):
    plt.cla()
    todays_numbers = plotting_array[it, :]
    zipped = zip(todays_numbers, list_of_countries, color_array)
    tuple_list = sorted(zipped)
    todays_numbers, list_of_countries, color_array = zip(*tuple_list)

    plt.barh(list_of_countries, todays_numbers, color=color_array)

    # plt.grid(True)
    plt.title(dates[it])

    pass


def randomColor():
    r_color = '#'
    for j in range(6):
        r_color += random.choice('0123456789ABCDEF')
    return r_color


if __name__ == "__main__":

    countries = ['China', 'Austria', 'Sweden', 'Germany', 'Italy', 'United_States_of_America', 'United_Kingdom', 'Netherlands', 'Belgium', 'Norway', 'Denmark', 'Spain', 'France']

    plot_array, dates_iter = getData(countries, 'death_per_100.000_capita')
    day = 10
    month = 2

    colors = []
    for country in countries:
        colors.append(randomColor())
    data_start = datetime(2019, 12, 31)
    plot_from_day = datetime(2020, month, day)
    delta = plot_from_day - data_start
    offset = delta.days

    ani = FuncAnimation(plt.gcf(), animate, frames=np.arange(offset, len(dates_iter), 1), interval=200,
                        fargs=[plot_array, countries, dates_iter, colors], repeat=False)



    plt.tight_layout()
    plt.show()
