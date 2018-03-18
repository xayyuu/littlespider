#!/usr/bin/env python
#-*- utf-8 -*-

import requests
import pymongo

def get_headers(cookies):
    default_headers = {
                        'Connection':'keep-alive',
                        'Content-Length':'38',
                        'Pragma':'no-cache',
                        'Cache-Control':'no-cache',
                        'Accept':'application/json, text/javascript, */*; q=0.01',
                        'Origin':'http://ggfw.gdhrss.gov.cn',
                        'X-Requested-With':'XMLHttpRequest',
                        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
                        'Content-Type':'application/x-www-form-urlencoded',
                        'DNT':'1',
                        'Referer':'http://ggfw.gdhrss.gov.cn/gwyks/center.do',
                        'Accept-Encoding':'gzip, deflate',
                        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
                        'Cookie':'JSESSIONID=RI42_fh_zNNRCVM-2bLOJ8lAxGPtR0bU6ibj1ZyEpmdrKM5SC8Ci!-1453701390'
    }

    default_headers.update({'Cookie':cookies})
    return default_headers

def build_data(areacode, pagenum, when="201801", rownum=50):
    return {
              'bfa001':when,
              'bab301':areacode,
              'page':pagenum,
              'rows':rownum
     }
    

def get_row_data(cookies, areacode="01", pagenum=1):
    headers = get_headers(cookies)
    payload = build_data(areacode, pagenum)  

    print(headers, payload)

    url = "http://ggfw.gdhrss.gov.cn/gwyks/exam/details/spQuery.do"
    rsp = requests.post(url, headers=headers, data=payload)
    print(rsp.text)


if __name__ == "__main__":
    cookies="JSESSIONID=Xow3b6XOOBn3GlG6-O5VLNWHNHRb8BQPWra0aNX5IOqldFhCeDzE!2012375495"
    get_row_data(cookies)


