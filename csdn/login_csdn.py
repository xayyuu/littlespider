#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import requests
from lxml import etree


def getlt(session, url):
    r = session.get(url)
    page = r.text

    html = etree.HTML(page)
    lt = html.xpath("//input[@name='lt']")[0]

    return lt.get("value")


def login_success(session, verify_url, expect_element):
    if session is None or url is None or expect_element is None:
        return False

    rsp = session.get(verify_url)

    page = rsp.content
    # print page
    html = etree.HTML(page)
    if html.xpath(expect_element):
        return True
    else:
        return False


def login(url, verify_url, expect_element, *args):
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0"})

    # data which will be post
    username, password, execution, _eventid = args

    # get lt's id, which need by the post data. It's the csdn's login feature.
    lt = getlt(s, url)

    post_data = {"username": username, "password": password, "lt": lt, "execution": execution, "_eventId": _eventid}

    # send data
    r = s.post(url, data=post_data)

    # verify login status
    if login_success(s, verify_url, expect_element):
        print "Login SUCCESS"
    else:
        print "Login FAILED! SO SAD!"

if __name__ == "__main__":
    # login info
    url = "http://passport.csdn.net/account/login"
    verify_url = "http://my.csdn.net/my/mycsdn"
    expect_element = "//a[@href='/kidult1107']"
    data = ("kidult1107@126.com", os.environ.get("MYPASSWD"), "e1s1", "submit")

    login(url, verify_url, expect_element, *data)
