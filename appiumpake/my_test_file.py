#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-



from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from appium import webdriver
import os, time, pymysql



class DnPlayer(object):
    def __init__(self, info: list):
        super(DnPlayer, self).__init__()
        # 索引，标题，顶层窗口句柄，绑定窗口句柄，是否进入android，进程PID，VBox进程PID
        self.index = int(info[0])
        self.name = info[1]
        self.top_win_handler = int(info[2])
        self.bind_win_handler = int(info[3])
        self.is_in_android = True if int(info[4]) == 1 else False
        self.pid = int(info[5])
        self.vbox_pid = int(info[6])

    def is_running(self) -> bool:
        return self.is_in_android

    def __str__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (index, name, twh, bwh, r, pid, vpid)

    def __repr__(self):
        index = self.index
        name = self.name
        r = str(self.is_in_android)
        twh = self.top_win_handler
        bwh = self.bind_win_handler
        pid = self.pid
        vpid = self.vbox_pid
        return "\nindex:%d name:%s top:%08X bind:%08X running:%s pid:%d vbox_pid:%d\n" % (index, name, twh, bwh, r, pid, vpid)



class Dnconsole:
    # 请根据自己电脑配置
    console = 'D:\\Changzhi\\dnplayer2\\dnconsole.exe '
    ld = 'D:\\Changzhi\\dnplayer2\\ld.exe '
    share_path = 'C:\\Users\\Administrator\\Documents\\雷电模拟器\\Pictures'

    def __init__(self, index):
        self.index = index
        self.mysqlconn = pymysql.connect(
            host='120.27.147.99',
            user="root",
            password="Root_12root",
            database="python_taobao_demo",
            charset='utf8'
        )
        self.cur = self.mysqlconn.cursor()

        selectsql = "SELECT udid FROM appiumtable_test WHERE id={}".format(index)
        try:
            self.cur.execute(selectsql)
        except Exception as ef:
            print("查询失败")

        udid = self.cur.fetchall()[0][0]
        self.cur.close()
        self.mysqlconn.close()
        print(udid)

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



    #执行shell命令
    @staticmethod
    def dnld(index: int, command: str, silence: bool = True):
        cmd = Dnconsole.ld + '-s %d %s' % (index, command)
        if silence:
            os.system(cmd)
            return ''
        process = os.popen(cmd)
        result = process.read()
        process.close()
        return result




    #启动模拟器
    @staticmethod
    def launch(index: int):
        cmd = Dnconsole.console + 'launch --index ' + str(index)
        process = os.popen(cmd)
        result = process.read()
        print("result>>>>>> ", result)
        process.close()
        return result




    # 点击订单搜索框
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
                    searchbut = WebDriverWait(self.driver, 3).until(lambda x: x.find_element_by_accessibility_id("搜索"))
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




    def main(self):
        self.launch(self.index)
        self.ClickSearch()





if __name__ == '__main__':
    index = input("请输入模拟器编号>>>>>>>>")
    Dnconsole(index).main()