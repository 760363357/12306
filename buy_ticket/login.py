from buy_ticket.__init__ import *

from buy_ticket.vaild_image import VaildImage


class Login(object):
    def __init__(self, user, password):
        self.__user = user
        self.__password = password
        self.__vaild = VaildImage()
        self.__vaild.vaild()
        self.sess = self.__vaild.sess

    def login(self, url):
        data = {
            'username': self.__user,
            'password': self.__password,
            'appid': 'otn'
        }
        res = self.sess.post(url, data=data, verify=False)
        print(res.json())
        if res.status_code == 200:
            print('第一次获取uamtk成功！')
        else:
            print('第一次获取uamtk发生未知错误！')
            raise requests.HTTPError
        # res = self.__sess.get('https://kyfw.12306.cn/otn/index/init', verify=False)
        # res_text = res.content.decode(chardet.detect(res.content)['encoding'])
        # print(res_text)
        # self.__sess.get('https://kyfw.12306.cn/otn/resources/images/loading.gif', verify=False)

        # self.__sess.get(CAPTCHA_URL, verify=False)

        # self.__sess.post('https://kyfw.12306.cn/otn/login/userLogin', data={'_json_att': ''}, verify=False)

        res = self.sess.post('https://kyfw.12306.cn/passport/web/auth/uamtk', data={'appid': 'otn'}, verify=False)
        print(res.json())
        if res.json()['result_code'] == 0:
            print('更新uamtk成功！')
            uamtk = res.json()['newapptk']
            res = self.sess.post('https://kyfw.12306.cn/otn/uamauthclient', data={'tk': uamtk}, verify=False)
            print(res.json())
            assert res.json()['result_code'] == 0
            print('登录用户名是：', res.json()['username'])
            res = self.sess.get('https://kyfw.12306.cn/otn/login/userLogin', verify=False)
            assert 'initMy12306' in res.url
            print('模拟登录成功！自动跳转到个人主页！')
            print('主页标题为：', re.findall('<title>(.*)</title>', res.content.decode(chardet.detect(res.content)['encoding']))[0])
        else:
            print('更新uamtk出错！')
            print('请检查请求：', res.url)


if __name__ == '__main__':
    login = Login(13025668791, 'qq13653041784')
    login.login(LOGIN_URL)