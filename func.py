import re
import requests


def make_url(user, password, operator):
    base_url = r'http://10.2.5.251:801'
    param = r'/eportal/?c=Portal&a=login&callback=dr1566863997635&login_method=1&user_account={}{}&user_password={}&wlan_user_ip=10.4.18.17&wlan_user_mac=302432c506a7&wlan_ac_ip=&wlan_ac_name=NAS&jsVersion=3.0&_=1566863977460'.format(user, operator, password)
    url = base_url + param
    return url


def login(user, password, operator):
    url = make_url(user, password, operator)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'PHPSESSID=d35ars7ch1tuc5offqso888cs1'
    }
    #proxies = {'http':'127.0.0.1:8080'}
    r = requests.get(url, headers=headers)
    response = r.content.decode('utf-8')
    msg = re.search(r'"msg":"(.*?)"', response)
    if msg and msg.group(1):
        if msg.group(1) == 'dXNlcmlkIGVycm9yMQ==':
            return '登录失败'
        elif msg.group(1) == 'QXV0aGVudGljYXRpb24gRmFpbCBFcnJDb2RlPTE2':
            return '断网时间'
        elif msg.group(1) == '认证成功':
            return '登陆成功'
        else:
            return msg.group(1)
    elif re.search(r'({"result":"0","msg":"","ret_code":"2"})', response):
        return '早已登录'
    else:
        return response
        

def logout():
    url = 'http://10.2.5.251:801/eportal/?c=Portal&a=logout&callback=dr1566899766532&login_method=1&user_account=drcom&user_password=123&ac_logout=0&wlan_user_ip=10.4.18.17&wlan_user_ipv6=&wlan_vlan_id=0&wlan_user_mac=302432c506a7&wlan_ac_ip=&wlan_ac_name=NAS&jsVersion=3.0&_=1566899754744'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'PHPSESSID=d35ars7ch1tuc5offqso888cs1'
    }
    r = requests.get(url, headers=headers)
    response = r.content.decode('utf-8')
    if re.search(r'注销成功', response):
        return '注销成功'
    elif re.search(r'注销失败', response):
        return '早已注销'
    else:
        return response
    

def ping_baidu():   
    url = 'https://baidu.com'
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return True
    except:
        return False


if __name__ == '__main__':
    user = ''
    password = ''
    operator = ''
    '''
    联通：unicom
    移动：cmcc
    电信：telecom
    校园网：留空即可
    '''
    #login(user, password, operator)
    #logout()