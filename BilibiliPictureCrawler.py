# -*- coding:utf-8 -*-
import os
import re
import time
import threading
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# 获取热门的总页数
def getPage():
    try:
        print('开始检测页数...')
        page = 1
        print("已检测到页面数量%d" % page)
        while True:
            url = f"https://api.vc.bilibili.com/link_draw/v2/Photo/list?category=cos&type=hot&page_num={page}&page_size=20"
            headers = {
                'Host': 'api.vc.bilibili.com',
                'Origin': 'https://h.bilibili.com',
                'Referer': 'https://h.bilibili.com/eden/picture_area',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
            }
            response = requests.request('get', url, headers=headers, verify=False).json()
            total_count = response['data']['total_count']
            if total_count != 0:
                page += 1
                print("已检测到页面数量%d" % page)
                time.sleep(0.2)
            else:
                print("页面页数检测完毕!一共%d页" % page)
                return page
    except Exception as e:
        print(e)
        getPage()


# 获取图片链接
def getImageUrl(page):
    url = f"https://api.vc.bilibili.com/link_draw/v2/Photo/list?category=cos&type=hot&page_num={page}&page_size=20"
    headers = {
        'Host': 'api.vc.bilibili.com',
        'Origin': 'https://h.bilibili.com',
        'Referer': 'https://h.bilibili.com/eden/picture_area',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    response = requests.request('get', url, headers=headers, verify=False).json()
    # 有多少图集
    subPageNum = len(response['data']['items'])
    for index in range(0, subPageNum):
        # 标题
        title = response['data']['items'][index]['item']['title']
        title = re.sub(r'[<||>.:?]+', '', title)
        dir = 'Picture/' + title
        # print(dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
        print(title)
        # 图片集
        picturesNum = len(response['data']['items'][index]['item']['pictures'])
        for i in range(0, picturesNum):
            ImageUrl = response['data']['items'][index]['item']['pictures'][i]['img_src']
            downloadImage(title, ImageUrl)


# 下载图片
def downloadImage(title, ImageUrl):
    Image = requests.get(ImageUrl)
    ImageName = ImageUrl.split('/')[-1]
    fileName = 'Picture//' + title + '//' + ImageName
    with open(fileName, 'wb+')as f:
        print('Downloading...', fileName)
        f.write(Image.content)


def _request(pageNum):
    thread_list = []
    start = time.time()
    for i in range(1, pageNum + 1):
        temp = threading.Thread(target=getImageUrl, args=(i,))
        thread_list.append(temp)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    print("本次用时:", time.time() - start)


if __name__ == '__main__':
    if not os.path.exists('Picture'):
        os.mkdir('Picture')
    pageNum = getPage()
    _request(pageNum)
