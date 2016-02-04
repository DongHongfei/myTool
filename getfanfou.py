# -*- coding: utf-8 -*-

# 爬了张小龙饭否的爬虫
# 参考文档：
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html
# http://docs.python-requests.org/en/master/

# author：小学生董宏飞
#


from bs4 import BeautifulSoup
import requests
import urllib
import sys
import os

# 根据抓取的网页内容获取关键信息


def getContent(html_doc):
    # print("进入getContent……")
    soup = BeautifulSoup(html_doc, "lxml")
    # print(soup.prettify())
    msgs = []
    # 分析网页内容可以发现，每条消息都放在p标签里，所以抓取body下所有的p标签
    # （不要问我为什么不用正则表达式，不会！）
    datas = soup.body.find_all('p')

    # 第二个p标签才开始是发表的消息内容
    # print("准备进入循环……")
    i = 2
    while i > 0 and i <= 16:
        # print('进入第', i, '次循环……')
        data = datas[i]
        photo = ''
        # contents = data[i].contents
        # 删除掉转发、回复、收藏
        # print('进入第', i, '次循环……删除掉转发、回复、收藏')
        for a_tag in data.select(".a"):
            a_tag.decompose()

        # 取出日期和发送来源
        # print('进入第', i, '次循环……取出日期和发送来源')
        for t_tag in data.select(".t"):
            time = t_tag.extract().string.strip()

        # 取出图片
        # print('进入第', i, '次循环……取出图片')
        for photo_tag in data.select(".photo"):
            photo = photo_tag.extract().img['src']

        # 剩余部分则为消息正文
        # print('进入第', i, '次循环……处理消息正文')
        strs = ''
        for str_tag in data:
            if len(str_tag.string) != 0:
                strs = strs + str_tag.string.strip()

        msg = [strs, time, photo]
        msgs.append(msg)

        i = i + 1
    # print('msgs:', msgs)
    return msgs


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Host': 'm.fanfou.com',
    'Origin': 'http://m.fanfou.com',
    'Referer': 'http://m.fanfou.com/',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
}
formData = {}

# print('start……')
url = 'http://m.fanfou.com/'
loginUrl = "http://m.fanfou.com/home"
s = requests.Session()

# req = requests.Request('GET', url, headers=headers)
# prepped = s.prepare_request(req)
# print('prepped: ', prepped.body)

r = s.get(url, headers=headers)
# r = s.post(url)
# r = s.post(url, formData)
page = r.text

print('登录饭否...')
email = input('Email: ')
passwd = input('Password: ')

'''''获取验证码图片'''
# 利用bs4获取captcha地址
soup = BeautifulSoup(page, "lxml")
captchaAddr = soup.find('p', 'captcha-img').img['src']
# captchaAddr = 'http://captcha.fanfou.com/captcha.png'
# print('captchaAddr: ', captchaAddr)

# 保存到本地
captchaImg = s.get(captchaAddr)
with open('captcha.jpg', 'wb') as f:
    f.write(captchaImg.content)

# with open("code3.zip", "wb") as code:
#      code.write(r.content)

# urllib.request.urlretrieve(captchaAddr,"captcha.jpg")
captchaPath = 'captcha.jpg'

# 打开验证码
if sys.platform.find('darwin') >= 0:
    os.system('open %s' % captchaPath)
elif sys.platform.find('linux') >= 0:
    os.system('xdg-open %s' % captchaPath)
else:
    os.system('call %s' % captchaPath)

captcha = input('please input the captcha:')

# 获取 所有input输入框
element = {e['name']: e.get('value', '')
           for e in soup.find_all('input', {'name': True})}

# print(element)
token = element['token']
auto_login = element['token']
action = element['action']

# reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
# captchaID = re.findall(reCaptchaID,page)
# print captchaID

formData['captcha'] = captcha
formData['loginname'] = email
formData['loginpass'] = passwd
formData['token'] = token
formData['auto_login'] = auto_login
formData['action'] = action

# 进行登录，并验证登录返回信息
r = s.post(loginUrl, data=formData, headers=headers)
page = r.text
# print(page)
soup = BeautifulSoup(page, "lxml")
# 获取报错信息
error = soup.find('p', 'n')

if(error != None):
    print(error.string)
elif r.url == 'http://m.fanfou.com/home':
    print('Login successfully!!!')
    # 开始抓取张小龙的内容
    # 循环抓取第1-118页内容
    i = 1
    msgs = []
    while i <= 157:
        print('正在抓取第', i, '页内容……')
        url = 'http://m.fanfou.com/~RLhcIDBjZAM/p.' + str(i)
        # print(url)
        html_doc = s.get(url).text
        contents = getContent(html_doc)
        msgs.extend(contents)
        i = i + 1
        # print(contents)

    # 对抓取内容整理显示
    # 最终显示在个人博客中，markdown格式
    data = ''

    msgs.reverse()
    for msg in msgs:
        photo = ''
        if len(msg[2]) != 0:
            photo = '\n' + '![图](' + msg[2] + ')'
        data = data + '> ' + msg[0] + photo + '\n> ' + msg[1] + '\n\n---\n\n'

    print('正在写入文件……')
    with open('test.txt', 'w') as f:
        f.write(data)

else:
    print("failed!")

# # print(r.text)
#
# data = s.get('http://m.fanfou.com/~RLhcIDBjZAM/p.2').text
# print(data)
# data = ''
