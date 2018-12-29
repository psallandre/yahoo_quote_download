# -*- coding: utf-8 -*-
"""
Created on Thu May 18 22:58:12 2017

@author: c0redumb
"""

# To make print working for Python2/3
from __future__ import print_function
import requests
import time
from os.path import expanduser

'''
Starting on May 2017, Yahoo financial has terminated its service on
the well used EOD data download without warning. This is confirmed
by Yahoo employee in forum posts.

Yahoo financial EOD data, however, still works on Yahoo financial pages.
These download links uses a "crumb" for authentication with a cookie "B".
This code is provided to obtain such matching cookie and crumb.
'''

default_useragent = 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.12'

class YahooQuote(object):
    def __init__(self, cookie_crumb=None, useragent=default_useragent):
        self.session = requests.session()
        self.session.headers['User-Agent'] = useragent
        self.cookie_crumb = cookie_crumb or self._get_cookie_crumb()

    def _get_cookie_crumb(self):
        '''
        This function perform a query and extract the matching cookie and crumb.
        '''

        r = self.session.get('https://finance.yahoo.com/quote/^GSPC')

        # Extract the crumb from the response (it's part of a massive ugly blob of JSON)
        cs = r.content.find(b'CrumbStore')
        cr = r.content.find(b'crumb', cs + 10)
        cl = r.content.find(b':', cr + 5)
        q1 = r.content.find(b'"', cl + 1)
        q2 = r.content.find(b'"', q1 + 1)
        crumb = r.content[q1 + 1:q2]

        # Extract the cookie
        cookie = self.session.cookies.get('B', domain='.yahoo.com')
        #print(self.session.cookies)

        self.session.cookies.clear()
        return cookie, crumb.decode()

    def csv(self, tickers, events='history', begindate=None, enddate=None, headers=True):
        if isinstance(tickers, str):
            tickers = tickers,

        now = int(time.time())
        if enddate is None:
            enddate = now
        if begindate is None:
            begindate = now - 86400

        cookie, crumb = self.cookie_crumb
        self.session.cookies['B'] = cookie
        #print(self.session.cookies)

        header_shown = False
        for ii, ticker in enumerate(tickers):
            r = self.session.get('https://query1.finance.yahoo.com/v7/finance/download/' + ticker,
                                 params = dict(period1=begindate, period2=enddate, events=events, interval='1d', crumb=crumb))
            r.raise_for_status()
            #print(r.cookies, r.url)
            rows = r.text.splitlines(True)
            for jj, row in enumerate(rows):
                if headers and not header_shown:
                    yield 'Symbol,' + row
                    header_shown = True
                elif jj>0:
                    yield ','.join((ticker, row))
