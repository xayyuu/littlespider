import unittest
import requests
import sys
sys.path.append("..")

from qichacha.main import *


class QichachaCase(unittest.TestCase):
    def setUp(self):
        self.session = requests.Session()
        self.crawler = QichachaCrawler(self.session)

    def tearDown(self):
        self.session.close()

    def atest_search_and_parse_first_page(self):
        with open("company.csv", "w") as f:
            pass
        with open("notfound.csv", "w") as f:
            pass
        self.crawler.search_and_parse_first_page("百度")
        self.crawler.search_and_parse_first_page("大红袍zxcvsadfqa")

    def _test_get_location(self):
        self.crawler.update_session()
        result = self.crawler.get_location("firm_3f603703d59a04cbe427e5825099a565.html", "百度在线网络技术（北京）有限公司")
        self.assertTrue(result == "北京市")

    def _test_get_website(self):
        self.crawler.update_session()
        result = self.crawler.get_official_website("/firm_98c5dc7bbebb2c94db67a071a0d49325.html")
        print(result)

    def ctest_crawl_weiya(self):
        with open("weiya.csv", "r+", encoding='utf-8') as f:
            i = 1
            for name in f.readlines():
                name = name.strip()
                print(i, name)
                self.crawler.search_and_parse_first_page(name, companyfile="weiya_company_info.csv", notfoundfile="weiya_404.csv")
                self.crawler.random_delay()
                i += 1

    def ctest_crawl_weibo(self):
        with open("meibo.csv", "r+", encoding='utf-8') as f:
            i = 1
            for name in f.readlines():
                name = name.strip()
                print(i, name)
                self.crawler.search_and_parse_first_page(name, companyfile="meibo_company_info.csv", notfoundfile="meibo_404.csv")
                self.crawler.random_delay()
                i += 1

    def test_selenium(self):
        self.crawler.try_avoid_verify("http://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E4%B8%8A%E6%B5%B7%E5%A5%A5%E8%B4%9D%E4%BC%A6%E8%B4%B8%E6%98%93%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8")
        # self.crawler.try_avoid_verify("http://www.qichacha.com/user_login")


if __name__ == "__main__":
    unittest.main()
