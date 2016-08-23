#!/usr/bin/env python
#_*_ coding:utf-8 _*_

class PepObject:
    def __init__(self):
        self.pep_project = {}
        self.__conf()

    def get_value(self, name):
        if name in self.pep_project:
            return self.pep_project[name]
        else:
            return ''  # 如果没有找到这个值，返回空

    def set_value(self, name, value):
        if (value != '' or value is not None) and name in self.__key_set:
            self.pep_project[name] = value

    def __str__(self):
        return self.get_value(u'流水号')

    def __conf(self):
        self.__key_set = set([u'流水号', u'报告号'])

        # 客户信息
        customer_info = [u'客户手机', u'固定电话', u'客户姓名', u'所属机构', u'分支机构', u'客户QQ']
        self.__key_set.update(customer_info)

        # 项目信息
        project_info = [u'项目来源', u'项目类型', u'项目分类', u'估价目的', u'物业类型', u'子物业类型', u'报告类型', u'发送份数', u'城市', u'行政区', u'小区名',
                        u'小区地址', u'楼栋号', u'单元号', u'户号名', u'项目地址', u'建筑面积', u'土地面积', u'询值单价', u'询值总价', u'建成年代', u'紧急程度',
                        u'贷款机构', u'贷款支行', u'期贷信息', u'估价委托方', u'所属部门', u'立项备注', u'线上信息']
        self.__key_set.update(project_info)

        # 收费信息
        free_info = [u'市场负责人', u'收费责任人', u'内部报单人', u'结算方式', u'应收金额', u'收费方式', u'公司帐号', u'票据类型', u'(普票)发票抬头', u'(专票)名称',
                     u'(专票)纳税人识别号', u'(专票)开户行', u'(专票)账号', u'(专票)地址', u'(专票)电话']
        self.__key_set.update(free_info)

        # 勘查事项
        live_search_info = [u'是否勘查', u'预收费用', u'资料提供方式', u'看房联系人信息',u'看房联系人', u'联系人电话']
        self.__key_set.update(live_search_info)

        # 收件信息
        receipt_info = [u'收取方式', u'收件人姓名', u'收件人联系方式', u'收件人公司', u'收件人地址', u'收件人邮政编码']
        self.__key_set.update(receipt_info)
