# -*- coding: utf8
import json, time, os
import httplib, urllib, urllib2
import xml.etree.ElementTree as ET

try:
    from WXBizMsgCrypt import WXBizMsgCrypt
except Exception:
    class WXBizMsgCrypt(object):
        def __init__(self, Token, EncodingAESKey, CorpID):
            self.m_sCorpid = CorpID

CorpID = "wxe8c28e24336f65d4"
Token = "G5EAQH0hMiWt"
EncodingAESKey = "mTRnFdzsGY191Vy2fhm5ayHTX9vXcacfqo76ofbnfaa"

TokenFile = os.path.join(os.path.dirname(__file__), 'token.json')

class WeiXin(WXBizMsgCrypt):

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        ret, msg = super(WeiXin, self).DecryptMsg(sPostData, sMsgSignature, sTimeStamp, sNonce)
        return ret, (ret==0 and self.to_json(msg) or msg)

    def token(self, groupId):
        if not hasattr(self, 'tokens'):
            self.tokens = json.loads(file(TokenFile).read())

        access = self.tokens[groupId]
        if access['expires'] < time.time():
            # get new token
            res = urllib2.urlopen('https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(self.m_sCorpid, access['corpsecret']))
            res_dict = json.loads(res.read())
            if res_dict.get('access_token', False):
                access['token'] = res_dict['access_token']
                access['expires'] = int(time.time()) + int(res_dict['expires_in']) - 600

                with open(TokenFile,'w') as f:
                    f.write(json.dumps(self.tokens))

        return access['token']


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

    def auth_url(self, url):
        return 'https://open.weixin.qq.com/connect/oauth2/authorize?' + \
           'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=0#wechat_redirect' % \
            (self.m_sCorpid, urllib.quote_plus(url))

    def send_msg(self, msg):
        try:
            headers = {"Accept": "text/plain"}
            httpClient = httplib.HTTPSConnection("qyapi.weixin.qq.com", 443, timeout=30)
            httpClient.request("POST", "/cgi-bin/message/send?access_token=%s" % self.token('sendMsg'), json.dumps(msg, ensure_ascii=False).encode('utf-8'), headers)
         
            response = httpClient.getresponse()
            ret = json.loads(response.read())
            print ret
            return ret
        except Exception, e:
            print e
            return {"errcode":-1, "errmsg":str(e)}

    def get_users(self, department, fetch_child=True, status=0):
        res = urllib2.urlopen(
            'https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token=%s&department_id=%d&fetch_child=%d&status=%d' \
            % (self.token('sendMsg'), department, fetch_child and 1 or 0, status))
        return json.loads(res.read())

    def get_user(self, userId):
        res = urllib2.urlopen(
            'https://qyapi.weixin.qq.com/cgi-bin/user/get?access_token=%s&userid=%s' \
            % (self.token('sendMsg'), userId))
        return json.loads(res.read())

wx = WeiXin(Token, EncodingAESKey, CorpID)

if __name__ == '__main__':
    wx.send_msg({
       "touser": "MB1408435",
        "msgtype": "text",
        "agentid": "2",
        "text": {
            "content": u'您的账户余额为'.encode('utf-8')
        }
    })

