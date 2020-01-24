#导入Flask类库
from flask import Flask,request,make_response,redirect,url_for,abort,session
#导入类库
from flask_script import Manager
#创建应用实例

app=Flask(__name__)

app.config['SECRET_KEY'] = '加密用的秘钥字符串'
# 创建对象
manager = Manager(app)


#视图函数
@app.route('/')
def index():
    return '<h1>Hello AAAAAAGGFlask!</h1>'

@app.route('/user/<username>')
def welcome(username):
    return '<h1>HELLO,你妹的 %s!</h1>' % username

#带类型限定的参数
@app.route('/test/<path:info>')
def test(info):
    return info

@app.route('/request/<path:info>')
def url(info):
    #完整的请求的url
    # return request.url
    #去掉GET参数的URL
    # return request.base_url
    #只有主机和端口号的URL
    # return request.host_url
    #装饰器中写的路由地址
    # return request.path
    #客户端的IP地址
    # return request.remote_addr
    #请求方法类型GET/POST
    # return request.method
    #所有的GET参数都保存到args字典中
    # return str(request.args)
    #所有的请求头信息都在headers字段中
    return request.headers.get('User-Agent')

#响应构造
@app.route('/response/')
def response():
    #不指定状态码，默认为200，表示OK
    # return 'OK'
    #可以指定状态码，以元祖的形式
    # return '你TM在逗我？',888
    #先构造一个响应，然后返回，构造是可以指定状态码
    resp=make_response('HELLO 你大爷',999)
    return resp

#重定向
@app.route('/old/')
def old():
    # return '这是最开始'
    #重定向到指定网址
    # return redirect('https://www.baidu.com')
    # return redirect('/new/')
    return redirect(url_for('welcome',username='妹总'))
@app.route('/new/')
def new():
    return '这是新内容'

#终止abort
@app.route('/login/')
def login():
    # return '欢迎登录'
    abort(200)

#会话控制session
@app.route('/set_session/')
def set_session():
    session['username']='xiaoming'
    return 'session已设置'

@app.route('/get_session/')
def get_session():
    return session.get('username','who are you')




#启动实例(只在当前模块运行)
if __name__=='__main__':
    # app.run(debug=True,threaded=True)
    manager.run()


#debug:是否开启调试模式(代码更新可以自动重启)，默认为False
#threaded:是否开启多线程，默认为False
#port:指定端口号，默认为5000
#host:指定主机，默认127.0.0.1，设置为0.0.0.0可以通过IP访问


