依赖
flask
flask_socketio
eventlet

1，从前端获取 q号和密码，后端存在session里面
2，前端定时向后端要 聊天信息
3，后端的聊天信息 目前存在session里面（也可以存在文档中），前端有请求时发送
4，前端获取聊天信息，可以更改，按speech，改好的发回给后端。并再次开启计时器
5，走的是websocket
6，还没有和bot相关程序结合