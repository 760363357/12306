from query.__init__ import *
from config import HEADER
'''
该模块的功能有：查票（query），然后选票（get_train），最后返回一条车票信息
用到的URL：
GET：https://kyfw.12306.cn/otn/leftTicket/query?...

'''


def query(src_sta, dst_sta, launch_time, purpose_code='ADULT'):
    '''
    传入指定参数获取并排版车次和url返回，否则继续请求，最多五次，超过就结束程序。
    :param src_sta: 起点代码
    :param dst_sta: 终点代码
    :param launch_time: 乘车日期
    :param purpose_code: 票的类型，默认是成人票
    :return:
    '''
    info_list = []
    count_link = 0
    url = 'https://kyfw.12306.cn/otn/leftTicket/query'
    res = requests.get(url, params={
        'leftTicketDTO.train_date': launch_time,
        'leftTicketDTO.from_station': src_sta,
        'leftTicketDTO.to_station': dst_sta,
        'purpose_codes': purpose_code
    }, headers=HEADER)

    if res.json()['status'] and res.json()['data']:
        tickets = res.json()['data'].get('result')
        for ticket in tickets:
            seat = {}
            info = {}
            s1 = ticket.split('|')
            info['secretStr'] = s1[0]
            info['train_no'] = s1[2]
            info['stationTrainCode'] = s1[3]
            info['start'] = s1[4]
            info['end'] = s1[5]
            info['my_src'] = s1[6]
            info['my_start_time'] = s1[8]
            info['end_time'] = s1[9]
            info['exper_time'] = s1[10]
            info['leftTicket'] = s1[12]
            info['start_tick'] = s1[13]
            info['train_location'] = s1[15]
            seat['特等座'] = s1[-5]
            seat['一等座'] = s1[-6]
            seat['二等座'] = s1[-7]
            seat['软卧'] = s1[-14]
            seat['无座'] = s1[-11]
            seat['硬座'] = s1[-8]
            seat['硬卧'] = s1[-9]
            info['seat'] = seat
            info_list.append(info)
        return res.url, info_list
    else:
        print('获取车票信息出错！正在重新获取...')
        time.sleep(1)
        count_link += 1
        query(src_sta, dst_sta, launch_time, purpose_code)
        if count_link == 5:
            sys.exit('无法获取车票信息，程序退出！')


def get_train(seat, info_list, kwargs):
    '''
    1.如果参数seat存在，则先根据座位来选取车次，其次是'stationTrainCode'参数，然后是'my_start_time'参数。
    2.如果seat不存在，则会根据'stationTrainCode'参数，然后是'my_start_time'参数
    3.否则就会根据无座，硬座，硬卧，软卧有位置后再随机选择一个车次返回。
    :param seat:
    :param info_list:
    :param kwargs: 'stationTrainCode', 'my_start_time'
    :return:
    '''
    li = []
    if seat:
        info = li
        for i in info_list:
            if i['seat'][seat] == '无' or not i['seat'][seat]:
                continue
            else:
                li.append(i)
    else:
        info = info_list
    for i in info:
        for k in kwargs:
            if k == 'stationTrainCode' and kwargs[k] == i[k]:
                return i
            elif k == 'my_start_time':
                ts = kwargs[k].split(':')
                ds = i[k].split(':')
                m_s = int(ts[0])*60 + int(ts[1])
                s_s = int(ds[0])*60 + int(ds[1])
                if m_s <= s_s:
                    return i
    if not li:
        print('无法选取车次信息！系统正在随机为您选取车次与座位...')
        while 1:
            key = input('请输入K键继续购票，退出按任意键')
            if key == 'K':
                break
            elif not key:
                sys.exit('程序退出成功！')
        for i in info_list:
            for k in i['seat']:
                if k == '硬座' and i['seat'][k] != '无' and not i['seat'][k]:
                    li.append(i)
                    continue
                elif k == '无座' and i['seat'][k] != '无' and not i['seat'][k]:
                    li.append(i)
                    continue
                elif k == '硬卧' and i['seat'][k] != '无' and not i['seat'][k]:
                    li.append(i)
                    continue
                elif k == '软卧' and i['seat'][k] != '无' and not i['seat'][k]:
                    li.append(i)
                    continue
        return random.choice(info_list)
    return random.choice(li)


if __name__ == '__main__':
    url, li = query('GZQ', 'SHH', '2018-06-14')
    infor = get_train('硬座', li, my_start_time='08:16')
    print(infor)
