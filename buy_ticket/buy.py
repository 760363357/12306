from buy_ticket.__init__ import *
from config import USER, PASSWORD, NAME, ID
from config import DATE,SRC_STAT,DST_STAT,SEAT,ATTACH_INFO,GET_TICKET_MODE,SRC_NAME,DST_NAME,SEAT_CODE

from buy_ticket.login import Login
from query.ticket import Ticket

'''
买票类会先登录，然后再查询票信息，获得票之后再通过一系列的URL进行购买操作。
使用到的URL：
GET:
  1.https://kyfw.12306.cn/otn/leftTicket/init
  2.https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime
POST：
  1.https://kyfw.12306.cn/otn/login/checkUser
  2.https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest
  3.https://kyfw.12306.cn/otn/confirmPassenger/initDc
  4.https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo
  5.https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount
  6.https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue
  7.https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue
  8.https://kyfw.12306.cn/otn//payOrder/init?random=
'''


class Buy(object):
    def __init__(self):
        self.login = Login(USER, PASSWORD)
        self.login.login(LOGIN_URL)
        self.sess = self.login.sess
        time.sleep(0.5)
        self.sess.get('https://kyfw.12306.cn/otn/leftTicket/init', verify=False)
        time.sleep(1)

    def vaild_query(self, src_stat, dst_stat, date, seat, attch):
        t = Ticket(src_stat, dst_stat, date, seat, attch)
        url, tick = t.get_tick()
        if tick['seat'][seat] == '无' or not tick['seat'][seat]:
            print('正在重新获取车票信息...')
            url, tick = t.get_tick()
        return url, tick

    def buy(self):
        url, tick = self.vaild_query(SRC_STAT, DST_STAT, DATE, SEAT, ATTACH_INFO)
        res = self.sess.post('https://kyfw.12306.cn/otn/login/checkUser', data={'_json_att': ''}, verify=False)
        print('检验用户状态：', res.json())
        assert res.json()['data']['flag']
        data = {
            'secretStr': parse.unquote(tick['secretStr']),
            'train_date': DATE,
            'back_train_date': DATE,
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': SRC_NAME,
            'query_to_station_name': DST_NAME,
            'undefined': ''
        }
        res = self.sess.post('https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest', data=data, verify=False)
        if res.json()['status']:
            print('数据提交成功！正在填写订票信息...')
            res = self.sess.post('https://kyfw.12306.cn/otn/confirmPassenger/initDc', data={'_json_att': ''}, verify=False)
            token = re.findall("globalRepeatSubmitToken = '(.*)'", res.content.decode())[0]
            key = re.findall("'key_check_isChange':'(.*?)',", res.text)[0]
            print('获取到页面的token: ', token)
            print('获取到页面的key：', key)
            # print('------------------------------')
            # print(res.text)
            # print('------------------------------')
            time.sleep(1)
            assert token
            assert key
            res = self.sess.post('https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo', data={
                'cancel_flag': '2',
                'bed_level_order_num': '000000000000000000000000000000',
                'passengerTicketStr': SEAT_CODE[SEAT] + ',0,1,'+ NAME + ',1,'+ID+','+str(USER)+',N',
                'oldPassengerStr': NAME + ',1,' + ID + ',1_',
                'tour_flag': 'dc',
                'randCode': '',
                'whatsSelect': '1',
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)
            print('------------------------------')
            print('检查用户表单信息: ', res.json())
            print('------------------------------')
            assert res.json()['data']['submitStatus']
            res = self.sess.post('https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount', data={
                'train_date': 'Thu Jun 14 2018 00:00:00 GMT+0800 (中国标准时间)',
                'train_no': tick['train_no'],
                'stationTrainCode': parse.unquote(tick['stationTrainCode']),
                'seatType': SEAT_CODE[SEAT],
                'fromStationTelecode': SRC_STAT,
                'toStationTelecode': DST_STAT,
                'leftTicket': parse.unquote(tick['leftTicket']),
                'purpose_codes': '00',
                'train_location': tick['train_location'],
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)
            print('------------------------------')
            print('根据时间查询信息：', res.json())
            print('------------------------------')
            assert res.json()['status']
            res = self.sess.post('https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue', data={
                'passengerTicketStr': SEAT_CODE[SEAT] + ',0,1,'+ NAME + ',1,'+ID+','+str(USER)+',N',
                'oldPassengerStr': NAME + ',1,' + ID + ',1_',
                'randCode': '',
                'purpose_codes': '00',
                'key_check_isChange': key,
                'leftTicketStr': parse.unquote(tick['leftTicket']),
                'train_location': tick['train_location'],
                'choose_seats': '',
                'seatDetailType': '000',
                'whatsSelect': '1',
                'roomType': '00',
                'dwAll': 'N',
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)
            print('------------------------------')
            print('confirm_info: ', res.json())
            print('------------------------------')
            assert res.json()['data']['submitStatus']
            time.sleep(0.5)
            res = self.sess.get('https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime', params={
                'random': str(int(time.time()*1000)),
                'tourFlag': 'dc',
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)
            print('-----------------------------------------------------------------')
            print('重要一步\n查询等待时间：', res.json())
            print('-----------------------------------------------------------------')
            assert res.json()['status'] and res.json()['data']['orderId'] != 'null' and not res.json()['data']['orderId']
            # res = self.sess.get('https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime', params={
            #     'random': int(time.time() * 1000),
            #     'tourFlag': 'dc',
            #     '_json_att': '',
            #     'REPEAT_SUBMIT_TOKEN': token
            # }, verify=False)
            # print('-----------------------------------------------------------------')
            # print(res.status_code)
            # print(res.text)
            # print('-----------------------------------------------------------------')

            res = self.sess.post('https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue', data={
                'orderSequence_no': res.json()['data']['orderId'],
                '_json_att': '',
                'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)
            print('-----------------------------------------------------------------')
            print('最后提交请求: ', res.json())
            print('-----------------------------------------------------------------')
            res = self.sess.post('https://kyfw.12306.cn/otn//payOrder/init?random=' + str(int(time.time() * 1000)),
                                 data={
                                     '_json_att': '',
                                     'REPEAT_SUBMIT_TOKEN': token
            }, verify=False)

        else:
            print('用户有已存在未支付的订单，需要取消订单才可用！')
            print(res.json())


if __name__ == '__main__':
    b = Buy()
    b.buy()
