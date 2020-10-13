# Auto Daka

经常看手机对手机不好，但是老师又要求天天体温打卡怎末办？

试试这个自动打卡的程序

在[链接](http://59.72.118.127:8035/daka)中登录自身的信息，实现自动打卡 

如果不想自动打卡了，请联系我。。。

或者如果学院不要求打卡了，这个程序也会被关掉。。。

**注意**：这个程序写得比较死，是做的研究生打卡的:)

🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫🤫

## 免责声明
本自动程序适用于 2020-2021 秋季学期吉林大学研究生每日健康打卡（三测温一点名）

使用本程序自动提交打卡，你必须实际完成一日三测温，在指定时间回到寝室，并在身体状况出现异常时立刻联系校医院和辅导员。

如运行本程序，您理解并认可，本自动程序的一切操作均视为您本人进行、或由您授权的操作。本程序作者对您因使用此程序可能受到的损失、处罚以及造成的法律后果不负任何责任。（copy from [JLU Daily Reporter](https://github.com/fichas/JLU-Daily-Reporter)）


## 1. How to use it?

直接登录http://59.72.118.127:8035/daka 填写相关信息, 若是本学院学生的话简单填填、其他默认就可。

![](https://gitee.com/JLUtangchuan/imgbed/raw/master/img/20201011213123.png)

- 一定要注意邮箱密码填写正确！！！
- 一定要注意邮箱密码填写正确！！！
- 一定要注意邮箱密码填写正确！！！


## 2. 如果想自己部署

1. 配置环境
    ```
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome*
    sudo apt-get -f install
    ```
2. 改改daka_plus.py的内容
