#-*- coding:utf-8 -*-
__auth = '吕梓清'

import os, io, sys, re, time, json, random
from PIL import Image,ImageEnhance,ImageFile,ImageDraw,ImageFont
from time import ctime

class img(object):
    def __init__(self,file,num,Roadking):
        self.lj = file
        self.num = num
        self.Roadking = Roadking
        print self.lj,self.num,self.Roadking


    def img(self):
            im = Image.open(self.lj).convert('RGBA')
            txt = Image.new('RGBA',im.size,(0,0,0,0))
            # fnt = ImageFont.truetype("C:\\Windows\\Fonts\\COOPBL.TTF",20)
            d = ImageDraw.Draw(txt)
            d.text((txt.size[0]-280,txt.size[1]-30),time.ctime(),fill=(255,255,255,255))
            out = Image.composite(im, txt,im)
            # out.show()
            # a = 'C:\\Users\\Administrator\\Desktop\\'+str(time.time())+'.jpg'
            a = self.Roadking+u'测试图片'+str(self.num)+'.jpg'
            out.save(a)

            return out,a
