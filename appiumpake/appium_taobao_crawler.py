#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""
appium操作淘宝，获取关键字搜索排名
"""
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
import time




class AppiumCrawler():
    def __init__(self):
        self.caps = {
            "platformName": "Android",
            "platformVersion": "5.1.1",
            "udid": "emulator-5558",
            "deviceName": "emulator-5558",
            "appPackage": "com.taobao.taobao",
            "appActivity": "com.taobao.tao.welcome.Welcome",
            "unicodeKeyboard": True,
            "resetKeyboard": True,
            "dontStopAppOnReset": True,
            "autoGrantPermissions": True,
            "noReset": True,
            "automationName": "uiautomator2",
            "newCommandTimeout": "36000"
        }
        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", self.caps)




    #点击“我的淘宝”
    def clickMyself(self):
        time.sleep(2)
        WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_xpath("//android.widget.FrameLayout[@content-desc=\"我的淘宝\"]/android.widget.FrameLayout/android.widget.ImageView")).click()




    #点击其他用户登录
    def clickother(self):
        while True:
            try:
                time.sleep(2)
                otheruser = WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_id("com.taobao.taobao:id/switchLogin"))
                if otheruser:
                    otheruser.click()
                    break
            except AttributeError:
                print("点击其他用户重试")




    # 点击登录
    def clicklogin(self):
        while True:
            ellogbot = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/ali_user_guide_account_login_tv"))
            if ellogbot:
                ellogbot.click()
                break




    #点击用户名输入框并输入用户名
    def InputUsername(self, username):
        while True:
            try:
                elusername = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/accountCompleteTextView"))
                print(elusername)
                if elusername:
                    elusername.click()
                    time.sleep(2)
                    elusername.send_keys(username)
                    break
            except AttributeError:
                print("输入用户名重试")




    #点击密码输入框并输入密码
    def inputPwd(self, passworld):
        while True:
            try:
                elpwd = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/content"))

                if elpwd:
                    print(elpwd)
                    elpwd.click()
                    time.sleep(2)
                    elpwd.send_keys(passworld)
                    break
            except AttributeError:
                print("输入密码重试！")




    #点击登陆按钮
    def loginclick(self):
        while True:
            try:
                loginbot = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('com.taobao.taobao:id/loginButton'))
                if loginbot:
                    loginbot.click()
                    break
            except AttributeError:
                print("获取登录按钮重试")




    #滑块验证
    def Slide_the_slider(self, passworld):
        print("开始滑块验证")
        while True:
            try:
                time.sleep(3)
                slidertap = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_accessibility_id(""))
                print(slidertap)
                TouchAction(self.driver).press(slidertap).move_to(x=720, y=354).perform()
                break
            except NoSuchElementException:
                getback = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/title_bar_back_button"))
                print(getback)
                if getback:
                    getback.click()
                self.inputPwd(passworld)
                self.loginclick()



    #获取屏幕尺寸大小
    def get_size(self, driver: WebDriver = None):
        driver = driver or self.driver
        if not driver:
            return driver

        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        return [x, y]



    #滑动屏幕
    def swipe_up(self, driver: WebDriver = None, _time: int = 1000):
        driver = driver or self.driver
        if not driver:
            return driver
        try:
            size = self.get_size(driver)
            x1 = int(size[0] * 0.5)  # 起始x坐标
            y1 = int(size[1] * 0.75)  # 起始y坐标
            y2 = int(size[1] * 0.5)  # 终点y坐标
            driver.swipe(x1, y1, x1, y2, _time)
            return True
        except:
            return False



    #启动函数
    def main(self, username, passworld):
        self.clickMyself()                                  #点击我的淘宝
        self.clickother()                                   #点击其他用户登录
        self.clicklogin()                                   #点击登陆
        self.InputUsername(username)                        #点击用户名输入框
        self.inputPwd(passworld)                            #点击密码输入框
        self.loginclick()                                   #点击登陆按钮
        self.Slide_the_slider(passworld)                    #滑块验证




if __name__ == '__main__':
    username = input("请输入用户名>>>>>>>")
    passworld = input("请输入密码>>>>>>>>")
    starttime = time.time()
    AppiumCrawler().main(username, passworld)
    endtime = time.time()
    print("程序耗时：", endtime-starttime, "秒")