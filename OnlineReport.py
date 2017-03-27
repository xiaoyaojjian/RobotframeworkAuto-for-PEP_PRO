# encoding: utf-8
import base64
import httplib
import re
import traceback
import urlparse

import xlwt
from jpype import *

import requests
import xlrd
from xlutils.copy import copy
from robot.output import librarylogger

class OnlineReport:
    _trustno = None
    _rnumber = None
    _strWsdl = None
    _host = None
    _postName = None
    _username = None
    _cookie = None
    _ContentType = "text/xml; charset=utf-8"
    _ppid = None
    _message = None
    _basePath=None
    _pid=None
    _saveUrl=None
    _calcTableMsg=None
    _jvmPath=None

    def initInfo(self , trustno , rnumber , strWsdl , username,basePath,jvmPath):
        """
        trustno：流水号
        rnumber：报告号
        strWsdl:wsdl的完整url,如http://reporttest2.yunfangdata.com:81/self._webservice/PeacockReportWS.asmx?WSDL
        username:设置登录用户
        basePath：文件所在的父目录
        jvmpath:1.6jdk根目录
       """
        self._rnumber = rnumber
        self._trustno = trustno
        self._strWsdl = strWsdl
        self._username = username
        self._cookie = "UsersCookies= {\"UserName\": \"%s\",  \"IsAuthenticated\": true}" % (username)
        self._splitUrl ( )
        self._basePath=basePath
        self._jvmPath=jvmPath

    def _getSoapMessage(self , xmlName):
        try:
            f = open ( self._basePath+"/"+xmlName , 'r' )
            lines = f.readlines ( )
            f.close ( )
            SoapMessage = ''.join ( lines )
            return SoapMessage
        except IOError , e:
            librarylogger.info ( "Fail to open the file: %s" % (self._basePath+"/"+xmlName))

    def _splitUrl(self):
        temp = urlparse.urlsplit ( self._strWsdl )
        self._host = temp[1]
        self._postName = temp[2]

    def _getReportInfoByTrustNo(self,xmlName):
        '''根据流水后获取生成报告需要的rid'''
        msg =self._send_message(xmlName)
        result = msg.replace ( "&lt;" , "<" ).replace ( "&gt;" , ">" )
        if(result.find("抵押标准版正式报告")!=-1):
            librarylogger.info(u'获取pid成功')
        else:
            librarylogger.info(u'获取Pid出错')
        detepatProjectId = re.compile ( '<ProjectId>(.+)</ProjectId>' )
        pid=detepatProjectId.findall(result)[0]
        self._pid=pid
        #生成pid后给属性_saveUrl初始化值
        self._saveUrl="http://reporttest2.yunfangdata.com:81/zzOffice/SaveFile.aspx?Id=%s&calcTemplateID=2782&DocType=xls" %self._pid
    def _generate_report(self,xmlName):
        '''生成报告'''
        librarylogger.info (u'估价辅助系统正在对%s生成报告' % self._trustno )
        msg =self._send_message(xmlName )
        result = msg.replace ( "&lt;" , "<" ).replace ( "&gt;" , ">" )
        detepatScuccess = re.compile ( '<Success>(.+)</Success>' )
        success_result = detepatScuccess.findall ( result )[0]
        if (success_result == "true"):
            librarylogger.info ( u'估价辅助系统生成项目%s报告成功' % self._trustno )
        else:
            librarylogger.info ( "估价辅助系统生成项目%s报告失败" %self._trustno )


    def createReport(self , xmlName):
        '''传入create_Report.xml文件名称，不是路径'''
        librarylogger.info ( u'估价辅助系统正在关联内业报告' )
        msg =self._send_message(xmlName )
        result = msg.replace ( "&lt;" , "<" ).replace ( "&gt;" , ">" )
        detepatScuccess = re.compile ( '<Success>(.+)</Success>' )
        success_result = detepatScuccess.findall ( result )[0]

        if (success_result == "true"):
            librarylogger.info ( u'估价辅助系统关联内业项目成功' )
        else:
            if (result.find("报告已创建，请刷新浏览器")!=-1):
                librarylogger.info ( u'报告已创建，请刷新浏览器' )
            else:
                librarylogger.info ( u'估价辅助系统关联报告失败' )
        self._getReportInfoByTrustNo("GetReportInfoByTrustNo.xml")
        librarylogger.info ( u'开始上传计算表' )
        try:
            result =self._save_file(self._basePath)
            if(result==200):
                librarylogger.info ( u'计算表上传完毕' )
            else:
                librarylogger.info ( u'计算表上传失败' )
        except Exception ,e:
            print "上传计算表出错"
        self._generate_report("generate_report.xml")



    def _set_message(self , xmlName):

        if(xmlName=="create_report.xml"):
            SoapMessage = self._getSoapMessage (xmlName )
            SoapMessage = SoapMessage % (self._rnumber , self._trustno)

        elif(xmlName=="GetReportInfoByTrustNo.xml"):
            SoapMessage = self._getSoapMessage (xmlName )
            SoapMessage = SoapMessage % self._trustno
        elif(xmlName=="save.xml"):
             SoapMessage = self._getSoapMessage (xmlName )
             SoapMessage = SoapMessage %  self._calcTableMsg
        else:
            SoapMessage = self._getSoapMessage (xmlName )
            SoapMessage = SoapMessage % self._pid

        self._message = SoapMessage


    def _send_message(self , xmlName):
        self._set_message(xmlName)
        librarylogger.info(u'开始发送请求头文件')
        webservice = httplib.HTTP(self._host)
        webservice.putrequest("POST" , self._postName)
        webservice.putheader("Host" , self._host)
        webservice.putheader("Content-Type" , self._ContentType)
        webservice.putheader("Content-length" , "%d" % len ( self._message))
        webservice.putheader("SOAPAction" , "\"http://tempuri.org/WSMethod\"")
        webservice.putheader("Cookie" , self._cookie)
        # 发送空行到服务器，指示header的结束
        webservice.endheaders( )
        librarylogger.info(u'头文件发送完成')
        librarylogger.info(u'开始发送请求data')
        webservice.send(self._message)
        webservice.getreply()
        msg = webservice.getfile().read()
        if(msg!=None and len(msg)>0):
             librarylogger.info(u'请求数据发送完成并成功响应')
        return msg

    def _update_excel(self,parent_path):
        '''更新计算表的报告编号'''
        rb=xlrd.open_workbook(parent_path+"/test.xls",formatting_info=True)
        wb =copy(rb)
        summary = wb.get_sheet(11)#汇总表
        basemessage=wb.get_sheet(1)#基础信息
        protection=xlwt.Protection()
        protection.cell_locked=0
        cellStyle1=xlwt.easyxf("protection:cell_locked false;")
        cellStyle2=xlwt.XFStyle()

        librarylogger.info(u"开始修改汇总表中的报告编号")
        try:
            summary.write(2, 2, u'仁达房（土）估字第'+self._rnumber+u'号')
            librarylogger.info(u"修改汇总表中的报告编号成功")
            basemessage.write(7,1,self._rnumber,cellStyle1)
            librarylogger.info(u"修改基础信息表中的报告编号成功")
        except Exception, e:
            print traceback.format_exc()
            librarylogger.info(u"修改汇总表中的报告编号失败")
       
        wb.save(parent_path+"/test.xls")

    def _base64_encode(self,parent_path):
        '''对文件进行base64编码'''
        self._calcTableMsg=base64.b64encode(open(parent_path+"/test.xls",'rb').read())
        self._set_message("save.xml")
    def _save_file(self,parent_path):
        '''对计算表进行上传操作'''
        try:
            self._update_excel(parent_path)
            #self._set_Cell_Nolock()
            self._base64_encode(parent_path)
            result=requests.post(self._saveUrl,data=self._message)
            return result.status_code
        except Exception,e:
            print traceback.print_exc()
            print  e.message
    def _set_Cell_Nolock(self):
        '''通过调用jar包来实现excel单元格的取消锁定'''
        classpath=self._basePath+"/ExcelUpdate.jar"
        startJVM(self._jvmPath+"/jre/bin/server/jvm.dll","-ea","-Djava.class.path=%s" % classpath)
        try:
            javaClass =JClass("com.aoxiang.excel.ExcelStyleUpdate")
            javaInstance =javaClass()
            librarylogger.info(u"正在取消报告编号单元格锁定状态")
            javaInstance.setLock(self._basePath+"/test.xls")
            librarylogger.info(u"取消报告编号单元格锁定状态成功")
            shutdownJVM()
        except Exception,e:
            print traceback.format_exc()
            librarylogger.info(u"取消报告编号单元格锁定状态失败")

if __name__ == '__main__':
    test = OnlineReport ( )
    # D:/PEP/new/xmlFile/creat_report.xml
    # info=test.getSoapMessage("D:/PEP/new/xmlFile/creat_report.xml")
    #test.initInfo ( "472356088885" , "201701101088885","http://reporttest2.yunfangdata.com:81/WebService/PeacockReportWS.asmx?WSDL" , "李楠","D:/PEP/new/xmlFile" )
    # test.setNodeValue()
    # test.createReport ("create_report.xml")
    # test=OnlineReport()
    test.initInfo ( "490133306446" , "201701101000777","http://reporttest2.yunfangdata.com:81/WebService/PeacockReportWS.asmx?WSDL" , "李楠","D:/PEP/new/xmlFile","D:/jre1.6/jdk1.6.0_31_64" )
    test.createReport("create_report.xml")
    # a.update_excel("D:/PEP/new/xmlFile")
    #a.base64_encode("D:/PEP/new/xmlFile")
    #test.set_Cell_Nolock()
