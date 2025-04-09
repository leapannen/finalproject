import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import html5lib
import lxml

pio.renderers.default = 'iframe'

import warnings

#ignore all warnings
warnings.filterwarnings('ignore', category = FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(tickformat="%Y", row=1, col=1)  # For displaying only years in the first subplot
    fig.update_xaxes(tickformat="%Y", row=2, col=1)  # For displaying only years in the second subplot (CORRECTED LINE)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period='max')

tesla_data.reset_index(inplace=True)
#print(tesla_data.head())

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, 'html.parser')
tesla_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    if len(col) == 2:
        Date = col[0].text
        Revenue = col[1].text
    tesla_revenue = pd.concat([tesla_revenue, pd.DataFrame({'Date':[Date], 'Revenue':[Revenue]})],ignore_index=True)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$', "", regex=True)  # Убираем $, запятую
tesla_revenue["Revenue"] = pd.to_numeric(tesla_revenue["Revenue"], errors='coerce')  # Преобразуем в числовой тип
tesla_revenue.dropna(inplace=True)  # Удаляем строки с NaN
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]  # Удаляем пустые значения в 'Revenue'

# Вывод последних строк
#print(tesla_revenue.tail())

GameStop = yf.Ticker("GME")
gme_data = GameStop.history(period='max')
gme_data.reset_index(inplace=True)

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data_2 = requests.get(url).text

soup = BeautifulSoup(html_data_2, 'html.parser')

gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in soup.find('tbody').find_all('tr'):
    col = row.find_all('td')
    if len(col) == 2:
        Date = col[0].text
        Revenue = col[1].text
    gme_revenue = pd.concat([gme_revenue, pd.DataFrame({'Date': [Date], 'Revenue': [Revenue]})], ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$', "", regex=True)  # Убираем $, запятую
#print(gme_revenue.tail())

pio.renderers.default = 'browser'
#make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')