from flask import (
    Flask,
    session
)
from flask_socketio import (
    SocketIO,
    emit,
    join_room,
    leave_room,
)
import time
socketio = SocketIO()


@socketio.on('connect', namespace="/chat")
def hello():
    print("*** get connect")


# 给前端 聊天消息
@socketio.on("refresh", namespace="/chat")
def text_to_fe():
    print("*** refresh")
    time_str = time.asctime( time.localtime(time.time()))

    # 这里获取 bot 收到的消息
    # with open('sbsb.txt', 'r') as f:
    #     output_word = f.readlines()
    #     emit("text_to_fe", {"msg": "{} {}".format(output_word, time_str)})

    output_list = session.get("text_to_fe", "")
    if output_list:
        output_word = output_list.pop(0)
        emit("text_to_fe", {"msg": "{} {}".format(output_word, time_str)})

        session["text_to_fe"].append("{}".format(time_str))


@socketio.on("send_to_be", namespace="/chat")
def get_from_fe(data):
    text = data.get("msg", "")
    print("*** get_from_fe:", text)