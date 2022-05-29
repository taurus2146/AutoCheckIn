import os

import requests

requests.packages.urllib3.disable_warnings()

push_plus_token = os.environ['PUSH_PLUS_TOKEN']


def check_in_all(title=os.environ['AIRPORT_TITLES'], email=os.environ['AIRPORT_EMAILS'],
                 password=os.environ['AIRPORT_PASSWORDS'], url=os.environ['AIRPORT_URLS']):
    titles = title.split(',')
    emails = email.split(',')
    passwords = password.split(',')
    urls = url.split(',')
    size = len(titles)
    for i in range(size):
        try:
            check_in_one(titles[i], emails[i], passwords[i], urls[i])
        except Exception as e:
            requests.post('http://www.pushplus.plus/send/' + push_plus_token + '?title=' + title + '&content=签到失败')


def check_in_one(title, email, password, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    session = requests.session()
    post_data = 'email=' + email + '&passwd=' + password
    login_r = session.post(url + '/auth/login', verify=False, headers=headers,
                           data=post_data)
    if login_r.json()['ret']:
        # 开始签到
        check_in = session.post(url + '/user/checkin')
        msg = check_in.json()['msg']
    else:
        msg = '登录失败,请校验邮箱和密码'
    # 推送请求结果-使用的是push_plus
    notify = session.post('http://www.pushplus.plus/send/' + push_plus_token + '?title=' + title + '&content=' + msg)


if __name__ == '__main__':
    check_in_all()
