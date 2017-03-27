#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests

from robot.libraries.BuiltIn import BuiltIn
import time
from PIL import Image,ImageEnhance,ImageFile,ImageDraw,ImageFont
from time import ctime

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

class repositoryimage:
    def create_new(self,Request_the_address,Local_initial_address):
        url = Request_the_address
        files = {'file': (open(Local_initial_address, 'rb'))}

        r = requests.post(url, files=files)
        a = r.text.split(":")
        serialnumber = a[3].split(',')[0].strip('"').encode('utf-8')
        print type(serialnumber)
        # print(r.status_code, r.headers['Content-Type'], r.encoding, r.text)
        if r.status_code != 200:
            return BuiltIn().log(u"\"%s\"报错" % (r.status_code,), level='ERROR')

        else:
            return u'成功', serialnumber

    def upload_pictures(self,Local_initial_address,i, local_store_address, Request_the_address,addr):
        """
            需要传参：
                Local_initial_address：第一个是图片初始路劲
                local_store_address：第二个图片的保存路劲（文件名称）
                Request_the_address：请求服务器地址，需要IP地址
                addr：URL参数
        """
        new_image = repositoryimage().img(Local_initial_address, i, local_store_address)
        print new_image
        nwi = new_image[0].split('\\')[-1]
        print nwi
        url = Request_the_address + addr
        mu = repositoryimage().create_new(url, new_image)
        return mu

    def show_upload_result(self,Request_the_address,addr1,par,addr2):
        """
            需要传参：
                par：id号
                Request_the_address：请求服务器地址，需要IP地址
                addr：URL参数
        """
        url = Request_the_address + addr1 + par +addr2
        r = requests.get(url)
        print(r.status_code, r.headers['Content-Type'], r.encoding, r.text)


    def select_data(self,Request_the_address):
        url = Request_the_address
        r = requests.get(url)
        print(r.status_code, r.headers['Content-Type'], r.encoding, r.text)

    def img(self, Local_initial_address, i, local_store_address):
        print Local_initial_address, i, local_store_address
        # tt = u'lvziqing'
        im = Image.open(Local_initial_address)
        text = time.ctime()
        width, height = im.size
        print width, height
        txt = Image.new('RGB', im.size, (0, 0, 0, 0))
        text_width = (txt.size[0] - 280)
        text_height = (txt.size[1] - 130)
        # watermark = txt.resize((text_width,text_height), Image.ANTIALIAS)
        draw = ImageDraw.Draw(txt, 'RGBA')  # 在水印层加画笔
        draw.text((text_width, text_height),
                  text, fill=(255,255,255))
        watermark = txt.rotate(23, Image.BICUBIC)
        alpha = watermark.split()[2]
        alpha = ImageEnhance.Brightness(alpha).enhance(0.50)
        watermark.putalpha(alpha)
        a = local_store_address + 'ceshi' + str(i) + '.jpg'
        Image.composite(watermark, im, watermark).save(a, 'JPEG')
        return a

    def respository_run(self, Local_initial_address, local_store_address, Request_the_address):
        """
        需要传参：
            Local_initial_address：第一个是图片初始路劲
            local_store_address：第二个图片的保存路劲（文件名称）
            Request_the_address：请求服务器地址，需要IP地址即可，不用带端口

        """
        for i in range(2):
            # m, new = img('C:\\Users\\Administrator\\Desktop\\Chrysanthemum.jpg', i,'C:\\Users\\Administrator\\Desktop\\').img()
            # new = img(Local_initial_address, i, local_store_address).img()
            new = repositoryimage().img(Local_initial_address, i, local_store_address)
            print new
            n = new[0].split('\\')[-1]
            print n

            # 写
            url = Request_the_address + ':8082/ResourcesPoolWrite/ExtAPI/extend/Create?title=测试&format=jpg&belongPID=2&belongDesc=2&systemName=内业系统&belongID=2'
            # m = operator(url, Local_initial_address).create_new()
            m = repositoryimage().create_new(url, Local_initial_address)
            # u =':8082/ResourcesPoolWrite/ExtAPI/extend/Create?title=测试&format=jpg&belongPID=2&belongDesc=2&systemName=内业系统&belongID=2'
            # m = repositoryimage().create_new(Request_the_address,u, Local_initial_address)

            # 读
            readaddr = Request_the_address + ':8081/ResourcesPoolRead/ExtAPI/extend/' + m[1] + '/GetFileFormat'
            # operator(readaddr, new).select_data()
            repositoryimage().select_data(readaddr)

