import requests
import random
import chardet
import traceback
import time
import re
from urllib import parse
import sys
sys.path.insert(1, '../')


requests.packages.urllib3.disable_warnings()

RAND_NUM = '{:.16f}'.format(random.random())

CAPTCHA_URL = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand' + '&' + RAND_NUM
VAILD_URL = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
LOGIN_URL = 'https://kyfw.12306.cn/passport/web/login'

# https://kyfw.12306.cn/otn/login/userLogin
# headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'zh-CN,zh;q=0.9',
# 'Cache-Control': 'max-age=0',
# 'Connection': 'keep-alive',
# 'Content-Length': '10',
# 'Content-Type': 'application/x-www-form-urlencoded',
# 'Host': 'kyfw.12306.cn',
# 'Origin': 'https://kyfw.12306.cn',
# 'Referer': 'https://kyfw.12306.cn/otn/login/init',
# 'Upgrade-Insecure-Requests': '1'}

# https://kyfw.12306.cn/passport/web/auth/uamtk
# headers={'Host': 'kyfw.12306.cn',
# 'Origin': 'https://kyfw.12306.cn',
# 'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
# 'X-Requested-With': 'XMLHttpRequest'}


# https://kyfw.12306.cn/otn/uamauthclient
# headers={'Host': 'kyfw.12306.cn',
# 'Origin': 'https://kyfw.12306.cn',
# 'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
# 'X-Requested-With': 'XMLHttpRequest'}

# https://kyfw.12306.cn/otn/login/userLogin
# headers={'Host': 'kyfw.12306.cn',
# 'Upgrade-Insecure-Requests': '1', 'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin'}