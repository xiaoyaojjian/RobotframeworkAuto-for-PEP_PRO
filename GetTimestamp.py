# encoding: utf-8
import time

class GetTimestamp:

    def getStamp(self,inputDate):
        """
        通过输入一个类似2007-01-02格式的字符串，返回一个时间长度
        """
        #强制转为字符串
        if(isinstance(inputDate,str)==False):
            inputDate=str(inputDate)
        # 将其转换为时间数组
        timeArray = time.strptime(inputDate, "%Y-%m-%d")

        # 转换为时间戳
        timeStamp = int(time.mktime(timeArray))

        return timeStamp

