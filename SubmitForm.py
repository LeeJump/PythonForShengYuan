from urllib import request, parse
from bs4 import BeautifulSoup
import http.cookiejar
import time


class FormSubmitScript(object):
    # 初始化时,需要手动输入 url_login,url_submit
    def __init__(self, url_login, url_submit):
        # 初始化: 1,登录url  2,提交url  3,伪装浏览器代理   4,伪装请求头
        # agent: IE9
        self.url_login = url_login
        self.url_submit = url_submit

        self.user_agent = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)"
        self.req_headers = {
            'User-Agent': self.user_agent,
            'Proxy-Connection': "Keep-Alive",
        }
        # 新客信息
        self.consumer_count = 0
        self.consumer_info_list = []
        # 增加的成功和失败信息
        self.success_count = 0
        self.error_count = 0
        self.success_list = []
        self.error_list = []

    def InitOpener(self, user, psw):
        # 加载带有的登录信息cookie的self.opener
        # 登录网站,并保存cookie,拿到带有cookie的opener
        # 构造登录参数
        username = user
        password = psw
        type = ''
        loginscript = "/CRMSelfServiceDemo/logoncn.asp?"
        loginattempt = 'Y'
        Login = "登录"
        login_data = {
            "username": username,
            "password": password,
            "type": type,
            "loginscript": loginscript,
            "loginattempt": loginattempt,
            "Login": Login,
        }
        # 登录参数 -> utf-8
        post_data = parse.urlencode(login_data).encode("utf-8")
        # 构造请求
        req = request.Request(self.url_login, data=post_data, headers=self.req_headers)
        # 构造cookie
        #    (1) 生成cookie对象
        cookie = http.cookiejar.CookieJar()
        #    (2) 生成一个带有该cookie对象的request对象为opener
        opener = request.build_opener(request.HTTPCookieProcessor(cookie))
        # 发送登录请求,此后这个opener就携带了cookie
        opener.open(req)
        self.opener = opener

    def AddNewConsumer(self, name, birthday, telnumber, town):
        # 添加新客到客户list
        # telnumber=11231233
        # name="测试"
        # birthday=2011/1/1
        new_info = {
            'town': town,
            'prsl_telnumber': telnumber,
            'prsl_name': name,
            'prsl_birthday': birthday
        }
        self.consumer_info_list.append(new_info)
        self.consumer_count += 1

    def GetParaTempByTown(self, town):
        towm_dic = {
            "binhu": "para_binhu_newConsumer.txt",
            "dengwan": "para_dengwan_newConsumer.txt",
            "fanghu": "para_fanghu_newConsumer.txt",
            "gucheng": "para_gucheng_newConsumer.txt",
            "gudui": "para_gudui_newConsumer.txt",
            "guihua": "para_guihua_newConsumer.txt",
            "langan": "para_langan_newConsumer.txt",
            "luji": "para_luji_newConsumer.txt",
            "maji": "para_maji_newConsumer.txt",
            "qisi": "para_qisi_newConsumer.txt",
            "sankongqiao": "para_sankongqiao_newConsumer.txt",
            "shunhe": "para_shunhe_newConsumer.txt",
            "taitou": "para_taitou_newConsumer.txt",
            "wangdian": "para_wangdian_newConsumer.txt",
            "wanggang": "para_wanggang_newConsumer.txt",
            "xinli": "para_xinli_newConsumer.txt",
            "zhangli": "para_zhangli_newConsumer.txt",
            "zhangzhuang": "para_zhangzhuang_newConsumer.txt",
            "zhaoji": "para_zhaoji_newConsumer.txt",
        }
        filename = towm_dic[town]
        with open("para_town_template/" + filename) as fp:
            consume_info_template = fp.read()
            # 将参数转换为dict
            consume_info_template = dict(parse.parse_qsl(consume_info_template))
        print(town, ":", consume_info_template["prslctowns"])
        '''
        print("tel:", consume_info_template["prsl_telnumber"])
        print("name:", consume_info_template["prsl_name"])
        print("birt:", consume_info_template["prsl_birthday"])
        '''
        # 生成post_data,
        post_data = parse.urlencode(consume_info_template).encode('utf-8')
        return consume_info_template

    def CommitNewConsumer(self):
        # 遍历新客数组,依次新增新客
        for consumer_info in self.consumer_info_list:
            # 1, 先获取新客地址,找到新客参数信息模板para
            town = consumer_info["town"]
            para_template = self.GetParaTempByTown(town)
            # 2, 填写新客信息,即修改模板
            para_template["prsl_telnumber"] = consumer_info["prsl_telnumber"]
            para_template["prsl_name"] = consumer_info["prsl_name"]
            para_template["prsl_birthday"] = consumer_info['prsl_birthday']
            # 3, 修改完,进行urlencode,utf-8encode
            info_post_data = parse.urlencode(para_template).encode('utf-8')
            # 4, 构造增加新客的请求
            new_req = request.Request(self.url_submit, data=info_post_data, headers=self.req_headers)
            # 5, 利用opener去发送post请求,得到响应
            #time.sleep(0.5)
            response = self.opener.open(new_req)
            # sleep
            #time.sleep(0.5)
            # 6, 解析response,打印Error
            print("正在解析新客提交结果:")
            bp = BeautifulSoup(response.read(), "html.parser", from_encoding='utf-8')
            error_list = bp.find_all("table", attrs={'class': 'ErrorContent'})
            if error_list:
                self.error_count += 1
                error_info = {consumer_info["prsl_name"]: error_list}
                self.error_list.append(error_info)
                print('Error:')
                print(error_list)
            else:
                self.success_count += 1
                success_info = self.success_list.append(consumer_info["prsl_name"])
                print('提交成功')

    def PrintResult(self):
        print("共计新客数量:", self.consumer_count)
        print("新增成功计数:", self.success_count)
        print("新增失败计数:", self.error_count)


# 手动添加新客信息
newconsumer_list = [('测试的', '2018/6/10', '1', 'taitou')]
#240
newconsumer_list.append(('张燕飞', '2018/11/25', '13918719403', 'langan'))
newconsumer_list.append(('郑云飞', '2018/11/25', '15705835556', 'langan'))
newconsumer_list.append(('许继红', '2018/11/25', '13774050025', 'maji'))
newconsumer_list.append(('刘玲', '2018/11/26', '13213897855', 'zhangzhuang'))
newconsumer_list.append(('温玲玲', '2018/11/26', '18717735459', 'langan'))
newconsumer_list.append(('马云飞', '2018/11/26', '18638381119', 'gudui'))
newconsumer_list.append(('陈紫风', '2018/11/27', '13538327715', 'wangdian'))
newconsumer_list.append(('黄楠', '2018/11/27', '13776336022', 'zhangli'))
newconsumer_list.append(('王亚楠', '2018/11/27', '18377170900', 'zhangli'))
newconsumer_list.append(('杜毛毛', '2018/11/28', '15737638559', 'sankongqiao'))
newconsumer_list.append(('韩婷', '2018/11/28', '17317877622', 'wanggang'))
newconsumer_list.append(('任玉', '2018/11/28', '15001989207', 'guihua'))
newconsumer_list.append(('田豆豆', '2018/11/28', '15188581812', 'guihua'))
newconsumer_list.append(('李平', '2018/11/28', '15188582161', 'guihua'))
newconsumer_list.append(('吴刚', '2018/11/28', '17746880106', 'zhangli'))
newconsumer_list.append(('张敏', '2018/11/28', '15939757802', 'binhu'))
newconsumer_list.append(('代洁丽', '2018/11/28', '13586365270', 'langan'))
newconsumer_list.append(('寥哲', '2018/11/29', '13173668661', 'zhangzhuang'))
newconsumer_list.append(('楚静', '2018/11/29', '18237673686', 'zhangzhuang'))
newconsumer_list.append(('张磊', '2018/11/29', '18268389808', 'guihua'))
#340

if __name__ == '__main__':
    # 默认参数: 1,登录参数 2,登录URL 3,提交URL
    user = '816288'
    psw = 'jw20120208'
    url_login = "http://mmsynut.shengyuan.com/CRMSelfServiceDemo/Logoncn.asp"
    url_submit = "http://mmsynut.shengyuan.com/CRMSelfServiceDemo/newconsumernew.asp?fumuid=7625"
    # 自定义新客信息(name,birthday,tel,town)
    consumer_list = newconsumer_list
    # 实例化
    obj_script = FormSubmitScript(url_login, url_submit)
    # 登录,加载cookie
    obj_script.InitOpener(user, psw)
    # 加载新客
    for consumer in consumer_list:
        obj_script.AddNewConsumer(consumer[0], consumer[1], consumer[2], consumer[3])

    # 提交新客
    obj_script.CommitNewConsumer()
    # 加载信息.
    obj_script.PrintResult()
