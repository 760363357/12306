# from __init__ import RAND_NUM
#
# CAPTCHA_URL = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand' + '&' + RAND_NUM


# COORS和SEAT_CODE这两个配置信息不可以改，其他的配置可以根据自己的需求改变。

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
}
IMAGE_NAME = '12306.png'

USER = 12345678901      # 你的12306账号用户名，直接输入手机号码
PASSWORD = '你的密码'   # 你的密码
COORS = {
    '1': '32,47',
    '2': '102,44',
    '3': '187,44',
    '4': '256,40',
    '5': '34,121',
    '6': '108,124',
    '7': '180,115',
    '8': '248,113'
}

# 开启买票，还是抢票模式
GET_TICKET_MODE = 'buy'  # 'rob'为抢票模式

# 所有模式都需要的参数，可更改
DATE = '2018-06-25'
SRC_STAT = 'GZQ'
DST_STAT = 'SHH'
SRC_NAME = '广州'
DST_NAME = '上海'
SEAT = '硬座'

# ATTACH_INFO区别于买票模式还是抢票模式
# 提供my_start_time车次开始时间参数，指定上车时间'07:55'属于买票模式
# 提供stationTrainCode车次参数，指定车次'K512',强制为抢票模式
ATTACH_INFO = {
}

SEAT_CODE = {
    '无座': '1',
    '硬座': '1',
    '硬卧': '3',
    '软卧': '4'
}

# 本账号购票人名字
NAME = '李XX'

# 本账号购票人的身份证号
ID = '440923199XXXX'






