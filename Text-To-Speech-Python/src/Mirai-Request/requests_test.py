import requests
import json
import websockets
import asyncio


def http_api_version(bot_host):
    url = bot_host + "/about"
    response = requests.get(url=url).json()
    print("*** response: {}".format(response))


def send_friend_msg(bot_host):
    send_msg = "/sendFriendMessage"
    url = bot_host + send_msg
    msg = {
        "sessionKey": "",
        "target": "460411092",
        "messageChain": [
            {"type": "Plain", "text": "我是\n"},
            {"type": "Plain", "text": "你爹"},
        ]
    }

    msg = json.dumps(msg)
    response = requests.post(url=url, data=msg).json()
    print("*** response: {}".format(response))

def get_message_count(bot_host):
    url = bot_host + "/countMessage?sessionKey=false"
    response = requests.get(url=url).json()
    print("*** response: {}".format(response))

def fetch_latest_message(bot_host):
    url = bot_host + "/fetchLatestMessage?sessionKey=false&count=1"
    response = requests.get(url=url).json()
    print("*** response: {}".format(response))
    print("data: {}".format(response["data"]))

async def ws_send_friend_msg(bot_host):
    url = bot_host + '/message?verifyKey=false'
    msg = {
        "syncId": "",                # 消息同步的字段
        "command": "sendFriendMessage", # 命令字
        "subCommand": "",             # 子命令字, 可空
        "content": {
            "sessionKey": "",
            "target": "460411092",
            "messageChain": [
                {"type": "Plain", "text": "hello"},
            ]
        }                   # 命令的数据对象, 与通用接口定义相同
    }
    msg = json.dumps(msg)
    async with websockets.connect(url) as websoket:
        await websoket.send(msg)
        receive = await websoket.recv()
        print(receive)

async def ws_get_msg(bot_host):
    url = bot_host + '/message'
    async with websockets.connect(url) as websoket:
        async for data in websoket:
            #print(message)
            message = json.loads(data)
            print(message)
            if "messageChain" in message["data"]:
                print(message["data"]["messageChain"][1]["text"])

async def ws_get_msg_by_sender(bot_host, sender_id):
    url = bot_host + '/message'
    async with websockets.connect(url) as websoket:
        async for data in websoket:
            #print(message)
            message = json.loads(data)
            #print(json.dumps(message, indent = 4))
            print(get_group_text_from_message(message))
            print(get_id_in_group_from_message(message))
            """
            if "type" in message["data"]:
                if "GroupMessage" in message["data"]["type"]:
                    if "Plain" in message["data"]["messageChain"][1]["type"]:
                        if sender_id in message["data"]["sender"]["id"]:
                            print(message["data"]["sender"]["id"])
                            print(message["data"]["messageChain"][1]["text"])
            """

def get_group_text_from_message(message):
    if "type" in message["data"]:
        if "GroupMessage" in message["data"]["type"]:
            if "Plain" in message["data"]["messageChain"][1]["type"]:
                    return message["data"]["messageChain"][1]["text"]

def get_id_in_group_from_message(message):
    if "type" in message["data"]:
        if "GroupMessage" in message["data"]["type"]:
            if "Plain" in message["data"]["messageChain"][1]["type"]:
                    return message["data"]["sender"]["id"]



def main():
    ws_bot_host = "ws://localhost:8080"
    #http_api_version(bot_host)
    #send_friend_msg(bot_host)
    #get_message_count(bot_host)
    #fetch_latest_message(bot_host)
    #get_message_count(bot_host)

    #asyncio.get_event_loop().run_until_complete(ws_send_friend_msg(ws_bot_host))
    #asyncio.get_event_loop().run_until_complete(ws_get_msg(ws_bot_host))
    asyncio.get_event_loop().run_until_complete(ws_get_msg_by_sender(ws_bot_host, "Ooooo"))

if __name__ == "__main__":
    main()
