from PyQt5.QtCore import *
from scapy.all import *
from pywifi import PyWiFi, const

class MonitorThread(QThread):
    notify_Progress = pyqtSignal(str)

    def __init__(self, interface, parent=None):
        super(MonitorThread, self).__init__(parent)
        self.interface = interface
        self.running = True  # スレッドを制御するフラグ

    def run(self):
        while self.running:
            status = self.interface.status()
            status_text = self.get_status_text(status)
            self.notify_Status.emit(f"Wi-Fi Status: {status_text}")
            time.sleep(2)  # 2秒ごとに状態を確認

    def stop(self):
        self.running = False  # スレッドを停止

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

