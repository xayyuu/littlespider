#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree
import sys


baseurl =  "http://www.csdn.net"


def get_geek_info(islog=False):
    rsp = requests.get(baseurl)
    page = rsp.content
    rsp.raise_for_status()

    html = etree.HTML(page)
    if html is None:
        print "Nothing in RESPONSE'S HTML'"
        print page
        return

    geek_elements = html.xpath("//div[@class='left']/div[1]//li/a")
    if islog:

        with open("csdn_geek_info.txt", "a") as f:
            f.write("{:^18}{:^18}\n".format("Title", "Link"))

            for element in geek_elements:
                f.write("{title},{link}\n".format(title=element.get('title'), link=element.get('href')))

            f.write("\n")

    else:

        print "{:^8}{:^18}\n".format("Title", "Link")
        for element in geek_elements:
            print "{title},{link}\n".format(title=element.get('title'), link=element.get('href'))
        print "\n"


if __name__ == "__main__":
    reload(sys) 
    sys.setdefaultencoding('utf-8')  # set to utf-8 codec
    get_geek_info(True)

