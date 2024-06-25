import requests
import time
import json

cookies = {

}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'dnt': '1',
    'origin': 'https://www.nssctf.cn',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.nssctf.cn/user/login?redirect=/index',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

json_data = {
    'remember': '1',
}


def checkin():
    response = requests.post('https://www.nssctf.cn/api/user/login/',
                             cookies=cookies, headers=headers, json=json_data)

    login_json_data = json.loads(response.text)
    print(json.dumps(login_json_data, indent=4, ensure_ascii=False))
    token = login_json_data['data']['token']
    expiry = login_json_data['data']['expiry']
    print(f'vip 剩余天数: {expiry}')
    cookies.update({'token': token})  # str
    headers.update({'content-type': 'application/x-www-form-urlencoded',
                    'referer': 'https://www.nssctf.cn/', })

    time.sleep(0.5)
    response = requests.post(
        'https://www.nssctf.cn/api/user/clockin/', cookies=cookies, headers=headers)
    checkin_json_data = json.loads(response.text)
    print(json.dumps(checkin_json_data, indent=4, ensure_ascii=False))


json_data.update({'username': '', 'password': ''})
checkin()
time.sleep(1)
print(f'{"-"*20}')
json_data.update({'username': '', 'password': ''})
checkin()
