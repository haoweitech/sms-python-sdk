#-*- coding=utf-8 -*-

import time
import json
import hashlib
import urllib
import urllib2


app_id = '你的开发者id'
secret_key = '你的开发密码'
version = '1.0'
method = 'sms.message.send'
    
biz_content = {
    'mobile': ['13800138000'],
    'sign': '好为科技',
    'send_time': '',
    'type': 0,
    'template_id': 'ST_2019043000000001',
    'params': {
        'code': 1569
    }
}


post = {
    'app_id': app_id,
    'timestamp': bytes(int(round(time.time() * 1000))),
    'method': method,
    'version': version,
    'sign_type': 'md5',
    'biz_content': json.dumps(biz_content, separators=(',',':'))
}

print (post)

list = []
for k in sorted(post):
    list.append('='.join([k, post[k]]))
list.append('key=' + secret_key)
sign = hashlib.md5('&'.join(list)).hexdigest().upper()

print (sign)
post['sign'] = sign
print (post)

headers = {
    'User-Agent': 'Mozilla 5.0 Python-SMS-SDK v1.0.0 (Haowei tech)'
}
data = urllib.urlencode(post)
print (data)
request = urllib2.Request('https://api.haowei.tech/gateway.do', data=data, headers=headers)
response = urllib2.urlopen(request)

print ('-' * 32)
print (response.read().decode('utf8'))
