#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
import time
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup


def fetch(url, wait=0):
    time.sleep(wait)
    print('GET %s' % url, end=' ', flush=True)
    page = urlopen(Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}))
    print('DONE')
    return page

class Price(object):
    def __init__(self, value: float, currency: str):
        self.value = value
        self.currency = currency
    def __str__(self):
        return f'{self.value} {self.currency}'

class Investment(object):
    def __init__(self, name: str, date, buy_price: Price, sell_price: Price):
        self.name = name
        self.date = date
        self.buy_price = buy_price
        self.sell_price = sell_price

    def __str__(self):
        return f'{self.date}, {self.name}, {self.buy_price}, {self.sell_price}'

class Tracker(object):
    def __init__(self, name):
        self.name = name
        self.date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def track(self): # -> List[Investment]:
        raise NotImplementedError

class EURUSDTracker(Tracker):
    def __init__(self):
        super().__init__("1-EUR")
    def track(self):
        usd_price = None
        cny_price = None
        rates_xml = fetch('https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        rates = rates_xml.read().decode('utf-8').split('\n')
        for rate in rates:
            rate = rate.strip()
            if "<Cube currency='USD'" in rate:
                usd_price = sum(map(float, re.findall('\d+\.\d\d?', rate)))
            if "<Cube currency='CNY'" in rate:
                cny_price = sum(map(float, re.findall('\d+\.\d\d?', rate)))

        return [Investment(self.name, self.date, Price(usd_price, "USD"), Price(usd_price, "USD")),
                Investment(self.name, self.date, Price(cny_price, "CNY"), Price(cny_price, "CNY"))]

class CrudeOilBrentTracker(Tracker):
    def __init__(self):
        super().__init__("crude-oil-brent-barrel")
    def track(self):
        oil_page = fetch('https://oilprice.com/')
        soup = BeautifulSoup(oil_page, 'html.parser')
        rows = soup.find_all('tr', attrs = {'data-spread': 'Crude Oil Brent'})
        for row in rows:
            value_columns = row.find_all('td', attrs = {'class': 'value'})
            if len(value_columns):
                value = float(value_columns[0].text.strip())
                return [Investment(self.name, self.date, Price(value, "USD"), Price(value, "USD"))]
        return []

class GoldTracker(Tracker):
    def __init__(self):
        super().__init__("gold-10g")
    def track(self):
        gold_page = fetch("https://feingoldhandel.de/preisliste")
        soup = BeautifulSoup(gold_page, 'html.parser')
        prices = soup.find_all('tr')
        buy_price = None
        sell_price = None
        for price in prices:
            columns = price.find_all('td')
            if len(columns) == 5:
                if columns[0].text == 'Goldbarren (999,9)' and columns[1].text == '10.00g':
                    sell_price = float(columns[2].text.replace('\xa0', ' ').split(' ')[0].replace(',', '.'))
                    buy_price = float(columns[3].text.replace('\xa0', ' ').split(' ')[0].replace(',', '.'))
                    break

        return [Investment(self.name, self.date, Price(buy_price, "EUR"), Price(sell_price, "EUR"))]

class LegoTracker(Tracker):
    def __init__(self, year, number, name):
        super().__init__(f'lego-{year}-{number}-{name}')
        self.number = number
    def track(self):
        item_price = None
        lego_page = fetch(f'https://brickset.com/sets/{self.number}', wait=1)
        soup = BeautifulSoup(lego_page, 'html.parser')
        fields = soup.find_all('dd')
        currency = 'EUR'
        for field in fields:
            if field.text.strip().startswith('New:'):
                links = field.find_all('a')
                if len(links):
                    if '$' in links[0].text:
                        currency = 'USD'
                    item_price = float(links[0].text.replace('~', '').replace('€', '').replace('$', ''))
                    break

        return [Investment(self.name, self.date, Price(item_price, currency), Price(item_price, currency))]

class LegoSatellitTracker(LegoTracker):
    def __init__(self):
        super().__init__("2019", "30365-1", "satellit")

class LegoSatellitenwartungTracker(LegoTracker):
    def __init__(self):
        super().__init__("2019", "60224-1", "satellitenwartung")

class LegoRovertestfahrtTracker(LegoTracker):
    def __init__(self):
        super().__init__("2019", "60225-1", "rovertestfahrt")


def as_html(investments):
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="UTF-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Investment tracker</title>
</head>
<body>
<h1>Investments</h1>
<p>Last file update: ~ {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
<pre>{investments}</pre>
<p>
<a href="investments.csv">Download csv</a>,
<a href="https://github.com/ooz/investment-tracker">code</a> crafted by <a href="https://ooz.github.io/">ooz</a>,
2019
</p>
</body>
</html>
'''

def main():
    TRACKERS = [
        EURUSDTracker(),
        CrudeOilBrentTracker(),
        GoldTracker(),
        LegoSatellitTracker(),
        LegoSatellitenwartungTracker(),
        LegoRovertestfahrtTracker()
    ]

    investments = [investment for tracker in TRACKERS for investment in tracker.track()]

    investments_csv = 'date, investment, buy price, sell price\n' + '\n'.join([str(investment) for investment in investments])
    print(investments_csv)
    with open('investments.csv', 'w') as f:
        f.write(investments_csv + '\n')

    investments_html = as_html(investments_csv)
    with open('index.html', 'w') as f:
        f.write(investments_html)

if __name__ == "__main__":
    main()
