#!/usr/bin/env python
# _*_ coding:utf-8 _*_


from PepObject import PepObject
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class PepExt:
    def create_pep_object(self):
        """创建评E评对象，用于存储评E评系统键值对."""
        return PepObject()

    def set_pep_value(self, pep, key, value):
        """设置传入的pep对象的键值信息."""
        pep.set_value(key, value)

    def set_kanfang_value(self, pep, contacts, phone):
        """设置看房人信息，contacts为看房联系人名称，phone为看房联系人手机."""
        watch_info_list = pep.get_value(u'看房联系人信息')
        watch_info = {u'姓名': contacts, u'手机': phone}
        if watch_info_list == '':
            pep.set_value(u'看房联系人信息', [watch_info])
        else:
            pep.set_value(u'看房联系人信息', watch_info_list.append(watch_info))

    def get_list_Count(self, Heir):
        """输入框最大输入个数"""
        m = list(str(Heir)).__len__()
        return m
