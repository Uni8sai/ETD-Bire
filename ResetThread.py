from PyQt5.QtCore import QThread, pyqtSignal
from pywifi import PyWiFi, const
from scapy.all import *

class ResetThread(QThread):
    finished = pyqtSignal()

    def __init__(self, iface_name,parent=None):  
        super(ResetThread,self).__init__(parent)
        self.iface_name = iface_name
        self.running = True  # スレッドを制御するフラグ
    def run(self):
        interface = self.iface_choose(self.iface_name)
        interface.disconnect()  # 切断
        self.finished.emit()  # 完了通知
        time.sleep(2)
    @staticmethod
    def iface_choose(face_name):
        iface_list = PyWiFi().interfaces()
        for interface in iface_list:
            if interface.name() == face_name:
                return interface