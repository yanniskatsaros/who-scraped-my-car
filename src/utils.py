"""
Various miscellaneous functions and utilities helpful
in common web scraping tasks used in this project.
"""
# common user agents
# https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser/1
# TODO download top 500-1000 most common user agents

import time
import random
from typing import Union, Optional, List, Dict

import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from urllib.parse import urlencode

USER_AGENTS_BASE_URL = 'https://developers.whatismybrowser.com/useragents/explore/software_type_specific/web-browser'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

def get_car_make_codes() -> List[Dict[str, str]]:
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

def get_user_agents(n: int) -> List[str]:
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
    import json

    # downloads all the car make names and codes
    print('Downloading car make names and codes to: static/cars.json')
    codes = get_car_make_codes()
    with open('static/cars.json', 'w') as f:
        json.dump(codes, f, indent=2)

    top_n_agents = 1000
    print(f'Downloading the top {top_n_agents} browser user-agents to: static/user-agents.txt')
    agents = get_user_agents(top_n_agents)
    with open('static/user-agents.txt', 'w') as f:
        for a in agents:
            f.write(f'{a}\n')
