#!/usr/bin/env python
# coding=utf-8
# 爬取猪八戒网站
import time
import codecs
import copy
import requests
import lxml
from lxml import etree
import time
import random
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from shutil import copyfile
import os


basedir='/home/ubuntu/projects/littlespider/break_zbj/results/'  # 临时的
#basedir=os.getenv("RESULTPATH")
# 延迟时间 
min_time = 2.0 # s
max_time = 4.0 


area_code = {"广州": "3493", "深圳": "3510", "佛山": "3498"}

catalog_code = {
                "软件开发": "rjkf", 
                "APP开发": "ydyykf", 
                "IT解决方案": "itfangan",
                "软件/SAAS": "saas",
                "微信开发": "wxptkf",
                "技术服务": "jsfwzbj",
                "研究开发": "yjkfzbj"
                }

first_page_url_template="http://www.zbj.com/{catalog}/pd{area}.html"
url_template="http://www.zbj.com/{catalog}/pd{area}k{pagenum}.html"

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get("http://www.zbj.com/home/p.html")
cookies = list(map(lambda c: c["name"] + "=" + c["value"], browser.get_cookies()))
cookie = "; ".join(cookies)
#print(cookie)
browser.close()

headers={
        "Host":"www.zbj.com",
        "Connection":"keep-alive",
	#"Pragma":"no-cache",
	"Cache-Control":"no-cache",
	"Upgrade-Insecure-Requests":"1",
	"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
	"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate",
	"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
        "DNT": "1",
        "Cookie": cookie
        }

def transform_headers(headers, **kw):
    tmp = copy.deepcopy(headers)
    tmp.update(kw)
    return tmp

def save_url(url_set):
    client = MongoClient('localhost', 27017)
    db = client['zhubajie']
    collection = db['shopurl']
    for _url in url_set:
        print("saving url: ", _url)
        collection.insert({"url": _url})

def get_total_page_num(text):
    """  从html中找出总页数"""
    dom = etree.HTML(text)
    spans = dom.xpath("//span[@class='ui-minipaging-pagenum']")
    if len(spans) == 1:
        span = spans[0]
        pagenum_list = span.xpath("string(.)").split("/")
        assert(len(pagenum_list) == 2)
        pagenum = pagenum_list[1].strip()
    else: pagenum = 0
    return int(pagenum)


def get_child_urls(text):
    """ 从html中找到所有的子链接, 返回列表"""
    dom = etree.HTML(text)
    hrefs = dom.xpath("//div[@class='service-provider-wrap j-service-provider-wrap ']/div//a[@class='shop-name text-overflow']/@href")
    child_url = ["http:"+href for href in hrefs]
    print(child_url)
    return child_url


def aggregate_url(catalog, area, size=40):
    """ 根据不同区域，不同类别，找到相似的一类url地址集合 
        catalog: 行业分类代码 area:  地区代码 """
    first_page_url = first_page_url_template.format(catalog=catalog, area=area)
    rsp = requests.get(first_page_url, headers=headers)
    pagenum = get_total_page_num(rsp.text)
    url_cluster = set()
    urls = get_child_urls(rsp.text)  # 第一页也要获取其所有子链接
    url_cluster.update(urls)
    #print(url_cluster)
    for i in range(1, pagenum):
        print("aggregate url......", i)
        pagenum_suffix = i*size
        url = url_template.format(catalog=catalog, area=area, pagenum=pagenum_suffix) 
        rsp = requests.get(url, headers=headers)
        urls = get_child_urls(rsp.text)
        url_cluster.update(urls)
        time.sleep(random.uniform(min_time, max_time)) # 避免访问过于频繁
    return url_cluster

def transform_url(url):
    """ 转换url，让其变成档案首页的url"""
    """ url示例: http://shop.zbj.com/17054627/ """
    assert isinstance(url, str)
    salerinfo_url=url+"salerinfo.html"
    spec_headers=transform_headers(headers, Host="shop.zbj.com")
    try:
        rsp = requests.get(salerinfo_url, headers=spec_headers, timeout=1)
        dom = etree.HTML(rsp.text)
        hrefs = dom.xpath("//iframe[contains(@src, 'ucenter.zbj.com/rencai')]/@src")
    except:   # 处理不了异常
        save([url], basedir+"failurl.txt")
        return None, None
    hrefs_length = len(hrefs)
    if hrefs_length >= 1:
        url_type = "ucenter"  # 普通会员
        target_url = "http:"+hrefs[0]
    else:
        url_type = "tianpeng"  # 天蓬网会员
        target_url = salerinfo_url
    
    return target_url, url_type

def extract_info(page, url_type="ucenter"):
    """ 提取企业信息，包括 企业名，企业地址，企业自我介绍"""
    def get_info_func(lst):
        try:
            return lst[0].xpath("string(.)").strip()
        except IndexError:
            return "NONE"

    dom = etree.HTML(page)
    if url_type == "ucenter":
        company_name = get_info_func(dom.xpath("//span[@class='user-tit fl']"))  # 找到公司名字
        area = get_info_func(dom.xpath("//span[@class='fr active-address']"))  # 找到公司地址
        about = get_info_func(dom.xpath("//span[@class='about']"))  # 找到公司介绍
    else:  # "tianpeng"
        company_name = get_info_func(dom.xpath("//p[@class='introduce-company-title']"))
        about = get_info_func(dom.xpath("//p[@class='introduce-company-msg']"))
        area = get_info_func(dom.xpath("//div[@class='company-info-container']//dd"))
    return (company_name, area, about) 

def process_url(url):
    """ 这个函数需要加入随机事件等待，避免被屏蔽  """
    url, url_type = transform_url(url)
    if url_type == "tianpeng":
        spec_headers=transform_headers(headers, Host="shop.zbj.com")
    elif url_type == "ucenter":
        spec_headers=transform_headers(headers, Host="ucenter.zbj.com")
    else:  # 异常处理
        return ()
    rsp = requests.get(url, headers=spec_headers)
    time.sleep(random.uniform(min_time, max_time)) # 避免访问过于频繁
    print("now process url: ", url)
    company_info = extract_info(rsp.text, url_type)
    return company_info

def save(info, filename="text.txt"):
    """ info 是 元组类型 """
    with codecs.open(filename, 'a', 'utf-8') as f:
        for _info in info:
            f.write(_info)
            f.write(" "*8)
        f.write("\n")
    

if __name__ == "__main__":
#    # 保存url 
#    for catalogcode in catalog_code.values():
#        for areacode in area_code.values():
#            urls = aggregate_url(catalogcode, areacode)
#            save_url(urls)
    
    client = MongoClient()
    db = client["zhubajie"]
    collection = db["shopurl"]
    
    filename=basedir+'all.txt'
    ts = str(int(time.time()))
    newfile=filename+"."+ts
    copyfile(filename, newfile)  # backup the result
    open(filename, 'w').close() # emtpy the file

    # 处理单个url
    filename = basedir+"all.txt"
    for _url in collection.find():
         info = process_url(_url['url'])
         info = info + (_url['url'],)  # add url into info(which is a tuple)
         save(info, filename)

