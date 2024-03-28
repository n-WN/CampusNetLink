import requests
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format=f'\033[1;36m[*]\033[0m %(asctime)s - \033[1;32m%(levelname)s\033[0m - \033[1;32m%(message)s\033[0m')

# 只需修改以下 3 处参数:
cookies = {
    'username': '',  # 学号 ---------- 1
    'password': '',  # 密码 ---------- 2
}

host = ''  # 登录页面地址    ---------- 3

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
package = '学生-电信-100M'  # 套餐名称
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
        headers.update({'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'DNT': '1', 'Origin': host, 'Pragma': 'no-cache'})
    elif task not in ['下线', '查询']:
        logging.error('未知任务: %s', task)

def login():
    load_headers(task='登录')
    json_data = {'username': cookies['username'], 'password': cookies['password'], 'remember': True, 'DoWhat': 'Login'}
    try:
        response = requests.post(f'{host}/Auth.ashx', cookies=cookies, headers=headers, json=json_data)
        return response.text
    except requests.RequestException as e:
        logging.error('登录请求失败: %s', e)
        return str(e)

def get_info():
    load_headers(task='查询')
    json_data = {'DoWhat': 'GetInfo'}
    try:
        response = requests.post(f'{host}/Auth.ashx', headers=headers, json=json_data)
        package_info = response.json().get('Data', {}).get('KXTC', [])
        global ip
        ip = response.json().get('Data', {}).get('OIA', [])[0].get('IP', '') # 常规获取第零项 ip
        logging.info
        for item in package_info:
            # 偏好 电信 / 移动
            if '电信' in item.get('套餐名称', ''):
                global package
                package = item['套餐名称']
                break
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
    print(login())
    # 随机等待 1-3 秒, 避免可能的风控
    time.sleep(1 + 2 * random.random())
    print(go_online())
    time.sleep(1 + 2 * random.random())
    get_info()
    time.sleep(1 + 2 * random.random())
    # print(go_offline())
    
