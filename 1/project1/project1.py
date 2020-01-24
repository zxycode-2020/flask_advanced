#导入Flask类库
from flask import Flask
#创建应用实例
app=Flask(__name__)
#视图函数
@app.route('/')
def index():
    return '<h1>Hello AAAAAAGGFlask!</h1>'
#启动实例(只在当前模块运行)
if __name__=='__main__':
    app.run(debug=True,threaded=True)


#debug:是否开启调试模式(代码更新可以自动重启)，默认为False
#threaded:是否开启多线程，默认为False
#port:指定端口号，默认为5000
#host:指定主机，默认127.0.0.1，设置为0.0.0.0可以通过IP访问


