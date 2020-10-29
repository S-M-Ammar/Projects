import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

df =  pd.read_csv('data.csv')
#
# print(df.describe())



df_feb = df[pd.to_datetime(df['date']).dt.month == 2]
df_feb = df_feb.drop('Cumulative cases', 1)
df_feb = df_feb.drop('days', 1)
# df_feb = df[pd.to_datetime(df['date']).dt.strftime('%B') == 'Feb']
# print(df_feb.head(10))
# print("here   ",df_feb[' cases/day'].mean())

df_feb.set_index('date',inplace=True)
# df_feb.plot()
# plt.show()

df_mar = df[pd.to_datetime(df['date']).dt.month == 3]
df_mar = df_mar.drop('Cumulative cases', 1)
df_mar = df_mar.drop('days', 1)

df_mar.set_index('date',inplace=True)
# df_mar.plot()
# plt.show()

cases_df_mar = df_mar.drop(columns=['ICU','Deaths','Cured'])
print(cases_df_mar.mean())
deaths_df_mar = df_mar.drop(columns=['ICU',' cases/day','Cured'])
cured_df_mar = df_mar.drop(columns=['ICU','Deaths',' cases/day'])
icu_df_mar = df_mar.drop(columns=[' cases/day','Deaths','Cured'])

# cases_df_mar.plot()
# plt.show()
#
# deaths_df_mar.plot()
# plt.show()
#
# cured_df_mar.plot()
# plt.show()
#
# icu_df_mar.plot()
# plt.show()
# print("cured mean = ",cured_df_mar['Cured'].mean())

df_apr = df[pd.to_datetime(df['date']).dt.month == 4]
df_apr = df_apr.drop('Cumulative cases', 1)
df_apr = df_apr.drop('days', 1)
df_apr.set_index('date',inplace=True)
# df_apr.plot()
# plt.show()

cases_df_apr = df_apr.drop(columns=['ICU','Deaths','Cured'])
print("Mean of cases/day in april =  ",cases_df_apr[' cases/day'].mean())
deaths_df_apr = df_apr.drop(columns=['ICU',' cases/day','Cured'])
print("Mean of deaths in april =  ",deaths_df_mar['Deaths'].mean())
cured_df_apr = df_apr.drop(columns=['ICU','Deaths',' cases/day'])
print("Mean of cured in april =  ",cured_df_apr['Cured'].mean())
icu_df_apr = df_apr.drop(columns=[' cases/day','Deaths','Cured'])
print("Mean of icu in april =  ",icu_df_apr['ICU'].mean())

# icu_df_apr.plot()
# plt.show()
# cured_df_apr.plot()
# plt.show()

def bar_plot(ax, data, colors=None, total_width=0.5, single_width=1, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of the
        data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """

    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (name, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2

        # Draw a bar for every value of that type
        for x, y in enumerate(values):
            bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())


if __name__ == "__main__":
    '''
            fequency in particular year
    word :

    '''

    # Usage example:
    data = {
        "Cases in Feb": [df_feb[' cases/day'].sum()],
        "Cases in March": [df_mar[' cases/day'].sum()],
        "Cases in April": [df_apr[' cases/day'].sum()],

    }

    fig, ax = plt.subplots()
    bar_plot(ax, data, total_width=.8, single_width=.9)
    index = np.arange(len(
        ['Cases / day']))
    plt.xticks(index,
               ['Cases / Day'], fontsize=8, rotation=0)
    # plt.show()

    data = {
        "ICU in Feb": [df_feb['ICU'].sum()],
        "ICU in March": [df_mar['ICU'].sum()],
        "ICU in April": [df_apr['ICU'].sum()],

    }

    fig, ax = plt.subplots()
    bar_plot(ax, data, total_width=.8, single_width=.9)
    index = np.arange(len(
        ['ICU']))
    plt.xticks(index,
               ['ICU'], fontsize=8, rotation=0)
    # plt.show()

    data = {
        "Deaths in Feb": [df_feb['Deaths'].sum()],
        "Deaths in March": [df_mar['Deaths'].sum()],
        "Deaths in April": [df_apr['Deaths'].sum()],

    }

    fig, ax = plt.subplots()
    bar_plot(ax, data, total_width=.8, single_width=.9)
    index = np.arange(len(
        ['Deaths']))
    plt.xticks(index,
               ['Deaths'], fontsize=8, rotation=0)
    # plt.show()

    data = {
        "Cured in Feb": [df_feb['Cured'].sum()],
        "Cured in March": [df_mar['Cured'].sum()],
        "Cured in April": [df_apr['Cured'].sum()],

    }

    fig, ax = plt.subplots()
    bar_plot(ax, data, total_width=.8, single_width=.9)
    index = np.arange(len(
        ['Cured']))
    plt.xticks(index,
               ['Cured'], fontsize=8, rotation=0)
    # plt.show()

df = df.drop('Cumulative cases', 1)
df = df.drop('days', 1)

deathRate = (df['Deaths'].sum() * 100) / (df[' cases/day'].sum())
print("Death Rate = ",deathRate)


curedRate = (df['Cured'].sum() * 100) / (df[' cases/day'].sum())
print("Cured Rate = ",curedRate)

# InfectionRate = ((df['Deaths'].sum() + df['ICU'].sum() - df['Cured'].sum()) * 100) / (df[' cases/day'].sum())
# print("Infection Rate = ",InfectionRate)

InfectionRate = ((df[' cases/day'].sum() - df['Cured'].sum())*100 ) / df[' cases/day'].sum()
print("Infection Rate = ",InfectionRate)
