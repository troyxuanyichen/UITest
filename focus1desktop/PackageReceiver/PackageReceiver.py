import socket
from focus1desktop.DataProcessor import DataProcessor
import sys


class PackageReceiver:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.sock = None
        self.sendData = True
        self.isPackageBody = False
        self.fourBytesBuff = []
        self.packageBody = []
        self.dataProcessor = DataProcessor()
        self.tcpfile = open('tcp_rawdata.txt', 'w')
        # self.dataProcessor.setSocket(self.sock)

    def startConnecting(self):
        address = (self.ip, self.port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(address)
        self.sock.settimeout(10.0)
        if self.sendData == True and self.sock != None:
            self.dataProcessor.setSocket(self.sock)
        self.processStream()

    def sendDataToWifi(self):
        self.sendData = True

    def stopConnecting(self):
        return

    def processStream(self):
        # aaa = self.sock.recv(1024)
        # print aaa.decode("hex")
        # print len(aaa)
        while True:
            byteList = list(bytearray(self.sock.recv(1)))
            self.tcpfile.writelines('%x  ' % byteList[0])
            if len(byteList) == 0:
                continue
            oneByte = byteList[0]

            if len(self.fourBytesBuff) == 4:
                del self.fourBytesBuff[:1]

            self.fourBytesBuff.append(oneByte)

            if self.isPackageBody:
                self.packageBody.append(oneByte)

            if self.fourBytesParse() == 1:
                if not self.isPackageBody:
                    self.isPackageBody = True
            elif self.fourBytesParse() == -1:
                if self.isPackageBody:
                    self.isPackageBody = False
                    del self.packageBody[-4:]
                    subpackageDict = self.parsePackageBody()
                    finalDict = self.getFinalDict(subpackageDict)
                    if not finalDict == None and not len(finalDict) == 0:
                        # print finalDict['EG']
                        print 'Connected to device.'
                        self.dataProcessor.processRawDataWithFFT(finalDict['EG'])
                        # print finalDict['EG'] # todo
                        # self.dataProcessor.realTimePlotting()
                        ### TODO deal with subpackage dict ###

    def fourBytesParse(self):
        if self.fourBytesBuff == None or len(self.fourBytesBuff) < 4:
            return 0

        if self.fourBytesBuff[0] == ord('B') and self.fourBytesBuff[1] == ord('r') and self.fourBytesBuff[2] == ord(
                'n') and self.fourBytesBuff[3] == ord('C'):
            return 1

        if self.fourBytesBuff[0] == ord('P') and self.fourBytesBuff[1] == ord('K') and self.fourBytesBuff[2] == ord(
                'E') and self.fourBytesBuff[3] == ord('D'):
            return -1

    def parsePackageBody(self):
        size = self.packageBody[2] * 256 + self.packageBody[3]
        if not size == len(self.packageBody) + 8:
            self.packageBody = []
            return None

        byteCheck = [None] * 4
        for i in range(0, 4):
            byteCheck[i] = self.packageBody[i] ^ self.packageBody[i + 4]

        if not (byteCheck[0] == ord('B') and byteCheck[1] == ord('r') and byteCheck[2] == ord('n') and byteCheck[
            3] == ord('C')):
            self.packageBody = []
            return None
        subpackages = self.packageBody[8:]
        subpackageList = self.parseSubPackages(subpackages)
        # startByte = 8
        # while startByte < size:
        #     subpackages = self.packageBody[startByte:]
        #     subpackageList = self.parseSubPackages(subpackages)

        self.packageBody = []
        return subpackageList

    def int24To32(self, byteArray):
        bigEnd = byteArray[0]
        int32 = 0
        if (bigEnd >> 7) & 0x01 == 1:
            int32 = (0xff << 24) + (byteArray[0] << 16) + (byteArray[1] << 8) + byteArray[2]
        else:
            int32 = (0x00 << 24) + (byteArray[0] << 16) + (byteArray[1] << 8) + byteArray[2]
        int32 &= 0xffffffff
        return int32 | (-(int32 & 0x80000000))

    def parseSubPackages(self, subpackages):
        rst = {}
        while not len(subpackages) == 0:
            key = str(bytearray(subpackages[:2]))
            subSize = subpackages[2] * 256 + subpackages[3]
            del subpackages[:4]
            subpackage = subpackages[:subSize]
            del subpackages[:subSize]
            if key in rst:
                rst[key].extend(subpackage)
            else:
                rst[key] = subpackage
        return rst

    def getFinalDict(self, inputDict):
        rst = {}
        for key, value in inputDict.items():
            if key == 'AS':
                rst['AS'] = value
                self.dataProcessor.changeParameter((value[0] << 8) + value[1], value[2])
                # print value # todo
        for key, value in inputDict.items():
            if key == 'EG':
                rst['EG'] = []
                # print len(value)
                for i in range(0, len(value), 3):
                    rst['EG'].append(self.int24To32(value[i:i + 3]))


                # elif key == ''
        return rst
