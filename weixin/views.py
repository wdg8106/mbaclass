# -*- coding: utf8
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pyweixin import wx
from member.models import Member

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
                wx.new_events(user)
            elif msg['EventKey'] == 'MY_ACCOUNT':
                wx.my_account(user)

        return HttpResponse('')
    