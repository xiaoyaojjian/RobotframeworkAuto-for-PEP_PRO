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
        if isinstance(value, (str, unicode)):
            # 如果是字符串或unicode字符则清空首尾的空格
            value = value.strip()
        pep.set_value(key, value)

    def set_kanfang_value(self, pep, contacts, phone):
        """设置看房人信息，contacts为看房联系人名称，phone为看房联系人手机."""
        watch_info_list = pep.get_value(u'看房联系人信息')
        watch_info = {u'姓名': contacts, u'手机': phone}
        if watch_info_list == '':
            pep.set_value(u'看房联系人信息', [watch_info])
        else:
            watch_info_list.append(watch_info)
            pep.set_value(u'看房联系人信息', watch_info_list)

    def set_kuaidi_value(self, pep, receiver, phone, company,
                         address, postcode):
        """
        设置快递收件人信息，receiver为收件人姓名, phone为联系方式,
        company为公司, address为地址, postcode为邮政编码.
        """
        receipt_info_list = pep.get_value(u'快递信息')
        receipt_info = {u'姓名': receiver, u'联系方式': phone,
                        u'公司': company, u'地址': address, u'邮政编码': postcode}
        if receipt_info_list == '':
            pep.set_value(u'快递信息', [receipt_info])
        else:
            receipt_info_list.append(receipt_info)
            pep.set_value(u'快递信息', receipt_info_list)

    def clean_pep_list(self, pep):
        """清空pep对象里的list数据
        """
        pep.set_value(u'快递信息', [])
        pep.set_value(u'看房联系人信息', [])

    def get_list_Count(self, Heir):
        """输入框最大输入个数"""
        m = list(str(Heir)).__len__()
        return m
		
    	
    def return_list(self,NO_list,para):
        """存储随机选择项目的流水号"""
        NO_list.append(para)
        return NO_list
		
    def return_list_count(self,NO_list):
        """返回列表个数"""
        list_count = NO_list.__len__()
        return list_count
		
    def return_string_strip(self,string):
        """清除字符末尾为空的字符串"""
        strip_string = string.strip()
        return strip_string
