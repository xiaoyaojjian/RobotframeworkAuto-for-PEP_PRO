# encoding: utf-8
# !/usr/bin/env python
# Filename: TestDataLib.py

import MySQLdb
import os, sys
import random, types
from robot.libraries.BuiltIn import BuiltIn


class TestDataLib:
    conn = ''
    cursor = ''

    def __init__(self, host='192.168.14.38', user='root', password='gh001', db='robot_result'):
        try:
            self.conn = MySQLdb.connect(host, user, password, db, charset='utf8')
        except Exception, e:
            print e
            sys.exit()
        self.cursor = self.conn.cursor()

    def _query(self, sql):
        return self.cursor.execute(sql)

    def _show(self):
        return self.cursor.fetchall()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def _get_test_data(self, case_name, data_name):
        """根据数据名称和用例名获取数据列表，返回一个List
        """
        strsql = 'SELECT '
        for index in range(len(data_name)):
            if index == len(data_name) - 1:
                strsql = strsql + ' max(if(dataName=\'' + data_name[index] + '\',dataContent,\'\'))'
            else:
                strsql = strsql + ' max(if(dataName=\'' + data_name[index] + '\',dataContent,\'\')),'
        strsql = strsql + ' FROM dict_test_data td WHERE EXISTS ( SELECT 1 FROM dict_test_case tc  WHERE tc.id = td.caseId AND tc.caseName = \'' + case_name + '\')'
        strsql = strsql + ' GROUP BY groupid'
        print strsql
        self._query(strsql)
        data = self._show()
        return data

    def run_keyword_by_testdata(self, caseName, keywordName, *dataName):
        """根据用例名称去查询数据库，获取测试数据，并运行指定关键字
            参数说明：caseName<数据库测试数据的用例名>
                      keywordName<需要运行的关键字名称>
                      dataName<数据库中测试数据的中文名称>
            例子：
            | Run Keyword By Testdata | 用例名称 | 某个关键字 | 参数名称1 | 参数名称2 | 参数名称3 | 参数名称4 |
        """
        data = self._get_test_data(caseName, list(dataName))
        bi = BuiltIn()
        for i in data:
            args = tuple(i)
            return bi.run_keyword_and_continue_on_failure(keywordName, *args)

    def run_keyword_by_testdata_return_dict(self, caseName, getValueType, keywordName, *dataName):
        """根据用例名称去查询数据库，获取测试数据，并返回一个字典类型给指定关键字
            参数说明：caseName<数据库测试数据的用例名>
                      getValueType<获取数据的方式：0-全部数据，-1-随机获取一条记录(该模式有可以传出返回值)，n-随机获取n条记录>
                      keywordName<需要运行的关键字名称,该关键字只能接收字典类的参数>
                      dataName<数据库中测试数据的中文名称>
            例子：
            | Run Keyword By Testdata | 用例名称 | -1 | 某个关键字 | 参数名称1 | 参数名称2 | 参数名称3 | 参数名称4 |
        """
        bi = BuiltIn()
        if isinstance(getValueType, int) is False:
            bi.log("传入的getValueType不是int类型，请输入正确的值！")
        dataNameList = list(dataName)
        data = self._get_test_data(caseName, dataNameList)

        # 随机获取一条记录
        if getValueType == -1:
            args = {}
            i = random.choice(data)
            for j in range(len(dataNameList)):
                args[dataNameList[j]] = i[j]
            return bi.run_keyword_and_continue_on_failure(keywordName, args)

        # 如果是0或大于表格的数量，则取数据的最大值
        if getValueType == 0 or getValueType > len(data):
            get_row_count = len(data)
        else:
            get_row_count = getValueType
        for i in random.sample(data, get_row_count):
            args = {}
            for j in range(len(dataNameList)):
                args[dataNameList[j]] = i[j]
            bi.run_keyword_and_continue_on_failure(keywordName, args)

    def run_keyword_by_testdata_return_keyvalue(self, caseName, getValueType, keywordName, *dataName):
        """根据用例名称去查询数据库，获取测试数据，并运行指定关键字
            参数说明：caseName<数据库测试数据的用例名>
                      getValueType<获取数据的方式：0-全部数据，-1-随机获取一条记录(该模式有可以传出返回值)，n-随机获取n条记录>
                      keywordName<需要运行的关键字名称,该关键字只能接收字典类的参数>
                      dataName<数据库中测试数据的中文名称>
            例子：
            | Run Keyword By Testdata | 用例名称 | -1 | 某个关键字 | 参数名称1 | 参数名称2 | 参数名称3 | 参数名称4 |
        """
        bi = BuiltIn()
        dataNameList = list(dataName)
        data = self._get_test_data(caseName, dataNameList)

        # 随机获取一条记录
        if int(getValueType) == -1:
            args = []
            i = random.choice(data)
            for j in range(len(dataNameList)):
                if i[j] != '':
                    args.append(dataNameList[j] + '=' + i[j])
                else:
                    args.append(dataNameList[j] + '=None')
            return bi.run_keyword_and_continue_on_failure(keywordName, *args)

        # 如果是0或大于表格的数量，则取数据的最大值
        get_row_count = int(getValueType)
        if int(getValueType) == 0 or int(getValueType) > len(data):
            get_row_count = len(data)

        for i in random.sample(data, get_row_count):
            args = []
            for j in range(len(dataNameList)):
                if i[j] != '':
                    args.append(dataNameList[j] + '=' + i[j])
                else:
                    args.append(dataNameList[j] + '=None')
            bi.run_keyword_and_continue_on_failure(keywordName, *args)


if __name__ == '__main__':
    td = TestDataLib()
    '''data = td.get_test_data('线上业务',['流水号','交易编号','物业地址'])
    for i in data:
        print i[2]
    #print data'''
    # td.run_keyword_by_testdata('线上业务','name','流水号','交易编号','物业地址')
