import matplotlib.pyplot as plt
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import apikey


class AlphaGet:
    # initializes time series of symbol with 'duration' weeks
    def __init__(self, symbol, duration=260):
        ts = TimeSeries(key=apikey.api_key, output_format='pandas')
        df, _ = ts.get_weekly_adjusted(symbol=symbol)
        df = df[:duration]

        self.df = df
        self.symbol = symbol

    def plot(self):
        self.df['4. close'].plot()
        plt.title(self.symbol)
        plt.grid()
        plt.show()

    # returns average increase and decrease magnitudes and probabilities
    # for use in generating a random walk which models the data
    def walk_analysis(self):
        # closing prices
        series = pd.Series(self.df['4. close'].values)

        # average increase
        av_pos_var = 0
        n_inc = 0
        # average decrease
        av_neg_var = 0
        n_dec = 0
        # probability of increase
        inc_prob = 0

        previous_value = series[0]

        for index, value in series.items():
            delta = previous_value - value
            if delta < 0:
                av_neg_var += -delta
                n_dec += 1
            else:
                inc_prob += 1
                av_pos_var += delta
                n_inc += 1

            previous_value = value

        length = series.__len__()

        result = {
            'average_increase': av_pos_var / n_inc,
            'average_decrease': av_neg_var / n_dec,
            'increase_probability': inc_prob / length,
        }

        return result


def main():
    ag = AlphaGet(symbol='AMD')
    # print(ag.df)
    res = ag.walk_analysis()
    print(res)
    ag.plot()


if __name__ == '__main__':
    main()
