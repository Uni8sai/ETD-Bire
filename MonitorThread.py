from PyQt5.QtCore import *
from scapy.all import *
from pywifi import PyWiFi, const

class MonitorThread(QThread):
    notify_Progress = pyqtSignal(str)
    def __init__(self, face_name, parent=None):
        super(MonitorThread, self).__init__(parent)
        self.iface_name = face_name
        self.running = True  # スレッドを制御するフラグ

    def run(self):
        
        interface = self.iface_choose(self.iface_name)
        while self.running:
            status = interface.status()
            status_text = self.get_status_text(status)
            interface_text = interface.name()
            print(f"Interface: {interface_text} Status: {status_text}")
            self.notify_Progress.emit(f"Interface: {interface_text} Status: {status_text}")
            time.sleep(2)  # 2秒ごとに状態を確認

    def stop(self):
        self.running = False  # スレッドを停止

    @staticmethod
    def iface_choose(face_name):
        iface_list = PyWiFi().interfaces()
        for interface in iface_list:
            if interface.name() == face_name:
                return interface
            
    @staticmethod
    def get_status_text(status):
        status_dict = {
            const.IFACE_DISCONNECTED: "Disconnected",
            const.IFACE_SCANNING: "Scanning",
            const.IFACE_INACTIVE: "Inactive",
            const.IFACE_CONNECTING: "Connecting",
            const.IFACE_CONNECTED: "Connected",
        }
        return status_dict.get(status, "Unknown")

