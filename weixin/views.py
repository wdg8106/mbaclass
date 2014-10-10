# coding=utf-8
from django.shortcuts import HttpResponse
from pyweixin import WeiXin
from WXBizMsgCrypt import WXBizMsgCrypt

CorpID = "wxe8c28e24336f65d4"
Token = "G5EAQH0hMiWt"
EncodingAESKey = "mTRnFdzsGY191Vy2fhm5ayHTX9vXcacfqo76ofbnfaa"

def callback(request):
    wxcpt = WXBizMsgCrypt(Token, EncodingAESKey, CorpID)

    if request.method == 'GET':
        ret, echoStr = wxcpt.VerifyURL(request.GET['msg_signature'], 
            request.GET['timestamp'],request.GET['nonce'],request.GET['echostr'])
        if(ret != 0):
            return HttpResponse('')
        else:
            return HttpResponse(echoStr)
    else:
        weixin = WeiXin.on_message(request.body)
        j = weixin.to_json()
        msg_type = j['MsgType']
        message = None

        if msg_type == 'text':
            message = '您刚刚输入了 %s' % j['Content']
        elif msg_type == 'event':
            if j['Event'] == 'subscribe':
                message = '欢迎加入'

        if message:
            return HttpResponse(WeiXin().to_xml(to_user_name=j['FromUserName'],
                from_user_name=j['ToUserName'],
                create_time=j['CreateTime'],
                msg_type='text',
                content=message,
                func_flag=0))
        else:
            return HttpResponse('')

    