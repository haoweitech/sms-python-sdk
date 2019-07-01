#-*- coding=utf-8 -*-

import time
import json
import hashlib
import urllib
import urllib2

class Request:

    method = ''
    bizContent = ''

    def setBizContent(self, bizContent):
        if type(bizContent) is dict or type(bizContent) is list:
            self.bizContent = json.dumps(bizContent, separators=(',',':'))
        else:
            self.bizContent = bytes(bizContent)
        
    def getBizContent(self):
        return self.bizContent

    def setMethod(self, method):
        self.method = method
        return self
        
    def getMethod(self):
        return self.method

        

class Client:
    
    appId = ''
    timestamp = ''
    version = ''
    signType = ''
    secretKey = ''
    
    
    def __init__(self):
        self.timestamp = bytes(int(round(time.time() * 1000)))
        self.version = '1.0'

    def setAppId(self, appId):
        self.appId = appId

    def setSecretKey(self, secretKey):
        self.secretKey = secretKey

    def setSignType(self, signType):
        self.signType = signType

    def setVersion(self, version):
        self.version = version

    def setTimestamp(self, timestamp):
        self.timestamp = bytes(timestamp)

    def createSignature(self, data, secretKey):
        list = []
        for k in sorted(data):
            list.append('='.join([k, data[k]]))
        list.append('key=' + secretKey)
        return hashlib.md5('&'.join(list)).hexdigest().upper()
        
    def execute(self, request):
        post = {}
        post['app_id'] = self.appId
        post['version'] = self.version
        post['timestamp'] = self.timestamp
        post['biz_content'] = request.getBizContent()
        post['method'] = request.getMethod()
        post['sign_type'] = self.signType
        post['sign'] = self.createSignature(data = post, secretKey = self.secretKey)
        headers = {
            'User-Agent': 'Mozilla 5.0 Python-SMS-SDK v1.0.0 (Haowei tech)'
        }
        data = urllib.urlencode(post)
        request = urllib2.Request('https://api.haowei.tech/gateway.do', data=data, headers=headers)
        return urllib2.urlopen(request).read().decode('utf8')
        
    
if __name__ == '__main__':
    
    req = Request()
    req.setMethod(method = 'sms.message.send')
    req.setBizContent(bizContent = {
        'mobile': ['13800138000'],
        'sign': '好为科技',
        'send_time': '',
        'type': 0,
        'template_id': 'ST_2019043000000001',
        'params': {
            'code': 1569
        }
    })

    client = Client()
    client.setAppId('你的开发者id')
    client.setSecretKey('你的开发者密钥')
    client.setVersion('1.0')
    res = client.execute(req)
    print (res)



