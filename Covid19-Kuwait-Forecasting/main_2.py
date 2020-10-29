import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pmdarima as pm
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

df =  pd.read_csv('data.csv')
print(df.head(10))
print(df.describe())
print(df.dtypes)


deaths_df = df[['date','Deaths']]
deaths_df = deaths_df.dropna(how='any',axis=0)

lastDateData = deaths_df.tail(1)
lastDate = lastDateData['date'].iloc[0]

deaths_df.set_index('date',inplace=True)
deaths_df.index = pd.to_datetime(deaths_df.index)

cases_df = df[['date',' cases/day']]
cases_df = cases_df.dropna(how='any',axis=0)
cases_df.set_index('date',inplace=True)
cases_df.index = pd.to_datetime(cases_df.index)



deaths_df.plot()
plt.show()

cases_df.plot()
plt.show()


stepwise_model = pm.auto_arima(deaths_df, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
print(stepwise_model.aic())


dateRange = pd.date_range(start=lastDate, periods = 100)

stepwise_model.fit(deaths_df)
future_forecast = stepwise_model.predict(n_periods=100)

predictionList = []

for x in future_forecast:
    if(x<0):
        y = x*-1
        predictionList.append(int(y))
    else:
        predictionList.append(int(x))

i = 0
for x in dateRange:
    print("Date : ",x,"   Death = ",predictionList[i])
    i = i+1