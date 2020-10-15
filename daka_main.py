# -*- coding=utf-8 -*-

import base64
import getpass
import logging
from multiprocessing import Process
import json
import parse
from flask import Flask, request

import daka_plus

saved_file = '/home/tangchuan/workdir/daka/user_info.json'
log_fmt = "%(asctime)s|%(message)s"
logging.basicConfig(filename='qiandao.log', format=log_fmt, level=logging.INFO)

# 启动flask
# 当收到一个表单就加一个打卡子程序
# 

def getInfo(form):
    items = ["username", "major",
            "grade", "building", "dormitory", "password", "xuewei"]
    default = [None, "计算机科学与技术", 2020, "文苑6公寓", None, None, "硕士"]
    dic = {}
    for idx, i in enumerate(items):
        dic[i] = form[i]
        if dic[i] == "":
            dic[i] = default[idx]
    
    return dic

def panduan(dic):
    if dic["building"] not in ["文苑6公寓", "南苑7公寓"]:
        return False
    if dic["username"][-2:] != "20":
        return False
    with open(saved_file, 'r') as f:
        user_dic = json.load(f) 
    for user in user_dic:
        if user["username"] == dic["username"]:
            return False
    # 加密保存 一个很无聊的加密。。
    dic["password"] = str(base64.b64encode(dic["password"].encode("utf-8")), encoding = "utf8")
    user_dic.append(dic)
    with open(saved_file,'w+') as f:
        json.dump(user_dic, f)

    return True
        

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Daka: http://59.72.118.127:8035/daka</h1>'

@app.route('/daka', methods=['GET'])
def signin_form():
    return '''
              <h2>仅限本学院同学daka</h2>
              <h3>填写说明参见 https://github.com/JLUtangchuan/AutoDaka</h3>
              <form action="/daka" method="post">
              
              <p>username 邮箱前缀（如:xiaoming20）：<input name="username"></p>
              <p>major 默认为计算机科学与技术（不用填写即可）：<input name="major" value="计算机科学与技术"></p>
              <p>grade （如：2020，默认2020）：<input name="grade" value="2020"></p>
              <p>building （如：文苑6公寓, 默认文苑6公寓）：<input name="building" value="文苑6公寓"></p>
              <p>硕士/博士（默认填写硕士）<input name="xuewei" value="硕士"></p>
              <p>dormitory 寝室号：<input name="dormitory"></p>
              <p>密码：<input name="password" type="password"></p>
              <p><button type="submit">Auto Daka</button></p>
              </form>'''

@app.route('/daka', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    # 获取信息
    dic = getInfo(request.form)
    if panduan(dic):

        # print(dic)
        desp = dic["username"] + "加入打卡"
        logging.info(desp)
        p = Process(target=daka_plus.signProgram, args=(dic,))
        p.start()
        print(f"{dic['username']} 已添加到自动打卡")
        return f'<h3>{dic["username"]}已添加到自动打卡，签到完成将通过邮件的方式发到您的学校邮件！</h3>'
    else:
        print(f"{dic['username']} 添加打卡失败")
        return f'<h3>可能ni输入信息有误，或者判断ni不是人院20级研究生,或者ni已经填过,请重新填写正确信息</h3>'
    

if __name__ == '__main__':
    # 加载以往的user并启动
    with open(saved_file, 'r') as f:
        user_dic = json.load(f)
    print("开启", len(user_dic), "个服务")
    for user in user_dic:
        desp = user["username"] + "加入打卡"
        print(user)
        logging.info(desp)
        p = Process(target=daka_plus.signProgram, args=(user,))
        p.start()

    # 开启服务
    app.run(host="0.0.0.0", port=8035)
