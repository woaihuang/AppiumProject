#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



"""
appium操作雷电模拟器，抓取淘宝信息
"""
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
from appiumpake import leidiansimulatorusage
import time, re





class CrawlerTaobao():
    def __init__(self, index):
        leidiansimulatorusage.Dnconsole().launch(index)

        while True:
            flag = leidiansimulatorusage.Dnconsole().is_running(1)
            if flag:
                break

        self.caps = {
            "platformName": "Android",
            "platformVersion": "5.1.1",
            "udid": "emulator-5556",
            "deviceName": "emulator-5556",
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




    # 点击“我的淘宝”
    def clickMyself(self):
        time.sleep(2)
        while True:
            try:
                WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//android.widget.FrameLayout[@content-desc=\"我的淘宝\"]/android.widget.FrameLayout/android.widget.ImageView")).click()
                break
            except:
                print("点击我的淘宝重试")




    #获取淘气值
    def GetNaughtyValue(self):
        time.sleep(3)
        while True:
            try:
                NaughtyValueTag = WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/tv_vip_score"))
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
                AllOrder = WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_id("com.taobao.taobao:id/card_subtitle_name"))
                if AllOrder:
                    AllOrder.click()
                    time.sleep(2)
                    break
            except TimeoutException:
                print("点击所有订单重试")




    #点击订单搜索框
    def ClickSearch(self):
        order = input("请输入订单号>>>>>>")
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
        #点击搜索按钮
        while True:
            try:
                searchbut = WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_accessibility_id("搜索"))
                if searchbut:
                    searchbut.click()
                    break
            except TimeoutException:
                print("点击搜索按钮重试")
        #获取订单状态
        StatusName = None
        statusnum = 1
        while True:
            statusname = ["交易成功", "交易关闭", "卖家已发货", "充值成功"]
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
                return StatusName
            if statusnum > 5:
                break
            statusnum += 1



    #启动函数
    def main(self):
        time.sleep(3)
        print("--------------点击我的淘宝--------------")
        self.clickMyself()
        print("--------------获取淘气值--------------")
        NaughtyValue = self.GetNaughtyValue()
        print("--------------查询订单--------------")
        self.SearchOrder()
        print("--------------获取订单状态--------------")
        self.ClickSearch()




if __name__ == '__main__':
    index = input("请输入模拟器编号>>>>>")
    CrawlerTaobao(index).main()







