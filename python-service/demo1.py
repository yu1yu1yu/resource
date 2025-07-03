import json
import time
import requests
 
'''
获取特定UP主的所有动态内容
'''
 
def fetch_data(offset):
    cookies = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': '', # 防盗链，需要重新获取
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    }
   
    # 每次请求时延时0.5秒
    time.sleep(0.5)
 
    # 请求的URL
    url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/space"
 
    # 请求参数
    params = {
        "offset": offset,
        "host_mid": 4142659
    }
 
    # 发送请求
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
 
    # 解析JSON数据
    data = response.json()
    print(data) # 先不做处理
 
    # 检查是否还有更多数据
    if data['data']['has_more']:
        # 如果有更多数据，使用新的offset发起新的请求
        fetch_data(data['data']['offset'])


# 从offset为空开始
fetch_data("")