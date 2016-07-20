# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import time

class CrawlFail(Exception):
    pass

def get_item_urls(url_enterence):
    response = requests.get(url_enterence)
    if response.status_code != 200:
        raise CrawlFail("crawl for 58.com, failed, please check")
    soup = BeautifulSoup(response.text)
    target_urls = soup.select("#infolist > table > tbody > tr > td.t > a")
    return [url.get("href") for url in target_urls
            if url.get("href") and "zhuanzhuan" not in url.get("href")]


def get_item_info(url):
    time.sleep(1)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text)
    labels = soup.select("#header > div.breadCrumb.f12 > span:nth-of-type(3) > a")
    titles = soup.select("#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.mainTitle > h1")
    publish_times = soup.select("#index_show > ul.mtit_con_left.fl > li.time")
    prices = soup.select("#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(1) > div.su_con > span")
    areas = soup.select("#content > div.person_add_top.no_ident_top > div.per_ad_left > div.col_sub.sumary > ul > li:nth-of-type(3) > div.su_con > span")

    d = {
        "label" : labels[0].get_text() if len(labels) >= 1 else "",
        "title" : titles[0].get_text() if len(titles) >= 1 else "",
        "time" : publish_times[0].get_text() if len(publish_times) >= 1 else "",
        "price" : prices[0].get_text() if len(prices) >= 1 else ""
        }
    if len(areas) >= 1:
        d["area"] =  " ".join([e.get_text() for e in areas[0].find_all("a")])
    else:
        d["area"] = ""
    return d

if __name__ == "__main__":
    url_enterence = "http://bj.58.com/pbdn/0/"
    urls =  get_item_urls(url_enterence)
    for url in urls:
        print (get_item_info(url))
