# -*- coding:utf-8 -*-

import re
import requests
from lxml import etree

import os
import csv
import random
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException


class QichachaCrawler(object):
    user_agents_path = "D:\\projects\\littlespider\\qichacha\\user_agents.txt"
    wrote_header = False

    # 搜索后获取公司信息的链接url， 公司名称，法定代表人名称， 成立时间， 电话，邮箱，地址，存续状态
    search_url = "https://www.qichacha.com/search?key="

    # 获得 官网地址
    company_base_url = "https://www.qichacha.com"

    # 获得 所属地区
    location_url_template = "https://www.qichacha.com/company_getinfos?unique={0}&companyname={1}&tab=base"
    # https://www.qichacha.com/company_getinfos?unique=7ad2a0791c09e4f3114998459073af3c&companyname="江苏阳生生物股份有限公司"&tab=base
    # business_info_url= "https://www.qichacha.com/company_getinfos?unique=heb94c770e65bf030fe82ff87a818115&companyname=ABCDE12345%20LIMITED&tab=base"

    cookie_set = (
    "PHPSESSID=ql6spb62iiqov0dipv8j7de833; UM_distinctid=160983ac2e9b3f-0ab2f5b884fb7e-b7a103e-1fa400-160983ac2ead79; zg_did=%7B%22did%22%3A%20%22160983ac2fc1e1-04f71ac82a9fe4-b7a103e-1fa400-160983ac2ff1fa%22%7D; _uab_collina=151438247814653212727998; acw_tc=AQAAAJ437kLX5wIAnD6MPakvAKPEopN2; hasShow=1; CNZZDATA1254842228=406624423-1514379896-https%253A%252F%252Fwww.google.com%252F%7C1514475409; _umdata=85957DF9A4B3B3E843111A17D5F9886AE383001B083F6046C28F3C2A6140E53525CC69A6C8E1BDE0CD43AD3E795C914C08D93F421B97AAA610DD30DC35EC986E; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201514478866549%2C%22updated%22%3A%201514480087779%2C%22info%22%3A%201514382476037%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%224e8aecdd470126768f3b704117e3b0ab%22%7D",
    "acw_tc=AQAAAILIHxiF2AMAmM1BceOk8dI9HmH6; PHPSESSID=c6g5umhkvtebp89qfugrg0pft3; UM_distinctid=160b0a92c6f4d3-00f16a353ad4848-4c322e7d-1fa400-160b0a92c7044b; CNZZDATA1254842228=2013502518-1514790652-%7C1514790652; zg_did=%7B%22did%22%3A%20%22160b0a92cce6fc-0b6c7e870ef498-4c322e7d-1fa400-160b0a92ccf4a2%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201514792365266%2C%22updated%22%3A%201514792388901%2C%22info%22%3A%201514792365269%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22d5c0308842912575c3c65ab026a7011f%22%7D; hasShow=1; _uab_collina=151479236667792434788809; _umdata=486B7B12C6AA95F23B1BC43ABC4B5F62E7E66AF68993418B321A7F2B0C2B5ADCB60C576716A050B6CD43AD3E795C914CD3FF998CF5CA0748A17DE72E2CB0ECB0",
    )

    cookie_dict = {
        "PHPSESSID": "ql6spb62iiqov0dipv8j7de833",
        "UM_distinctid":"160983ac2e9b3f-0ab2f5b884fb7e-b7a103e-1fa400-160983ac2ead79",
        "zg_did": "%7B%22did%22%3A%20%22160983ac2fc1e1-04f71ac82a9fe4-b7a103e-1fa400-160983ac2ff1fa%22%7D",
        "_uab_collina": "151438247814653212727998",
        "acw_tc":"AQAAAJ437kLX5wIAnD6MPakvAKPEopN2",
        "hasShow":"1",
        "CNZZDATA1254842228":"406624423-1514379896-https%253A%252F%252Fwww.google.com%252F%7C1514475409",
        "_umdata":"85957DF9A4B3B3E843111A17D5F9886AE383001B083F6046C28F3C2A6140E53525CC69A6C8E1BDE0CD43AD3E795C914C08D93F421B97AAA610DD30DC35EC986E",
        "zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f":"%7B%22sid%22%3A%201514478866549%2C%22updated%22%3A%201514480087779%2C%22info%22%3A%201514382476037%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%224e8aecdd470126768f3b704117e3b0ab%22%7D"
    }

    http_proxy_pool = (
                       "121.196.226.246:84",
                       "47.94.23.128:8888",
                       "116.199.2.209:82",
                       "116.199.2.210:80",
                       "67.216.209.241:80"
    )

    headers = {
        "Host": "www.qichacha.com",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "DNT": "1",
        "Referer": "http://www.qichacha.com/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
    }

    def __init__(self, session):
        self.session = session

    def update_session(self):
        self.session.proxies.update(self.get_proxies(isproxy=True))
        self.session.headers.update(self.get_headers(israndom=True))
        self.session.cookies.update(self.get_cookie())

    def get_proxies(self, isproxy=True):
        # proxies=proxies
        if not isproxy:
            return {}
        return {"http": random.choice(self.http_proxy_pool)}

    def get_headers(self, israndom=False):
        if israndom:
            useragents = []
            with open(self.user_agents_path, "rb") as uaf:
                for ua in uaf.readlines():
                    if ua:
                        useragents.append(ua.strip()[1:-1 - 1])
            self.headers['User-Agent'] = random.choice(useragents).decode('utf-8')
        return self.headers

    def get_cookie(self):
        cookies = {}
        length = len(self.cookie_set)
        idx = random.randint(0, length-1)
        for field in self.cookie_set[idx].split(";"):
            key, value = field.strip().split("=")
            cookies[key.strip()] = value.strip()
        return cookies

    def random_delay(self, mintime=0.5, maxtime=1.5):
        time.sleep(random.uniform(mintime, maxtime))

    def check_verify(self, page):
        url = []
        if page.xpath("//span[@id='nc_1_n1z']"):
            self.try_avoid_verify(url)

    def try_avoid_verify(self, url):
        try:
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(self.company_base_url+"/user_login")
            time.sleep(40)
            print( {str(cookie['name']): str(cookie['value']) for cookie in driver.get_cookies()})
            self.cookie_dict.update({str(cookie['name']): str(cookie['value']) for cookie in driver.get_cookies()})
            print(self.cookie_dict)
            driver.add_cookie(self.cookie_dict)
            driver.get(url)
            driver.implicitly_wait(5)
            fuck_slider = driver.find_element_by_xpath("//span[@id='nc_1_n1z']")
            ActionChains(driver).click_and_hold(fuck_slider).move_by_offset(268, 0).release().perform()
            fuck_btn = driver.find_element_by_xpath("//button[@type='submit']")
            ActionChains(driver).move_to_element(fuck_btn).click().perform()
        finally:
            driver.quit()

    def get_official_website(self, href):
        """
        获取官网地址
        :param href: 通常为/firm_3f603703d59a04cbe427e5825099a565.html
        :return:
        """
        s = self.session

        url = self.company_base_url+href
        rsp = s.get(url)
        html = etree.HTML(rsp.text)
        website = html.xpath("//span[contains(text(), '官网')]/parent::div/span[@class='cvlu']")
        if website:
            return website[0].xpath("string(.)").strip()
        else:
            return None

    def get_location(self, href, name):
        """
        直接用https://www.qichacha.com/firm_heb94c770e65bf030fe82ff87a818115.html是无法获取所属地址信息的，只有通过构造以下链接才可以所属地址信息。
        所属地址信息可能不存在。
        :param href: something like firm_heb94c770e65bf030fe82ff87a818115.html
        :param name: 公司名称
        :return: 公司所属地，或者None
        """
        s = self.session

        id = re.split(r'[_.]', href)[1]
        location_url = self.location_url_template.format(id, name)
        rsp = s.get(location_url)
        # with open("tmp.html", "w") as f:
        #     f.write(rsp.text)
        html = etree.HTML(rsp.text)
        location = html.xpath("//td[contains(text(), '所属地区')]/parent::tr/td[2]")
        if location:
            return location[0].xpath("string(.)").strip()
        else:
            return None

    def get_company_info(self, search_key, companytr):
        result = {"关键字": search_key}
        tds = companytr.xpath("./td")
        assert len(tds) == 3

        # 获得企业信息
        link_element = tds[1].xpath("./a")
        link_element = link_element[0]
        href = link_element.xpath("@href")[0].strip()
        company_name = link_element.xpath("string(.)").strip()
        result["公司名"] = company_name

        # 获得所属地
        result["所属地区"] = self.get_location(href, company_name)

        #  获得官网地址
        result['官网地址'] = self.get_official_website(href)

        # 获得法人代表、 股本、 成立时间、电话、邮箱、地址等信息
        basic_info = []
        for p in tds[1].xpath("./p"):
            basic_info.append(p.xpath("string(.)").strip())
        result["基本信息"] = basic_info

        #  获得企业状态
        result["公司状态"] = tds[2].xpath("string(.)").strip()
        return result

    def search_and_parse_first_page(self, search_key, num=1, companyfile="company.csv", notfoundfile="notfound.csv"):
        self.update_session()
        s = self.session
        search_result = s.get(self.search_url + search_key)
        html = etree.HTML(search_result.text)

        self.write_rsp_into_html(search_result.text)
        trs = html.xpath("//tbody/tr")

        if len(trs) == 0:
            result = {"关键字": search_key}
            print("rsp.text:   ", search_result.text)

            self.write_data_into_csv(notfoundfile, result)
            return
        for idx, tr in enumerate(trs):
            if idx >= num:
                break
            result = self.get_company_info(search_key, tr)
            self.write_data_into_csv(companyfile, result)

    def write_data_into_csv(self, filepath, result):
        with open(filepath, "a+") as csvfile:
            w = csv.DictWriter(csvfile, result.keys())
            if not self.wrote_header:
                w.writeheader()
                self.wrote_header = True
            w.writerow(result)

    def write_rsp_into_html(self, html):
        with open("tmp.html", "w") as f:
            f.write(html)

if __name__ == "__main__":
    pass
