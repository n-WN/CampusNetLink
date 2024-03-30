import json
import requests
import logging
import time
import random
import string

logging.basicConfig(level=logging.INFO,
                    format=f'\033[1;36m[*]\033[0m %(asctime)s - \033[1;32m%(levelname)s\033[0m - \033[1;32m%('
                           f'message)s\033[0m')

cookies = {
    # 只需填入以下 2 处参数:
    'username': '',  # 学号 ---------- 1
    'password': '',  # 密码 ---------- 2
}

host = 'http://1.1.1.1'

user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 '
              'Safari/537.36')
package = ''
ip = ''


def load_headers(task):
    global headers
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Referer': host,
        'User-Agent': user_agent,
        'Content-Type': 'application/json',
    }
    if task in ['登录', '上线']:
        headers.update(
            {'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'DNT': '1', 'Origin': host, 'Pragma': 'no-cache'})
    elif task not in ['下线', '查询']:
        logging.error('未知任务: %s', task)


def generate_asp_session_id():
    return ''.join(
        random.choices(
            string.ascii_lowercase + string.digits, 
            k=24
        )
    )


def login_aspx():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',  # 预期响应内容类型
        'accept-language': 'zh-CN,zh;q=0.9',  # 语言偏好 | zh-CN 中文简体 优先 | 其次 zh 中文
        'cache-control': 'no-cache',  # 缓存机制 | 表示请求不应从缓存中获取信息
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',  # 用户的隐私偏好 - Do Not Track | 1 表示用户不希望他们的浏览活动被追踪
        'origin': host,
        'pragma': 'no-cache',  # 缓存控制 | 用于向后兼容HTTP/1.0缓存控制
        'referer': f'{host}/basic.aspx',
        'sec-ch-ua': '"Google Chrome";v="75", "Not:A-Brand";v="99", "Chromium";v="75"',
        'sec-ch-ua-mobile': '?0',  # 设备类型 | 非移动设备
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',  # 文档 | 目的地类型: HTML 文档
        'sec-fetch-mode': 'navigate',  # 导航 | 请求导航到另一个页面
        'sec-fetch-site': 'same-origin',  # 同源 | 请求是从与目标资源同一域的页面发起的
        'sec-fetch-user': '?1',  # 触发方式 | 用户触发
        'upgrade-insecure-requests': '1',  # 升级 | 期望 https 请求
        'user-agent': user_agent,
    }

    params = {
        'DoWhat': 'login',
    }

    data = cookies

    response = requests.post(f'{host}/basic.aspx', params=params, cookies={
        'ASP.NET_SessionId': generate_asp_session_id(),
    }, headers=headers, data=data, verify=False)

    return response.text


# 需要跟踪确认 hash 方式
"""
def login():
    load_headers(task='登录')
    json_data = {'username': cookies['username'], 'password': cookies['password'], 'remember': True, 'DoWhat': 'Login'}
    try:
        response = requests.post(f'{host}/Auth.ashx', cookies=cookies, headers=headers, json=json_data)
        return response.text
    except requests.RequestException as e:
        logging.error('登录请求失败: %s', e)
        return str(e)
"""


def get_info():
    load_headers(task='查询')
    json_data = {'DoWhat': 'GetInfo'}
    try:
        response = requests.post(f'{host}/Auth.ashx', headers=headers, json=json_data)
        global ip
        try:
            ip = response.json().get('Data', {}).get('OIA', [])[0].get('IP', '')  # 常规获取第零项 ip
        except Exception as e:  # 指定异常类型
            logging.error('获取 IP 时发生错误, 正在登陆: %s', e)

        package_info = response.json().get('Data', {}).get('KXTC', [])
        global package
        for item in package_info:
            if '电信' in item.get('套餐名称', ''):
                package = item['套餐名称']
                break
            elif '移动' in item.get('套餐名称', ''):
                package = item['套餐名称']
                # break
        logging.info('当前默认套餐: %s', package)
        return response.text
    except requests.RequestException as e:
        logging.error('查询请求失败: %s', e)
        return str(e)


def go_online():
    load_headers(task='上线')
    json_data = {'DoWhat': 'OpenNet', 'Package': package}
    try:
        response = requests.post(f'{host}/Auth.ashx', cookies=cookies, headers=headers, json=json_data)
        return response.text
    except requests.RequestException as e:
        logging.error('上线请求失败: %s', e)
        return str(e)


def go_offline():
    load_headers(task='下线')
    # ip 从 get_info() 中获取
    json_data = {'DoWhat': 'CloseNet', 'IP': ip}
    try:
        response = requests.post(f'{host}/Auth.ashx', headers=headers, json=json_data)
        return response.text
    except requests.RequestException as e:
        logging.error('下线请求失败: %s', e)
        return str(e)


if __name__ == '__main__':
    login_aspx()
    # 随机等待 1-3 秒, 避免可能的风控
    time.sleep(1 + 2 * random.random())
    get_info()
    time.sleep(1 + 2 * random.random())
    for i in range(2): # 换掉 where True 避免某些原因没有上线导致程序陷入循环
        online_msg = json.loads(go_online())
        if online_msg["Result"]:
            print(online_msg["Message"])
            exit()
        else:
            time.sleep(1 + 2 * random.random())
            go_offline() # 踢别的设备下线 | ip 获取时确认获取为其余设备 ip
