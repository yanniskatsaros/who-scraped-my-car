"""
A quick hacky-sack prototype to download listings from Autotrader.com
"""
import argparse
import logging
import time
import random
import json
from math import ceil
from typing import Union, Optional, List, Dict

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from utils import DEFAULT_USER_AGENT, urlbuilder, load_car_codes

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

BASE_URL = 'https://www.autotrader.com/cars-for-sale/searchresults.xhtml?'
LISTINGS_PER_PAGE = 100

def download_links(car_code: str, zip_code: int, search_radius: int, limit: Optional[int]) -> Optional[List[str]]:
    log = logging.getLogger('main.download_links')

    # start with the first page
    params = {
        'makeCodeList': car_code,
        'zip': zip_code,
        'searchRadius': search_radius,
        'sortBy': 'relevance',
        'numRecords': LISTINGS_PER_PAGE,
        'firstRecord': 0
    }
    url = urlbuilder(BASE_URL, **params)
    log.debug(f'Downloading: {url}')

    response = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT})
    soup = BeautifulSoup(response.text, 'html.parser')

    # begin by inferring the total number of pages that need to be searched
    total_results = int(soup
        .find('div', 'results-text-container')
        .text.split('Results')[0]
        .strip().split(' ')[-1]
    )
    pages = ceil(total_results / LISTINGS_PER_PAGE)

    # get the links for the current (first) page
    try:
        listings: List[Tag] = (soup
            .find('div', {'data-qaid': 'cntnr-listings-tier-listings'})
            .find_all('script', {'data-cmp': 'lstgSchema'})
        )
    except AttributeError:
        return None

    data: List[Dict] = [json.loads(t.contents[0]) for t in listings]
    links: List[str] = [d['url'] for d in data]

    # loop through the remaining pages
    for i in range(1, pages + 1):
        # relax the interval between consecutive requests to avoid bans
        time.sleep(random.randint(2, 5))

        # paginate by 100 records at a time
        params['firstRecord'] = 100 * i
        url = urlbuilder(BASE_URL, **params)
        log.debug(f'Downloading: {url}')
    
        response = requests.get(url, headers={'User-Agent': DEFAULT_USER_AGENT})
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            listings: List[Tag] = (soup
                .find('div', {'data-qaid': 'cntnr-listings-tier-listings'})
                .find_all('script', {'data-cmp': 'lstgSchema'})
            )
        # reached a page with no more entries
        except AttributeError:
            return list(set(links))

        data: List[Dict] = [json.loads(t.contents[0]) for t in listings]
        links.extend([d['url'] for d in data])

    # remove any duplicates if they exist due to repeated
    # entries from promoted/ad listings
    return list(set(links))

if __name__ == '__main__':
    log = logging.getLogger('main.main')
    car_codes = load_car_codes() 

    parser = argparse.ArgumentParser(
        description=(
            'Download car listings for a given car make, '
            'within a certain radius of a given ZIP code'
        )
    )
    parser.add_argument(
        'car_code',
        choices=[x['code'] for x in car_codes],
        help='A code representing the car make'
    )
    parser.add_argument(
        'zip_code',
        type=int,
        help='ZIP code of the area to search listings for'
    )
    parser.add_argument(
        '--search-radius',
        dest='search_radius',
        type=int,
        default=100,
        help='A search radius (in miles) within the given ZIP code'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        dest='limit',
        help='Limit the total number of entries to search for'
    )
    args = parser.parse_args()

    links = download_links(
        car_code=args.car_code,
        zip_code=args.zip_code,
        search_radius=args.search_radius,
        limit=args.limit
    )
    for link in links:
        print(link)