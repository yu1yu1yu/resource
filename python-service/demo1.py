import json
import time
import requests
import re
import os
 
'''
获取特定UP主的所有动态内容
'''

def get_video(url: str):
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://www.bilibili.com',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("test.mp4", "wb") as f:
            f.write(response.content)
        return 200
    else:
        return response.status_code


def get_audio(url: str):
    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        'sec-ch-ua':
        '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Referer': 'https://www.bilibili.com',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open("test.m4a", "wb") as f:
            f.write(response.content)
        return 200
    else:
        return response.status_code
    

def load_cookies_from_file(file_path='cookies.json'):
    """从JSON文件加载cookies"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"错误：找不到cookies文件 {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"错误：{file_path} 不是有效的JSON格式")
        return {}


def fetch_data(offset):
    # 从文件加载cookies
    cookies = load_cookies_from_file()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'referer': 'https://space.bilibili.com/91567405/relation/follow', # 防盗链
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
    print(data)

    # # 提取Video相关的JSON数据
    # pattern = r'"video":(.*?),"dolby"'
    # result = re.search(pattern, response.text)
    # file = "{" + f'"video":{result.group(1)}' + '}'
    # file = json.loads(file)
    
    # # 获取视频，只提取有效的
    # for i in file['video']:
    #     tmp = get_video(i['baseUrl'])
    #     if tmp == 200:
    #         break
    #     tmp = get_video(i['"base_url"'])
    #     if tmp == 200:
    #         break
    #     tmp = get_video(i["backupUrl"][0])
    #     if tmp == 200:
    #         break
    #     tmp = get_video(i["backup_url"][0])
    #     if tmp == 200:
    #         break

    # # 获取音频
    # for i in file['audio']:
    #     tmp = get_audio(i['baseUrl'])
    #     if tmp == 200:
    #         break
    #     tmp = get_audio(i['"base_url"'])
    #     if tmp == 200:
    #         break
    #     tmp = get_audio(i["backupUrl"][0])
    #     if tmp == 200:
    #         break
    #     tmp = get_audio(i["backup_url"][0])
    #     if tmp == 200:
    #         break

    # # .*? 非贪婪匹配任意字符（尽可能少地匹配）
    # pattern = r'<title data-vue-meta="true">(.*?)</title>'
    # result = re.search(pattern, response.text)
    # # 匹配原视频标题
    # title = result.group(1)

    # # 合并视频和音频
    # os.system("ffmpeg -i test.mp4 -i test.m4a -c:v copy -c:a aac file/output.mp4")
    # os.remove("test.mp4")
    # os.remove("test.m4a")
    # os.rename("file/output.mp4", f"file/{title}.mp4")
    # print('Done for ' + title)
    print("\nDone!\n")
    # 检查是否还有更多数据
    if data['data']['has_more']:
        # 如果有更多数据，使用新的offset发起新的请求
        fetch_data(data['data']['offset'])


# 从offset为空开始
fetch_data("")