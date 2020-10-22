from windows import *
import pandas as pd
from SerialPort import *
import time

class Controller:
    def __init__(self):
        self.login = MainApp()
        self.serialThread = QThread()
        self.open_admin = False
        self.open_user = False
        self.open_scan = False

    def showLogin(self):
        self.login.QTxtLogin.setText('')
        self.login.QTxtPass.setText('')
        if not self.login.loaded:
            self.login.switchWindow.connect(self.showUser)
            self.login.loaded = True
        if self.open_admin:    
            self.admin.close()
        if self.open_user:
            self.user.close()
        if self.open_scan:
            self.scan.close()
        self.login.show()

    def showUser(self,text):
        try:
            self.serialThread.started.disconnect()
            self.serialThread.terminate()
        except Exception as e:
            print(e)
        users = pd.read_csv('../files/users.csv')
        res = users[(users['username'] == text)]
        if res['username'].item() == "admin":
            if not self.open_admin:
                self.admin = Admin('')
                self.open_admin = True
            self.admin.login = text
            self.admin.handleHeaders()
            if not self.admin.loaded:
                self.admin.switchWindow.connect(self.showLogin)
                self.admin.loaded = True
            self.login.close()
            self.admin.show()
        else :
            if not self.open_user:
                self.user = User('')
                self.open_user = True
            self.user.QTxtQuan.setText('')
            self.user.QTxtRef.setText('')
            self.user.login = text
            self.user.handleHeaders()
            if not self.user.loaded:
                self.user.switchWindow.connect(self.showLogin)
                self.user.switchWindow2.connect(self.showScan)
                self.user.loaded = True
            
            self.login.close()
            if self.open_scan:
                self.scan.close()
            self.user.show()

    def sendToOutput(self,data):
        print('[+]Sending',data,'to serial port')
        self.serialPort.writeSerialPort(data)

    def showScan(self,text):
        if not self.open_scan:
            self.scan = Scan('')
            self.open_scan = True
        self.scan.login = text.split(';')[0]
        self.scan.reference = text.split(';')[1]
        self.scan.quantity = int(text.split(';')[2])
        self.scan.processed = 0
        self.scan.handleHeaders()
        self.scan.handel_progressBar()
        if not self.scan.loaded:
            self.scan.switchWindow.connect(self.showUser)
            self.scan.loaded = True

        self.serialPort = SerialPort()
        self.serialPort.moveToThread(self.serialThread)
        self.serialPort.signal.connect(self.scan.recieveData)
        self.serialThread.started.connect(self.serialPort.readSerialPort)
        self.serialThread.setTerminationEnabled(True)
        self.serialThread.start()
        self.user.close()
        time.sleep(0.5)
        self.scan.show()