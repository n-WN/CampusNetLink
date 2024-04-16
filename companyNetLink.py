import sys
import time
import requests # pip install requests
from Crypto.Cipher import ARC4 # pip install pycryptodome

phone_number = ''
password = b''
ip = ''

def encrypt_rc4_python(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def header():
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'http://' + ip,
        'Pragma': 'no-cache',
        'Referer': 'http://' + ip + '/ac_portal/default/pc.html?tabs=pwd',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    return headers

def login():
    rc4_key = str(int(time.time() * 1000)).encode('utf-8')

    encrypted_data = encrypt_rc4_python(password, rc4_key).hex()

    headers = header()

    data = {
        'opr': 'pwdLogin',
        'userName': phone_number,
        'pwd': encrypted_data,
        'rc4Key': rc4_key,
        'rememberPwd': '0',
    }

    response = requests.post('http://' + ip + /ac_portal/login.php', headers=headers, data=data, verify=False)
    response.encoding = 'utf-8'
    print(response.text)

def logout():
    headers = header()
    headers['Referer'] = 'http://' + ip + '/ac_portal/default/pc.html?type=logout&tabs=pwd'
    print(headers)

    cookies = {
        'ac_login_info': 'passwork',
    }

    data = {
        'opr': 'logout',
    }

    response = requests.post('http://' + ip + '/ac_portal/login.php', cookies=cookies, headers=headers, data=data, verify=False)
    response.encoding = 'utf-8'
    print(response.text)

if __name__ == "__main__":
    if "-q" in sys.argv:
        logout()
    else:
        login()
