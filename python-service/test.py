import requests

'''
爬取原始数据并保存，以便于后续提取
'''

cookies = {
    'buvid3': '0A4791A2-C8DB-742E-A3F3-891AF1E888DA28242infoc',
    'b_nut': '1746970527',
    'rpdid': "|(kY)kJmmRm)0J'u~RYm~|lJl",
    'SESSDATA': '6a674b6e%2C1762522570%2Cb00da%2A52CjBlpHSxk8zAxXmGUpOKTtGlZsjsTHtz6yZWAG3Vfu0UP8REbPansrWo8ESRdy17RS8SVk5OZHM3aWUya2FSWW9WOENLWFhaT1FIa0RjQm1sZEJoVklKaEJfX2ZUSXVvR0J0SVRYbzFGQlJibG9LdGE5ajcxSW44UDJaQ09OazhjSzVwazBfYXZ3IIEC',
    'bili_jct': '560808942c0f640011f0196a1d04ba4d',
    'DedeUserID': '91567405',
    'DedeUserID__ckMd5': 'e65557090450a8fc',
    '_uuid': '5DE2FEB1-E461-AD65-47D8-5FC92D3DE5B591799infoc',
    'header_theme_version': 'CLOSE',
    'enable_web_push': 'DISABLE',
    'enable_feed_channel': 'ENABLE',
    'buvid4': '91EA2C7B-515B-4135-B962-3D9B9492E04428242-025051121-lkAklX%2B8JZlP9z%2BHSyHEww%3D%3D',
    'buvid_fp_plain': 'undefined',
    'home_feed_column': '5',
    'hit-dyn-v2': '1',
    'fingerprint': '586fb78937f3259a054e0bb95a53bc90',
    'buvid_fp': '732fced7f511fd9d4e356a1ebef392b1',
    'bili_ticket': 'eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTE2Mjk4MjIsImlhdCI6MTc1MTM3MDU2MiwicGx0IjotMX0.FSoIkAMmwCBVaNBkwq2C_u_MRe6u1aDmHjcpULAsm-I',
    'bili_ticket_expires': '1751629762',
    'CURRENT_QUALITY': '80',
    'browser_resolution': '1488-702',
    'bmg_af_switch': '1',
    'bmg_src_def_domain': 'i0.hdslb.com',
    'sid': '7iarmc46',
    'bp_t_offset_91567405': '1085318122367352832',
    'b_lsid': '29744BE10_197CFAB5267',
    'CURRENT_FNVAL': '4048',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    # 'cookie': "buvid3=0A4791A2-C8DB-742E-A3F3-891AF1E888DA28242infoc; b_nut=1746970527; rpdid=|(kY)kJmmRm)0J'u~RYm~|lJl; SESSDATA=6a674b6e%2C1762522570%2Cb00da%2A52CjBlpHSxk8zAxXmGUpOKTtGlZsjsTHtz6yZWAG3Vfu0UP8REbPansrWo8ESRdy17RS8SVk5OZHM3aWUya2FSWW9WOENLWFhaT1FIa0RjQm1sZEJoVklKaEJfX2ZUSXVvR0J0SVRYbzFGQlJibG9LdGE5ajcxSW44UDJaQ09OazhjSzVwazBfYXZ3IIEC; bili_jct=560808942c0f640011f0196a1d04ba4d; DedeUserID=91567405; DedeUserID__ckMd5=e65557090450a8fc; _uuid=5DE2FEB1-E461-AD65-47D8-5FC92D3DE5B591799infoc; header_theme_version=CLOSE; enable_web_push=DISABLE; enable_feed_channel=ENABLE; buvid4=91EA2C7B-515B-4135-B962-3D9B9492E04428242-025051121-lkAklX%2B8JZlP9z%2BHSyHEww%3D%3D; buvid_fp_plain=undefined; home_feed_column=5; hit-dyn-v2=1; fingerprint=586fb78937f3259a054e0bb95a53bc90; buvid_fp=732fced7f511fd9d4e356a1ebef392b1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTE2Mjk4MjIsImlhdCI6MTc1MTM3MDU2MiwicGx0IjotMX0.FSoIkAMmwCBVaNBkwq2C_u_MRe6u1aDmHjcpULAsm-I; bili_ticket_expires=1751629762; CURRENT_QUALITY=80; browser_resolution=1488-702; bmg_af_switch=1; bmg_src_def_domain=i0.hdslb.com; sid=7iarmc46; bp_t_offset_91567405=1085318122367352832; b_lsid=29744BE10_197CFAB5267; CURRENT_FNVAL=4048",
}

params = {
    'spm_id_from': '333.1007.tianma.1-3-3.click',
    'vd_source': '5c3a503c984d9075efb718e289a60685',
}

response = requests.get('https://www.bilibili.com/video/BV12gMtzZEZ3/', params=params, cookies=cookies, headers=headers)

with open('bilibili.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
    print("HTML content saved to bilibili.html")
