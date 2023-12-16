from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
import pandas as pd
import itertools
import streamlit as st
import warnings
from datetime import timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

warnings.filterwarnings('ignore')


def train_arima(df, end_date):
    # df = pd.read_csv("data/train.csv")
    # df = df[df['Store'] == store_id]
    #
    # df['Date'] = pd.to_datetime(df['Date'])
    # df.sort_values(by='Date', inplace=True)
    # df.fillna(0, inplace=True)
    # df['Sales'] = df['Sales'] * 1.0
    #
    #df_indexed = df.set_index('Date', drop=False)
    df_train_arima = df[["Sales"]]

    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    params, param_seasons, aic = [], [], []
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(df_train_arima,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit(disp=False)
                params.append(param)
                param_seasons.append(param_seasonal)
                aic.append(results.aic)
            except:
                continue

    index = aic.index(min(aic))

    print(f"Min AIC: {min(aic)} | Order: {params[index]} | Seasonal Order: {param_seasons[index]}")

    model_sarima = sm.tsa.statespace.SARIMAX(df_train_arima,
                                             order=params[index],
                                             seasonal_order=param_seasons[index],
                                             enforce_stationarity=False,
                                             enforce_invertibility=False)

    results_sarima = model_sarima.fit(disp=False)

    st.write(f"Prediction Duration: {str(df.idxmax()[0].date())} to {str(end_date)}")
    pred = results_sarima.get_prediction(start=df.idxmax()[0],
                                         end=end_date,
                                         dynamic=True)
    pred_ci = pred.conf_int()
    st.markdown(f"<i>RMSE: {round(min(aic), 2)}</i>", unsafe_allow_html=True)
    return pred, pred_ci






