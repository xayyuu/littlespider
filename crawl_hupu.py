#!/usr/bin/env python
# coding=utf-8

import os
import sys

import requests
from requests.exceptions import HTTPError
from lxml import etree


LOGINURL = "https://passport.hupu.com/login"
GOALURL = "https://bbs.hupu.com/bxj"
ACCOUNT = "kidult1107@126.com"
PASSWORD = os.environ.get("HUPUPASSWD")
COOKIES = " _dacevid3=be13bf24.7d0b.9f2b.cd50.205183df23fb; \
            __gads=ID=41162384d043251a:T=1500259740:S=ALNI_MbtMchjn0bWkdLa189R6swzIQRsDQ; \
            _HUPUSSOID=395f3e8e-1e87-4e98-9059-c083151a2f1a; \
            _fmdata=95ED791C7A9EF0498D1B4469C8552AD3472C92E203DF0B8429F5569E5686D09C5A3090AD9CA23E69806085FE7249527EB9BBD0AF9FFEA4F5; _CLT=918ebe7bb324d8673460f7af1d701a5c; \
            __dacevid3=0x596588adb413f8f9; __dacevst=86421b7d.738c3369|1503502431548; \
            u=18622660|5Yi65a2Q5Li55b+D|05f9|e30a155a53053139e9889b4e2c9a6440|53053139e9889b4e|5Yi65a2Q5Li55b+D; \
            us=5309feec1eb1606a298a6d84b0593bdbf8716c50950a0def1b51d4bce207fbd0872223607a7a8efa6257450686b3311cb4dc97246ee8d88d72ceb6a9c7f1c37c; \
            ua=24647552"
COOKIES2 = "_dacevid3=3ed3498d.71ba.e162.ac79.9c07e99d812d; __gads=ID=6a00903366af8ba9:T=1496638803:S=ALNI_MY7ItNzkOJHSIBrP4S4EusdB6OBbQ; _HUPUSSOID=d741abf6-876c-46be-ae35-020ed5850c2c; AUM=dg3y8190kJcqM2eCiQSwGyyXjN5nt-yqlWtWpTno5j7lw; PHPSESSID=ouahcf0kad2t54abg9a1f61mc7; __dacevid3=0x2ca13e7aae1aed5d; ipfrom=476fc8c0bc1ec45f611a1bc6e3ac2025%09Unknown; _fmdata=4A27D0679DAB552ED27BC5358D1540FA316382DA90E06A4B0532AACB9A8CC1D33EA41942F339C62C0291C0445FE9398B97EF5DC1A69C93BB; UM_distinctid=15e196a204a7-0d8a9b2e482525-764e2673-100200-15e196a204b31; Hm_lvt_3d37bd93521c56eba4cc11e2353632e2=1503664940; Hm_lpvt_3d37bd93521c56eba4cc11e2353632e2=1503664940; lastvisit=8491%091503665912%09%2Fthread.php%3Fboardname%3Dbxj; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1503628598,1503632220,1503632409,1503632750; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1503665915; _cnzz_CV30020080=buzi_cookie%7C3ed3498d.71ba.e162.ac79.9c07e99d812d%7C-1; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18622660|5Yi65a2Q5Li55b+D|05f9|e30a155a53053139e9889b4e2c9a6440|53053139e9889b4e|5Yi65a2Q5Li55b+D; ua=24650264; us=8903d08cd9458a729710ed0185c5a2d9cacaea355f4d500e948674eeba8b73dc67a45a9fe0fae25351db88bd655cecb56a21ff470123a4198d3f1f524537b1a1; __dacevst=a1ab4c63.3f41d609|1503668041127"


def get_cookies(cookies=COOKIES):
    result = {}
    if not cookies:
        return result

    cookies = [data.strip().split("=") for data in cookies.split(";")]
    assert len(cookies) > 0  and len(cookies[0]) == 2

    for data in cookies:
        result[data[0]] = data[1]

    return result


def get_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "DNT":   "1",
        "Host":    "passport.hupu.com",
        "Referer": "https://passport.hupu.com/pc/login?project=bbs&from=pc",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0"
    }


def login():
    auth = (ACCOUNT, PASSWORD)
    r = requests.get(GOALURL, headers = get_headers(), auth=auth, cookies=get_cookies(COOKIES2))
    try:
        r.raise_for_status()
    except HTTPError as why:
        print "cookies:\n{0}\n".format(get_cookies())
        print "headers:\n{0}\n".format(get_headers())
        print why, "\n"
        return

    page = etree.HTML(r.content)
    islogin = page.xpath("//ul[@class='hasLogin']")
    if not islogin:
        print "\nLogin FAILED!!!!!!!!\n"
        return

    font = page.xpath("//font[@color='red']")
    if not font:
        print "\nACCESS KFQ FAILED\n"
        return

    print("\nLOGIN SUCCESS\n")


def navigation(url, session):
    pass


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    login()



# csdn 流水号
# LT-2297214-oRywt1EBS137NchFB6SafltbigeLeM
# LT-2298784-cTNihQtAxBEghcChv1NUYf0q2XGA6L
# LT-2297132-Jdf1rueQNk7xVNZMVxcnpjOK9jWUhV
# LT-2297243-zLqgale5ow2wZ2AUsDbyoMSeg1XFAw