import os
import requests
import json
import websockets
import asyncio
import xml.etree.ElementTree as ET

#print formatted message
def print_json_message(message):
    print(json.dumps(message),indent = 4)

#get message chain type
def get_message_chain_type(message):
    if "data" in message:
        if "type" in message["data"]:
            return message["data"]["type"]
        else:
            raise Exception("Type does not exist!")
    else:
        raise Exception("Data does not exist!")

#get message type
def get_message_type(message):
    if "data" in message:
        if "messageChain" in message["data"]:
                return message["data"]["messageChain"][1]["type"]


#get qq id in message
def get_qqid(message):
    if "data" in message:
        if "sender" in message["data"]:
            if "id" in message["data"]["sender"]:
                return str(message["data"]["sender"]["id"])
    else:
        raise Exception("Data does not exist!")

#get group id from group message
def get_group_message_group_id(message):
    if "data" in message:
        return str(message["data"]["sender"]["group"]["id"])

#get text by certain group member in a group
def get_text_in_group_by_sender(message, sender_id, group_id):
    if "data" in message:
        if "messageChain" in message["data"] and len(message["data"]["messageChain"]) == 2:
            if "Plain" in message["data"]["messageChain"][1]["type"]:
                return message["data"]["messageChain"][1]["text"]

    else:
        raise Exception("Data does not exist!")


#write to temp.txt
def write_text(text_path, plain_text):
    print("--- Writing Text ---")
    file = open(file = text_path, mode =  "w+")
    file.write(plain_text)

#write to ssml.xml
def writ_xml(plain_txt):
    print("--- Write XML ---")
    text_path = "../TTS/ssml.xml"
    tree = ET.parse(text_path)
    for node in tree.findall("voice"):
        node.text = plain_txt
    tree.write(text_path, encoding="utf-8")



#build ws connection to host
#ws_host - host listen to
#sessionKey - session eky
#bot_id - bot id
#text_path - text output path
#sender id - sender id listen to
#group id - group id listen to
async def ws_connect_mirai(ws_host, sessionKey, bot_id, text_path, sender_id, group_id):
    print("--- WebSocket Connect ---")
    url = ws_host + '/message?verifyKey=TextToSpeech&qq=' + bot_id
    async with websockets.connect(url) as websoket:
        async for data in websoket:
            message = json.loads(data)
            print(message)
            #屎
            if "type" in message["data"]:
                if sender_id in get_qqid(message) and "GroupMessage" in get_message_chain_type(message):
                    if "Plain" in get_message_type(message) and group_id in get_group_message_group_id(message):
                        plain_text = get_text_in_group_by_sender(message, sender_id, group_id)
                        if not plain_text.startswith("."):
                            writ_xml(plain_text)
                            exec_tts()
                            send_group_voice("http://localhost:8080", group_id, sessionKey)
                            #send_friend_voice("http://localhost:8080", group_id, sessionKey)


#get ws sessionKey and return
async def ws_get_sessionKey(ws_host, bot_id):
    print("---Get Session Key---")
    url = ws_host + '/message?verifyKey=TextToSpeech&qq=' + str(bot_id)
    async with websockets.connect(url) as websoket:
        raw_data = await websoket.recv()
        message = json.loads(raw_data)
        print(message)
        if "data" in message:
            if "session" in message["data"]:
                print("Session key:", message["data"]["session"])
                return message["data"]["session"]
            else:
                raise Exception("No session key!")
        else:
            raise Exception("No data")

#send voice to group
def send_group_voice(http_host, target_id, session_key):
    send_message = "/sendGroupMessage"
    url = http_host + send_message
    message = {
        "sessionKey": session_key,
        "target": target_id,
        "messageChain": [
            {"type": "Voice",
             "path": "../Text-To-Speech-Python/temp/temp.amr"
            }
        ]
    }
    message = json.dumps(message)
    response = requests.post(url = url, data = message).json()
    print("--- Send Group Voice ---\n", response)

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
    print("--- Send Friend Voice ---\n", response)

#exctute Text-to-Speech.py
def exec_tts():
    start_py = r"../TTS/Text-to-Speech.py"
    r = os.system("python %s" %start_py)
    print("--- Execute TTS ---")
    if r != 0:
        raise Exception("TTS failed!")

def read_ids():
    file = open("../../config/config.txt","r")
    qq_id = file.readlines()[2].split(":")[1]
    qq_id = qq_id.split("\n")[0]
    file.seek(0)
    group_id = file.readlines()[3].split(":")[1]
    group_id = group_id.split("\n")[0]
    print(qq_id, group_id)
    file.close()
    return qq_id, group_id
def main():
    text_path = "../../temp/temp.txt"
    bot_id = "3558994956"
    ws_host = "ws://localhost:8080"
    sender_id, group_id = read_ids()
    sessionKey = asyncio.get_event_loop().run_until_complete(ws_get_sessionKey(ws_host, bot_id))
    asyncio.get_event_loop().run_until_complete(ws_connect_mirai(ws_host,sessionKey, bot_id, text_path, sender_id, group_id))
    #writ_xml("人呢我佛了")
if __name__ == "__main__":
    main()
