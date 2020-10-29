import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import csv

df =  pd.read_csv('data.csv')
df = df.drop('Cumulative cases',axis=1)
df = df.drop('days',axis=1)
df = df.dropna()


lastIndex = len(df) - 1
lastDateData = df.tail(1)
lastDate = lastDateData['date'].iloc[0]

# deathRate = []
# CuredRate = []
# InfectionRate = []
# cumulativeFlag = 0
# cumulativeList = []
# for x in range(0,lastIndex+1):
#     deathNumber = df['Deaths'].iloc[x]
#     curedNumber = df['Cured'].iloc[x]
#     icuNumber = df['ICU'].iloc[x]
#     casesNumber = df[' cases/day'].iloc[x]
#     deathRateNumber = (deathNumber/casesNumber)*100
#     CuredRateNumber = (curedNumber/casesNumber)*100
#     InfectionRateNumber = ((((casesNumber-curedNumber)/casesNumber)*100))
#     deathRate.append(round(deathRateNumber,2))
#     CuredRate.append(round(CuredRateNumber,2))
#     InfectionRate.append(round(InfectionRateNumber,2))
#     cumulativeFlag = cumulativeFlag + casesNumber
#     cumulativeList.append(cumulativeFlag)



def forecastDeaths():

    dateRange = pd.date_range(start=lastDate, periods=100)

    deaths_df = df[['date', 'Deaths']]
    deaths_df.set_index('date', inplace=True)
    deaths_df.index = pd.to_datetime(deaths_df.index)
    stepwise_model = pm.auto_arima(deaths_df, start_p=1, start_q=1,
                                   max_p=3, max_q=3, m=12,
                                   start_P=0, seasonal=True,
                                   d=1, D=1, trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)
    print(stepwise_model.aic())
    stepwise_model.fit(deaths_df)
    future_forecast = stepwise_model.predict(n_periods=100)
    predictionList = []

    for x in future_forecast:
        if (x < 0):
            y = x * -1
            predictionList.append(int(y))
        else:
            predictionList.append(int(x))

    i = 0
    # for x in dateRange:
    #     print("Date : ", x, "   Death = ", predictionList[i])
    #     i = i + 1

    return predictionList

def forecasteCasesDay():
    dateRange = pd.date_range(start=lastDate, periods=100)

    cases_df = df[['date', ' cases/day']]
    cases_df.set_index('date', inplace=True)
    cases_df.index = pd.to_datetime(cases_df.index)
    stepwise_model = pm.auto_arima(cases_df, start_p=1, start_q=1,
                                   max_p=3, max_q=3, m=12,
                                   start_P=0, seasonal=True,
                                   d=1, D=1, trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)
    print(stepwise_model.aic())
    stepwise_model.fit(cases_df)
    future_forecast = stepwise_model.predict(n_periods=100)
    predictionList = []

    for x in future_forecast:
        if (x < 0):
            y = x * -1
            predictionList.append(int(y))
        else:
            predictionList.append(int(x))

    i = 0
    # for x in dateRange:
    #     print("Date : ", x, "   Cases/day = ", predictionList[i])
    #     i = i + 1

    return predictionList


def forecasteICU():
    dateRange = pd.date_range(start=lastDate, periods=100)

    cases_df = df[['date', 'ICU']]
    cases_df.set_index('date', inplace=True)
    cases_df.index = pd.to_datetime(cases_df.index)
    stepwise_model = pm.auto_arima(cases_df, start_p=1, start_q=1,
                                   max_p=3, max_q=3, m=12,
                                   start_P=0, seasonal=True,
                                   d=1, D=1, trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)
    print(stepwise_model.aic())
    stepwise_model.fit(cases_df)
    future_forecast = stepwise_model.predict(n_periods=100)
    predictionList = []

    for x in future_forecast:
        if (x < 0):
            y = x * -1
            predictionList.append(int(y))
        else:
            predictionList.append(int(x))

    i = 0
    # for x in dateRange:
    #     print("Date : ", x, "   ICU = ", predictionList[i])
    #     i = i + 1
    #
    return predictionList

def forecastCured():

    dateRange = pd.date_range(start=lastDate, periods=100)

    cases_df = df[['date', 'Cured']]
    cases_df.set_index('date', inplace=True)
    cases_df.index = pd.to_datetime(cases_df.index)
    stepwise_model = pm.auto_arima(cases_df, start_p=1, start_q=1,
                                   max_p=3, max_q=3, m=12,
                                   start_P=0, seasonal=True,
                                   d=1, D=1, trace=True,
                                   error_action='ignore',
                                   suppress_warnings=True,
                                   stepwise=True)
    print(stepwise_model.aic())
    stepwise_model.fit(cases_df)
    future_forecast = stepwise_model.predict(n_periods=100)
    predictionList = []

    for x in future_forecast:
        if (x < 0):
            y = x * -1
            predictionList.append(int(y))
        else:
            predictionList.append(int(x))

    i = 0
    # for x in dateRange:
    #     print("Date : ", x, "   Cured = ", predictionList[i])
    #     i = i + 1

    return predictionList


deaths_prediction = forecastDeaths()
cases_prediction = forecasteCasesDay()
icu_predictions = forecasteICU()
cured_predictions = forecastCured()


dateRange = pd.date_range(start=lastDate, periods=100)
flag = lastIndex + 1
for i in range(100):
     df.loc[flag] = [dateRange[i],cases_prediction[i],icu_predictions[i],deaths_prediction[i],cured_predictions[i]]
     flag += 1


lastIndex = len(df) - 1
deathRate = []
CuredRate = []
InfectionRate = []
cumulativeFlag = 0
cumulativeList = []
days_list = []
for x in range(0,lastIndex+1):
    days_list.append(x)
    deathNumber = df['Deaths'].iloc[x]
    curedNumber = df['Cured'].iloc[x]
    icuNumber = df['ICU'].iloc[x]
    casesNumber = df[' cases/day'].iloc[x]
    if(casesNumber==0):
        deathRateNumber = 0
        CuredRateNumber = 0
        InfectionRateNumber = 0
        deathRate.append(0)
        CuredRate.append(0)
        InfectionRate.append(0)
        cumulativeFlag = cumulativeFlag + casesNumber
        cumulativeList.append(cumulativeFlag)
    else:
        deathRateNumber = (deathNumber/casesNumber)*100
        CuredRateNumber = (curedNumber/casesNumber)*100
        InfectionRateNumber = ((((casesNumber-curedNumber)/casesNumber)*100))
        deathRate.append(abs(round(deathRateNumber,2)))
        CuredRate.append(abs(round(CuredRateNumber,2)))
        InfectionRate.append(abs(round(InfectionRateNumber,2)))
        cumulativeFlag = cumulativeFlag + casesNumber
        cumulativeList.append(abs(cumulativeFlag))

df['days'] = days_list
df['Death Rate %'] = deathRate
df['Cured Rate %'] = CuredRate
df['Infection Rate %'] = InfectionRate
df['Cumulative Cases'] = cumulativeList

print(df.head(100))


df.to_csv ('output.csv', index = False, header=True)


