# get_fuel.py
import feedparser


def fakeData(url):
    return [{'prices': '99.9'},
    {'prices': '101.9'},
    {'prices': '101.2'},
    {'prices': '99.9'}
    ]


def get_prices(day='Today', parseFunction=feedparser.parser):
    result = feedparser.parse('http://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS?Day=' + day)
    return [
       {'price': float(item['price'])}
        for item in result['entries']
    ]

