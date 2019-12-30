#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""
appium操作雷电模拟器，登陆淘宝
"""
from appiumpake import leidiansimulatorusage, AppiumTaobaoCrawler
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
import time, pymysql, re




class AppiumCrawler():
    def __init__(self, udid, username, passworld):
        self.flag = True

        self.mysqlconn = pymysql.connect(

        )
        self.cur = self.mysqlconn.cursor()

        self.caps = {
            "platformName": "Android",
            "platformVersion": "5.1.1",
            "udid": udid,
            "deviceName": udid,
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
        self.username = username
        self.passworld = passworld
        insertsql = 'INSERT INTO appiumtable_test (username, passworld, udid) VALUES("{}", "{}", "{}")'.format(self.username, self.passworld, udid)
        try:
            self.cur.execute(insertsql)
            self.mysqlconn.commit()
        except Exception as E:
            print("数据插入失败：", E)




    #登录授权
    def authorization(self):
        try:
            consent1 = self.driver.find_element_by_id("com.taobao.taobao:id/welcom_dialog_checkbox")
            if consent1:
                consent1.click()
        except NoSuchElementException:
            print("--------------")

        try:
            consent2 = self.driver.find_element_by_id("com.taobao.taobao:id/uik_mdButtonDefaultPositive")
            if consent2:
                consent2.click()
        except NoSuchElementException:
            print("----------------------------------------")

        self.updatespk()




    #不允许访问位置
    def notalow(self):
        try:
            location = self.driver.find_element_by_id("com.taobao.taobao:id/uik_mdButtonDefaultNegative")
            if location:
                location.click()
        except NoSuchElementException:
            print("----------------------------------------")




    #不允许下载更新
    def updatespk(self):
        if self.flag:
            print("--------------是否更新--------------")
            time.sleep(3)
            try:
                notupdate = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.RelativeLayout[1]/android.widget.TextView")
                if notupdate:
                    notupdate.click()
                    self.flag = False
            except NoSuchElementException:
                print("----------------------------------------")




    #点击“我的淘宝”
    def clickMyself(self):
        while True:
            try:
                self.updatespk()
                time.sleep(2)
                myselfbut = WebDriverWait(self.driver, 10).until(lambda x:x.find_element_by_xpath("//android.widget.FrameLayout[@content-desc=\"我的淘宝\"]/android.widget.FrameLayout/android.widget.ImageView"))
                if myselfbut:
                    myselfbut.click()
                    break
            except:
                print("点击我的淘宝重试")




    #点击其他用户登录
    def clickother(self):
        while True:
            try:
                try:
                    time.sleep(2)
                    otheruser = WebDriverWait(self.driver, 3).until(lambda x:x.find_element_by_id("com.taobao.taobao:id/switchLogin"))
                    if otheruser:
                        otheruser.click()
                        break
                except TimeoutException:
                    print("--------------新用户--------------")
                    break
            except AttributeError:
                print("点击其他用户重试")




    # 点击登录
    def clicklogin(self):
        while True:
            self.updatespk()
            ellogbot = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/ali_user_guide_account_login_tv"))
            if ellogbot:
                ellogbot.click()
                break




    #点击用户名输入框并输入用户名
    def InputUsername(self, username):
        while True:
            try:
                try:
                    self.updatespk()
                    elusername = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/accountCompleteTextView"))
                    print(elusername)
                    if elusername:
                        elusername.click()
                        time.sleep(2)
                        elusername.send_keys(username)
                        break
                except AttributeError:
                    print("输入用户名重试")
            except Exception as E:
                print("输入用户名重试")




    #点击密码输入框并输入密码
    def inputPwd(self, passworld):
        while True:
            try:
                self.updatespk()
                elpwd = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/content"))
                print(elpwd)
                if elpwd:
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
                self.updatespk()
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
                try:
                    slidertap = WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_accessibility_id(""))
                    print(slidertap)
                    TouchAction(self.driver).press(slidertap).move_to(x=720, y=354).perform()
                    break
                except TimeoutException:
                    getback = WebDriverWait(self.driver, 10).until(
                        lambda x: x.find_element_by_id("com.taobao.taobao:id/title_bar_back_button"))
                    print(getback)
                    if getback:
                        getback.click()
                    self.inputPwd(passworld)
                    self.loginclick()
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

    # 获取淘气值
    def GetNaughtyValue(self):
        time.sleep(3)
        while True:
            try:
                NaughtyValueTag = WebDriverWait(self.driver, 3).until(
                    lambda x: x.find_element_by_id("com.taobao.taobao:id/tv_vip_score"))
                print(NaughtyValueTag)
                if NaughtyValueTag:
                    NaughtyValue = re.findall("淘气值 (.*)", NaughtyValueTag.text)[0]
                    return NaughtyValue
            except:
                print("获取淘气值重试")




    #查询订单
    def SearchOrder(self):
        while True:
            try:
                AllOrder = WebDriverWait(self.driver, 3).until(
                    lambda x: x.find_element_by_id("com.taobao.taobao:id/card_subtitle_name"))
                if AllOrder:
                    AllOrder.click()
                    time.sleep(2)
                    break
            except TimeoutException:
                print("点击所有订单重试")




    #点击订单搜索框
    def ClickSearch(self):
        while True:
            order = input("请输入订单号>>>>>>")
            if order == "quit":
                break
            while True:
                try:
                    try:
                        searchinput = WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_xpath("//android.webkit.WebView[@content-desc=\"订单列表\"]/android.view.View[2]/android.view.View[1]/android.view.View[1]/android.widget.EditText"))
                        if searchinput:
                            searchinput.click()
                            time.sleep(3)
                            print(order)
                            searchinput.send_keys(order)
                            time.sleep(2)
                            break
                    except TimeoutException:
                        print("输入订单重试")
                except:
                    print("输入订单重试")
            # 点击搜索按钮
            while True:
                try:
                    searchbut = WebDriverWait(self.driver, 3).until(
                        lambda x: x.find_element_by_accessibility_id("搜索"))
                    if searchbut:
                        searchbut.click()
                        break
                except TimeoutException:
                    print("点击搜索按钮重试")
            # 获取订单状态
            StatusName = None
            statusnum = 1
            while True:
                statusname = ["交易成功", "交易关闭", "卖家已发货"]
                for i in statusname:
                    try:
                        OrderStatus = self.driver.find_element_by_accessibility_id("{}".format(i))
                        if OrderStatus:
                            OrderStatus.get_attribute("name")
                            StatusName = i
                            break
                    except Exception as e:
                        continue
                if StatusName:
                    print("订单状态为：", StatusName)
                    self.driver.back()
                    break
                if statusnum > 5:
                    break
                statusnum += 1




    #启动函数
    def main(self):
        self.authorization()                                #登录授权
        time.sleep(3)
        self.notalow()                                      #点击未知授权
        self.clickMyself()                                  #点击我的淘宝
        self.updatespk()
        self.clickother()                                   #点击其他用户登录
        print("--------------点击登录--------------")
        self.clicklogin()                                   #点击登陆

        print("--------------输入用户--------------")
        self.InputUsername(self.username)                   #点击用户名输入框

        print("--------------输入密码--------------")
        self.inputPwd(self.passworld)                       #点击密码输入框

        print("--------------点击登陆--------------")
        self.loginclick()                                   #点击登陆按钮

        print("--------------滑块验证--------------")
        self.Slide_the_slider(passworld)                    #滑块验证
        print("--------------取淘气值--------------")
        NaughtyValue = self.GetNaughtyValue()
        print("--------------查订单号--------------")
        self.SearchOrder()
        self.driver.back()
        self.SearchOrder()
        self.ClickSearch()



def main(username, passworld):
    starttime = time.time()
    udid = leidiansimulatorusage.Dnconsole().main()
    print(udid)
    AppiumCrawler(udid, username, passworld).main()
    endtime = time.time()
    print("程序耗时：", endtime - starttime, "秒")




if __name__ == '__main__':
    username = input("请输入用户名>>>>>>>")
    passworld = input("请输入密码>>>>>>>>")
    main(username, passworld)