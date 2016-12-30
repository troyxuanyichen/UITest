import socket
import sys
import binascii


class PackageSender:
    def __init__(self, socket):
        self.socket = socket

    def sendData(self, valueDict):
        self.subPackageDict = valueDict
        binaryArray = self.preparePackage()
        binarylist = bytearray()
        i = 0
        while i < len(binaryArray):
            c = binaryArray[i:i + 8]
            binarylist.append(int(c, 2))
            i += 8
        print binarylist[0:10]
        self.socket.send(binarylist)

    def preparePackage(self):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        binaryArray = ''
        for k, v in self.subPackageDict.items():
            subpackArray = self.prepareSubpackage(k, v)
            binaryArray += subpackArray

        subpackageLen = len(binaryArray) / 8
        # print subpackageLen
        totalLen = subpackageLen + 16
        totalPac = len(self.subPackageDict)
        header = get_bin(ord('B'), 8) + get_bin(ord('r'), 8) + get_bin(ord('n'), 8) + get_bin(ord('C'), 8)
        secondFour = get_bin(totalPac, 16) + get_bin(totalLen, 16)
        checking = get_bin(int(header, 2) ^ int(secondFour, 2), 32)
        tail = get_bin(ord('P'), 8) + get_bin(ord('K'), 8) + get_bin(ord('E'), 8) + get_bin(ord('D'), 8)
        binaryArray = header + secondFour + checking + binaryArray + tail
        return binaryArray

    def prepareSubpackage(self, key, value):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        binaryArray = ''
        if key == 'color':
            binaryArray += get_bin(ord('C'), 8)
            binaryArray += get_bin(ord('L'), 8)
            binaryArray += get_bin(4, 16)
            if value == 'blue':
                x = (0x00 << 16) + (0x00 << 8) + 0xff
                print 'blue sent'
            if value == 'green':
                x = (0xff << 16) + (0xf0 << 8) + 0x00
                print 'yellow sent'
            if value == 'red':
                x = (0xff << 16) + (0x11 << 8) + 0x00
                print 'red sent'
            if value == 'white':
                x = (0xff << 16) + (0xff << 8) + 0xff
                print 'white sent'
            if value == 'off':
                x = (0x00 << 16) + (0x00 << 8) + 0x00
                print 'off sent'
            binaryArray += get_bin(x, 24)
            binaryArray += get_bin(0xff, 8)
        if key == 'slowColor':
            binaryArray += get_bin(ord('C'), 8)
            binaryArray += get_bin(ord('L'), 8)
            binaryArray += get_bin(4, 16)
            if value == 'blue':
                x = (0x00 << 16) + (0x00 << 8) + 0xff
                print 'blue sent'
            if value == 'green':
                x = (0xff << 16) + (0xf0 << 8) + 0x00
                print 'yellow sent'
            if value == 'red':
                x = (0xff << 16) + (0x11 << 8) + 0x00
                print 'red sent'
            if value == 'white':
                x = (0xff << 16) + (0xff << 8) + 0xff
                print 'white sent'
            if value == 'off':
                x = (0x00 << 16) + (0x00 << 8) + 0x00
                print 'off sent'
            binaryArray += get_bin(x, 24)
            binaryArray += get_bin(0xff, 8)
        return binaryArray
