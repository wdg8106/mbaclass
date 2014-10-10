# -*- coding: utf8
import json
import httplib, urllib
import xml.etree.ElementTree as ET
from WXBizMsgCrypt import WXBizMsgCrypt

CorpID = "wxe8c28e24336f65d4"
Token = "G5EAQH0hMiWt"
EncodingAESKey = "mTRnFdzsGY191Vy2fhm5ayHTX9vXcacfqo76ofbnfaa"

getTokenUrl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=wxe8c28e24336f65d4&corpsecret=AwxxQ3xpUUUau-TJUvg3xT4N4wFCEllYu-_MQjvSgz-hWZ6qOWOro_sTKbMwxks-'
token = 'Zc3DY8GrFl-v1o8qwmDGi_H17yVtBbSjt44NPoBLeaQIOKUobs0YOK-8arBxbK2n'

class WeiXin(WXBizMsgCrypt):

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        ret, msg = super(WeiXin, self).DecryptMsg(sPostData, sMsgSignature, sTimeStamp, sNonce)
        return ret, (ret==0 and self.to_json(msg) or msg)

    def to_json(self, msg):
        '''http://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.XML
        '''
        j = {}
        root = ET.fromstring(msg)
        for child in root:
            if child.tag == 'CreateTime':
                value = long(child.text)
            else:
                value = child.text
            j[child.tag] = value
        return j

    def _cdata(self, data):
        '''http://stackoverflow.com/questions/174890/how-to-output-cdata-using-elementtree
        '''
        if type(data) is str:
            return '<![CDATA[%s]]>' % data.replace(']]>', ']]]]><![CDATA[>')
        return data

    def to_xml(self, **kwargs):
        xml = '<xml>'
        for tag in kwargs.iterkeys():
            v = kwargs[tag]
            xml += '<%s>%s</%s>' % (tag, self._cdata(v), tag)
        xml += '</xml>'
        return xml

    def send_msg(self, msg):
        try:
            headers = {"Accept": "text/plain"}

            httpClient = httplib.HTTPSConnection("qyapi.weixin.qq.com", 443, timeout=30)
            httpClient.request("POST", "/cgi-bin/message/send?access_token=%s" % token, json.dumps(msg), headers)
         
            response = httpClient.getresponse()
            print response.status
            print response.reason
            print response.read()
            print response.getheaders() #获取头信息
        except Exception, e:
            print e

if __name__ == '__main__':
    wxcpt = WeiXin(Token, EncodingAESKey, CorpID)
    wxcpt.send_msg({
        "touser": "MB1408435",
        "msgtype": "text",
        "agentid": "1",
        "text": {
            "content": 'https://open.weixin.qq.com/connect/oauth2/authorize?' + 
                'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=0#wechat_redirect' % 
                (CorpID, urllib.quote_plus('http://182.92.101.78/event/show/1'))
        },
        "safe":"0"
    })