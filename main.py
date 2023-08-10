from datetime import date, timedelta
import requests
import time
import math
from twilio.rest import Client

# Stock market API requests
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://gnews.io/api/v4/search"
API_KEY = "INSERT_API_KEY"

parameters = {
    "symbol": STOCK,
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "interval": "60min",
    "apikey": API_KEY
}

r = requests.get(STOCK_ENDPOINT, params=parameters)
r.raise_for_status()
data = r.json()
print(data)
yesterday = date.today() -timedelta(days=1)
day_before = yesterday - timedelta(days=1)

y_day_close = data["Time Series (Daily)"][f"{yesterday}"]["4. close"]
day_before_close = data["Time Series (Daily)"][f"{day_before}"]["4. close"]

diff = (float(y_day_close) - float(day_before_close)) * 0.05
print(abs(diff))

#News data API request
API_KEY2 = "INSERT_API_KEY2"
parameter2 = {
    "q": COMPANY_NAME,
    "lang": "en",
    "token": API_KEY2
}
news_data = requests.get(NEWS_ENDPOINT, params=parameter2)
x = slice(3)
news = news_data.json()['articles'][x]


account_sid = 'INSERT_SID'
auth_token = 'INSERT_TOKEN'
client = Client(account_sid, auth_token)
number = 0
for art in news:
    title = news[number]['title']
    content = news[number]['content']
    number += 1
    print(title)
    message = f"{STOCK}: {round(diff,1)}🔺\n\n"\
              f"Title:{title}\n" \
              f"Brief: {content}"
    message = client.messages.create(
        body=message,
        from_='+15618166864',
        to='INSERT_NUMBER')
    print(message.status)


# message.sid - prints the SID to show it's sent.

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

