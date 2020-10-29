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

deaths_df = df[['date','Cured']]
deaths_df.set_index('date',inplace=True)
deaths_df.index = pd.to_datetime(deaths_df.index)



deaths_df = deaths_df.dropna(how='any',axis=0)

deaths_df.plot()
plt.show()


totalLenght = deaths_df.__len__()
trainSize = int((70/100)*totalLenght)
train = deaths_df.iloc[0:trainSize]
test = deaths_df.iloc[trainSize:]

stepwise_model = pm.auto_arima(train, start_p=1, start_q=1,
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal=True,
                           d=1, D=1, trace=True,
                           error_action='ignore',
                           suppress_warnings=True,
                           stepwise=True)
print(stepwise_model.aic())



stepwise_model.fit(train)
future_forecast = stepwise_model.predict(n_periods=15)
print(future_forecast)
print(type(future_forecast))

predictionList = []

for x in future_forecast:
    if(x<0):
        y = x*-1
        predictionList.append(int(y))
    else:
        predictionList.append(int(x))

predictionArray = np.array(predictionList)
future_forecast = pd.DataFrame(predictionArray,index = test.index,columns=['Prediction'])
pd.concat([test,future_forecast],axis=1).plot()
plt.show()

print("\n\n")

ytrue = test['Cured'].tolist()
yPred = predictionList

print("MSE = ",mean_squared_error(ytrue,yPred))
