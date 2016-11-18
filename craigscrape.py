import pandas as pd

import numpy as np

import requests

from bs4 import BeautifulSoup

loc_prefixes = ['gbs', 'bmw', 'nos', 'nwb', 'sob']

for loc in loc_prefixes:

    url_base = 'https://boston.craigslist.org/search/{0}/aap'.format(loc)
    params = dict(bedrooms=1)
    rsp = requests.get(url_base, params=params)

    # print(rsp.url)

    loc_prefixes = ['gbs', 'bmw', 'nos', 'nwb', 'sob']

    html = BeautifulSoup(rsp.text, 'html.parser')
    # print(html.prettify()[:1000])

    apts = html.find_all('p', attrs={'class': 'result-info'})
    # print(len(apts))



    for this_appt in apts:


        size = this_appt.findAll(attrs={'class': 'housing'})[0].text
        # print(size)

        def find_size_and_brs(size):
            split = size.strip(' /- \n').split(' -\n')
            if len(split) == 2:
                n_brs = split[0].replace('br', '')
                this_size = split[1].replace('ft2', '')
            elif 'br' in split[0]:
                # It's the n_bedrooms
                n_brs = split[0].replace('br', '')
                this_size = np.nan
            elif 'ft2' in split[0]:
                # It's the size
                this_size = split[0].replace('ft2', '')
                n_brs = np.nan
            return float(this_size), float(n_brs)
        this_size, n_brs = find_size_and_brs(size)


        this_time = this_appt.find('time')['datetime']
        this_time = pd.to_datetime(this_time)
        try:
            this_price = float(this_appt.find('span', {'class': 'result-price'}).text.strip('$'))
        except AttributeError:
            this_price = 9999.99
        this_title = this_appt.find('a', attrs={'class': 'hdrlnk'}).text

        print("%s $%6.2f %s" % (this_time, this_price, this_title))




