#!/usr/bin/env python
# coding=utf-8

# 登录新浪微博，并抓取某个人的所有微博记录
# 登录表单需要：
# username:
# password:
# savestate:1
# ec:0
# pagerefer:https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4
# entry:mweibo
# 登录地址：https://passport.weibo.cn/sso/login


from bs4 import BeautifulSoup
import requests
import urllib
import sys
import os

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'close',
    'Host': 'passport.weibo.cn',
    'Origin': 'https://passport.weibo.cn',
    'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=http%3A%2F%2Fm.weibo.cn%2F',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}
formData = {
    'entry': 'mweibo',
    'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry=mweibo&r=http%3A%2F%2Fm.weibo.cn%2F&wm=3349&vt=4',
    'savestate': '1',
    'ec': 0
}
loginUrl = "https://passport.weibo.cn/sso/login"
# username = input('username: ')
# password = input('password: ')
username = ''
password = ''

formData['username'] = username
formData['password'] = password


s = requests.Session()
r = s.post(loginUrl, data=formData, headers=headers)
page = r.text

# print(page)

r = s.get('http://m.weibo.cn/page/json?containerid=1005051646492790_-_WEIBO_SECOND_PROFILE_WEIBO&page=1')
page = r.json()
print(page)

# 可以抓到json，可是不想往下写了，好傻啊，直接看就好了，干嘛要爬下来看
