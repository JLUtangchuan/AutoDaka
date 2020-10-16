# -*- coding=utf-8 -*-

import base64
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import json
from datetime import datetime
import time
import random
import traceback
import getpass
import logging
import smtplib
# import json
import poplib
from email import parser
from email.mime.text import MIMEText
from email.header import Header

log_fmt = "%(asctime)s|%(message)s"

logging.basicConfig(filename='qiandao.log', format=log_fmt,level=logging.INFO)

URL = "https://ehall.jlu.edu.cn/taskcenter/workflow/appall?tags=%E7%A0%94%E7%A9%B6%E7%94%9F%E9%99%A2"
WAIT = 1
# 邮箱,密码,专业,年级,校区,宿舍楼,寝室,硕博0/1

def sendEmail(msg_from, msg_to, auth_id, title, content):
    """发送邮件：目前只支持qq邮箱自动发送邮件

    Args:
        msg_from ([type]): [description]
        msg_to ([type]): [description]
        auth_id ([type]): [description]
        title ([type]): [description]
        content ([type]): [description]
    """
    msg = MIMEText(content)
    msg['Subject'] = title
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com",465)
        s.login(msg_from, auth_id)
        s.sendmail(msg_from, msg_to, msg.as_string())
        # print(msg_from, "发送成功")
    except s.SMTPException:
        print("发送失败")
    finally:
        s.quit()

def sign(sign_time, index, info):
    username = info["username"]
    major = info["major"]
    grade = info["grade"]
    campus = "中心校区"
    building = info["building"]
    dormitory = info["dormitory"]
    password = info["password"]
    if info["xuewei"] == "硕士":
        type = 0
    else:
        type = 0
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')  # 这个配置很重要

    # 后面是你的浏览器驱动位置，记得前面加r'','r'是防止字符转义的
    driver = webdriver.Chrome(r'/home/tangchuan/workdir/daka/chromedriver', chrome_options=chrome_options)
    driver_ = driver
    mainWindow = driver_.current_window_handle
    # 用get打开页面
    driver.get(
        "https://ehall.jlu.edu.cn/sso/login?x_started=true&redirect_uri=https%3A%2F%2Fehall.jlu.edu.cn%2Fsso%2Foauth2%2Fauthorize%3Fscope%3Dopenid%26response_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Fehall.jlu.edu.cn%252Finfoplus%252Flogin%253FretUrl%253Dhttps%25253A%25252F%25252Fehall.jlu.edu.cn%25252Finfoplus%25252Foauth2%25252Fauthorize%25253Fx_redirected%25253Dtrue%252526scope%25253Dprofile%25252Bprofile_edit%25252Bapp%25252Btask%25252Bprocess%25252Bsubmit%25252Bprocess_edit%25252Btriple%25252Bstats%25252Bsys_profile%25252Bsys_enterprise%25252Bsys_triple%25252Bsys_stats%25252Bsys_entrust%25252Bsys_entrust_edit%252526response_type%25253Dcode%252526redirect_uri%25253Dhttps%2525253A%2525252F%2525252Fehall.jlu.edu.cn%2525252Ftaskcenter%2525252Fwall%2525252Fendpoint%2525253FretUrl%2525253Dhttps%252525253A%252525252F%252525252Fehall.jlu.edu.cn%252525252Ftaskcenter%252525252Fwechat%252525252Fappall%252526client_id%25253D1640e2e4-f213-11e3-815d-fa163e9215bb%26state%3D26dac3%26client_id%3DbwDBpMCWbid5RFcljQRP#/")
    # print("  ", driver.title, driver.current_url)

    # 登陆界面
    driver.find_element_by_xpath("//input[@name='username']").clear()
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//input[@name='password']").clear()

    driver.find_element_by_xpath("//input[@name='password']").send_keys(base64.b64decode(password).decode("utf-8"))
    time.sleep(WAIT)
    driver.find_element_by_xpath("//input[@name='login_submit']").click()

    # print('登录完成')

    # 所有办理事项界面
    time.sleep(WAIT)
    # print("  ", driver.title, driver.current_url)

    # 每日健康打卡
    driver.get("https://ehall.jlu.edu.cn/infoplus/form/YJSMRDK/start")
    time.sleep(WAIT)
    # print("  ", driver.title, driver.current_url)

    # 循环页面句柄，获取非主页句柄，只适用于2个页面窗口的情况下
    toHandle = driver_.window_handles

    for handle in toHandle:
        if handle == mainWindow:
            continue
    driver.switch_to_window(handle)

    time.sleep(2 * WAIT)

    # 得到输入的表单
    tbody = driver.find_elements_by_tag_name("tbody")[1]

    # 输入专业
    tbody.find_element_by_xpath("//input[@name='fieldZY']").clear()
    tbody.find_element_by_xpath("//input[@name='fieldZY']").send_keys(major)

    # 输入年级，校园，宿舍楼
    tbody.find_element_by_xpath("//select[@name='fieldSQnj']").send_keys(grade)
    tbody.find_element_by_xpath("//select[@name='fieldSQxq']").send_keys(campus)
    tbody.find_element_by_xpath("//select[@name='fieldSQgyl']").send_keys(building)

    time.sleep(WAIT)
    # 输入宿舍号
    tbody.find_element_by_xpath("//input[@name='fieldSQqsh']").clear()
    tbody.find_element_by_xpath("//input[@name='fieldSQqsh']").send_keys(dormitory)

    # 得到一天四次测温度
    temperature = tbody.find_elements_by_xpath("//input[@type='radio' and @value='1']")

    # 硕博选项，0硕1博
    temperature[type].click()
    time.sleep(WAIT)

    # 早中晚温度选项
    if (index == 1 or index == 2 or index == 3):
        temperature[index].click()
    # 夜间无这个选项
    elif (index == 4):
        pass

    # 点击提交
    driver.find_elements_by_xpath("//a[@class='command_button_content']")[0].click()
    time.sleep(WAIT)

    # 弹出对话框点击确定
    driver.find_element_by_xpath("//button[@class='dialog_button default fr']").click()
    time.sleep(WAIT)

    # 获得最终的提示消息
    time.sleep(WAIT)
    warning = driver.find_element_by_xpath("//div[@class='dialog_body']").text
    # print("  ", sign_time, warning)

    time.sleep(random.random())
    driver.quit()

def signProgram(info):
    filename = './info.json'
    with open(filename, 'r') as f:
        dic = json.load(f)
    msg_from = dic['msg_from'] #发送方邮箱
    passwd = dic['passwd']  #填入发送方邮箱的授权码
    msg_to = info["username"] + dic["msg_to"] #收件人邮箱
    try_num = 30
    while True:
        # print("---------------------------------------------------")
        localtime = time.strftime("%Y.%m %H:%M:%S", time.localtime())
        index = -1
        # print(localtime, end="\t")

        hour = int(localtime.split(" ")[1].split(":")[0])
        minite = int(localtime.split(" ")[1].split(":")[1])

        if (hour == 7):
            sign_time = "早签到"
            index = 1
        elif (hour == 11):
            sign_time = "午签到"
            index = 2
        elif (hour == 17):
            sign_time = "晚签到"
            index = 3
        elif (hour == 21):
            sign_time = "夜签到"
            index = 4
        else:
            # print(60 - minite, "分钟后再次尝试")
            time.sleep((60 - minite) * 60)
            continue
        # print(sign_time)

        try:
            sign(sign_time, index, info)
            content = f"{info['username']} {sign_time}-签到完毕"
            logging.info(content)
            try_num = 30
            # sendEmail(msg_from, msg_to, passwd, "自动打卡", content)
            time.sleep((4 * 60 - minite) * 60)
        except Exception:
            try_num -= 1
            print("error: ", try_num, info['username'])
            print(traceback.format_exc())
            time.sleep(WAIT)
            if try_num <= 0:
                break

        
if __name__ == "__main__":
    pass
    
