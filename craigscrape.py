import pandas as pd

import numpy as np

import requests

from bs4 import BeautifulSoup

url_base = 'https://boston.craigslist.org/search/aap'
params = dict(bedrooms=1)
rsp = requests.get(url_base, params=params)

# print(rsp.url)

html = BeautifulSoup(rsp.text, 'html.parser')
# print(html.prettify()[:1000])

apts = html.find_all('p', attrs={'class': 'result-info'})
print(len(apts))

this_appt = apts[3]
print(this_appt.prettify())

size = this_appt.findAll(attrs={'class': 'housing'})[0].text
print(size)

def find_size_and_brs(size):
    split = size.strip(' /- ').split(' - ')
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
this_price = float(this_appt.find('span', {'class': 'price'}).text.strip('$'))
this_title = this_appt.find('a', attrs={'class': 'hdrlnk'}).text





