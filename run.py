# coding=utf-8
# wechat auto reply
import os
import itchat
import time
import random


# 回复文本／表情
# 封装好的装饰器，接收Text消息
# 设置接收好友和微信公众号回复
# 接收群聊isGroupChat=True
@itchat.msg_register(['Text'], isFriendChat=True, isMpChat=True)
def text_reply(msg):
    # 将接收的指定好友的的回复转发到小冰机器人，用小冰的回复去回复好友，实现自动聊天
    if msg['FromUserName'] == userName:
        if msg.__getitem__("Type") == 'Text':
            itchat.send(msg['Text'], toUserName=mpsName)
    if msg['FromUserName'] == mpsName:
        if msg.__getitem__("Type") == 'Text':
            time.sleep(random.randint(0, 10))
            itchat.send(msg['Text'], toUserName=userName)


# 回复文件（图片／动画表情／语音／附件／视频）
# Picture:只能下载自己的图片或者收藏的表情，微信的表情包不支持下载
@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'], isFriendChat=True, isMpChat=True)
def download_files(msg):
    # 转发文件实现：
    # 1. 下载好友发送文件／小冰回复文件
    # 2. 文件发送给小冰／回复好友
    # 3. 删除文件
    if msg['FromUserName'] == userName:
        # 下载文件
        # msg.download(msg['FileName'])
        msg['Text'](msg['FileName'])
        itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg["FileName"]), mpsName)
    if msg['FromUserName'] == mpsName:
        time.sleep(random.randint(0, 10))
        msg['Text'](msg['FileName'])
        itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg["FileName"]), userName)

    # 执行shell命令删除下载的文件
    os.popen('find . -name *.gif | xargs rm -fr && '
             'find . -name *.png | xargs rm -fr && '
             'find . -name *.mp4 | xargs rm -fr')


if __name__ == '__main__':
    itchat.auto_login()

    # 获取指定好友UserName，用于发送消息
    users = itchat.search_friends(name='好友微信昵称'.decode("utf-8"))  # 字典列表
    userName = users[0]["UserName"]

    # 获取指定公众号
    # 小冰日常机器人／小冰机器人等
    mps = itchat.search_mps(name='小冰日常机器人'.decode("utf-8"))
    mpsName = mps[0]['UserName']

    itchat.run()
