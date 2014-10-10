# -*- coding: utf8
import xml.etree.ElementTree as ET
from WXBizMsgCrypt import WXBizMsgCrypt

class WeiXin(WXBizMsgCrypt):

    def DecryptMsg(self, sPostData, sMsgSignature, sTimeStamp, sNonce):
        ret, msg = super(WeiXin, self).DecryptMsg(sPostData, sMsgSignature, sTimeStamp, sNonce)
        return ret, (ret==0 and self.to_json(msg) or msg)

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

    def _to_tag(self, k):
        return ''.join([w.capitalize() for w in k.split('_')])

    def _cdata(self, data):
        '''http://stackoverflow.com/questions/174890/how-to-output-cdata-using-elementtree
        '''
        if type(data) is str:
            return '<![CDATA[%s]]>' % data.replace(']]>', ']]]]><![CDATA[>')
        return data

    def to_xml(self, **kwargs):
        xml = '<xml>'
        for k in kwargs.iterkeys():
            v = kwargs[k]
            tag = self._to_tag(k)
            xml += '<%s>%s</%s>' % (tag, self._cdata(v), tag)
        xml += '</xml>'
        return xml
