import sys
import math
import time

import hmac
import hashlib
import base64
import struct

import pyqrcode

class TOTP:

    def getCounter(self):
        currTime = time.time()
        temp = math.floor( (currTime - 0) / self.ga.timeStep)
        return temp

    
    def getHash(self):
        key = self.ga.secret
        counter = self.getCounter()
        
        k = base64.b32decode(key)
        counter = struct.pack('>q', counter)

        myHash = hmac.new(k, counter, hashlib.sha1)
        myByteArrayHash = bytearray(myHash.digest())

        binaryArr = []
        for c in myByteArrayHash:
            bits = bin(c)[2:]
            bits = '00000000'[len(bits):] + bits
            binaryArr.extend([int(b) for b in bits])

        binary = ""
        for i in binaryArr:
            binary += str(i)

        return binary

    def truncate(self, s):
        lastFour = s[len(s)-4:]

        offset = int(lastFour, 2)

        charOffset = (offset * 8) + 1
        return s[charOffset:charOffset+31]


    def start(self):
        hotp = self.truncate( self.getHash())
        hotp = int(hotp, 2)
        hotp = hotp % (pow(10, 6))
        self.code = '000000'[len(str(hotp)):] + str(hotp)
        self.code = self.code[:3] + " " + self.code[3:]

    def __init__(self, ga):
        self.ga = ga

class GoogleAuth:

    def generateQR(self):
        s = "otpauth://totp/Provider1:" + self.email + "?secret=" + self.secret + "&issuer=Provider1"
        url = pyqrcode.create(s) 
        url.svg("QR-Code.svg", scale = 8) 

    
    def getOTP(self):
        otp = TOTP(self)
        while True:
            otp.start()
            print(otp.code)
            time.sleep(30)
            


    def __init__(self, time, length, email, secret):
        self.timeStep = time
        self.passwordLen = length
        self.email = email
        self.secret = secret


email = "testing123@google.com"
secret = "JBSWY3DPEHPK3PXP"

if len(sys.argv) == 2:
    ga = GoogleAuth(30, 6, email, secret)
    arg = sys.argv[1]

    if arg == "generate":
        ga.generateQR()

    elif arg == "get":
        ga.getOTP()


