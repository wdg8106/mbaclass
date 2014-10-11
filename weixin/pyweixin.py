# -*- coding: utf8
import json, time, os
import httplib, urllib, urllib2
import xml.etree.ElementTree as ET
from WXBizMsgCrypt import WXBizMsgCrypt

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
            httpClient.request("POST", "/cgi-bin/message/send?access_token=%s" % self.token('sendMsg'), json.dumps(msg, ensure_ascii=False), headers)
         
            response = httpClient.getresponse()
            print response.status
            print response.reason
            print response.read()
            print response.getheaders() #获取头信息
        except Exception, e:
            print e

wx = WeiXin(Token, EncodingAESKey, CorpID)

if __name__ == '__main__':
    # wxcpt.send_msg({
    #     "touser": "MB1408435",
    #     "msgtype": "text",
    #     "agentid": "1",
    #     "text": {
    #         "content": 'https://open.weixin.qq.com/connect/oauth2/authorize?' + 
    #             'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=0#wechat_redirect' % 
    #             (CorpID, urllib.quote_plus('http://182.92.101.78/event/show/1'))
    #     },
    #     "safe":"0"
    # })

    wx.send_msg({
       "touser": "MB1408435",
       "msgtype": "news",
       "agentid": "1",
       "news": {
           "articles":[
               {
                   "title": "北航经管学院2014年专项奖学金评定",
                   "description": "2014年专项奖学金的评选工作已开始，评奖范围为硕士2、3年级、博士2、3、4年级（具体要求参见附件）。原则上，每名学生在校期间只能获得一次同类专项奖学金（不包括研究生学业奖学金），不能重复获得，获得国家奖学金的同学原则上不再获得其他奖学金。本次评定工作分为两部分，光华奖学金采用名额下放、班级推荐的形式，其他专项奖学金采用个人申报、学院统一评定的形式，现将具体的评定方法公布如下：",
                   "url": 'https://open.weixin.qq.com/connect/oauth2/authorize?' + 
                        'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=0#wechat_redirect' % 
                        (CorpID, urllib.quote_plus('http://182.92.101.78/event/show/1')),
                   "picurl": "http://www.sucai123.com/sucai/img2/193/064.jpg"
               },
               {
                   "title": "北航经管学院2014年专项奖学金评定",
                   "description": "2014年专项奖学金的评选工作已开始，评奖范围为硕士2、3年级、博士2、3、4年级（具体要求参见附件）。原则上，每名学生在校期间只能获得一次同类专项奖学金（不包括研究生学业奖学金），不能重复获得，获得国家奖学金的同学原则上不再获得其他奖学金。本次评定工作分为两部分，光华奖学金采用名额下放、班级推荐的形式，其他专项奖学金采用个人申报、学院统一评定的形式，现将具体的评定方法公布如下：",
                   "url": 'https://open.weixin.qq.com/connect/oauth2/authorize?' + 
                        'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_base&state=0#wechat_redirect' % 
                        (CorpID, urllib.quote_plus('http://182.92.101.78/event/show/1')),
                   "picurl": "http://www.sucai123.com/sucai/img2/193/064.jpg"
               }
           ]
       }
    })


