from buy_ticket.__init__ import *
from config import HEADER
from config import IMAGE_NAME
from config import COORS




class VaildImage(object):
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers.update(HEADER)
        self.sess.get('https://kyfw.12306.cn/otn/login/init#', verify=False)
        time.sleep(1)

    def get_image(self, url):
        respon = self.sess.get(url, verify=False)
        if respon.status_code == 200:
            print('获取验证图片成功！')
            with open(IMAGE_NAME, 'wb') as file:
                file.write(respon.content)
        else:
            print('无法获取验证图片，请检查原因！')
            raise requests.HTTPError

    def get_coors(self):
        coors = []
        while 1:
            coor = input('请输入具体坐标！\n')
            if coor == 'q':
                break
            elif coor == 'r':
                self.get_image(CAPTCHA_URL)
            else:
                coors.append(COORS.get(coor))
        return coors

    def vaild_image(self, url, coors):
        data = {
            'answer': ','.join(coors),
            'login_site': 'E',
            'rand': 'sjrand'
        }
        res = self.sess.post(url, data=data, verify=False)
        print(res.json())
        if res.json()['result_code'] == '4':
            print('验证码验证成功！')
        else:
            print('验证码错误，请重新输入！')
            self.vaild()

    def vaild(self):
        self.get_image(CAPTCHA_URL)
        coors = self.get_coors()
        self.vaild_image(VAILD_URL, coors)


if __name__ == '__main__':
    v = VaildImage()
    v.vaild()