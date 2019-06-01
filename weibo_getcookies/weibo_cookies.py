# coding=utf-8

import redis
import time
import json
from selenium import webdriver
from weibo_getcookies.yundama import verify_captcha
from weibo_getcookies.redis_config import *


r = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,db=REDIS_DB,charset=CHARSET)

num = 1     # 重试次数

def redis_save(r,cookie):

    cookies = json.dumps(cookie)
    try:
        r.lpush(REDIS_KEY_NAME, cookies)
        print('cookies数据保存成功!')
    except:
        print('重试')
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset=CHARSET)
        r.lpush(REDIS_KEY_NAME, cookies)
        print('cookies数据保存成功!')

    print('redis库中含有数据',r.llen(REDIS_KEY_NAME))
    print('-'*50)

def input_click_yzm(driver,user,password):
    global num
    try:
        driver.find_element_by_xpath('//*[@id="SI_Top_Login"]/a/i').click()
        driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[2]/input').send_keys(user)
        driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[3]/input').send_keys(password)
        print('账号 >>> {}'.format(user))
        time.sleep(2)

        driver.delete_all_cookies()

        # 如果出现验证码的图片链接
        yzm_img = driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/img').get_attribute('src')
        if yzm_img:
            # 点击刷新 以免出现网络问题没有加载出来,等待一秒等待jizai在出来对验证码元素截图
            driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/a[1]').click()
            time.sleep(2)
            driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/img').screenshot(
                'captcha.jpg')
            
            # 云打码
            uis, yzm = verify_captcha('captcha.jpg', 1004)
            driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/input').send_keys(yzm)
            driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[6]/span/a').click()

            time.sleep(1)
            # 如果出现验证码错误,不断验证,成功break出来进行下一步,错误3次之后登记失败账号break出来 else 登录失败
            while num:
                if '输入的验证码不正确' in driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/p').text:
                    print('第 {} 次验证码重试中'.format(num))
                    time.sleep(1)
                    driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/img').screenshot(
                        'captcha.jpg')
                    uis, yzm = verify_captcha('captcha.jpg', 1004)
                    driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[4]/input').send_keys(yzm)
                    driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[6]/span/a').click()

                    num += 1
                elif num == 4:
                    num = 1
                    with open('weibo_error.text','a')as f:
                        f.write(user+'----'+password )
                        f.write('\n')
                    break
                else:
                    break
            num = 1

            time.sleep(3)
            print('登录等待3秒 加载用户信息')

            user_name = driver.find_element_by_xpath('//*[@id="SI_Top_Nick_Name"]')
            if user_name:
                print('用户登录成功')

                cook = [x['name'] + '=' + x['value'] for x in driver.get_cookies()]
                cookie = '; '.join(item for item in cook)
                redis_save(r, cookie)

            else:
                print('登录失败')

        # 没有验证码直接登录
        else:
            driver.find_element_by_xpath('//*[@id="SI_Top_LoginLayer"]/div/div[2]/ul/li[6]/span/a').click()
            time.sleep(3)
            print('登录等待3秒 加载用户信息')

            user_name = driver.find_element_by_xpath('//*[@id="SI_Top_Nick_Name"]')  #
            if user_name:
                print('用户登录成功')

                cook = [x['name'] + '=' + x['value'] for x in driver.get_cookies()]
                cookie = '; '.join(item for item in cook)
                redis_save(r, cookie)

    except:
        print('出错了')
    finally:
        driver.quit()
'''
如果有必要可以试试导入
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

我没有试过,不确定这种模可不可以使用点击元素和screenshot截图,有空后来在可以试试
'''
if __name__ == '__main__':
    with open('weibozhanhao.txt')as f:
        for i in f.readlines():
            userinfo = i.strip().split('----')
            user = userinfo[0]
            password = userinfo[-1]

            # user = 'efbkrkrlnswoi-fzf742@yahoo.com'
            # password = 'UJgnvnlonaj'

            url = 'https://www.sina.com.cn/'
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(8)

            input_click_yzm(driver,user,password)
