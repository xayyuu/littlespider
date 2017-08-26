# 知识点
- 为什么使用session？
session可以保持连接状态。http本身属于无链接的协议，因此，对于一些需要登录验证的网站，在登录后访问某些资源（如网页等），都需要携带经过认证的cookies，也就是在每次使用requests时候，都需要在get方法后面加上cookies参数，稍显琐碎。总而言之，session提供了跨链接访问方式，使得服务器可以识别出多个链接属于同一个用户访问，从而在此基础上做相关的一些操作，比如记录用户的购物记录，记录用户的登录信息等等。
在csdn登录中，我刚开始没有使用session，每次都需要手动在get方法后面加入cookies参数，很繁琐。

- 学习分析网站登录过程。   
每个网站的登录方式可能不一样，通过学习csdn登录的方法，了解到这个过程。所以使用requests库来登录网站，关键在于分析出网站的登录方式，并模拟。


# 困难
- lt流水号。   
刚开始并不清除csdn的登录方式，以为使用帐号密码就可以登录，但是不行。然后使用firebug和tamper data来了解csdn登录过程，发现post数据中需要有一个lt号。然而并不清楚这个lt号从哪里来，看了资料才得知这个lt号隐藏在上一次get请求返回的html页面中。
找到lt，然后发送，仍然失败，原来对应的lt号需要对应的cookies才能生效，因此获取lt时，同时需要获取对应的cookies，并且在post时一起发送。

- 不理解session工作机制。



# 参考资料
- http://cn.python-requests.org/zh\_CN/latest/user/advanced.html
> 从这里面学了session的一些用法


- https://bblove.me/2015/05/23/python-requests-login-csdn-blog/
> 从这里学了csdn的登录方式，以及分析登录过程的插件firebug、tamper data 用法。

- HTTP权威指南

