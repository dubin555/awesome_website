'''
Get the url from the beginning url.
'''

from bs4 import BeautifulSoup
import requests
import re
import time
from USER_AGENT import headers, proxy_list
from multiprocessing import Pool
from functools import partial
import pymongo
import random

clinet = pymongo.MongoClient('localhost', 27017, connect=False)
table = clinet["ganji"]
url_list = table["detail_url_list"]

# get proxy_list from http://cn-proxy.com/
def get_proxy_list(url):
    response = requests.get(url, headers = headers)
    print(response)
    soup = BeautifulSoup(response.text)
    ips = soup.select("tr > td")
    for ip in ips:
        print(ip)



def _get_ganji_channel(enter_url = "http://www.bj.ganji.com/wu/"):
    '''
    Get all the channels from the enter_url.
    return a list containing all the available channels.
    '''
    base_url_pattern = re.compile(r'(.*?\.com)')
    base_url_match = base_url_pattern.search(enter_url)
    if base_url_match:
        base_url = base_url_match.group(1)
    else:
        raise KeyError("enter url {} is not endswith '.com' ".format(enter_url))
    res = []
    # choose a proxy from the proxy list
    proxies = {'http': random.choice(proxy_list)}
    response = requests.get(enter_url, headers = headers)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "html.parser")
    contexts = soup.select("#wrapper > div.content")
    print(contexts)
    if not contexts[0].find_all("a"):
        raise KeyError("Page not roaded correctly")
    for i in contexts[0].find_all("a"):
        res.append(base_url + i.get("href"))
    print(res)
    return res


def _get_detail_url_from(channel, i):
    '''
    Looking for the detail url in target channel.
    Put the url in the database within range of page from i to 100
    '''
    i = i
    while i < 100:
        time.sleep(5)
        target_url = channel + "o{}".format(i)
        print("***** looking for url ---", target_url)
        try:
            #proxies = {'http':random.choice(proxy_list)}
            response = requests.get(target_url, headers = headers)
        except requests.exceptions.ConnectionError as e:
            print("Connection for {} failed ...".format(target_url))

            return _get_detail_url(channel, i)
        soup = BeautifulSoup(response.text, "html.parser")
        urls = soup.select("#wrapper > div.leftBox > div.layoutlist > dl > dt > a")
        # Check if it is the last page base on the count of the result
        if len(urls) < 20:
            return
        for url in urls:
            detail_url = url.get("href")
            if "zhuanzhuan" not in detail_url:
                url_list.insert_one({"url":detail_url})
                print(detail_url)
        i += 1
    return



def extract_detail_url_from_channels():
    '''
    Get the detail url from all the channels
    Use multiprocess Pool to accelerate it.
    '''
    channels = _get_ganji_channel()
    pool = Pool()
    # get all the detail url start from 1
    pool.map(partial(_get_detail_url_from, i = 1), channels)
    pool.close()
    pool.join()
    return


if __name__ == "__main__":
    extract_detail_url_from_channels()