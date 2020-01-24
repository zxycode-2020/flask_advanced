# Flask表单

### 自定义验证函数

```python
from wtforms import ValidationError

class NameForm(FlaskForm):
  	name = StringField('用户名', validators=[DataRequired(), 
                  Length(2, 8, message='此处需要2~8个字符！')])
  	submit = SubmitField('提交')

	# 自定义验证器函数
	# 以validate_开头的函数会自动校验'_'后面的对应名字的字段
	def validate_name(self, field):
    	if len(field.data) < 6:
        	raise ValidationError('不能少于6个字符')
```
### CDN访问受限

1. 加载本地文件

   ```python
   # 使用本地扩展库中的文件，不是项目根目录下的static
   app.config['BOOTSTRAP_SERVE_LOCAL'] = True
   ```

2. 更换CND服务器

   将flask-bootstrap扩展库中的__ init __.py的末尾的内容

   ```python
   bootstrap = lwrap(
       WebCDN('//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/%s/' % BOOTSTRAP_VERSION), local)
   jquery = lwrap(
       WebCDN('//cdnjs.cloudflare.com/ajax/libs/jquery/%s/'
       % JQUERY_VERSION), local)
   html5shiv = lwrap(
       WebCDN('//cdnjs.cloudflare.com/ajax/libs/html5shiv/%s/' % HTML5SHIV_VERSION))
   respondjs = lwrap(
       WebCDN('//cdnjs.cloudflare.com/ajax/libs/respond.js/%s/' % RESPONDJS_VERSION))
   ```

   改为(bootcss的cdn)

   ```python
   bootstrap = lwrap(
           WebCDN('//cdn.bootcss.com/bootstrap/%s/' %
                  BOOTSTRAP_VERSION), local)
   jquery = lwrap(
           WebCDN('//cdn.bootcss.com/jquery/%s/' %
                  JQUERY_VERSION), local)
   html5shiv = lwrap(
           WebCDN('//cdn.bootcss.com/html5shiv/%s/' %
                  HTML5SHIV_VERSION))
   respondjs = lwrap(
           WebCDN('//cdn.bootcss.com/respond.js/%s/' 
           % RESPONDJS_VERSION))
   ```

### Flask消息

说明：当用户状态发生改变时，可以通过弹窗给与提示、警告等信息

```python
from flask import Flask, flash
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # 获取原来的名字
        last_name = session.get('name')
        if last_name is not None \
        	and last_name != form.name.data:
            flash('大哥，您的名字又换了')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    name = session.get('name')
    return render_template('index.html', form=form, name=name)
```

渲染(写在基础模板中)

```html
{# get_flashed_messages获取所有的flash消息 #}
{% for message in get_flashed_messages() %}
    <div class="alert alert-warning alert-dismissible" 
         role="alert">
        <button type="button" class="close" 
                data-dismiss="alert" aria-label="Close"><span
                aria-hidden="true">&times;</span></button>
        {{ message }}
    </div>
{% endfor %}
```
### 文件上传

1. 在模板文件中准备一个表单，内容如下：

   ```html
   {# 必须是post方法，enctype也必须指定 #}
   <form method="post" enctype="multipart/form-data">
   	<input type="file" name="photo" />
   	<input type="submit" value="上传" />
   </form>
   {% if img_url %}
   	<img src="{{img_url}}" />
   {% endif %}
   ```

2. 添加视图函数，内容如下：

   ```python
   @app.route('/', methods=['GET', 'POST'])
   def index():
       img_url = None
       if request.method == 'POST':
         	# 获取上传文件信息
           file = request.files.get('photo')
           # 上传信息得有，并且是允许的文件后缀
           if file and allowed_file(file.filename):
               # 获取文件后缀
               suffix = os.path.splitext(file.filename)[1]
               # 生成随机的文件名，然后拼接后缀
               filename = rand_str() + suffix
               file.save(os.path.join(
                     app.config['UPLOAD_FOLDER'], filename))
               img_url = url_for('show',imagename=filename)
       return render_template('index.html', img_url=img_url)
   ```

3. 相关配置及功能函数

   ```python
   # 设置允许上传的文件后缀
   ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg', 'gif'])
   # 配置上传文件的最大尺寸，默认不限制大小
   app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16
   # 配置上传文件的保存目录
   app.config['UPLOAD_FOLDER'] = os.getcwd()
   # 判断是否是允许的文件后缀
   def allowed_file(filename):
       return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
   # 生成随机的字符串
   def rand_str(length=32):
       import random
       base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
       return ''.join(random.choice(base_str) for i in 	
                      range(length))

   # 显示上传文件
   @app.route('/show/<imagename>')
   def show(imagename):
       # 发送指定的文件
       return send_from_directory(app.config['UPLOAD_FOLDER'], 
                                  imagename)
   ```

### flask-uploads

说明：该扩展库简化了文件上传的大量操作

安装：`pip install flask-uploads`

使用：

1. 模板文件保持不变

2. 相关配置

   ```python
   # 导入上传相关类库及函数
   from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class

   # 配置上传文件的最大尺寸，默认不限制大小
   app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 16
   # 配置上传文件的保存目录，还可以是FILES/DEFAULT
   app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd()

   # 文件类型过滤
   photos = UploadSet('photos', IMAGES)
   # 上传配置
   configure_uploads(app, photos)
   # 配置上传文件大小，默认64M，设置为None，会读取配置中的MAX_CONTENT_LENGTH选项
   patch_request_class(app, size=None)
   ```

3. 视图函数

   ```python
   @app.route('/', methods=['GET', 'POST'])
   def index():
       img_url = None
       if request.method == 'POST' \
       	and 'photo' in request.files:
           # 获取文件后缀
           suffix = os.path.splitext(
             request.files['photo'].filename)[1]
           # 生成随机的文件名，然后拼接后缀
           name = rand_str() + suffix
           # 保存文件
           filename = photos.save(request.files['photo'],
                                  name=name)
           # 获取文件的url
           img_url = photos.url(filename)
       return render_template('index.html', img_url=img_url)
   ```

### 结合flask-wtf

1. 相关配置

   ```python
   # 图片处理库，默认只支持python2.x，python3.x使用需要安装Pillow
   from PIL import Image

   from flask_wtf import FlaskForm
   from flask_wtf.file import FileField, FileRequired, FileAllowed
   from wtforms import SubmitField

   # 创建表单类库
   class UploadForm(FlaskForm):
       photo = FileField(validators=[
         FileAllowed(photos, '只能上传图片'), 
         FileRequired('请选择文件后再上传')])
       submit = SubmitField('上传')
       
   # 视图函数
   @app.route('/', methods=['GET', 'POST'])
   def index():
       img_url = None
       form = UploadForm()
       if form.validate_on_submit():
           # 保存文件
           filename = photos.save(form.photo.data)
           # 生成缩略图
           img = Image.open(filename)
           img.thumbnail((64, 64))
           img.save(filename)
           # 获取文件的url
           img_url = photos.url(filename)
       return render_template('index.html', 
                              form=form, img_url=img_url)
   ```

2. 模板渲染

   ```html
   <form method="post" enctype="multipart/form-data">
       {{ form.hidden_tag() }}
       {{ form.photo() }}
     	{# 错误显示 #}
       {% for error in form.photo.errors %}
           <span style="color: red;">{{ error }}</span>
       {% endfor %}
       {{ form.submit() }}
   </form>
   {% if img_url %}
       <img src="{{img_url}}" />
   {% endif %}
   ```

练习：结合flask-uploads、flask-wtf、flask-bootstrap、flash、缩略图，完成文件的上传

### 邮件发送

说明：邮件发送功能是一个网站的基本功能，经常用于账户激活，密码找回

安装：`pip install flask-mail`

使用：

1. 同步发送邮件

```python
# 导入邮件发送相关的库
from flask_mail import Mail, Message

# 邮件发送配置，所有的邮件相关配置都必须放在创建对象之前，否则设置不生效
# 邮件服务器
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') or 'smtp.1000phone.com'
# 邮件用户名
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME') or 'lijie@1000phone.com'
# 邮件密码
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') or '1234567890'

# 创建对象
mail = Mail(app)

@app.route('/')
def index():
    # 构建邮件消息对象
    msg = Message(subject='主题',
    	sender=app.config['MAIL_USERNAME'], 
    	recipients=['1256003884@qq.com'])
    # 设置内容(终端接受)
    msg.body = 'Hello 朋亮'
    # 设置内容(浏览器查看)
    msg.html = '<h1>Hello 朋亮</h1>'
    # 发送邮件
    mail.send(msg)
    return '邮件发送成功'
```

2. 异步发送邮件

```python
# 导入线程类库
from threading import Thread
# 异步发送邮件任务
def async_send_mail(app, msg):
    # 发送邮件需要程序的上下文，否则发送不了邮件
    # 在新的线程中没有上下文，需要手动创建
    with app.app_context():
        mail.send(msg)
# 发送邮件函数
def send_mail(to, subject, template, **kwargs):
    # 从current_app代理对象中获取程序的原始实例
    app = current_app._get_current_object()
    msg = Message(subject=subject, 
                  sender=app.config['MAIL_USERNAME'], 
                  recipients=[to])
    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)
    # 创建线程
    thr = Thread(target=async_send_mail, args=[app, msg])
    thr.start()
    return thr
 
@app.route('/')
def index():
    # 调用封装好的邮件发送函数
    send_mail('1256003884@qq.com', '账户激活', 
              'account', name='pengliang')
    # 这里就不会再出现等待的情况
    return '邮件发送成功'
```