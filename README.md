# python-selenium_weibo_cookies


只是用selenium和redis来进行一个微博cookies的获取并进行验证,并不需要使用flask,web啥的端口来进行

---------------------------------------------------------------------------------------
主程序是 
weibo_cookies 登录新浪网获取cookies
使用selenium点击网页上的元素进行登录,验证码使用selenium的screenshot功能,在使用云打码进行验证



redis_config 是配置文件

rm_redis 使用配置文件链接redis进行删除该db数据库中的REDIS_KEY_NAME数据

weibo_cookies_yanzhen 验证cookies是否有用,验证网站是个人设置页面

weibozhanhao.txt 是weibo账号

yundama  云打码,需要设置一下用户名和密码,以及打码类型

-------------------------------------------------------------------------------------

from selenium.webdriver.chrome.options import Options

chrome_options = Options()


chrome_options.add_argument('--headless')


chrome_options.add_argument('--disable-gpu')


driver = webdriver.Chrome(chrome_options=chrome_options)


