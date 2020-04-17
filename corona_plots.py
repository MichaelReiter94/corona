import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib import dates as mpl_dates
import matplotlib as mpl

def getCountryData(list_of_countries_):
    """ takes the covid-19 data (from www.ecdc.europa.eu) from the dowloaded .csv file and creates individual .csv files for each country in the list argument"""
    if type(list_of_countries_) is not list:
        list_of_countries_ = [list_of_countries_]


    for country_name in list_of_countries_:
        file_name = country_name + '.csv'

        with open(file_name, 'w') as write_file:
            field_names = ['dateRep', 'day', 'month', 'year', 'cases', 'deaths', 'countriesAndTerritories', 'geoId',
                           'countryterritoryCode', 'popData2018']
            csv_writer = csv.DictWriter(write_file, fieldnames=field_names)

            with open('corona.csv', 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                csv_writer.writeheader()

                for line in csv_reader:
                    if line['countriesAndTerritories'] == country_name:
                        csv_writer.writerow(line)

        print('updated csv file for {}'.format(country_name))

def getLabelsAndTitle(scenario):
    if scenario == 'cases':
        title = 'confirmed cases of Covid-19'
        ylabel = 'confirmed infections'
    elif scenario == 'cumulative cases':
        title = 'cumulated confirmed cases of Covid-19'
        ylabel = 'confirmed infections'
    elif scenario == 'deaths':
        title ='deaths caused by Covid-19'
        ylabel = 'deaths'
    elif scenario == 'cumulative deaths':
        title = 'cumulated deaths caused by Covid-19'
        ylabel = 'deaths'
    elif scenario == 'death rate':
        title = 'death rate: deaths per infection'
        ylabel = 'percent'
    elif scenario == 'deaths per 100.000 capita':
        title = 'deaths per 100.000 capita'
        ylabel = 'cumulated deaths per capita'
    elif scenario == 'growth rate':
        title = 'growth rate of infections'
        ylabel = 'percent'
    elif scenario == 'death growth rate':
        title = 'growth of deaths'
        ylabel = 'growth in percent'
    else:
        ylabel = 'not found'
        title = 'not found'
        print('scenario not found')


    return ylabel, title

def plotData(country_names, **kwargs):
    """**kwargs are:\n
    - threshold (from how many cases/deaths/at what deathrate the plot starts)\n
    - scenario ('cases', 'cumulative cases', 'deaths', 'cumulative deaths', 'death ratio', 'deaths per 100.000 capita', 'growth rate', 'death growth rate')\n
    - new_figure (bool)\n
    - relative_date (bool): all countries start on the same day '0' where the threshold condition is matcehd
    - averaged (int) where it is reasonable (growth rate) the data gets averaged over this number of days"""
    if True:
        if type(country_names) is not list:
            country_names = [country_names]

        try:
            threshold = kwargs['threshold']
        except KeyError:
            threshold = 1.0
        try:
            scenario = kwargs['scenario']
        except KeyError:
            scenario = 'cumulative cases'
        try:                                                        #### need to check type!
            new_figure = kwargs['new_figure']
        except KeyError:
            new_figure = False
        try:                                                        #### need to check type!
            relative_date = kwargs['relative_date']
        except KeyError:
            relative_date = False
        try:                                                        #### need to check type!
            averaged_over_x_days = kwargs['averaged']
        except KeyError:
            averaged_over_x_days = 1

    if scenario == 'cases' or scenario == 'deaths':
        bar_graph = True
    else:
        bar_graph = False

    for country_name in country_names:

        ### read in csv file
        try:
            file_name = country_name + '.csv'
            if True:
                data = pd.read_csv(file_name)

                cases = np.array(data['cases'])
                dates = np.array(data['date'])
                deaths = np.array(data['deaths'])
                cumulative_cases = np.array(data['cum_cases'])
                cumulative_deaths = np.array(data['cum_deaths'])
                cumulative_deaths_per_capita = np.array(data['death_per_100.000_capita'])
                growth_rate = np.array(data['growth_rate'])
                death_rate = np.array(data['death_rate'])
                death_growth_rate = np.array(data['death_growth_rate'])

            if averaged_over_x_days > 1:
                growth_rate = movingAverage(growth_rate, averaged_over_x_days)
                death_growth_rate = movingAverage(death_growth_rate, averaged_over_x_days)


            ### convert to dtype datetime
            seperator = '-'
            correct_dates = []
            for date in dates:
                [day, month, year] = date.split('/')
                correct_dates.append(datetime(int(year), int(month), int(day)))

            ### choose what to plot
            if True:
                if scenario == 'cases':
                    plotting_data = cases
                elif scenario == 'cumulative cases':
                    plotting_data = cumulative_cases
                elif scenario == 'deaths':
                    plotting_data = deaths
                elif scenario == 'cumulative deaths':
                    plotting_data = cumulative_deaths
                elif scenario == 'death rate':
                    plotting_data = death_rate
                elif scenario == 'deaths per 100.000 capita':
                    plotting_data = cumulative_deaths_per_capita
                elif scenario == 'growth rate':
                    plotting_data = growth_rate
                elif scenario == 'death growth rate':
                    plotting_data = death_growth_rate
                else:
                    print('scenario not found, plotting cumulative cases')
                    plotting_data = cases

            ## eliminate dates with 0 cases
            while plotting_data[0] < threshold:
                plotting_data = np.delete(plotting_data, 0)
                correct_dates = np.delete(correct_dates, 0)
                dates = np.delete(dates, 0)

            ### make x-Axis for a "relative time view"
            if relative_date:
                relative_dates = np.linspace(0, len(dates)-1, len(dates))

            ### plot
            if True:
                # if new_figure:
                #     plt.figure()
                plt.style.use("fast")
                if bar_graph:
                    if relative_date:
                        plt.bar(relative_dates, plotting_data, alpha = 0.6, label=country_name)
                    else:
                        plt.bar(correct_dates, plotting_data, alpha = 0.6, label=country_name)
                else:
                    if relative_date:
                        plt.plot(relative_dates, plotting_data, linestyle='solid', markersize=3.0, markeredgecolor='black', markeredgewidth=1.0, alpha = 0.75, marker='x', label=country_name)
                    else:
                        plt.plot_date(correct_dates, plotting_data, linestyle='solid', markersize=3.0, markeredgecolor='black', markeredgewidth=1.0, alpha = 0.75, marker='x', label=country_name)

                plt.plot()
                ylabel, title = getLabelsAndTitle(scenario)
                plt.ylabel(ylabel, fontname='Times New Roman', fontsize=12)
                plt.title(title, fontsize=15, color='black', fontname='Times New Roman')

                plt.grid(True)

                if not relative_date:
                    plt.gcf().autofmt_xdate()
                    date_format = mpl_dates.DateFormatter('%B %d, %Y')
                    plt.gca().xaxis.set_major_formatter(date_format)
                else:
                    plt.xlabel('days', fontname='Times New Roman', fontsize=12)
                if plotting_data.max() > 1000:
                    plt.gca().yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

                plt.legend()

        except FileNotFoundError:
            print('File not found: ' + file_name)
            print('Check for spelling! (the first letter is a capital letter e.g. "Austria")')

    pass

def movingAverage(input_array, window_length):
    ### kausaler (linksseitiger moving average filter --> rechtecksfenster
    length = len(input_array)
    output_array = np.zeros(length)
    input_array = np.pad(input_array, (window_length-1, 0), 'constant', constant_values=0)

    for i in range(0, length):
        for j in range(-window_length, 0):
            input_index = i + j + window_length
            output_array[i] += input_array[input_index]

    return output_array/window_length

def calculateAndSaveDate(list_of_countries_):
    if type(list_of_countries_) is not list:
        list_of_countries_ = [list_of_countries_]
    for country_name in list_of_countries_:
        file_name = country_name + '.csv'
        try:
            data = pd.read_csv(file_name)

            cases = np.array(data['cases'])
            dates = np.array(data['dateRep'])
            deaths = np.array(data['deaths'])
            capita = np.array(data['popData2018'])
            geoID = np.array(data['popData2018'])
            capita = capita[0] / 100000
            n_samples = len(cases)

            geoID = np.flip(geoID)
            cases = np.flip(cases)
            dates = np.flip(dates)
            deaths = np.flip(deaths)
            cumulative_cases = np.cumsum(cases)
            cumulative_deaths = np.cumsum(deaths)
            cumulative_deaths_per_capita = cumulative_deaths / capita

            growth_rate = np.zeros(n_samples)
            death_rate = np.zeros(n_samples)
            death_growth_rate = np.zeros(n_samples)
            for i in range(0, n_samples):
                if cumulative_deaths[i] > 5 and cumulative_cases[i] > 50:
                    death_rate[i] = float(cumulative_deaths[i] / cumulative_cases[i] * 100)
                if i > 0:
                    if cumulative_cases[i - 1] > 50:
                        growth_rate[i] = cumulative_cases[i] / cumulative_cases[i - 1]
                    if cumulative_deaths[i - 1] > 10:
                        death_growth_rate[i] = cumulative_deaths[i] / cumulative_deaths[i - 1]

            for i in range(0, len(growth_rate)):
                if growth_rate[i] > 0:
                    growth_rate[i] = (growth_rate[i] - 1) * 100
                if death_growth_rate[i] > 0:
                    death_growth_rate[i] = (death_growth_rate[i] - 1) * 100


            with open(file_name, mode='w') as csv_file:
                fieldnames = ['cases', 'cum_cases', 'deaths', 'cum_deaths', 'date', 'death_rate', 'growth_rate', 'death_growth_rate', 'death_per_100.000_capita']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                temp_dict = {}
                writer.writeheader()
                for i in range(0, len(cases)):

                    temp_dict['cases'] = cases[i]
                    temp_dict['cum_cases'] = cumulative_cases[i]
                    temp_dict['deaths'] = deaths[i]
                    temp_dict['cum_deaths'] = cumulative_deaths[i]
                    temp_dict['date'] = dates[i]
                    temp_dict['death_rate'] = death_rate[i]
                    temp_dict['growth_rate'] = growth_rate[i]
                    temp_dict['death_growth_rate'] = death_growth_rate[i]
                    temp_dict['death_per_100.000_capita'] = cumulative_deaths_per_capita[i]

                    writer.writerow(temp_dict)

        except FileNotFoundError:
            print('File not found: ' + file_name)
            print('Check for spelling! (the first letter is a capital letter e.g. "Austria")')

    pass

if __name__ == "__main__":
    list_of_countries = ['Brazil', 'Turkey', 'Iran', 'Canada', 'China', 'Austria', 'Sweden', 'Germany', 'Italy', 'United_States_of_America', 'United_Kingdom', 'India', 'Netherlands', 'Belgium', 'Norway', 'Denmark', 'Finland', 'Spain', 'France']


    getCountryData(list_of_countries)


    calculateAndSaveDate(list_of_countries)
    print('done')
