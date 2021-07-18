from flask import (
    session,
    redirect,
    url_for,
    render_template,
    request,
    Blueprint
)

main = Blueprint('main', __name__)


@main.route('/', methods=["GET", "POST"])
def login():
    if request.form.get('qq_id') is not None:
        session['qq_id'] = request.form['qq_id']
        session['qq_password'] = request.form['qq_password']
        return redirect(url_for('.tts_page'))
    elif request.method == "GET":
        return render_template("login.html")


@main.route('/chat')
def tts_page():
    qq_id = session.get("qq_id", "")
    qq_password = session.get("qq_password", "")

    # text_to_fe 存放 bot获取的信息，准备发送给前端，进行进一步的修改
    session["text_to_fe"] = ["Guo", "Chan", "S", "B"]

    if qq_id == "":
        return redirect(url_for(".login"))

    return render_template("tts.html")

# @main.route("/add/text_to_fe")
# def text_to_fe():

