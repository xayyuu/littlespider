#!/usr/bin/env python
import time
import requests
import os


template_url="http://resource.gaofi.cn/ebook/book_1410/pn_{pagenum}"


if __name__ == "__main__":
    #generate_url()
    headers = {
                "Host":"resource.gaofi.cn",
                "Connection":"keep-alive",
                "Pragma":"no-cache",
                "Cache-Control":"no-cache",
                "Upgrade-Insecure-Requests":"1",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "DNT":"1",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
                "Cookie":"UM_distinctid=1629f1511ae274-081813090e1f1c-b34356b-1fa400-1629f1511af94f; book_3160.curPage=0; book_1410.curPage=11; Hm_lvt_7e9fdf937bb3ab79260969006251185f=1523087382,1523087551; Hm_lpvt_7e9fdf937bb3ab79260969006251185f=1523087593"
             }

    min = 1 
    max = 312

    for i in range(min, max+1):
        url = template_url.format(pagenum=i)
        print(url)
        try:
            rsp = requests.get(url, headers=headers)
            imgname = str(i) + ".jpg"
            if rsp.status_code == 200:
                print("downloading ", imgname)
                open(imgname, 'wb').write(rsp.content)
        except:
            pass

        time.sleep(2)

