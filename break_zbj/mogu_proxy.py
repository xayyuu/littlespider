#!/usr/bin/env python
# coding=utf-8
import requests
import random
import json


def get_api(filename="api.txt"):
    with open(filename, "r") as f:
        api = f.read()
    return api.strip()

def get_random_proxy_ip():
    api = get_api()
    print(api)
    rsp = requests.get(api)
    ip_list = rsp.json()
    ip_list = ip_list['msg']
    idx = random.randint(0, len(ip_list)-1)
    ip ={"http": "http://"+ip_list[idx]["ip"]+":"+ip_list[idx]["port"]} 
    print("Using ip: ", ip)
    return ip

