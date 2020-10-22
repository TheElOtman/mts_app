import serial
from PyQt5.QtCore import *
import time
import pandas as pd

class SerialPort(QObject):
    
    def __init__(self, parent = None):
        super(SerialPort, self).__init__(parent)
        #initialization and open the port
        pins = pd.read_csv('../files/settings.csv')
        res = pins[(pins['purpose'] == 'PLC')]
        self.portName = res['name'].item()
        self.ComPort = None
        self.portConnect()

    def portConnect(self):
        try:
            self.ComPort = serial.Serial(self.portName,9600,timeout=0)
        except Exception as e:
            print('could not connect with port "%s"'%self.portName)

    # Explicit signal
    signal = pyqtSignal(str)

    def readSerialPort(self):
        print ("Start reading from port")
        if self.ComPort is not None:
            while True:
                try:
                    readOut = self.ComPort.read(268)
                    data = readOut.decode().strip()
                    print(readOut)
                    if data != "":
                        self.signal.emit(data)
                except Exception as e:
                    self.portConnect()

                time.sleep(1)
        print ("Finish reading from port")
    
    def writeSerialPort(self,data):
        try:
            if self.ComPort is not None:
                self.ComPort.write(data.encode())
        except Exception as e:
            print("Port not connect yet")
