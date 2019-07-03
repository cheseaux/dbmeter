import plotly.plotly as py
import plotly.graph_objs as go

import pandas as pd
from datetime import datetime

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv')

data = [go.Scatter(x=df.Date, y=df['AAPL.High'])]

py.iplot(data, filename = 'time-series-simple')
