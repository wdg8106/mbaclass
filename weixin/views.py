# coding=utf-8
import time
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pyweixin import WeiXin
from member.models import Member

CorpID = "wxe8c28e24336f65d4"
Token = "G5EAQH0hMiWt"
EncodingAESKey = "mTRnFdzsGY191Vy2fhm5ayHTX9vXcacfqo76ofbnfaa"

@csrf_exempt
def callback(request):
    wxcpt = WeiXin(Token, EncodingAESKey, CorpID)

    if request.method == 'GET':
        ret, echoStr = wxcpt.VerifyURL(request.GET['msg_signature'], 
            request.GET['timestamp'], request.GET['nonce'], request.GET['echostr'])
        if(ret != 0):
            return HttpResponse('')
        else:
            return HttpResponse(echoStr)
    else:
        ret, msg = wxcpt.DecryptMsg(request.body, request.GET['msg_signature'], 
            request.GET['timestamp'], request.GET['nonce'])
        if( ret!=0 ):
            return HttpResponse('')
        try:
            user = Member.objects.get(number=msg['FromUserName'])
            content = u'%s 您好，您刚才输入的内容是 "%s"' % (user.username, msg['Content'])

            xml = wxcpt.to_xml(ToUserName=CorpID, FromUserName=user.number, CreateTime=int(time.time()), 
                MsgType='text', Content=content, MsgId=int(msg['MsgId'])+1000, AgentID=1)
            ret,encryptMsg = wxcpt.EncryptMsg(xml, request.GET['nonce'])
            if( ret!=0 ):
                return HttpResponse('')
            return HttpResponse(encryptMsg)

        except Exception:
            return HttpResponse('')

    