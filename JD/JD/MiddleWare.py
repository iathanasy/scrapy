#!/usr/bin/env python3
# -*-coding:utf-8 -*-
# @author cd.wang
# @create 2021-03-06 14:54
# selenium下拉到底部，全部加载出来

import time
from selenium import webdriver
from scrapy.http import HtmlResponse


class SeleniumWare(object):
    def process_request(self,spider,request):
        self.option  = webdriver.ChromeOptions()
        self.option.add_argument("--headless")
        self.option.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        # 下载对应的版本： http://npm.taobao.org/mirrors/chromedriver/88.0.4324.96/
        self.driver = webdriver.Chrome(executable_path='D:\chromedriver.exe',options=self.option)
        self.driver.get(request.url)
        self.driver.implicitly_wait(10)
        self.driver.execute_script('var p = document.documentElement.scrollTop=100000')
        time.sleep(3)
        data = self.driver.page_source
        self.driver.close()
        data = str(data)
        res = HtmlResponse(body=data,encoding="utf-8",request=request,url=request.url)
        return res