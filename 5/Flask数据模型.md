# Flask数据模型

### 回顾

1. 分类

   关系型数据库：MySQL、Oracle、sqlite、...

   非关系型数据库：MongoDB、Redis、...

2. 选择

   数据库没有好坏，只有是否合适

### flask-sqlalchemy

说明：提供了大多数关系型数据库的支持，提供了ORM

安装：`pip install flask-sqlalchemy`

使用：

1. 配置

   ```
   链接地址：SQLALCHEMY_DATABASE_URI
   MySQL:	mysql://username:password@hostname/database
   sqlite：
   	windows:	sqlite:///c:/abc/def/database
   	unix:		sqlite:////root/sqlite/database
   ```

2. 代码配置

   ```python
   # 配置数据库连接地址
   base_dir = os.path.abspath(os.path.dirname(__name__))
   database_uri = 'sqlite:///' + os.path.join(base_dir, 'data.sqlite') 
   app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
   # 禁止对象的修改追踪
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   # 配置自动提交(在请求结束时自动执行提交操作)，
   # 否则每次数据库操作后都需要手动提交db.session.commit()
   app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
   ```

3. 创建对象

   ```python
   # 导入类库
   from flask_sqlalchemy import SQLAlchemy
   # 创建对象
   db = SQLAlchemy(app)
   ```

4. 定义模型类

   ```python
   # 定义模型，必须继承自db.Model
   class User(db.Model):
       # 可以指定表名，若不指定会默认将模型类名的'小写+下划线'
       # 如：模型名为UserModel，则默认表名为user_model
       __tablename__ = 'users'
       id = db.Column(db.Integer, primary_key=True)
       username = db.Column(db.String(30), unique=True)
       email = db.Column(db.String(64), unique=True)
   ```

5. 数据表的创建删除

   ```python
   # 创建数据库表，测试时需要注意以下方面
   # 连接sqlite：数据库不用创建，不存在会自动创建
   # 连接MySQL：数据库需要提前创建好，否则连接失败
   @app.route('/create/')
   def create():
     	# 表如果已经存在，则不会覆盖创建
       # 表更新时可以粗暴的先删除在创建
       db.drop_all()
       db.create_all()
       return '数据表创建成功'
   # 删除数据表
   @app.route('/drop/')
   def drop():
       db.drop_all()
       return '数据表删除成功'
   ```

6. 添加终端控制命令

   ```python
   from flask_script import Manager, prompt_bool

   # 添加终端创建数据表命令
   @manager.command
   def createall():
       db.create_all()
       return '数据表已创建'
   # 添加终端删除数据表命令
   @manager.command
   def dropall():
       # 终端下给与简单的确认提示
       if prompt_bool('确定要删除所有数据表吗?'):
           db.drop_all()
           return '数据表已删除'
       else:
           return '最好再考虑一下'
   ```

   使用：

   ```shell
   python manage.py dropall		# 删除所有表
   python manage.py createall		# 创建所有表
   ```


7. 数据库CURD

   1. 增加数据

   ```python
   # 创建一个模型对象
   yanxu = User(username='yanxu', email='yanxu@163.com')
   # 增加一条数据
   db.session.add(yanxu)
   # 创建多个对象
   bing = User(username='bing', email='bing@163.com')
   mei = User(username='mei', email='mei@163.com')
   yu = User(username='yu', email='yu@163.com')
   xiang = User(username='xiang', email='xiang@163.com')
   xuer = User(username='xuer', email='xuer@163.com')
   # 增加多条数据
   db.session.add_all([bing, mei, yu, xiang, xuer])
   # 提交操作，所有的数据库操作都必须提交后才有效，除非配置了自动提交
   db.session.commit()
   ```

   2. 查询数据

   ```python
   # 查询数据
   @app.route('/select/<int:uid>')
   def select(uid):
       # 根据id查询数据
       user = User.query.get(uid)
       if user:
           return user.username
       else:
           return '不存在此ID'
   ```

   3. 修改数据

   ```python
   # 修改数据
   @app.route('/update/<int:uid>')
   def update(uid):
       user = User.query.get(uid)
       if user:
           user.email = 'xxx@163.com'
           # 没有单独的更新数据的函数
           db.session.add(user)
           return '数据修改成功'
       else:
           return '不存在此ID'
   ```

   4. 删除数据

   ```python
   # 删除数据(通过情况下不做物理删除)
   # 通过只做逻辑删除(只做个删除的标记即可)
   @app.route('/delete/<int:uid>')
   def delete(uid):
       user = User.query.get(uid)
       if user:
           db.session.delete(user)
           return '数据删除成功'
       else:
           return '不存在此ID'
   ```

   5. 条件查询

   ```python
   # 条件查询
   @app.route('/selectby/')
   def select_by():
       # 根据ID查询
       #user = User.query.get(1)
       #return user.username

       # 查询所有数据
       #users = User.query.all()
       #return str(users)

       # 查询第一条数据
       #user = User.query.first()
       #return user.username

       # 指定等值条件，可以写多个条件
       #user = User.query.filter_by(id=3).first()
       #user = User.query.filter_by(email='mei@163.com').first()
       #return user.username

       # 指定特定条件
       #user = User.query.filter(User.id > 3).first()
       #return user.username

       # 找到就返回，没有就报404错误
       #user = User.query.get_or_404(8)
       #user = User.query.filter(User.id > 8).first_or_404()
       #return user.username

       # 统计总数
       count = User.query.filter(User.id > 3).count()
       return 'id > 3的数据共有%d条' % count
   ```

   练习：自行测试右边函数`limit、offset、order_by、group_by`

8. 常见字段类型

   | 类型名          | Python类型           | 说明                |
   | ------------ | ------------------ | ----------------- |
   | Integer      | int                | 32位               |
   | SmallInteger | int                | 16位               |
   | BigInteger   | int/long           | 不限制精度的整型          |
   | Float        | float              | 浮点数               |
   | String       | str                | 变长字符串             |
   | Text         | str                | 变长字符串，做了大量数据存储的优化 |
   | Boolean      | bool               | 布尔值               |
   | Date         | datetime.date      | 日期                |
   | Time         | datetime.time      | 时间                |
   | DateTime     | datetime.datetime  | 日期时间              |
   | Interval     | datetime.timedelta | 时间间隔              |

9. 字段可选项

   | 选项名         | 说明                  |
   | ----------- | ------------------- |
   | primary_key | 是否设为主键索引            |
   | unique      | 是否设为唯一索引            |
   | index       | 是否设为普通索引            |
   | nullable    | 是否可以为空，True(默认)可以为空 |
   |             | 设置默认值               |

### 数据库迁移

说明：当我们设计的Model类改变时，需要将改变应用到数据库，否则就会出现数据表与模型不对应的情况。这时就需要进行及时的数据库迁移操作。前面的简单粗暴的解决方案时删除原来的所有表，然后再创建，但是会有一个副作用(就是原来的所有数据将全部丢失)，因此，高效安全的数据库迁移操作是很有必要的，自己不会迁移最好使用别人写好的迁移工具。

flask框架中推荐使用flask-migrate

安装：`pip install flask-migrate`

使用：

```python
# 导入数据库迁移类库
from flask_migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
# 添加终端命令
manager.add_command('db', MigrateCommand)
```

操作：

```
# 创建数据库迁移使用的目录及初始化脚本(只需执行一次)
python manage.py db init
# 生成自动化迁移用到的脚本程序
python manage.py db migrate
# 执行数据库迁移脚本
python manage.py db upgrade
```

说明：数据库迁移不一定每次都成功，所以每次执行后都需要确认是否有问题，若有问题需要手动解决。

练习：试着写一下用户的注册登录功能

### 蓝本(Blueprint)

说明：将所有的视图函数放在一起，会使代码变得因庞大而混乱，我们可以根据自己的需要将不同功能的路由放在不同的文件中。flask的解决方案时使用蓝本，示例代码如下：

```python
# 导入蓝本类库
from flask import Blueprint
# 创建蓝本对象
user = Blueprint('user', __name__)
# 定制路由
@user.route('/login/')
def login():
    return '欢迎登录'
```

创建的蓝本无法使用，定义的路由默认处于休眠状态，需要注册才可使用

```python
# 蓝本创建后不能使用，需要注册才可以
from user import user
# 注册蓝本，可以顺便指定蓝本中的路由前缀
app.register_blueprint(user, url_prefix='/user')
```

### 扩充

在调试代码，如果不想写代码，可以通过终端进行调试，方法如下：`python manage.py shell`，但是遗憾的是启动的shell没有导入任何数据，需要的数据都需要自己手动导入，可以自己定制shell命令，方法如下：

```python
from flask_script import Shell
# 定制shell
def shell_make_context():
    # 返回的数据作为shell启动时的上下文
    return dict(db=db, User=User)
manager.add_command('shell', 
					Shell(make_context=shell_make_context))
```

