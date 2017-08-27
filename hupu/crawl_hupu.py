#!/usr/bin/env python
# coding=utf-8

import os
import sys
from hashlib import md5

import requests
from requests.exceptions import HTTPError
from lxml import etree

LOGINURL = 'https://passport.hupu.com/pc/login/member.action'
ACCOUNT = "kidult1107@126.com"
PASSWORD = os.environ.get("MYPASSWD")

PREFIXURL = "https://bbs.hupu.com"



def get_headers():
    return {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0",
        "Cookie": "_HUPUSSOID=c1401fb2-c638-4cf7-a7df-c0be12c7d072; _CLT=918ebe7bb324d8673460f7af1d701a5c; _dacevid3=35330dcc\
.95c1.8199.ec5c.7d2a14d1a3e1; AUM=dgtjwpyFcE2tV9cL-tM3ETdHjN5nt-yqlWtWpTno5j7lw; u=18622660|5Yi65a2Q5Li55b\
+D|05f9|e30a155a53053139e9889b4e2c9a6440|53053139e9889b4e|5Yi65a2Q5Li55b+D; us=4256ba43783844f8bde7a\
8cb3937328ea3bc75a2293dc98a9f6aa73458413f3d7777781f6825e2fdcf1c83b1e884bb15db609c3925350bd7304a5d8fbc2325c7\
; ua=24652471; __dacevst=6752836d.533edebb|1503802533883"
    }


def get_login_session():

    s = requests.session()
    s.headers.update(get_headers())

    # 目前通过帐号密码登录还不通，暂时直接通过手动登录后复制cookies直接访问
    # payload = {"username": ACCOUNT, "password": md5(PASSWORD).hexdigest()}
    # r = s.post(LOGINURL, data=payload)
    #

    return s


def verifyaccess(session, url, expectxpath):
    if not isinstance(url, str) or not url.startswith("http"):
        print("url format is WRONG, pls check it")
        return

    rsp = session.get(url)
    page = rsp.content

    with open("tryaccess.html", "w") as f:
        f.write(page)

    html = etree.HTML(page)
    verifyicon = html.xpath(expectxpath)
    if verifyicon:
        print("access {0} SUCCESS".format(url))
        return True
    else:
        print("access {0} FAILED".format(url))
        return False


def get_content(page, f):
    html = etree.HTML(page)
    f.wirte()


def get_kfq_highlights(pagenum=5):
    s = get_login_session()
    seperate_line = "".join(("\n","-"*16, "\n"))
    try_access = "".join((PREFIXURL, "/kfq/highlights"))
    if verifyaccess(s, try_access, "//div[@class='l_w_reply']"):
        for i in range(1, pagenum+1):
            try_access = try_access + "-" + str(i)
            rsp = s.get(try_access)
            with open('highlights.txt', 'a') as f:
                f.write(seperate_line)
                get_content(rsp.content, f)
                f.write(seperate_line)
        print("ok")


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    get_kfq_highlights()