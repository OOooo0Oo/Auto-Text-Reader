import tkinter
import configparser

class LoginPage(object):

    def __init__(self, master=None):
        self.window = master
        self.window.geometry('%dx%d' % (400, 180)) #设置窗口大小
        self.configuration()

    def configuration(self):
        self.page = tkinter.Frame(self.window)
        self.page.pack()
        tkinter.Label(self.page, text="Bot ID").grid(row = 0,column =0)
        tkinter.Label(self.page, text="Bot Password").grid(row = 1,column =0)
        tkinter.Label(self.page, text="TTS API Key").grid(row = 2,column =0)
        tkinter.Label(self.page, text="TTS API Area").grid(row = 3,column =0)
        tkinter.Label(self.page, text="Sender ID").grid(row = 4,column =0)
        tkinter.Label(self.page, text="Group ID").grid(row = 5,column =0)

        self.e1 = tkinter.Entry(self.page)
        self.e2 = tkinter.Entry(self.page)
        self.e3 = tkinter.Entry(self.page)
        self.e4 = tkinter.Entry(self.page)
        self.e5 = tkinter.Entry(self.page)
        self.e6 = tkinter.Entry(self.page)

        config = configparser.ConfigParser()
        config.read("../../config/config.ini")
        if config["common"]["botid"]:
            self.e1.insert(0, config["common"]["botid"])
        if config["common"]["botpassword"]:
            self.e2.insert(0, config["common"]["botpassword"])
        if config["common"]["tts api key"]:
            self.e3.insert(0, config["common"]["tts api key"])
        if config["common"]["tts api area"]:
            self.e4.insert(0, config["common"]["tts api area"])
        if config["common"]["senderid"]:
            self.e5.insert(0, config["common"]["senderid"])
        if config["common"]["groupid"]:
            self.e6.insert(0, config["common"]["groupid"])

        self.e1.grid(row =0 ,column =1)
        self.e2.grid(row =1 ,column =1)
        self.e3.grid(row =2 ,column =1)
        self.e4.grid(row =3 ,column =1)
        self.e5.grid(row =4 ,column =1)
        self.e6.grid(row =5 ,column =1)

        button1 = tkinter.Button(self.page, text = "Confirm", command = self.confirm)
        button1.grid(rowspan = 9, sticky = "s")


    def confirm(self):
        #renzheng
        config = configparser.ConfigParser()
        config.read("../../config/config.ini")
        config.set("common", "BotId", self.e1.get())
        config.set("common", "botpassword", self.e2.get())
        config.set("common", "tts api key", self.e3.get())
        config.set("common", "tts api area", self.e4.get())
        config.set("common", "senderid", self.e5.get())
        config.set("common", "groupid", self.e6.get())
        with open('../../config/config.ini', 'w') as configfile:
            config.write(configfile)

        self.page.destroy()
        SendPage(self.window)

class SendPage(object):

    def __init__(self, master=None):
        self.window = master #定义内部变量root
        self.window.geometry('%dx%d' % (600, 400)) #设置窗口大小
        self.sendpage()

    def sendpage(self):
        message = ""
        self.page = tkinter.Frame(self.window)
        self.page.pack()

        text = tkinter.Text(self.page, width = 80, height = 20)
        text.grid(row = 0)

        button1 = tkinter.Button(self.page, text = "Send")
        button1.grid(rowspan = 9, sticky = "s")



def initialize_window():
    window = tkinter.Tk()

    window.title("Auto Text Reader")
    window.geometry("500x300")

    return window


def main():
    window = initialize_window()
    LoginPage(window)
    window.mainloop()

if __name__ == '__main__':
    main()