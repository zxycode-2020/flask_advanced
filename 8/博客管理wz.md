# 博客管理

### 用户管理(修改头像)

1. 配置

   ```python
   # 最大上传文件大小
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024
   # 上传文件存储位置
   UPLOADED_PHOTOS_DEST = os.path.join(base_dir, 'static/upload')
   ```

2. 添加flask-uploads扩展

   ```python
   # 导入类库及函数
   from flask_uploads import UploadSet, IMAGES
   from flask_uploads import configure_uploads, patch_request_class
   # 创建对象
   photos = UploadSet('photos', IMAGES)
   # 初始化
   configure_uploads(app, photos)
   patch_request_class(app, size=None)
   ```

3. 修改头像中使用上传文件

   1. 在基础模板中添加点击链接

      ```html
      <li><a href="{{url_for('user.change_icon')}}">修改头像</a></li>
      ```

   2. 添加视图函数

      ```python
      @user.route('/change_icon/')
      @login_required
      def change_icon():
          form = IconForm()
          return render_template('user/change_icon.html', form=form)
      ```

   3. 创建模板文件

      ```html
      {% extends 'common/base.html' %}
      {% block title %}修改头像{% endblock %}
      {% block page_content %}
         {{ wtf.quick_form(form) }}
      {% endblock %}
      ```

   4. 设计上传文件的表单

      ```python
      # 导入上传文件的字段及验证器
      from flask_wtf.file import FileField, FileRequired, FileAllowed
      from app.extensions import photos

      # 修改头像表单
      class IconForm(FlaskForm):
          icon = FileField('头像', validators=[FileRequired('请选择上传文件'), FileAllowed(photos, '只能上传图片')])
          submit = SubmitField('上传')
      ```

   5. 修改user数据模型

      ```python
      class User(UserMixin, db.Model):
        	...
      	# 添加头像字段
      	icon = db.Column(db.String(64), default='default.jpg')
      ```

      > 记得迁移数据库，顺便将默认值也修改了

   6. 修改模型后在信息展示和上传头像中测试

   7. 完整的上传头像并生成缩略图

      ```python
      import os
      from PIL import Image

      @user.route('/change_icon/', methods=['GET', 'POST'])
      @login_required
      def change_icon():
          form = IconForm()
          if form.validate_on_submit():
              # 生成随机的文件名
              suffix = os.path.splitext(form.icon.data.filename)[1]
              name = rand_str() + suffix
              # 保存上传头像
              photos.save(form.icon.data, name=name)
              # 生成缩略图
              pathname = os.path.join(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], name))
              img = Image.open(pathname)
              img.thumbnail((64, 64))
              img.save(pathname)
              # 删除原有头像
              if current_user.icon != 'default.jpg':
                  # 第一次更换头像不删除，除此之外原来的头像都要删除
                  os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], current_user.icon))
              # 更新新的头像名至数据库
              current_user.icon = name
              db.session.add(current_user)
              flash('头像已更换')
          return render_template('user/change_icon.html', form=form)
        
      # 生成随机的字符串
      def rand_str(length=32):
          import random
          base_str = 'abcdefghijklmnopqrstuvwxyz1234567890'
          return ''.join(random.choice(base_str) for i in range(length))
      ```

### 博客管理

1. 设计博客的模型

   ```python
   from app.extensions import db
   from datetime import datetime

   class Posts(db.Model):
       __tablename__ = 'posts'
       id = db.Column(db.Integer, primary_key=True)
       rid = db.Column(db.Integer, index=True, default=0)
       content = db.Column(db.Text)
       timestamp = db.Column(db.DateTime, default=datetime.utcnow)
       # 指定外键(表名.字段)
       uid = db.Column(db.Integer, db.ForeignKey('users.id'))
   ```

   为了关联查询，需要修改User模型，如下：

   ```python
   class User(UserMixin, db.Model):
   	...
   	# 添加关联模型，相当于在关联的模型中动态的添加了一个字段
       # 参数说明：
       # 第一个参数：唯一一个必须的参数，关联的模型类名
       # backref：反向引用的字段名
       # lazy：指定加载关联数据的方式，dynamic:不加载记录，但是提供关联查询
       posts = db.relationship('Posts', backref='user', lazy='dynamic')
   ```

   > 数据模型添加或修改后，即可进行数据库迁移操作

2. 准备发表博客的表单

   ```python
   from flask_wtf import FlaskForm
   from wtforms import TextAreaField, SubmitField
   from wtforms.validators import DataRequired, Length

   class PostsForm(FlaskForm):
       # 如果想要设置字段的其它属性，可以通过render_kw完成
       content = TextAreaField('', render_kw={'placeholder': '这一刻的想法...'}, validators=[DataRequired(), Length(1, 128, message='说话要注意影响，不多不少最好')])
       submit = SubmitField('发表')
   ```

3. 添加视图函数

   ```python
   @main.route('/')
   def index():
       form = PostsForm()
       return render_template('main/index.html', form=form)
   ```

4. 渲染表单

   ```html
   {% extends 'common/base.html' %}
   {% block title %}首页{% endblock %}
   {% block page_content %}
       {{ wtf.quick_form(form) }}
   {% endblock %}
   ```

5. 发表博客

   ```python
   @main.route('/', methods=['GET', 'POST'])
   def index():
       form = PostsForm()
       if form.validate_on_submit():
           # 判断是否登录
           if current_user.is_authenticated:
               u = current_user._get_current_object()
               # 根据表单提交的数据常见对象
               p = Posts(content=form.content.data, user=u)
               # 然后写入数据库
               db.session.add(p)
               return redirect(url_for('main.index'))
           else:
               flash('登录后才能发表博客')
               return redirect(url_for('user.login'))
       return render_template('main/index.html', form=form)
   ```

6. 展示博客

   ```
   @main.route('/', methods=['GET', 'POST'])
   def index():
       form = PostsForm()
       ...
       # 从数据库中读取博客，并分配到模板中，然后在模板中渲染
       # 安装发表时间，降序排列
       # 只获取发表的帖子，过滤回复的帖子
       posts = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).all()
       return render_template('main/index.html', form=form, posts=posts)
   ```

   模板渲染

   ```html
   {# 展示博客内容 #}
   {% for p in posts %}
       <hr style="margin-top: 10px; margin-bottom: 10px;" />
       <div class="media">
           <div class="media-left">
               <a href="#">
                   <img class="media-object" 
                        src="{{url_for('static', 
                             filename='upload/'+p.user.icon)}}" 
                        style="width: 64px; height: 64px;" alt="icon">
               </a>
           </div>
           <div class="media-body">
               <div style="float: right;">{{moment(p.timestamp).fromNow()}}</div>
               <h4 class="media-heading">{{p.user.username}}</h4>
               {{p.content}}
           </div>
       </div>
   {% endfor %}
   <hr />
   ```

7. 分页展示

   插叙数据时使用专门的分页函数：paginate，参数如下：

   ​	page：是唯一的必须参数，表示当前页数

   ​	per_page：每页显示的记录数，默认为20条

   ​	error_out：页码超出范围时是否显示404错误，默认为True

   函数的返回值是一个对象(Pagination)，介绍如下：

   ​	属性：

   ​		items：当前页面的所有记录

   ​		page：当前的页码

   ​		pages：总页数

   ​		total：总记录数

   ​		prev_num：上一页的页码

   ​		next_num：下一页的页码

   ​		has_prev：是否有上一页，有返回True

   ​		has_next：是否有下一页，有返回True

   ​	方法：

   ​		iter_pages：是一个迭代器，每次返回一个在分页导航条上显示的页码

   ​		prev：上一页的分页对象

   ​		next：下一页的分页对象

   8. 封装一个宏，专门负责分页显示

      ```html
      {% macro pagination_show(pagination, endpoint) %}
      <nav aria-label="Page navigation">
          <ul class="pagination">
              {# 上一页 #}
              <li {%if not pagination.has_prev %}class="disabled"{% endif %}>
                  <a href="{% if pagination.has_prev %}{{url_for(endpoint, page=pagination.prev_num, **kwargs)}}{% else %}#{% endif %}" aria-label="Previous">
                      <span aria-hidden="true">&laquo;</span>
                  </a>
              </li>

              {# 分页页码 #}
              {% for p in pagination.iter_pages() %}
                  {% if p %}
                      <li {% if pagination.page == p %}class="active"{% endif %}><a href="{{url_for(endpoint, page=p, **kwargs)}}">{{p}}</a></li>
                  {% else %}
                      <li><a href="#">&hellip;</a></li>
                  {% endif %}
              {% endfor %}

              {# 下一页 #}
              <li {% if not pagination.has_next %}class="disabled"{% endif %}>
                  <a href="{% if pagination.has_next %}{{url_for(endpoint, page=pagination.next_num, **kwargs)}}{% else %}#{% endif %}" aria-label="Next">
                      <span aria-hidden="true">&raquo;</span>
                  </a>
              </li>
          </ul>
      </nav>
      {% endmacro %}
      ```

   9. 在视图函数中获取分页对象

      ```python
      @main.route('/', methods=['GET', 'POST'])
      def index():
          form = PostsForm()
          ...
          # 分页处理
          # 获取当前页码，没有认为是第一页
          page = request.args.get('page', 1, type=int)
          pagination = Posts.query.filter_by(rid=0)
          			.order_by(Posts.timestamp.desc())
            			.paginate(page, per_page=3, error_out=False)
          posts = pagination.items
          return render_template('main/index.html', form=form, 
                                 posts=posts, pagination=pagination)
      ```

   10. 在模板中渲染分页导航条

       ```html
       {# 导入分页展示的宏 #}
       {% from 'common/macro.html' import pagination_show %}

       {# 展示分页导航条 #}
       {{ pagination_show(pagination, 'main.index') }}
       ```

### 练习

1. 在首页的展示效果中添加点击链接，点击用户名跳转到该用户发表的所有博客展示页面，若内容比较多，请选择分页展示
2. 点击指定的博客内容，跳转到该博客的详情展示页面，要求显示所有的回复，如果回复内容比较多，请选择分页展示
3. 其余的自己发挥

