import os
import requests
import json
import websockets
import asyncio
import xml.etree.ElementTree as ET
import configparser

'''
{
    "type": "GroupMessage",
    "sender": {
        "id": 123,
        "memberName": "",
        "specialTitle": "",
        "permission": "OWNER",
        "joinTimestamp": 0,
        "lastSpeakTimestamp": 0,
        "muteTimeRemaining": 0,
        "group": {
            "id": 321,
            "name": "",
            "permission": "MEMBER",
        },
    },
    "messageChain": [
        {
            "type": "Plain",
            "text": "Mirai"
        }
    ] 
}
'''

#print formatted message
def print_json_message(message):
    print(json.dumps(message),indent = 4)

def get_session_key(message):
    print("*** Get Session Key ",message["data"]["session"])
    return message["data"]["session"]

#get message type
def get_message_type(message):
    if "type" in message["data"]:
        return message["data"]["type"]
    else:
        return "False"

#get message chian type
def get_message_chain_type(message):
    if "messageChain" in message["data"]:
        if "type" in message["data"]["messageChain"][1]:
            return message["data"]["messageChain"][1]["type"]
    return "False"

#get sender id in message
def get_sender_id(message):
    if "sender" in message["data"]:
        if "id" in message["data"]["sender"]:
            return str(message["data"]["sender"]["id"])
    else:
        return "False"

#get group id from group message
def get_group_id(message):
    if "group" in message["data"]["sender"]:
        if "id" in message["data"]["sender"]["group"]:
            return str(message["data"]["sender"]["group"]["id"])
    return "False"

#get text by certain group member in a group
def get_group_text(message):
    #print("*** Get Group Message")
    if len(message["data"]["messageChain"]) == 2:
            return message["data"]["messageChain"][1]["text"]
    else:
        return False

#write to ssml.xml
def write_xml(plain_txt):
    #print("*** Write XML")
    text_path = "../TTS/ssml.xml"
    tree = ET.parse(text_path)
    for node in tree.findall("voice"):
        node.text = plain_txt
    tree.write(text_path, encoding="utf-8")

#write to temp.txt
def write_text(text_path, plain_text):
    #print("*** Write Text ")
    file = open(file = text_path, mode =  "w+")
    file.write(plain_text)

#exctute Text-to-Speech.py
def exec_tts():
    #print("*** Execute TTS")
    start_py = r"../TTS/Text-to-Speech.py"
    r = os.system("python %s" %start_py)

    if r != 0:
        raise Exception("TTS failed!")

#build ws connection to host
# - ws_host - host listen to
# - bot_id - bot id
# - text_path - text output path
# - sender id - sender id listen to
# - group id - group id listen to
async def ws_connect_mirai(ws_host, bot_id, text_path, sender_id, group_id):
    session_key = ""
    print("*** WebSocket Connect")
    url = ws_host + '/message?verifyKey=TextToSpeech&qq=' + bot_id
    async with websockets.connect(url) as websoket:
        async for data in websoket:
            message = json.loads(data)
            #print(message)
            if "data" in message:
                if "session" in message["data"]:
                    session_key = get_session_key(message)
                    http_bind("http://localhost:8080", bot_id, session_key)
                else:
                    if "GroupMessage" in get_message_type(message):
                        if "Plain" in get_message_chain_type(message) and sender_id in get_sender_id(message):
                            if sender_id in get_sender_id(message) and group_id in get_group_id(message):
                                plain_text = get_group_text(message)
                                if plain_text or not plain_text.startswith("."):
                                    write_xml(plain_text)
                                    exec_tts()
                                    send_group_voice("http://localhost:8080", group_id, session_key)
                                    #send_friend_voice("http://localhost:8080", group_id, session_key)


def http_bind(http_host, bot_id, session_key):
    print("*** Bind Session ", end="")
    bind_url = "/bind"
    url = http_host + bind_url
    message = {
        "sessionKey": session_key,
        "qq": bot_id,
    }
    message = json.dumps(message)
    response = requests.post(url = url, data = message).json()
    print(response)

#send voice to group
def send_group_voice(http_host, target_id, session_key):
    print("*** Send Group Voice ", end="")
    send_message = "/sendGroupMessage"
    url = http_host + send_message
    message = {
        "sessionKey": session_key,
        "target": target_id,
        "messageChain": [
            {"type": "Voice",
             "path": "../Auto-Text-Reader/temp/temp.amr"
            }
        ]
    }
    message = json.dumps(message)
    response = requests.post(url = url, data = message).json()
    print(response)

#send voice to friend
def send_friend_voice(http_host, target_id, session_key):
    send_message = "/sendFriendMessage"
    url = http_host + send_message
    message = {
        "sessionKey": session_key,
        "target": 460411092,
        "messageChain": [
            {
                "type": "Voice",
                "path": "../Text-To-Speech-Python/temp/temp.amr"
 #               "text": "wwww"
             }
        ]
    }
    message = json.dumps(message)
    response = requests.post(url = url, data = message).json()
    print("*** Send Friend Voice\n", response)



#read config.txt and get ids
def read_ids():
    config = configparser.ConfigParser()
    config.read("../../config/config.ini")
    bot_id = config["common"]["BotId"]
    sender_id = config["common"]["SenderId"]
    group_id = config["common"]["GroupId"]
    print("*** Read Config IDs", bot_id, sender_id, group_id)
    return bot_id, sender_id, group_id
'''
    file = open("../../config/config.txt","r")
    bot_id = file.readlines()[0].split(":")[1]
    bot_id = bot_id.split("\n")[0]
    file.seek(0)
    sender_id = file.readlines()[2].split(":")[1]
    sender_id = sender_id.split("\n")[0]
    file.seek(0)
    group_id = file.readlines()[3].split(":")[1]
    group_id = group_id.split("\n")[0]
    file.close()
'''


def main():

    text_path = "../../temp/temp.txt"
    ws_host = "ws://localhost:8080"
    bot_id, sender_id, group_id = read_ids()
    asyncio.get_event_loop().run_until_complete(ws_connect_mirai(ws_host, bot_id, text_path, sender_id, group_id))
if __name__ == "__main__":
    main()
