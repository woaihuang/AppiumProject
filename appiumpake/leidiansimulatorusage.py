#!/usr/local/bin/python3
#-*- coding: UTF-8 -*-


import shutil, os, re, time, pymysql



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




    def __init__(self):
        self.mysqlconn = pymysql.connect(
        )
        self.cur = self.mysqlconn.cursor()




    #获取模拟器列表
    @staticmethod
    def get_list():
        cmd = os.popen(Dnconsole.console + 'list2')
        text = cmd.read()
        cmd.close()
        info = text.split('\n')
        result = list()
        for line in info:
            if len(line) > 1:
                dnplayer = line.split(',')
                result.append(DnPlayer(dnplayer))
        return result




    # 获取正在运行的模拟器列表
    @staticmethod
    def list_running() -> list:
        result = list()
        all = Dnconsole.get_list()
        for dn in all:
            if dn.is_running() is True:
                result.append(dn)
        return result




    # 检测指定序号的模拟器是否正在运行
    @staticmethod
    def is_running(index: int) -> bool:
        all = Dnconsole.get_list()
        if index >= len(all):
            raise IndexError('%d is not exist' % index)
        return all[index].is_running()




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




    #安装apk 指定模拟器必须已经启动
    @staticmethod
    def install(index: int, path: str):
        shutil.copy(path, Dnconsole.share_path + str(index) + '手机淘宝.apk')
        time.sleep(1)
        Dnconsole.dnld(index, 'pm install /sdcard/Pictures//手机淘宝.apk')




    #获取安装包列表
    @staticmethod
    def get_package_list(index: int) -> list:
        result = list()
        text = Dnconsole.dnld(index, 'pm list packages')
        info = text.split('\n')
        for i in info:
            if len(i) > 1:
                result.append(i[8:])
        return result




    #点击或者长按某点
    @staticmethod
    def touch(index: int, x: int, y: int, delay: int = 0):
        if delay == 0:
            Dnconsole.dnld(index, 'input tap %d %d' % (x, y))
        else:
            Dnconsole.dnld(index, 'input touch %d %d %d' % (x, y, delay))




    #滑动
    @staticmethod
    def swipe(index, coordinate_leftup: tuple, coordinate_rightdown: tuple, delay: int = 0):
        x0 = coordinate_leftup[0]
        y0 = coordinate_leftup[1]
        x1 = coordinate_rightdown[0]
        y1 = coordinate_rightdown[1]
        if delay == 0:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d' % (x0, y0, x1, y1))
        else:
            Dnconsole.dnld(index, 'input swipe %d %d %d %d %d' % (x0, y0, x1, y1, delay))




    #添加模拟器
    @staticmethod
    def add(name: str):
        cmd = Dnconsole.console + 'add --name %s' % name
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




    def main(self):
        sql = "SELECT MAX(id) FROM appiumtable_test"

        self.cur.execute(sql)

        index = self.cur.fetchall()[0][0]
        if index:
            index = index + 1
        else:
            index = 1

        self.add("雷电模拟器{}".format(index))
        self.launch(index)
        while True:
            flag = self.is_running(index)
            if flag:
                break
        self.install(index, "C:\\Users\\Administrator\\Documents\\雷电模拟器\\Pictures\\手机淘宝.apk")

        #获取正在运行的模拟器的udid，最大的即为最新创建的模拟器
        while True:
            try:
                output = os.popen('adb devices')
                aa = output.read()
                udidlist = re.findall("emulator-(.*)	", aa)
                udid = "emulator-" + max(udidlist)
                return udid
            except Exception as E:
                pass






if __name__ == '__main__':
    print(Dnconsole().get_list())