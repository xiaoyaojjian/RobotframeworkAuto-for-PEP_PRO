#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PepObject import PepObject

class PepExt:
    
    def create_pep_object(self):
        """创建评E评对象，用于存储评E评系统键值对."""
        return PepObject()
        
        
    def set_pep_value(self, pep,key,value):
        """设置传入的pep对象的键值信息."""
        pep.set_value(key,value)
		
    def get_list_Count(self,Heir):
        """输入框最大输入个数"""
        m = list(str(Heir)).__len__()
        return m