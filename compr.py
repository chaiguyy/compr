import PySimpleGUI as sg
import matplotlib.pyplot as plt
import randomwalk
from alphaget import AlphaGet

# UI layout + theme
sg.theme('Light Blue 3')
layout = [
    [sg.Text('Base salary')],
    [sg.InputText('80000')],  # value 0
    [sg.Text('Bonus')],
    [sg.InputText('20000')],  # value 1
    [sg.Text('Estimated benefits value')],
    [sg.InputText('8000')],  # value 2
    [sg.Text('Symbol of company stock option')],
    [sg.InputText('SNAP')],  # value 3
    [sg.Text('Number of months before option vests')],
    [sg.InputText('24')],  # value 4
    [sg.Text('Number of shares')],
    [sg.InputText('500')],  # value 5
    [sg.Submit(), sg.Cancel()],
]

window = sg.Window('Compr', layout)
event, values = window.read()
window.close()

if event == 'Submit':
    # stock symbol
    ticker = values[3].upper()
    # period in units of weeks
    period = int(values[4]) * 4

    ag = AlphaGet(ticker)
    data = ag.walk_analysis()

    stock = randomwalk.plot_walk(df_original=ag.df, avg_inc=data['average_increase'],
                                 avg_dec=data['average_decrease'], inc_prob=data['increase_probability'],
                                 period=period, title=ticker)
    stock = int(stock) * int(values[5])

    # bar graph data
    b_categories = ('Base salary', 'Bonus', 'Benefits', 'Stock')
    b_data = [int(values[0]), int(values[1]), int(values[2]), stock]

    plt.barh(b_categories, b_data)
    plt.title('Compensation Breakdown')
    plt.xlabel('USD')
    plt.tight_layout()
    plt.show()
