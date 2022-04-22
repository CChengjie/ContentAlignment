import csv

import requests
import random
import os
import re
import json
import threading
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import pandas as pd
from bs4 import BeautifulSoup
#from count import clean_data, write_csv
#from utils import get_proxy_session, extract_github_url, get_http_proxy
from urllib.request import urlretrieve

# ������б�
EXTERNAL_PROXIES = [
    "124.112.174.237:8080",
    "36.63.83.215:8888",
    "49.88.148.249:8888",
    "115.153.8.6:8080",
    "113.241.137.248:8080",
    "218.7.116.103:9999",
    "122.140.5.115:9999",
    "117.66.167.24:9999",
    "114.103.176.45:8888",
    "58.55.252.58:8080",
    "218.1.201.136:8888",
    "113.101.96.66:8080",
    "140.250.152.1:8888"
]


def get_http_proxy():
    random_proxy = random.choice(EXTERNAL_PROXIES)
    http_proxy = "http://{0}:{1}@{2}".format(os.getenv('HTTP_USER'), os.getenv('HTTP_PWD'), '127.0.0.1:7890')
    #print(http_proxy)
    return http_proxy


def get_proxy_session() -> requests.Session:
    session = get_default_session()
    session.proxies = {'https': get_http_proxy()}
    return session


def get_default_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.verify = False
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/86.0.4240.75 Safari/537.36'
    return session


def search_google(keyword: str):
    session = get_proxy_session()
    res = session.get("https://www.google.com/search?q={}".format(keyword))
    return res


# https://github.com/vuejs/vue-loader
# https://webcache.googleusercontent.com/search?q=cache:ANtseYv-KsYJ:https://github.com/vuejs/vue-loader+&cd=1&hl=en&ct=clnk&gl=uk
# /search?q=related:https://github.com/vuejs/vue-loader+vue-loader&sa=X&ved=2ahUKEwi_zZ3G1oTwAhWUXsAKHdFRDtEQHzAAegQIBhAJ
# https://github.com/vuejs/vue-loader/issues
# https://github.com/vuejs/vue-loader/releases
# https://github.com/vuejs/vue-loader/pulls
# https://github.com/vuejs/vue-loader/blob/master/.npmignore
def extract_github_url(url: str):
    return re.findall('github.com/[^/&+]+/[^/&+]+', url)

def write_csv(path, row=None):
    with open(path, 'a+', newline='')as csvfile:
        write = csv.writer(csvfile)
        write.writerow(row)
        csvfile.close()