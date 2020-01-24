#Flask项目目录

### 大型项目目录结构

```
project/				# 项目根目录
	app/				# 存放整个的应用程序
		static/				# 静态资源
			js/					# JS脚本
			css/				# 层叠样式表
			img/				# 图片资源
			favicon.ico			# 网站图标
		templates/			# 模板文件
			common/				# 通用模板文件
			main/				# 主蓝本模板文件
			errors/				# 错误模板文件
			email/				# 邮件模板文件
			user/				# 用户蓝本模板文件
			posts/				# 博客篮板模板文件
		forms/				# 存放所有表单
		models/				# 存放所有模型
		views/				# 存放视图函数
		email.py			# 邮件发送
		extensions.py		# 所有的扩展
		config.py			# 配置文件
	migrations/			# 数据库迁移脚本目录
	venv/				# 虚拟环境目录
	tests/				# 测试单元
	requirements.txt	# 所有的依赖包
	manage.py			# 项目启动控制文件
```

###代码书写步骤

1. 书写配置即使用配置文件

   config.py、__ init __.py、manage.py

2. 配置相关扩展

   extensions.py、__ init __.py

3. 配置相关蓝本

   views目录、__ init __.py

4. 定制项目基础模板

   common/base.html

5. 自定义错误页面

   templates/errors/404.html、__ init __.py

6. 异步发送邮件

   email.py、templates/email/

7. 用户注册登录相关知识点

   密码要加密存储与校验：

   ```python
   from werkzeug.security importgenerate_password_hash，check_password_hash

   @main.route('/jiami/')
   def jiami():
       return generate_password_hash('123456')


   @main.route('/check/<password>')
   def check(password):
       # 密码校验函数：加密后的值  密码
       # 正确：True，错误：False
       if check_password_hash('pbkdf2:sha256:50000$8tHnM54f$c1518c6e491e0a7c5ebd90beb8b56c1d3b03cef66ad940c566578e6a5cfd62ea', password):
           return '密码正确'
       else:
           return '密码错误'
   ```

   用户账户激活(token)

   ```python
   from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

   @main.route('/generate_token/')
   def generate_token():
       s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
       # 加密指定的数据，已字典的形式传入
       return s.dumps({'id': 250})


   @main.route('/activate/<token>')
   def activate(token):
       s = Serializer(current_app.config['SECRET_KEY'])
       try:
           data = s.loads(token)
       except:
           return 'token有误'
       return str(data.get('id'))
   ```

   ​	

   ​	

### 扩展

如何快速复制一个虚拟环境：

1. 将当前环境依赖冷冻起来

   pip freeze > requirements.txt

2. 创建虚拟环境

   virtualenv venv

3. 安装冷冻的依赖包

   pip install -r requirements.txt