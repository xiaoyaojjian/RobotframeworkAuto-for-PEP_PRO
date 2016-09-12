# encoding: utf-8
# !/usr/bin/env python
from robot.libraries.BuiltIn import BuiltIn


class PepObject:
    def __init__(self):
        self.pep_project = {}
        self.__conf()
        self.__builtin = BuiltIn()

    def get_value(self, name):
        if name in self.pep_project:
            return self.pep_project[name]
        else:
            return ''  # 如果没有找到这个值，返回空

    def set_value(self, name, value):
        if (value != '' and value is not None) and name in self.__key_set:
            self.pep_project[name] = value
            if isinstance(value,(int,str,unicode)):
                self.__builtin.log(u'将\'' + name + u'\'的值：\'' + value + '\'插入PEP对象', level='INFO')
            else:
                self.__builtin.log(u'将\'' + name + u'\'的非字符串的值插入PEP对象', level='INFO')
        elif name not in self.__key_set:
            self.__builtin.log(u'字段名：' + name + u' 没有定义,不能存储在PEP对象中！', level='WARN')

    # def __str__(self):
    #    return self.get_value(u'流水号')

    def __conf(self):
        self.__key_set = set([u'流水号', u'报告号'])

        # 客户信息
        customer_info = [u'客户手机', u'固定电话', u'客户姓名', u'所属机构', u'分支机构', u'客户QQ',u'机构全称']
        self.__key_set.update(customer_info)
		
        # 估值信息
        Valuation_info = [u'所在楼层',u'总楼层',u'朝向',u'户型',u'房屋类型',u'装修情况',u'特殊因素',
						u'询价来源',u'市场人员',u'备注',u'询价地址',u'修正单价',u'抵押单价',u'抵押总价',u'市场单价',u'市场总价',u'系统价格单价',u'系统价格总价',u'抵押价值区间单价最小',u'抵押价值区间单价最大',u'抵押价值区间总价最小',u'抵押价值区间总价最大',u'价格差异说明',u'物业类型',u'项目分类',u'估价委托人',u'估价目的',u'价值时点',
						u'评估方法',u'评估模板',u'评估单价(元)',u'评估总价(万元)',u'总价大写'
		]
        self.__key_set.update(Valuation_info)
		
        # 项目来源
        #Project_Source = [u'所属机构',u'分支机构',u'客户姓名',u'客户手机',u'机构全称']
		#self.__key_set.update(Project_Source)
		
		#项目负责人
        Project_leader = [u'询价人员',u'估价师',u'证书名称',u'证书证号',u'建筑结构',u'使用权来源',u'权属性质',
						u'土地用途',u'使用期限',u'地号',u'图号',u'土地摊分面积',u'房屋朝向',u'上落设施',u'其他权限情况',u'特殊事项说明',u'特殊事项说明'
		
		]
        self.__key_set.update(Project_leader)
		

        # 项目信息
        project_info = [u'项目来源', u'项目类型', u'项目分类', u'估价目的', u'物业类型', u'子物业类型', u'报告类型', u'发送份数', u'城市', u'行政区', u'小区名',u'小区名称',
                        u'小区地址', u'楼栋号', u'单元号', u'户号名', u'项目地址', u'建筑面积', u'土地面积', u'询值单价', u'询值单价(元/m²)', u'询值总价',u'询值总价(万元)',u'询价机构',u'询价人',
						u'询值单价最小', u'询值单价最大',u'询值总价最小',u'询价时间',u'询价来源',u'立项',
						u'询值总价最大',u'建成年代', u'紧急程度',u'贷款机构', u'贷款支行', u'期贷信息', u'估价委托方', u'所属部门', u'立项备注', u'线上信息', u'询价添加人']
        self.__key_set.update(project_info)

        # 收费信息
        free_info = [u'市场负责人', u'收费责任人', u'内部报单人', u'结算方式', u'应收金额', u'收费方式', u'公司帐号', u'票据类型', u'(普票)发票抬头', u'(专票)名称',
                     u'(专票)纳税人识别号', u'(专票)开户行', u'(专票)账号', u'(专票)地址', u'(专票)电话']
        self.__key_set.update(free_info)

        # 勘查事项,其中‘看房联系人信息’为一个list
        live_search_info = [u'是否勘查', u'预收费用', u'资料提供方式', u'看房联系人信息', u'看房联系人', u'联系人电话']
        self.__key_set.update(live_search_info)

        # 收件信息,其中‘快递信息’为一个list
        receipt_info = [u'收取方式', u'收件人姓名', u'收件人联系方式', u'收件人公司', u'收件人地址', u'收件人邮政编码', u'快递信息']
        self.__key_set.update(receipt_info)
        
        # 外业信息
        waicai_info = [u'查勘人员', u'查勘表', u'加急金额']
        self.__key_set.update(waicai_info)
        
        # 内业信息
        inwork_info = [u'撰写人员']
        self.__key_set.update(inwork_info)
