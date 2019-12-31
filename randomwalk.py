import matplotlib.pyplot as plt
import pandas as pd
from random import  random
from alphaget import AlphaGet
import datetime

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


def plot_walk(df_original, avg_inc=1, avg_dec=1, inc_prob=0.5, period=5, title=''):
    # start from newest historical data point
    new = df_original['4. close'].head(1)
    latest_price = new[current_day()]
    latest_date = new.keys()[0].strftime('%Y-%m-%d')

    # length of walk
    d_range = pd.date_range(start=latest_date, freq='7D', periods=period + 1)

    # generate walk
    df_walk = pd.DataFrame({
        'date': d_range,
        'Predicted': __walk(start_price=latest_price, avg_inc=avg_inc, avg_dec=avg_dec,
                            inc_prob=inc_prob, period=period)
    })

    # plot historical data and random walk data
    plt.plot('date', 'Predicted', data=df_walk, label='Predicted', linestyle='dashed')
    plt.plot(df_original['4. close'], label='Historical')
    plt.xticks(rotation=45)
    plt.ylabel('Share price (USD)')
    plt.legend(loc='upper left')
    plt.title(title)
    plt.tight_layout()

    plt.show()

    # return last price
    return df_walk['Predicted'][period]


def __walk(start_price, avg_inc, avg_dec, inc_prob, period):
    walk = list()
    walk.append(start_price)

    for i in range(1, period + 1):
        delta = avg_inc if random() < inc_prob else -avg_dec
        res = delta + walk[i-1]
        walk.append(res)

    return walk


def current_day():
    return datetime.date.today().strftime('%Y-%m-%d')


def main():
    ag = AlphaGet('SNAP', duration=25)
    plot_walk(ag.df, title='SNAP')
    print(current_day())


if __name__ == '__main__':
    main()
