# coding=utf-8
from xadmin import Settings

class Base(Settings):
    enable_themes = False
    use_bootswatch = False

class Comm(Settings):
    site_title = '北航MBA信息管理系统'
    site_footer = u'北航MBA14级4班 田淼'
    # menu_style = 'accordion'
    # globe_search_models = [Host, IDC]
    # globe_models_icon = {
    #     Host: 'laptop', IDC: 'cloud'
    # }

# class IndexView(Settings):
#     widgets = [
#         [
#             {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3><p>Github: <a href='https://github.com/sshwsfc/django-xadmin' target='_blank'>https://github.com/sshwsfc/django-xadmin</a></p><p>Join Online Group: <br/>QQ Qun : 282936295</p>"},
#             {"type": "chart", "model": "host.accessrecord", 'chart': 'user_count', 'params': {'_p_date__gte': '2013-01-08', 'p': 1, '_p_date__lt': '2013-01-29'}},
#             {"type": "list", "model": "host.host", 'params': {'o':'-guarantee_date'}},
#         ],
#         [
#             {"type": "qbutton", "title": "Quick Start", "btns": [{'model': Host}, {'model':IDC}, 
#                 {'title': "Github", 'url': "https://github.com/sshwsfc/django-xadmin", 'icon': 'github'},
#                 {'title': "Help Translate", 'url': "http://trans.xadmin.io", 'icon': 'flag'}]},
#             {"type": "addform", "model": MaintainLog},
#         ]
#     ]