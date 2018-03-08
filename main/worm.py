#!/usr/bin/python3
# -*- coding: utf-8 -*-

#1.读取已经绑定好了的学习卡及密码

import os
import json
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import sys

from bs4 import BeautifulSoup

' a worm module '

__author__ = 'Ender Mei'

BASE_DIR = os.path.dirname(__file__)
LOGIN_URL = "http://www.safetyme.cn/Login.shtml"
GET_URL = 'http://www.safetyme.cn//a/exam.shtml?method=index'
stnrs=[]


def get_file(filename):
    return os.path.join(BASE_DIR, filename)


def _get_user():
    myUser = open(get_file('user.res'), 'r', encoding='utf-8')
    users = json.load(myUser)
    return users

def doWorm(user):
    postdata = urllib.parse.urlencode(user).encode('gbk')
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Connection': 'keep-alive'}
    request = urllib.request.Request(LOGIN_URL)
    request.add_header('User-agent', 'Mozilla/5.0')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    request.add_header('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.7')
    cookie_filename = 'cookie.txt'
    cookie = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(handler)
    response = urllib.request.urlopen(request, postdata)
    try:
        response = opener.open(request)
        response.read().decode('gbk')
    except urllib.error.URLError as e:
        print(e)
    cookie.save(ignore_discard=True, ignore_expires=True)
   
    for item in cookie:
        print('Name = ' + item.name)
        print('Value = ' + item.value)
    get_request = urllib.request.Request(GET_URL, headers=headers)
    get_response = opener.open(get_request)
    soup = BeautifulSoup(get_response.read().decode('gbk'), 'html.parser')
    ids=[]
    examtk = []
    for link in soup.find_all('a'):
        id = link.get('onclick').replace("openPaper('", '').replace(
            "','3')", "")
        print(id)
        ids.append(id)
    for id in ids[1:]:
        get_url = "http://www.safetyme.cn//a/exam.shtml?method=showPaper&id=" + id
        print(get_url)
        get_request = urllib.request.Request(get_url, headers=headers)
        get_response = opener.open(get_request)
        soup = BeautifulSoup(get_response.read().decode('gbk'), 'html.parser')
        i = 0
        for div in zip(
                soup.find_all("div", "exam-content"),
                soup.find_all("div", "for-wrong")):
            i = i + 1
            st = div[0]
            da = div[1]
            sttype = st.p.span.string
            repstring = '<p><span style="color: green; font-weight: bold;">' + sttype + "</span>" + str(
                i) + "、"
            stnr=str(st.p).replace(repstring, "").replace("(1.0分)</p>", "")
            if stnr in stnrs:
                continue
            stnrs.append(stnr)
            tm = {}
            tm["stlx"] = sttype.replace("[", "").replace("]", "")
            tm["stnr"] = stnr
            tm["stda"] = da.contents[4].string.replace("正确答案：", "").strip()
            stxxs = []
            soup2 = BeautifulSoup(str(st.ul),"html.parser")
            # for li in st.ul:
            #     soup2 = BeautifulSoup(str(li), "html.parser")
            for inpt in zip(soup2.find_all("input"),soup2.find_all("li")):
                stxxs.append(inpt[0]['value'] + inpt[1].text)
            #print(stxxs)
            tm["stxx"]=stxxs
            examtk.append(tm)
        print(len(examtk))
    return examtk

def writeJsonFile(examtk):
    with open(get_file('examtk.json'), 'w', encoding='utf-8') as f:
        json.dump(examtk,f,ensure_ascii=False)
        print("加载入文件完成...")

def disExamTk():
    for user in _get_user():
        writeJsonFile(doWorm(user))

for user in _get_user():
        writeJsonFile(doWorm(user))