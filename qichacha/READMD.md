
# 企查查 反爬机制

- 非用户，限制search次数，超过search次数后，则必须登录后才能再次访问相关页面。
- search操作过于频繁，则会弹出验证码。
    - 即使控制search频率，仍然会遇见验证码。
- 验证码中包含文字图像验证。
  - 处理滑动不难，但从图像中识别汉字有难度。
- requests.get 无法获取到完整页面。
   - 分析页面代码，找到对应的信息的url；
   - 使用selenium；

## 预防反爬方法
- 随机useragent,用比较常见的几种，模拟真实场景，chrome，opera，firefox
- 代理ip pool
- 随机延迟数秒，拟人
- 创建多用户，变化使用用户cookies
- 结合selenium来规避验证码
    - 为selenium webdriver加cookies，是个很蛋疼的事情。找到为selenium webdriver加cookie的方法，要在add_cookies前使用webdriver.get()访问目标网站，不清楚为何。
    



```
代理IP 机制
def get_url(self,url=None,proxies=None):
    header = {
        'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection' : 'Keep-Alive',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
    for prox in proxies:
        try:
            r=requests.get(url,proxies=prox,headers=header)
            if r.status_code!=200:
                continue
            else:
                print "使用{0}连接成功>>".format(prox)
                return r.content
        except Exception, e:
            return None
```
