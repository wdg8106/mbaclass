# -*- coding: utf8
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pyweixin import wx

from member.models import Member
from event.models import Event
from fina.models import MemberAccount

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
            member = Member.objects.get(number=msg['FromUserName'])
        except Exception:
            return HttpResponse('')

        if msg['MsgType'] == 'event':
            # 点击按钮事件
            if msg['EventKey'] == 'NEW_EVENT':
                articles = [{
                   "title": e.title,
                   "description": e.slug,
                   "url": wx.auth_url('http://182.92.101.78/event/show/%d' % e.pk),
                    "picurl": e.pic and e.pic.url or "http://www.sucai123.com/sucai/img2/193/064.jpg"
                } for e in Event.objects.filter(is_active=True).order_by('-public_time')[0:8]]

                wx.send_msg({
                    "touser": member.number,
                    "msgtype": "news",
                    "agentid": "1",
                    "news": {
                       "articles": articles
                    }
                })
            elif msg['EventKey'] == 'MY_ACCOUNT':
                accs = MemberAccount.objects.filter(member=member)
                content = u'您的账户余额为:\n' + '\n'.join([u'%s: %.02f元' % (a.account.name, a.amount) for a in accs])
                
                wx.send_msg({
                    "touser": member.number,
                    "msgtype": "text",
                    "agentid": "2",
                    "text": {
                        "content": content
                    }
                })
            elif msg['EventKey'] == 'CHARGE':
                wx.send_msg({
                    "touser": member.number,
                    "msgtype": "text",
                    "agentid": "2",
                    "text": {
                        "content": u'您好，班费充值可以充值到支付宝账户 buaamba1404@163.com 名称校验“田淼”。目前是人工处理，充值后12小时内到班费中。谢谢'
                    }
                })

        return HttpResponse('')
    