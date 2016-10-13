#!/usr/bin/evn python
# coding:utf-8
from RequestsLibrary.RequestsKeywords import RequestsKeywords
from robot.libraries.BuiltIn import BuiltIn
import StringIO

# import xlrd
# import xlutils.copy
# import struct
# import time
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys


class ResultData:
    projectid = None
    projectname = None
    address = None
    appraisalpurpose = None
    appraisaltype = None
    propertytype = None
    trustno = None
    reportnumber = None
    reportwriterusserid = None
    waicaiid = None
    reportwritertime = None
    reportstatus = None
    calctemplatename = None
    calctemplateid = None
    reporttemplatename = None
    reporttemplateid = None
    success = None


class ReportRequests(object):
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.requestlibrary = RequestsKeywords()
        self._result_data = ResultData()
        self._builtin = BuiltIn()

    def create_session(self, user_name, url):
        self._headers = {'Content-Type': r'text/xml', 'charset': 'utf-8'}
        self._cookies = {'UsersCookies': '{"UserName":"%s","IsAuthenticated":true}' % user_name}
        self.requestlibrary.create_session('report', url, headers=self._headers,
                                           cookies=self._cookies)

    def _get_status(self, project_no):
        data = r'''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <SOAP-ENV:Body>
                        <tns:WSMethod xmlns:tns="http://tempuri.org/">
                            <tns:inputDTOXML>
                                <![CDATA[
                                    <WSInputDTO>
                                        <Command>
                                            <CommandName>GetReportInfoByTrustNo</CommandName>
                                            <IsAsynchronous>false</IsAsynchronous>
                                        </Command>
                                        <Paging>
                                            <IsPaging>false</IsPaging>
                                            <PageIndex>1</PageIndex>
                                            <Pages>0</Pages>
                                            <PageSize>10</PageSize>
                                            <RecordCount>0</RecordCount>
                                        </Paging>
                                        <Parameter>
                                            <File />
                                            <Params>
                                                <tno>%s</tno>
                                            </Params>
                                        </Parameter>
                                        <Security>
                                            <Content>b0lN</Content>
                                            <IsAuthenticated>false</IsAuthenticated>
                                        </Security>
                                    </WSInputDTO>
                                ]]>
                            </tns:inputDTOXML>
                        </tns:WSMethod>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>''' % project_no
        response = self.requestlibrary.post_request('report', r'/WebService/PeacockReportWS.asmx', data=data)
        self._format_response(response, 0)
        if self._result_data.success == 'true':
            if self._result_data.trustno == project_no:
                self._builtin.log('====GetReportInfoByTrustNo:Report is created!====')
                return 1  # 查询到项目编号，说明报告已经创建过了
            else:
                self._builtin.log('====GetReportInfoByTrustNo:Report is not created!====')
                return 0  # 报告未创建
        else:
            self._builtin.log('====Get ReportInfo By TrustNo Fail!====')
            self._builtin.log(response.content)
            return -1  # 请求服务失败

    def _format_response(self, response, get_status_only=1):
        try:
            root = ET.fromstring(response.content)
        except Exception, e:
            print e
            sys.exit(1)
        # 获取返回的xml
        result_xml = root[0][0][0].text

        try:
            utf8_parser = ET.XMLParser(encoding='utf-8')
            tree = ET.parse(StringIO.StringIO(result_xml.encode('utf-8')), parser=utf8_parser)
            root = tree.getroot()
        except Exception, e:
            print e
            sys.exit(1)

        data = root.iter('Success')
        try:
            self._result_data.success = data.next().text
        except StopIteration:
            self._result_data.success = None

        if self._result_data.success == 'true' and get_status_only == 0:
            data = root.iter('ProjectId')
            try:
                self._result_data.projectid = data.next().text
            except StopIteration:
                self._result_data.projectid = None

            data = root.iter('ProjectName')
            try:
                self._result_data.projectname = data.next().text
            except StopIteration:
                self._result_data.projectid = None

            data = root.iter('Address')
            try:
                self._result_data.address = data.next().text
            except StopIteration:
                self._result_data.address = None

            data = root.iter('AppraisalPurpose')
            try:
                self._result_data.appraisalpurpose = data.next().text
            except StopIteration:
                self._result_data.appraisalpurpose = None

            data = root.iter('AppraisalType')
            try:
                self._result_data.appraisaltype = data.next().text
            except StopIteration:
                self._result_data.appraisaltype = None

            data = root.iter('PropertyType')
            try:
                self._result_data.propertytype = data.next().text
            except StopIteration:
                self._result_data.propertytype = None

            data = root.iter('TrustNo')
            try:
                self._result_data.trustno = data.next().text
            except StopIteration:
                self._result_data.trustno = None

            data = root.iter('ReportNumber')
            try:
                self._result_data.reportnumber = data.next().text
            except StopIteration:
                self._result_data.reportnumber = None

            data = root.iter('ReportWriterUsserId')
            try:
                self._result_data.reportwriterusserid = data.next().text
            except StopIteration:
                self._result_data.reportwriterusserid = None

            data = root.iter('WaiCaiId')
            try:
                self._result_data.waicaiid = data.next().text
            except StopIteration:
                self._result_data.waicaiid = None

            data = root.iter('ReportWriterTime')
            try:
                self._result_data.reportwritertime = data.next().text
            except StopIteration:
                self._result_data.reportwritertime = None

            data = root.iter('ReportStatus')
            try:
                self._result_data.reportstatus = data.next().text
            except StopIteration:
                self._result_data.reportstatus = None

            data = root.iter('CalcTemplateName')
            try:
                self._result_data.calctemplatename = data.next().text
            except StopIteration:
                self._result_data.calctemplatename = None

            data = root.iter('CalcTemplateId')
            try:
                self._result_data.calctemplateid = data.next().text
            except StopIteration:
                self._result_data.calctemplateid = None

            data = root.iter('ReportTemplateName')
            try:
                self._result_data.reporttemplatename = data.next().text
            except StopIteration:
                self._result_data.reporttemplatename = None

            data = root.iter('ReportTemplateId')
            try:
                self._result_data.reporttemplateid = data.next().text
            except StopIteration:
                self._result_data.reporttemplateid = None

    def _create_report(self, project_no, report_no):
        data = u'''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <SOAP-ENV:Body>
                        <tns:WSMethod xmlns:tns="http://tempuri.org/">
                            <tns:inputDTOXML>
                                <![CDATA[
                                    <WSInputDTO>
                                        <Command>
                                            <CommandName>CreateReport</CommandName>
                                            <IsAsynchronous>false</IsAsynchronous>
                                        </Command>
                                        <Paging>
                                            <IsPaging>false</IsPaging>
                                            <PageIndex>1</PageIndex>
                                            <Pages>0</Pages>
                                            <PageSize>10</PageSize>
                                            <RecordCount>0</RecordCount>
                                        </Paging>
                                        <Parameter>
                                            <File />
                                            <Params>
                                                <atype>23</atype>
                                                <cid>31289</cid>
                                                <name></name>
                                                <ptype>25</ptype>
                                                <purpose>20</purpose>
                                                <rid>1586</rid>
                                                <rnumber>%s</rnumber>
                                                <tid>1585</tid>
                                                <trustno>%s</trustno>
                                            </Params>
                                        </Parameter>
                                        <Security>
                                            <Content>b0lN</Content>
                                            <IsAuthenticated>false</IsAuthenticated>
                                        </Security>
                                    </WSInputDTO>
                                ]]>
                            </tns:inputDTOXML>
                        </tns:WSMethod>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>''' % (report_no, project_no)
        self._builtin.log('=============================================================')
        response = self.requestlibrary.post_request('report', r'/WebService/PeacockReportWS.asmx', data=data)
        self._format_response(response)
        if self._result_data.success == 'true':
            self._builtin.log('====Create Report Success!====')
            return 1
        else:
            self._builtin.log('====Create Report Fail!====')
            self._builtin.log(response.content)
            return 0

    def _generate_report(self, project_id, report_template_id):
        data = r'''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <SOAP-ENV:Body>
                        <tns:WSMethod xmlns:tns="http://tempuri.org/">
                            <tns:inputDTOXML>
                                <![CDATA[
                                    <WSInputDTO>
                                        <Command>
                                            <CommandName>GenerateReport</CommandName>
                                            <IsAsynchronous>false</IsAsynchronous>
                                        </Command>
                                        <Paging>
                                            <IsPaging>false</IsPaging>
                                            <PageIndex>1</PageIndex>
                                            <Pages>0</Pages>
                                            <PageSize>10</PageSize>
                                            <RecordCount>0</RecordCount>
                                        </Paging>
                                        <Parameter>
                                            <File />
                                            <Params>
                                                <pid>%s</pid>
                                                <rid>%s</rid>
                                            </Params>
                                        </Parameter>
                                        <Security>
                                            <Content>b0lN</Content>
                                            <IsAuthenticated>false</IsAuthenticated>
                                        </Security>
                                    </WSInputDTO>
                                ]]>
                            </tns:inputDTOXML>
                        </tns:WSMethod>
                    </SOAP-ENV:Body>
                </SOAP-ENV:Envelope>''' % (report_template_id, project_id)
        response = self.requestlibrary.post_request('report', r'/WebService/PeacockReportWS.asmx', data=data)
        self._format_response(response)
        if self._result_data.success == 'true':
            self._builtin.log('====Generate Report Success!====')
            return 1
        else:
            self._builtin.log('====Generate Report Fail!====')
            self._builtin.log(response.content)
            return 0

    # def _updata_excel(self):
    #     data = xlrd.open_workbook(u'住宅测算表20150830.xls')
    #     wb = xlutils.copy.copy(data)
    #     # print  help(wb)
    #     table = wb.get_sheet(11)
    #     timeStamp = int(time.time())
    #     timeArray = time.localtime(timeStamp)
    #     otherStyleTime = time.strftime("%Y%m%d%H%M%S", timeArray)
    #     table.write(2, 2, otherStyleTime)
    #     wb.save(u'住宅测算表20150830.xls')
    #
    # def _upload_excel(self):
    #     # 实现Excel上传
    #     print '1212'

    def write_report(self, project_no, report_no):
        is_created = self._get_status(project_no)
        if is_created == 0:
            self._create_report(project_no, report_no)
            self._get_status(project_no)
            self._generate_report(self._result_data.projectid, self._result_data.reporttemplateid)
        elif is_created == 1:
            self._generate_report(self._result_data.projectid, self._result_data.reporttemplateid)
        else:
            sys.exit(0)


if __name__ == '__main__':
    rr = ReportRequests()
    rr.create_session('李楠', r'http://reporttest.yunfangdata.com')
    rr.write_report('5046201622', '201606011234')
