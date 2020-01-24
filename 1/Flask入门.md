#Flask入门

### WEB工作原理

1. B/S和C/S架构

   C/S：客户端/服务器架构

   B/S：浏览器/服务器架构

2. web工作原理

   客户端 <=> 服务器(nginx/apache) <=> Python等 <=> 数据库

### Flask框架

1. 简介

   是一个非常小的框架，可以称为微型框架，只提供了一个强健的核心，其它的功能都需要使用扩展来实现。意味着你可以针对自己的需求量身打造

2. 组成

   1. 调试、路由、WSGI系统
   2. 模板引擎(Jinja2，也是有Flask核心人员开发)

3. 安装

   pip install flask

4. 完整程序

   ```python
   # 导入Flask类库
   from flask import Flask
   # 创建应用实例
   app = Flask(__name__)
   # 视图函数(路由)
   @app.route('/')
   def index():
       return '<h1>Hello Flask !</h1>'
   # 启动实例(只在当前模块运行)
   if __name__ == '__main__':
       app.run(threaded=True)
   ```

   说明：默认访问127.0.0.1:5000

5. 参数设置

   | 参数       | 说明                                  |
   | -------- | ----------------------------------- |
   | debug    | 是否开启调试模式(代码更新可以自动重启)，默认为False       |
   | threaded | 是否开启多线程，默认为False                    |
   | port     | 指定端口号，默认为5000                       |
   | host     | 指定主机，默认127.0.0.1，设置为0.0.0.0可以通过IP访问 |

6. 请求与响应

   程序和请求上下文

   | 变量          | 上下文   | 描述                  |
   | ----------- | ----- | ------------------- |
   | current_app | 程序上下文 | 当前激活的程序实例           |
   | g           | 程序上下文 | 处理请求时的临时变量，每次会重置    |
   | request     | 请求上下文 | 请求对象，存放客户端发来的HTTP信息 |
   | session     | 请求上下文 | 用户会话，记录需要"记住"的信息    |

   请求钩子函数

   | 函数                   | 描述            |
   | -------------------- | ------------- |
   | before_first_request | 第一次请求之前       |
   | before_request       | 每次请求之前        |
   | after_request        | 没有异常，每次请求结束之后 |
   | teardown_request     | 每次请求之后，即使有异常  |

   说明：以上钩子函数若写在蓝本中，只能针对被蓝本的请求；若想在蓝本中设置全局有效的钩子函数，需要使用带'app'的相关钩子函数，如：

   第一个请求之前：before_first_request => before_app_first_request

7. 视图函数


   1. 视图函数可以不带参数，见《完整程序》

   2. 视图函数也可以带参数，如下：

      ```python
      @app.route('/user/<username>')
      def welcome(username):
          return '<h1>Hello %s !</h1>' % username
      # 带类型限定的参数，path也是字符串类型，只是不再将/作为分隔符 
      @app.route('/test/<path:info>')
      def test(info):
          return info  
      ```

      说明：

      1. 参数要写在<>中
      2. 视图函数的参数要与路由中的一致
      3. 也可以指定参数类型(int/float/path)，默认是字符串
      4. 路由中最后的'/'最好带上，否则访问时可能会报错

8. request

   ```python
   @app.route('/request/<path:info>')
   def url(info):
       # 完整的请求URL
       # return request.url
       # 去掉GET参数的URL
       # return request.base_url
       # 只有主机和端口号的URL
       # return request.host_url
       # 装饰器中写的路由地址
       # return request.path
       # 请求方法类型GET/POST
       # return request.method
       # 客户端的IP地址
       # return request.remote_addr
       # 所有的GET参数都保存在args字典中
       # return str(request.args)
       # 所有的请求头信息都在headers字段中
       return request.headers.get('User-Agent')
   ```

9. 响应构造(make_response)

   ```python
   @app.route('/response/')
   def response():
       # 不指定状态码，默认为200，表示OK
       # return 'OK'
       # 可以指定状态码，已元组的形式
       # return 'not found', 404
       # 先构造一个响应，然后返回，构造是也可以指定状态码
       resp = make_response('我是通过函数构造的响应', 404)
       return resp
   ```

10. 重定向(redirect)

   ```python
   @app.route('/old/')
   def old():
       # return '这里是原始内容'
       # 重定向到指定网址
       # return redirect('https://www.baidu.com')
       # 重定向到内部的另一路由
       # return redirect('/new/')
       # 根据视图函数找到路由，传递的参数是视图函数名
       # return redirect(url_for('new'))
       # 带参的视图函数也可以构造出来对于的路由
       return redirect(url_for('welcome', username='xiaoming'))

   @app.route('/new/')
   def new():
       return '这里是新的内容'
   ```

11. 终止abort

    ```python
    @app.route('/login/')
    def login():
        #return '欢迎登录'
        # 此处使用abort不是将控制权交给调用的地方，
        # 而是将抛出异常，将控制权交给WEB服务器
        abort(404)
    ```

12. 会话控制cookie/session

    ```python
    # 会话控制cookie
    @app.route('/set_cookie/')
    def set_cookie():
        resp = make_response('cookie已设置')
        # 指定过期时间
        expires = time.time() + 10
        resp.set_cookie('name', 'xiaoming', expires=expires)
        return resp

    @app.route('/get_cookie/')
    def get_cookie():
        return request.cookies.get('name') or '你是哪个二哥'
      

    # 会话控制session
    # 设置秘钥，可能不止一个地方使用该秘钥
    app.config['SECRET_KEY'] = '加密用的秘钥字符串'

    @app.route('/set_session/')
    def set_session():
        session['username'] = 'xiaoqiao'
        return 'session已设置'

    @app.route('/get_session/')
    def get_session():
        return session.get('username', 'who are you ?')
    ```

13. 命令行控制

    说明：默认的项目在不同的模式下不同的设置，在切换时只能通过修改代码来完成，这是有风险的，也是比较繁琐的。那么通过命令行参数控制是一个比较好的选择，需要用第三方扩展flask-script

    安装：pip install flask-script

    使用：

    ```python
    # 导入类库
    from flask_script import Manager
    # 创建对象
    manager = Manager(app)
    if __name__ == '__main__':
        # 启动程序
        manager.run()
    ```

    参数：

    ```shell
    启动：python manage.py runserver [-d] [-r]
    -?, --help		查看帮助
    -d				开启调试模式
    -r				修改文件自动加载
    -h, --host		指定主机
    -p, --port		指定端口
    --threaded		使用多线程
    ```

### 扩展：

1. MVC

   M：Model，模型，即数据模型

   V：View，视图，负责显示内容

   C：Controller，控制器，负责处理业务逻辑

2. MVT

   M：Model，模型，即数据模型

   V：View，视图函数，负责处理业务逻辑

   T：Template，模板，负责数据的表现逻辑(展示)