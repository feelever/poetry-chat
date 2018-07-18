# -*- coding: utf-8 -*-
import requests
import json
import itchat, time
from itchat.content import *
from itchat.storage.messagequeue import Message
data={
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "你好"
        }
    },
    "userInfo": {
        "apiKey": "2cdac5994ec44ec7a90c8c834f5d5091",
        "userId": "142233"
    }
}

def turing_answer(data):    
    headers={"Content-Type":"application/json"}
    page = requests.post('http://openapi.tuling123.com/openapi/api/v2',data=json.dumps(data),headers=headers)
    html = json.loads(page.text)
    return html
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    data['perception']['inputText']['text']=msg.text
    reply(msg,data)

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg.download(msg.fileName)
    typeSymbol = {
        PICTURE: 'img',
        VIDEO: 'vid', }.get(msg.type, 'fil')
    return '@%s@%s' % (typeSymbol, msg.fileName)

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply2(msg):
    data['perception']['inputText']['text']=msg.text
    if msg.get("User").get("NickName")=="wishu":
        reply(msg,data)
def reply(msg,data):
    turing = turing_answer(data)        
    for result in turing['results']:
        if  result['resultType']=='image':
            html = requests.get(result['values']['image'])
            with open('picture.jpg', 'wb') as file:
                file.write(html.content)
            msg.user.send_image('picture.jpg')
        if  result['resultType']=='text':
            msg.user.send(result['values']['text'])

itchat.auto_login(hotReload=True)
chatroom = itchat.search_chatrooms(name="wishu")[0]
itchat.send_image(r"C:\Users\jiguang\Desktop\chrome\captcha.png",toUserName=chatroom.get("UserName"))
itchat.run(True)
 
