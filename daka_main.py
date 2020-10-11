# -*- coding=utf-8 -*-
import daka_plus
import getpass
import logging
from multiprocessing import Process

from flask import Flask
from flask import request
logging.basicConfig(filename='username.log', level=logging.INFO)

# 启动flask
# 当收到一个表单就加一个打卡子程序
# 
def getInfo(form):
    items = ["username", "major",
            "grade", "building", "dormitory", "password"]
    default = [None, "计算机科学与技术", 2020, "文苑6公寓", None, None]
    dic = {}
    for idx, i in enumerate(items):
        dic[i] = form[i]
        if dic[i] == "":
            dic[i] = default[idx]
    
    return dic


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return '<h1>Daka: http://59.72.118.127:8035/daka</h1>'

@app.route('/daka', methods=['GET'])
def signin_form():
    return '''<form action="/daka" method="post">
              
              <p>username 邮箱前缀（如:xiaoming20）：<input name="username"></p>
              <p>major 默认为计算机科学与技术（不用填写即可）：<input name="major"></p>
              <p>grade （如：2020，默认2020）：<input name="grade"></p>
              <p>building （如：文苑6公寓, 默认文苑6公寓）：<input name="building"></p>
              <p>dormitory 寝室号：<input name="dormitory"></p>
              <p>密码：<input name="password" type="password"></p>
              <p><button type="submit">Auto Daka</button></p>
              </form>'''

@app.route('/daka', methods=['POST'])
def signin():
    # 需要从request对象读取表单内容：
    # 获取信息
    dic = getInfo(request.form)
    # print(dic)
    logging.info(dic["username"])

    p = Process(target=daka_plus.signProgram, args=(dic,))
    p.start()
    return f'<h3>{dic["username"]}已添加到自动打卡！</h3>'
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8035)