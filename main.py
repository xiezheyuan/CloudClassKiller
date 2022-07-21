import os
import subprocess
import sys
import threading
import time
from subprocess import Popen as system
import qdarkstyle
import win32con
import win32gui
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QCommandLinkButton, QInputDialog, QApplication

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE

KILL_PROCESSES = [
    'RJService.exe', 'CMService.exe', 'CMService.exe', 'CMService.exe',
    'RJAgent.exe', 'RJAgent.exe', 'RJUsbController.exe', 'CMLauncher.exe',
]


def open_main():
    system("C:\\Program Files (x86)\\RG-CloudManagerRemote\\CMLauncher.exe", shell=False, startupinfo=startupinfo)


def open_main_gdj():
    os.system("start C:\\Users\\Public\\Desktop\\教学管理软件.lnk")


# noinspection PyBroadException
class CloudClassKiller(QWidget):
    GDJ = 0
    TOP_WND = -1
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.gdj_thread_obj = threading.Thread(target=self.gdj_thread, name="【百万雄师过大江】进程")
        self.gdj_thread_obj.start()
        self.top_display_wnd_thread = threading.Thread(target=self.top_display_wnd, name="广播控制进程")
        self.top_display_wnd_thread.start()
        self.resize(640, 480)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5() + "*{font-family:仿宋,微软雅黑,Arial;font-size:20px;}")
        self.setWindowTitle("云课堂噩梦0.5")
        self.Layout = QGridLayout()
        label = QLabel("<h1>欢迎使用云课堂噩梦0.5</h1>")
        self.Layout.addWidget(label)
        label = QLabel("请在【管理员身份】运行！")
        self.Layout.addWidget(label)
        self.kill_action = QCommandLinkButton("立即查杀")
        self.kill_action.setFixedHeight(50)
        self.kill_action.clicked.connect(self.main)
        self.open_action = QCommandLinkButton("打开云课堂")
        self.open_action.setFixedHeight(50)
        self.open_action.clicked.connect(open_main)
        self.interval_close_action = QCommandLinkButton("定时关闭云课堂")
        self.interval_close_action.setFixedHeight(50)
        self.interval_close_action.clicked.connect(self.interval_close)
        self.interval_open_action = QCommandLinkButton("定时开启云课堂")
        self.interval_open_action.setFixedHeight(50)
        self.interval_open_action.clicked.connect(self.interval_open)
        self.gdj_action = QCommandLinkButton("打开/关闭【百万雄师过大江】效果")
        self.gdj_action.setFixedHeight(50)
        self.gdj_action.clicked.connect(self.gdj_controller)
        self.top_display_wnd_action = QCommandLinkButton("开启/关闭广播置顶")
        self.top_display_wnd_action.setEnabled(False)
        self.top_display_wnd_action.setFixedHeight(50)
        self.top_display_wnd_action.clicked.connect(self.top_display_wnd_controller)
        self.Layout.addWidget(self.kill_action)
        self.Layout.addWidget(self.open_action)
        self.Layout.addWidget(self.interval_close_action)
        self.Layout.addWidget(self.interval_open_action)
        self.Layout.addWidget(self.gdj_action)
        self.Layout.addWidget(self.top_display_wnd_action)
        self.setLayout(self.Layout)

    @staticmethod
    def main():
        for i in KILL_PROCESSES:
            system("taskkill /f /im " + i, shell=False, startupinfo=startupinfo)

    def interval_close(self):
        number = QInputDialog.getInt(self, "云课堂噩梦0.5", "何时定时关闭？（单位：秒）", min=1, value=1)
        if not number[1]:
            return
        threading.Timer(number[0], function=self.main).start()

    def interval_open(self):
        number = QInputDialog.getInt(self, "云课堂噩梦0.5", "何时定时开启？（单位：秒）", min=1, value=1)
        if not number[1]:
            return
        threading.Timer(number[0], function=open_main).start()

    def gdj_thread(self):
        while 1:
            if self.GDJ:
                open_main_gdj()
                time.sleep(1)
                self.main()
            if self.GDJ == -1:
                break

    def gdj_controller(self):
        if self.GDJ == 1:
            self.GDJ = 0
        else:
            self.GDJ = 1

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.TOP_WND = -1
        self.GDJ = -1
        a0.accept()

    def top_display_wnd(self):
        while 1:
            if self.TOP_WND == -1:
                break
            hwnd = win32gui.FindWindow("ApplicationFrameWindow", "计算器")
            if hwnd == 0:
                continue
            try:
                if not self.TOP_WND:
                    print("Hi")
                    win32gui.SetWindowPos(hwnd, win32con.HWND_BOTTOM, 0, 0, 800, 600,
                                          win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
                else:
                    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 800, 600,
                                          win32con.SWP_NOSIZE | win32con.SWP_NOMOVE)
            except BaseException:
                __import__("traceback").print_exc()

    def top_display_wnd_controller(self):
        if self.TOP_WND == 1:
            self.TOP_WND = 0
        else:
            self.TOP_WND = 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CloudClassKiller()
    win.show()
    app.exec()
