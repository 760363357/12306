from query.__init__ import *
from config import DATE,SRC_STAT,DST_STAT,SEAT,ATTACH_INFO,GET_TICKET_MODE
from query.query_ticket import query, get_train
'''
定义一个类，该类可以返回url和一条车票信息。
'''


class Ticket(object):
    def __init__(self, src_stat, dst_stat, date, seat, attch):
        self.__src = src_stat
        self.__dst = dst_stat
        self.__date = date
        self.__seat = seat
        self.__att = attch

    def get_tick(self):
        url, info_li = query(self.__src, self.__dst, self.__date)
        tick = get_train(self.__seat, info_li, self.__att)
        if GET_TICKET_MODE == 'buy':
            print('此模式为正常购票模式')
            print("车次：{}\n发车时间：{}\n座位: {}".format(tick['stationTrainCode'], tick['my_start_time'], self.__seat))
            return url, tick
        else:
            if tick.get('stationTrainCode', 1) == ATTACH_INFO.get('stationTrainCode', 2):
                print('查询到抢票信息！')
                print("车次：{}\n发车时间：{}\n座位: {}".format(tick['stationTrainCode'], tick['my_start_time'], self.__seat))
                return url, tick
            else:
                time.sleep(0.5)
                self.get_tick()


if __name__ == '__main__':
    T = Ticket(SRC_STAT,DST_STAT,DATE,SEAT,ATTACH_INFO)
    T.get_tick()