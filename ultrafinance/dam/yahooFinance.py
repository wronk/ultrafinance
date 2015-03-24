'''
Created on Dec 21, 2010

@author: ppa

Thanks to Corey Goldberg, this module is based
http://www.goldb.org/ystockquote.html

sample usage:
>>> import YahooFinance
>>> print YahooFinance.get_price('GOOG')
529.46
'''
import urllib
import traceback
from ultrafinance.model import Quote
from ultrafinance.lib.errors import UfException, Errors

import logging
LOG = logging.getLogger()


class YahooFinance(object):
    def __request(self, symbol, stat):
        try:
            url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (symbol,
                                                                       stat)
            return urllib.urlopen(url).read().strip().strip('"')
        except IOError:
            raise UfException(Errors.NETWORK_ERROR,
                              "Can't connect to Yahoo server")
        except BaseException:
            raise UfException(Errors.UNKNOWN_ERROR,
                              "Unknown Error in YahooFinance.__request %s" %
                              traceback.format_exc())

    def getAll(self, symbol):
        """
        Get all available quote data for the given ticker symbol.
        Returns a dictionary.
        """
        values = self.__request(symbol,
                                'l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7').split(',')
        data = {}
        data['price'] = values[0]
        data['change'] = values[1]
        data['volume'] = values[2]
        data['avg_daily_volume'] = values[3]
        data['stock_exchange'] = values[4]
        data['market_cap'] = values[5]
        data['book_value'] = values[6]
        data['ebitda'] = values[7]
        data['dividend_per_share'] = values[8]
        data['dividend_yield'] = values[9]
        data['earnings_per_share'] = values[10]
        data['52_week_high'] = values[11]
        data['52_week_low'] = values[12]
        data['50day_moving_avg'] = values[13]
        data['200day_moving_avg'] = values[14]
        data['price_earnings_ratio'] = values[15]
        data['price_earnings_growth_ratio'] = values[16]
        data['price_sales_ratio'] = values[17]
        data['price_book_ratio'] = values[18]
        data['short_ratio'] = values[19]
        return data

    def getQuotes(self, symbol, start_dt, end_dt):
        """
        Get historical prices for the given ticker symbol.
        Date format is 'YYYY-MM-DD'

        Returns a nested list.
        """
        try:
            # a, b, c = month, day, year
            # Yahoo's months are off by one
            url = 'http://ichart.finance.yahoo.com/table.csv?s=' + \
                symbol + \
                '&c=%s' % str(start_dt.year) + \
                '&a=%s' % str(start_dt.month - 1) + \
                '&b=%s' % str(start_dt.day) + \
                '&f=%s' % str(end_dt.year) + \
                '&d=%s' % str(end_dt.month - 1) + \
                '&e=%s' % str(end_dt.day) + \
                '&g=d' + \
                '&ignore=.csv'

            records = urllib.urlopen(url).readlines()
        except IOError:
            raise UfException(Errors.NETWORK_ERROR,
                              "Can't connect to Yahoo server")
        except BaseException:
            raise UfException(Errors.UNKNOWN_ERROR, ('Unknown Error in'
                              ' YahooFinance.getHistoricalPrices %s' %
                              traceback.format_exc()))

        # Dump all data into list of "Quote" objects
        quote_list = []
        for r in records[1:]:  # Avoid first line; contains field names
            vals = r[:-2].split(',')  # Split and remove newline char
            quote_list.append(Quote(vals[0], vals[1], vals[2], vals[3],
                                    vals[4], vals[5], vals[6]))
        return quote_list
