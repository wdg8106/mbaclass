# -*- coding: utf8
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pyweixin import wx
from member.models import Member
from event.models import Event

@csrf_exempt
def callback(request):

    if request.method == 'GET':
        ret, echoStr = wx.VerifyURL(request.GET['msg_signature'], 
            request.GET['timestamp'], request.GET['nonce'], request.GET['echostr'])
        if ret != 0:
            return HttpResponse('')
        else:
            return HttpResponse(echoStr)
    else:
        ret, msg = wx.DecryptMsg(request.body, request.GET['msg_signature'], 
            request.GET['timestamp'], request.GET['nonce'])
        if ret != 0:
            return HttpResponse('')

        try:
            user = Member.objects.get(number=msg['FromUserName'])
        except Exception:
            return HttpResponse('')

        if msg['MsgType'] == 'event':
            # 点击按钮事件
            if msg['EventKey'] == 'NEW_EVENT':
                articles = [{
                   "title": e.slug[0:20],
                   "description": e.slug,
                   "url": wx.auth_url('http://182.92.101.78/event/show/%d' % e.pk),
                   "picurl": "http://www.sucai123.com/sucai/img2/193/064.jpg"
                } for e in Event.objects.filter(is_active=True).order_by('-public_time')[0:8]]

                wx.send_msg({
                    "touser": user.number,
                    "msgtype": "news",
                    "agentid": "1",
                    "news": {
                       "articles": articles
                    }
                })
        
        return HttpResponse('')
    