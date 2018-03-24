#!/usr/bin/env python
# coding=utf-8
import requests
import random
import json


def get_api(filename="api.txt"):
    with open(filename, "r") as f:
        api = f.read()
    return api.strip()

def get_random_proxies():
    """ 每次返回30个代理ip """
    api = get_api()
    #print(api)
    rsp = requests.get(api)
    ip_list = rsp.json()
    ip_list = ip_list['msg']
    proxies = []
    for elem in ip_list:
        proxies.append({"http": "http://"+elem["ip"]+":"+elem["port"]})
    return proxies

