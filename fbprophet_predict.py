from fbprophet import Prophet
import pandas as pd

def read_data():
    df = pd.read_csv('./data.csv')
    return df

def prophet_train():
    try:
        df = read_data()
        df.rename(columns={'create_time':'ds', 'view':'y'}, inplace=True)
        df_f = df[['ds', 'y', 'coin', 'share', 'like', 'favorite']]
        m = Prophet()
        m.fit(df_f)
        future = m.make_future_dataframe(periods=365)
        future.tail()
        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        fig1 = m.plot(forecast)
        fig1.savefig('1233.jpeg')
        fig2 = m.plot_components(forecast)
        print('end...')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    prophet_train()
