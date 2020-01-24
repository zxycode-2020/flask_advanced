# Flask项目部署

### 回顾WEB原理

客户端 <=> WEB服务器(nginx/apache) <=转发动态请求=> Python <=> 数据库

具体：客户端 <=> WEB服务器(nginx/apache) <=>wsgi服务<=> Python <=> 数据库

###WSGI

简介：Web Server Gateway Interface的缩写

### 自己编写web框架

1. 框架只需实现一个函数即可(文件名为webapp.py)，内容如下：

   ```python
   def application(environ, start_response):
       start_response('200 OK', [('Conten-Type', 'text/html')])
       return '<b>Hello World</b>'
   ```

2. 使用测试版本的wsgi服务启动自己的框架(wsgi_server.py)，内容如下：

   ```
   # 这是一个官方提供的仅用于测试的wsgi程序
   from wsgiref.simple_server import make_server

   # 导入自己写框架
   from webapp import application

   # 创建一个服务
   # 参数：host port 执行的任务
   server = make_server('10.0.142.34', 5000, application)

   # 启动服务
   server.serve_forever()
   ```

3. 启动wsgi服务

   ```shell
   # python wsgi_server.py
   ```

4. 测试

   浏览器中输入：http://10.0.142.34:5000

   说明：只要是该主机和端口，任何url都返回`Hello World`

### uWSGI

说明：是专门的wsgi程序

安装：`pip install uwsgi`

启动：`uwsgi --http 10.0.142.34:5000  --wsgi-file webapp.py`

参数：	

```
http：指定http协议的主机和端口
socket：指定soket监听的主机和端口
wsgi-file：应用所在的模块
chdir：启动程序后的当前目录
callable：指定应用程序的实例
```

###Nginx + uWSGI + Flask	

1. nginx（添加虚拟主机）

   ```nginx
   server {
           listen 80; 
           server_name www.flask.com;

     		# 静态资源路由
     		location /static {
         			root /root/flask/static;
     		}
     
           location / { 
                   include uwsgi_params;   
                   uwsgi_pass 127.0.0.1:5000;
           }   
   }
   ```

   启动Nginx或重新加载配置文件

   重启nginx：service nginx restart

   重新加载配置：service nginx reload

2. uWSGI

   ```ini
   [uwsgi]
   # 指定soket的主机端口
   socket = 127.0.0.1:5000
   # 指定的模块
   wsgi-file = webapp.py
   # 应用实例
   callable = app 
   ```

   启动：uwsgi uwsgi.ini

3. 书写flask项目

   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def index():
           return 'Hello Flask'

   if __name__ == '__main__':
           app.run()
   ```

4. 添加本地的域名解析

   修改文件：C:\Windows\System32\drivers\etc\hosts

   末尾添加内容：10.0.142.34	www.flask.com

5. 测试服务

   在浏览器中输入：http://www.flask.com