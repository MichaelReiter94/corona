from corona_plots import plotData
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib as mlp

###  scenario: 'cases', 'cumulative cases', 'deaths', 'cumulative deaths', 'death rate', 'deaths per 100.000 capita', 'growth rate', 'death growth rate'
###['Brazil', 'Turkey', 'Iran', 'Canada', 'China', 'Austria', 'Sweden', 'Germany', 'Italy', 'United_States_of_America', 'United_Kingdom', 'India', 'Netherlands', 'Belgium', 'Norway', 'Denmark', 'Finland', 'Spain', 'France']


# countries = ['Austria', 'Sweden', 'Germany']
countries = ['Sweden', 'Denmark', 'Austria', 'Germany']
# countries = ['Brazil', 'Turkey', 'United_Kingdom', 'Germany', 'United_States_of_America']

# plotData(['Sweden'], threshold=20, scenario='cumulative cases', relative_date=False, averaged=5)
# plotData(['Austria', 'Netherlands'], threshold=100, scenario='cumulative cases', relative_date=False, averaged=5)
# plt.figure()
plotData(countries, threshold=0.1, scenario='deaths per 100.000 capita', relative_date=False, averaged=5)

x1 = dt.datetime(2020, 3, 9)
x2 = x1 + dt.timedelta(days=14)
x3 = x2 + dt.timedelta(days=14)


# plt.axvline(x1, c='red',)
# plt.axvline(x2,  c='red')
# plt.axvline(x3,  c='red')
# plt.yscale('log')
plt.show()



