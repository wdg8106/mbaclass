# coding=utf-8

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from pyweixin import WeiXin

def event(request):
    if request.method == 'GET':
        weixin = WeiXin.on_connect(token='W6VMThflrgp8nFQ',
            timestamp=request.GET['timestamp'],
            nonce=request.GET['nonce'],
            signature=request.GET['signature'],
            echostr=request.GET['echostr'])
        if weixin.validate():
            return HttpResponse(request.GET['echostr'])
        else:
            return HttpResponse('')
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

    