from flask import (
    Flask,
    session
)
from route import main as main_blueprint
from event import socketio


app = Flask(__name__)
app.secret_key = 'random string'
app.register_blueprint(main_blueprint)

socketio.init_app(app)


if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host="127.0.0.1",
        port="7077",
    )
    socketio.run(app, **config)
