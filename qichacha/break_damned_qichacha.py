# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.webdriver.common.by import By

import time
from urllib.parse import quote
import csv
import random
import re
import sys
import common
from common import wait_for_element, write_data_into_input, is_element_present, screenshot
import unittest
import os
import random
import pickle
import requests
import xlwt
import time
from tempfile import TemporaryFile

# global var
separator = " " * 4


class BreakIntoDamnedQichacha(object):
    index_url = "https://www.qichacha.com"
    login_url = "https://www.qichacha.com/user_login"
    search_url = "http://www.qichacha.com/search?key="
    username = "xxxxxxxxxxx"
    password = "xxxxxxxxx"

    def __init__(self, options=None):
        self.options = options

    def __enter__(self):
        if self.options is not None:
            driver = webdriver.Chrome(chrome_options=self.options)
        else:
            driver = webdriver.Chrome()
        self.driver = driver
        self.driver.maximize_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def load_driver_cookies(self, file="cookies.pkl"):
        driver = self.driver
        driver.get(self.index_url)
        driver.delete_all_cookies()
        with open(file, 'rb') as pkl:
            cookies = pickle.load(pkl)
        for cookie in cookies:
            self.driver.add_cookie(cookie)

    def dump_driver_cookies(self, file="cookies.pkl"):
        """
        login and dump cookies
        cookies example
        cookies = [
        	{'domain': 'www.qichacha.com', 'httpOnly': True, 'name': 'acw_tc', 'path': '/', 'secure': False, 'value': 'AQAAAD/sO3YKSAkAQRw+Or0ZC/l59qyK'},
        	{'domain': '.qichacha.com', 'expiry': 1546412771, 'httpOnly': False, 'name': 'zg_did', 'path': '/', 'secure': False, 'value': '%7B%22did%22%3A%20%22160b5b0fe432ff-00763755f4cedc-5c1b3517-1fa400-160b5b0fe44459%22%7D'},
        	{'domain': 'www.qichacha.com', 'expiry': 1830236763, 'httpOnly': False, 'name': '_uab_collina', 'path': '/', 'secure': False, 'value': '151487676354893897660017'},
        	{'domain': 'www.qichacha.com', 'expiry': 1514919971, 'httpOnly': False, 'name': 'hasShow', 'path': '/', 'secure': False, 'value': '1'},
        	{'domain': '.qichacha.com', 'expiry': 1530601563, 'httpOnly': False, 'name': 'UM_distinctid', 'path': '/', 'secure': False, 'value': '160b5b0fe313ab-0e02e8c949d5f6-5c1b3517-1fa400-160b5b0fe322b4'},
        	{'domain': 'www.qichacha.com', 'expiry': 1515481570.366184, 'httpOnly': False, 'name': 'PHPSESSID', 'path': '/', 'secure': False, 'value': 'nivf3hah9730r4e0k68b9q7cn1'},
        	{'domain': 'www.qichacha.com', 'expiry': 1546412765, 'httpOnly': False, 'name': '_umdata', 'path': '/', 'secure': False, 'value': '0712F33290AB8A6D6919B4B8EEAE8991AA096FEFBA8941BC2FB0688E110CE1E1FEFB77CAE9271967CD43AD3E795C914C2AC5467951C63486B17A0EE323AED9B2'},
        	{'domain': '.qichacha.com', 'expiry': 1546412771, 'httpOnly': False, 'name': 'zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f', 'path': '/', 'secure': False, 'value': '%7B%22sid%22%3A%201514876763720%2C%22updated%22%3A%201514876771029%2C%22info%22%3A%201514876763724%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%224e8aecdd470126768f3b704117e3b0ab%22%7D'},
            {'domain': 'www.qichacha.com', 'expiry': 1530601571, 'httpOnly': False, 'name': 'CNZZDATA1254842228', 'path': '/', 'secure': False, 'value': '1744144506-1514871419-%7C1514871419'}
        ]

        """
        driver = self.driver
        driver.delete_all_cookies()
        driver.get(self.login_url)
        username_input = wait_for_element(driver, (By.XPATH, "//input[@name='nameNormal']"))
        password_input = wait_for_element(driver, (By.XPATH, "//input[@name='pwdNormal']"))
        write_data_into_input(driver, username_input, self.username)
        write_data_into_input(driver, password_input, self.password)
        fuck_slider = wait_for_element(driver, (By.XPATH, "//span[@id='nc_1_n1z']"))
        action = ActionChains(driver)
        action.click_and_hold(fuck_slider)
        action.move_by_offset(308, 0)
        action.release().perform()
        time.sleep(10)
        cookies = driver.get_cookies()
        with open(file, 'wb') as pkl:
            pickle.dump(cookies, pkl)

    @staticmethod
    def read_csv_into_list(path):
        if not path or path is None:
            return []

        commany_list = []
        with open(path, 'r', encoding="utf-8") as csvfile:
            company_reader = csv.reader(csvfile)
            for row in company_reader:
                if len(row) > 0:
                    commany_list.append(row[0].strip())  # row[0] 公司名称
        return commany_list

    @staticmethod
    def delaytime(mintime=1.5, maxtime=4):
        return time.sleep(random.uniform(mintime, maxtime))

    @staticmethod
    def export_info_to_csv(info, name):
        """

        :param info: [[]] list's list
        :param name:
        :return:
        """
        with open(name, 'a', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            for fragment in info:
                f_csv.writerow(fragment)
            f.flush()

    def find_all_company_info_about_keyword(self, paths):
        driver = self.driver
        for path in paths:
            keywords = self.read_csv_into_list(path)
            csvfile = "".join(["company", time.strftime("%Y%m%d%H%M%S", time.localtime()), ".csv"])
            for keyword in keywords:
                search_page_url = "".join((self.search_url, keyword))
                driver.get(search_page_url)
                self.delaytime(mintime=15, maxtime=20)

                links = []
                while common.is_element_present(driver, By.XPATH, "//a[@id='ajaxpage' and text()='>']"):
                    try:
                        search_result = wait_for_element(driver, (By.XPATH, "//section[@id='searchlist']//tr//a[@class='ma_h1']"), eager=True)
                        # 根据搜索条件获得多个链接，然后解析每个链接，获得信息
                        for url in search_result:
                            links.append(url.get_attribute("href"))
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 拉倒页面底部，才能点击跳转按钮
                        common.click(driver, (By.XPATH, "//a[@id='ajaxpage' and text()='>']"), presleep=3, postsleep=3)
                    except (NoSuchElementException, common.WaitForElementException):
                        pass

                info = []  # list'list
                for link in links:
                    fragment = self.parse_url(link)
                    info.append(fragment)
                    self.delaytime(mintime=5, maxtime=8)
                self.export_info_to_csv(info, csvfile)

    @screenshot
    def find_company_info_by_input(self, paths):
        for path in paths:
            companies = self.read_csv_into_list(path)
            csvfile = "".join(["company", time.strftime("%Y%m%d%H%M%S", time.localtime()), ".csv"])
            for company in companies:
                self.search_company(company)
                info = self.get_info_by_company_name(company, num=3)
                self.export_info_to_csv(info, csvfile)
                self.delaytime()

    def search_company(self, name):
        driver = self.driver
        # search company
        driver.get(self.index_url)
        wait_for_element(driver, (By.XPATH, "//input[@id='searchkey']")).send_keys(name)
        common.click(driver, (By.XPATH, "//input[@id='V3_Search_bt']"))

    def get_info_by_company_name(self, name, num=1):
        driver = self.driver
        info = []  # list'list

        try:
            search_result = wait_for_element(driver, (By.XPATH, "//section[@id='searchlist']//tr//a[@class='ma_h1']"), eager=True)
            # 根据搜索条件获得多个链接，然后解析每个链接，获得信息
            links = []
            for idx, url in enumerate(search_result):
                if idx >= num:
                    break
                links.append(url.get_attribute("href"))
            for link in links:
                fragment = [name + separator]
                fragment += self.parse_url(link)
                info.append(fragment)
                self.delaytime(mintime=2, maxtime=4)
        except (NoSuchElementException, common.WaitForElementException):
            note = "Can not find any info with {}".format(name)
            print(note)
            fragment = [name + separator, note]
            info.append(fragment)
        return info

    @staticmethod
    def find_text_from_element(origin, locator, hint=None):
        try:
            return wait_for_element(origin, locator, timeout=1).text
        except (NoSuchElementException, common.WaitForElementException):
            return "Can not find {0}".format(hint)

    def parse_url(self, link_url):
        fragment = []
        driver = self.driver
        if not link_url:
            raise NoSuchElementException

        driver.get(link_url)

        company_top_box = wait_for_element(driver, (By.XPATH, "//div[@id='company-top']"))

        title = self.find_text_from_element(company_top_box, (By.XPATH, "//div[@class='row title']"), "公司名及状态")
        fragment.append(title + separator)

        phone = self.find_text_from_element(company_top_box, (By.XPATH, "//span[contains(text(), '电话')]/../span[@class='cvlu']"), "手机号")
        fragment.append(phone + separator)

        website = self.find_text_from_element(company_top_box, (By.XPATH, "//span[contains(text(), '邮箱')]/parent::div/span[@class='cvlu'][1]"), "官网")
        fragment.append(website + separator)

        email = self.find_text_from_element(company_top_box, (By.XPATH, "//span[contains(text(), '邮箱')]/parent::div/span[@class='cvlu'][2]"), "电子邮箱")
        fragment.append(email + separator)

        address = self.find_text_from_element(company_top_box, (By.XPATH, "//a[contains(@id, 'mapPreview')]"), "地址")
        fragment.append(address + separator)

        person_name = self.find_text_from_element(driver, (By.XPATH, "//a[contains(@class, 'bname')]"), "法人代表")
        fragment.append(person_name + separator)

        location = self.find_text_from_element(driver, (By.XPATH, "//td[contains(text(), '所属地区')]/parent::tr/td[2]"), "所属地区")
        fragment.append(location + separator)

        print(fragment)
        return fragment


class BreakQichachaCase(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        prefs = {'profile.managed_default_content_settings.images': 2}
        options.add_experimental_option('prefs', prefs)
        self.options = options

    def tearDown(self):
        pass

    def _test_load_driver_cookies(self):
        with BreakIntoDamnedQichacha(options=self.options) as mycrawler:
            mycrawler.load_driver_cookies()
            print(mycrawler.driver.get_cookies())
            mycrawler.driver.get("http://www.qichacha.com/search?key=asdf")
            self.assertTrue(mycrawler.driver.find_element_by_xpath("//a[@href='/firm_6402b5cedc2ad62491df77a55a520bf0.html']").text.strip() == 'asdf')

    def _test_dump_driver_cookies(self):
        with BreakIntoDamnedQichacha(options=None) as mycrawler:
            mycrawler.dump_driver_cookies()
            print(mycrawler.driver.get_cookies())

    def _test_find_company_info_by_input_gui(self):
        # paths = ["D:\\projects\\tianyancha_selenium\\meibo.csv", "D:\\projects\\tianyancha_selenium\\weibo.csv"
        paths = ["D:\\projects\\tianyancha_selenium\\weibo.csv"]
        with BreakIntoDamnedQichacha(options=None) as mycrawler:
            mycrawler.load_driver_cookies()
            mycrawler.find_company_info_by_input(paths)

    def _test_find_company_info_by_input_cmd(self):
        # paths = ["D:\\projects\\tianyancha_selenium\\meibo.csv", "D:\\projects\\tianyancha_selenium\\weibo.csv"
        paths = ["D:\\projects\\tianyancha_selenium\\weibo.csv"]
        with BreakIntoDamnedQichacha(options=self.options) as mycrawler:
            mycrawler.load_driver_cookies()
            print(mycrawler.driver.get_cookies())
            mycrawler.find_company_info_by_input(paths)

    def test_find_all_company_info_about_keyword_gui(self):
        paths = [".\\keywords.csv"]
        with BreakIntoDamnedQichacha(options=None) as mycrawler:
            mycrawler.load_driver_cookies()
            mycrawler.find_all_company_info_about_keyword(paths)


if __name__ == "__main__":
    unittest.main()
