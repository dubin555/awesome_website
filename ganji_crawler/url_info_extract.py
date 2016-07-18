"""
__author__ = "DuBin"

Get the information from the detail url
"""

from bs4 import BeautifulSoup
import requests
import pymongo
from CONFIG import headers, proxy_list, config_logger_from
from multiprocessing import Pool
import logging

client = pymongo.MongoClient('localhost', 27017, connect=False)
table = client['ganji']
url_list = table["detail_url_list"]
item_info = table["item_info"]


def get_detail_info_from(url):
    """
        get the detail information : title, publish time, type, price and area
    of the thing, if no such type of information, put None into the database.
    """
    # time.sleep(1)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return
    except requests.exceptions.ConnectionError as e:
        # Maybe the url is not legel, so if the ConnectionError occur, just continue.
        print ("connection for {} failed ...".format(url))
        logging.warning("connection for %s failed ..." % url)
        return
    soup = BeautifulSoup(response.text, "html.parser")
    try:

        title = soup.select("#wrapper h1")[0].text if soup.select("#wrapper h1") else None
        pub_time = soup.select("#wrapper i.pr-5")[0].text.split()[0] if soup.select("#wrapper i.pr-5") else None
        types = soup.select(
            "#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(1) > span > a")
        type = types[0].text if types else None
        prices = soup.select(
            "#wrapper > div.content.clearfix > div.leftBox > div > div > ul > li > i.f22.fc-orange.f-type")
        price = prices[0].text if prices else None
        locations = soup.select(
            '#wrapper > div.content.clearfix > div.leftBox > div:nth-of-type(3) > div > ul > li:nth-of-type(3)')[
            0].find_all("a")
        area = locations[1].text if locations else None
        d = {
            "title": title,
            "publish_time": pub_time,
            "type": type,
            "price": price,
            "area": area
        }
    except AttributeError as e:
        # if cannot find the target attribute, continue
        print (e)
        print ("This page cannot be fully parsed {}".format(url))
        logging.warning("This page cannot be fully parsed %s" % url)
        return
    except IndexError as e:
        # if the attribute do not have the target index, continue
        print (e)
        print ("The element specified in the code is not correct {}".format(url))
        logging.warning("The Page %s element is not fully satisfy the statement" % url)
        return

    logging.info("Got one piece valid information %s " % str(d))
    item_info.insert_one(d)
    return


def crawl_item_info():
    """
    function to get detail information from the url_list stored in the database.
    Use multiprocess pool to accelerate the crawler.
    """
    config_logger_from("url_info_extract")
    full_url_lists = [url["url"] for url in url_list.find()]
    pool = Pool()
    pool.map(get_detail_info_from, full_url_lists)


if __name__ == "__main__":
    crawl_item_info()
