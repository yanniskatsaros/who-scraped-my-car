"""
Various miscellaneous functions and utilities helpful
in common web scraping tasks used in this project.
"""
import time
import random
import json
from typing import Union, Optional, List, Dict
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urlencode

USER_AGENTS_BASE_URL = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

# path information
SRC_PATH = Path(__file__).parent.resolve()
CARS_PATH = SRC_PATH / 'static' / 'cars.json'
USER_AGENTS_PATH = SRC_PATH / 'static' / 'user-agents.txt'

def download_car_codes() -> List[Dict[str, str]]:
    """
    Downloads and parses a list of all available car make codes
    from Autotrader.com
    """
    response = requests.get(
        'https://autotrader.com',
        headers={
            'User-Agent': DEFAULT_USER_AGENT
        }
    )
    response.raise_for_status()
    
    # extracts the make codes from the dropdown list
    soup = BeautifulSoup(response.text, 'html.parser')
    options: List[Tag] = (
        soup
        .find('select', 'form-control')
        .find('optgroup', label='All Makes')
        .find_all('option')
    )
    return [{'name': t.text, 'code': t['value']} for t in options]

def load_car_codes() -> List[Dict[str, str]]:
    with open(CARS_PATH, 'r') as f:
        codes = json.load(f)

    return codes

def download_user_agents(n: int) -> List[str]:
    """
    Downloads a list of the top `n` most common
    browser user agents.
    """
    results: List[str] = []
    # the website only has 12 pages of entries
    for i in range(1, 12):
        # sleep between requests to be nice to their servers
        time.sleep(random.randint(1, 5))
        print(f'Downloading user agents, page: {i}')

        url = f'{USER_AGENTS_BASE_URL}/{i}'
        response = requests.get(
            url,
            headers={
                'User-Agent': DEFAULT_USER_AGENT
            }
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        agents = [td.text for td in soup.find_all('td', 'useragent')]
        results.extend(agents)
    
    return results[0:n]

def urlbuilder(base: str, **kwargs: Union[str, int]) -> str:
    """
    Construct a URL from a base URL and query parameters
    provided as keyword arguments.
    
    Parameters
    ----------
    base: str
        The base URL (https://example.com)
        
    **kwargs: Union[str, int]
        The query search parameters
        
    Returns
    -------
    str
    """
    # copy to avoid mutation
    if not base.endswith('?'):
        _base = f'{base}?'
    _base = f'{base}'
    
    return f'{_base}{urlencode(kwargs)}'

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Download static files required by project'
    )
    parser.add_argument('--user-agents', action='store_true', dest='user_agents')
    parser.add_argument('--car-makes', action='store_true', dest='car_makes')
    args = parser.parse_args()

    if args.user_agents:
        n = 1000
        print(f'Downloading the top {n} browser user-agents to: static/user-agents.txt')
        agents = download_user_agents(n)
        with open(USER_AGENTS_PATH, 'w') as f:
            for a in agents:
                f.write(f'{a}\n')

    if args.car_makes:
        # downloads all the car make names and codes
        print('Downloading car make names and codes to: static/cars.json')
        codes = download_car_codes()
        with open(CARS_PATH, 'w') as f:
            json.dump(codes, f, indent=2)
