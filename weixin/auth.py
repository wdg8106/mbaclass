
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

import httplib, json
from .pyweixin import wx

getUserInfoUri = '/cgi-bin/user/getuserinfo?access_token=%s&code=%s&agentid=%d'

class WeiXinAuthenticationMiddleware(object):

    def process_request(self, request):
        if request.user and request.user.is_authenticated():
            return

        if request.GET.get('code') and request.GET.get('state') == '0':
            user = auth.authenticate(wx_code=request.GET['code'])
            auth.login(request, user)


class WeiXinModelBackend(ModelBackend):

    def authenticate(self, wx_code=None, **kwargs):
        # weixin login
        UserModel = get_user_model()
        try:
            httpClient = httplib.HTTPSConnection('qyapi.weixin.qq.com', 443, timeout=30)
            httpClient.request('GET', getUserInfoUri % (wx.token('sendMsg'), wx_code, 1))
         
            response = httpClient.getresponse()
            userId = json.loads(response.read())['UserId']

            user = UserModel._default_manager.get_by_natural_key(userId)
            return user
        except UserModel.DoesNotExist:
            return None
        except Exception, e:
            print e
            return None

