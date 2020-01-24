#Flask表单

###加载静态资源(昨日补充)

1. 构造URL(url_for)

   1. _external=True：可以构造完整(带主机和端口号)的URL，默认为False；站内调转时可以忽略，当需要站外跳转时必须设置为True。

      ```
      构造：url_for('register', _external=True)
      结果：http://127.0.0.1:5000/register/
      ```

   2. 构造带参数的路由时，参数直接写在后面即可，多出来的参数直接会作为GET参数拼接在URL的尾部，如：

      ```
      视图函数：
      @app.route('/user/<name>')
      def welcome(name):
          pass

      构造：url_for('welcome', name='xiaohan', page=2, 
      			_external=True)
      结果：http://127.0.0.1:5000/user/xiaohan?page=2
      ```

2. 加载静态资源

   说明：所有的静态资源必须放在static目录下，可以存放图片、CSS、JS等；为了让目录看起来更清晰，我们将静态资源分类存放，如下：

   ```
   project/				# 项目跟目录
   	templates/			# 所有的模板文件
   	static/				# 所有的静态资源
   		img/			# 图片资源
   		css/			# 层叠样式表
   		js/				# JS文件
   		favicon.ico		#网站图标
   	manage.py
   ```

   说明：框架中之所以规定静态资源统一放在static目录，是因为他已经自动的帮我们提供了static目录下的路由，我们无需再写即可直接使用。

   1. 加载网站的图标

   ```html
   {% block head %}
       {{ super() }}
       <link rel="icon" href="{{url_for('static', 			
                              filename='favicon.ico')}}" 
             					type="image/x-icon">
   {% endblock %}
   ```

   说明：为了简化书写，我们写在base.html中

   2. 加载普通图片

   ```html
   <img src="{{url_for('static', filename='img/meinv.jpg')}}">
   ```

   说明：只要构造出来对应的资源路径即可

   3. 加载层叠样式表

   ```html
   {% block styles %}
       {{ super() }}
       <link rel="stylesheet" type="text/css" href="{{url_for('static', filename='css/common.css')}}" />
   {% endblock %}
   ```

   4. 加载JS脚本文件

   ```html
   {% block scripts %}
       {{ super() }}
       <script type="text/javascript" src="{{url_for('static', filename='js/common.js')}}"></script>
   {% endblock %}
   ```

### 时间戳显示

作用：专门负责时间戳的转换与显示

安装：`pip install flask-moment` 

使用：

1. 在manage.py中添加

   ```python
   # 导入类库
   from flask_moment import Moment
   # 创建对象
   moment = Moment(app)
   # 测试路由
   @app.route('/moment/')
   def show_time():
       current_time = datetime.utcnow() + 
       					timedelta(seconds=-3600)
       return render_template('moment.html', 
                              current_time=current_time)
   ```

2. 创建模板文件moment.html

   ```html
   {% extends 'base.html' %}
   {% block title %}时间戳显示{% endblock %}
   {% block page_content %}
   {# 简化的格式化显示方式 #}
   <p>时间日期(简化)：{{ moment(current_time).format('L') }}</p>
   {# 定制的格式化显示方式 #}
   <p>时间日期(定制)：{{ moment(current_time).format('YYYY-MM-DD') }}</p>
   <p>发表于：{{ moment(current_time).fromNow() }}</p>
   {% endblock %}
   {% block scripts %}
       {{ super() }}
       {# 加载moment需要的js文件 #}
       {{ moment.include_moment() }}
   	{# 本身依赖jQuery，但是bootstrap已经加载 #}
   	{{ moment.include_jquery() }}
       {# 设置中文显示，默认是英文 #}
       {{ moment.locale('zh-CN') }}
   {% endblock %}
   ```

   格式化：http://momentjs.com/docs/#/displaying/

### 表单处理

1. 原生表单

   模板文件index.html

   ```html
   <form method="post" action="{{url_for('check')}}">
       用户名:<input type="text" name="username" />
       <input type="submit" name="submit" value="提交"/>
   </form>
   ```

   视图函数

   ```python
   # 表单展示
   @app.route('/')
   def index():
       return render_template('index.html')
   # 表单校验
   @app.route('/check/', methods=['POST'])
   def check():
       return 'Hello ' + request.form['username']
   ```

   为了简化代码，我们可以将表单的展示与校验写在一个路由中，如下：

   ```python
   @app.route('/', methods=['GET', 'POST'])
   def index():
       if request.method == 'POST':
           return 'Hello ' + request.form['username']
       return render_template('index.html')
   ```

   说明：提交到统一页面校验表单可以不写form的action，通过请求的方法不同做出不同的响应，显示不同的结果。

2. flask-wtf使用

   说明：可以让我们的繁琐重复的表单处理变得愉悦很多，另外还提供CSRF的保护，就是将一个加密的隐藏字段添加到表单中。

   安装：`pip install flask-wtf`

   使用：

   1. 配置

      ```python
      # 秘钥，表单会用到，若不想公开写出来，可以配置环境变量
      app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '很难猜到的字符串'
      ```

   2. 定义表单类

      ```python
      # 表单基本类库
      from flask_wtf import FlaskForm
      # 所需字段类型
      from wtforms import StringField, SubmitField
      # 验证器
      from wtforms.validators import DataRequired
      # 表单使用，定义一个表单类
      class NameForm(FlaskForm):
          name = StringField('用户名', 
                             validators=[DataRequired()])
          submit = SubmitField('提交')
      ```

   3. 使用表单

      ```python
      @app.route('/form/')
      def test_form():
        	# 创建表单对象
          form = NameForm()
          return render_template('test_form.html', form=form)
      ```

   4. 表单渲染

      原生渲染

      ```html
      <form method="post">
          {{ form.hidden_tag() }}
          {{ form.name.label }}{{ form.name(id="xxx", class="yyy") }}
          {{ form.submit() }}
      </form>
      ```

      bootstrap渲染

      ```html
      {# 导入渲染需要的文件 #}
      {% import 'bootstrap/wtf.html' as wtf %}
      {# 在需要的位置渲染表单 #}
      {{ wtf.quick_form(form) }}
      ```

      说明：默认是POST请求，提交到当前页面

3. 表单的校验(重定向/用户会话)

   ```python
   @app.route('/form/', methods=['GET', 'POST'])
   def test_form():
       form = NameForm()
       # 表单校验
       if form.validate_on_submit():
           session['name'] = form.name.data
           return redirect(url_for('test_form'))
       name = session.get('name')
       return render_template('test_form.html', form=form, 
                              name=name)
   ```

   说明：浏览器会记录最后的请求，刷新时会使用最后的请求，若是POST多数情况是不必须的，因此我们将其重定向到GET。表单中存储的数据在重定向后会丢失，记录会话信息可以存放在session中。

4. 常用表单字段

   | 字段类型          | 说明                       |
   | ------------- | ------------------------ |
   | StringField   | 普通文本字段                   |
   | SubmitField   | 提交按钮                     |
   | PasswordField | 密文文本字段                   |
   | HiddenField   | 隐藏字段                     |
   | TextAreaField | 文本域字段                    |
   | IntegerField  | 整数字段                     |
   | FloatField    | 浮点数字段                    |
   | BooleanField  | 复选框                      |
   | DateField     | 日期字段，datetime.date       |
   | DateTimeField | 日期时间字段，datetime.datetime |

   常用验证器类：

   | 验证器          | 说明                    |
   | ------------ | --------------------- |
   | DataRequired | 确保字段有数据               |
   | Required     | DataRequired的别名       |
   | Email        | 邮箱格式                  |
   | EqualTo      | 校验字段一致性，通过用于两次密码一致的校验 |
   | Length       | 长度限定                  |
   | NumberRange  | 限定数字范围                |
   | IPAdress     | 默认IPv4的地址             |
   |              | 正则验证                  |
   |              | 有效的URL                |

   说明：类名都有对象的小写加下划线的形式(见到了不要纠结)

### 练习：

1. 定义一个网站用的相关表单，如：注册、登录等

2. 熟练掌握表单的使用(定义、渲染、校验)

   ​

###扩展：环境变量的配置

windows：

​	设置：set SECRET_KEY=123456

​	获取：set SECRET_KEY

unix：

​	设置：export SECRET_KEY=123456

​	获取：echo $SECRET_KEY

代码获取：

​	import os

​	os.environ.get('SECRET_KEY')