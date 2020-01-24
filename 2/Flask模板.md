#Flask模板

### 模板简介

若想开发出结构清晰易于维护的代码，目前我们所写的代码都比较简单，但是很明显的可以预见的一个问题是，当项目越来越复杂时，视图函数将变得异常庞大和繁琐，因为视图函数中存放了业务逻辑和表现逻辑。

解决此类问题的通用方式是将不同种类的逻辑分开存放

业务逻辑：存放视图函数中，专门处理用户的业务需求

表现逻辑：存放在单独的(模板)文件中，负责展示效果

### 模板引擎

规定了一套特定的语法，提供了一种为表现逻辑的灵活实现的特殊替换，然后提供一种专门的替换借口负责将模板文件转换成目标文件(html)

说明：flask中提供了专门的模板引擎(Jinja2)

###Jinja2

1. 准备工作，创建项目

   ```
   project/			# 项目根目录
   	templates/		# 存放模板文件
   	manage.py		# 启动控制文件
   ```

2. 渲染模板

   1. 创建模板文件templates/index.html

   2. 使用渲染函数render_template渲染指定的模板文件

      ```python
      @app.route('/')
      def index():
          # 渲染模板文件
          return render_template('index.html')
      ```

   3. 若渲染字符串可以使用render_template_string函数

3. 使用变量

   1. 在templates目录下创建模板文件user.html，内容如下：

      ```html
      {# 这里是注释，解释变量要使用两个大括号 #}
      <h1>Hello {{ name }} !</h1>
      <h2>Hello {{ g.name }}</h2>
      ```

   2. 在manage.py中添加视图函数，内容如下：

      ```python
      @app.route('/user/<name>')
      def welcome(name):
        	# g变量不需要分配就可以在模板文件中使用
          g.name = name
        	# 将分类的变量直接写在渲染函数的后面，作为参数即可
          return render_template('user.html', name=name)
        	# 渲染模板字符串，使用函数render_template_string
          return render_template_string(
            	'<h1>Hello {{ name }} !</h1>', name=name)
      ```

4. 使用函数

   1. 在要解析的变量的后面添加一个'|'

   2. 在'|'的后面添加一个需要处理的函数，代码如下

      ```html
      <h1>Hello {{ name|capitalize }} !</h1>
      ```

   3. 常用的函数

      | 函数         | 说明          |
      | ---------- | ----------- |
      | capitalize | 首字母大写       |
      | upper      | 全部大写        |
      | lower      | 全部小写        |
      | title      | 每个单词首字母大写   |
      | trim       | 去掉两边的空白     |
      | striptags  | 去掉所有的HTML标签 |
      | safe       | 渲染时不转义，默认转义 |

      说明：不要在不信任的变量上使用safe（如：用户表单数据）

5. 控制结构

   1. if-else，代码如下：

      ```html
      {% if name %}
          <h1>Hello {{ name }}</h1>
      {% else %}
          <h1>请登录</h1>
      {% endif %}
      ```

      说明：会根据是否分配name变量显示不同的内容

   2. for，代码如下：

      ```html
      <ol>
          {% for x in range(1, 5) %}
              <li>{{ x }}</li>
          {% endfor %}
      </ol>
      ```

6. 宏的使用

   说明：模板中可以采用类似于python中的函数方式定义宏，使用的地方调用即可，这样就可以减少大量的代码的重复书写，提高开发效率。

   实例：

   ```html
   {# 定义宏 #}
   {% macro show(name) %}
       <h1>This is {{name}}</h1>
   {% endmacro %}

   {# 调用宏 #}
   {{ show(name) }}

   {# 从另一个文件导入宏 #}
   {% from 'macro2.html' import welcome %}

   {{ welcome(name) }}
   ```

   > 可以将宏放在一个单独的文件中，专门负责处理特定的显示效果，然后哪里需要就在哪里导入，然后调用一次即可。

7. 文件包含

   文件包含相当于直接将被包含的文件的内容粘贴到包含处，用法如下：

   ```html
   {# 直接包含另一个模板文件，相当于将内容粘贴过来 #}
   {% include 'macro.html' %}
   ```

8. 模板继承

   基础模板parents.html

   ```html
   <html>
   <head>
       {% block head %}
       <title>{% block title %}默认标题{% endblock %}</title>
       {% endblock %}
   </head>
   <body>
       {% block body %}
       默认内容
       {% endblock %}
   </body>
   </html>
   ```

   子模板children.html

   ```html
   {# 继承自另一个模板 #}
   {% extends 'parents.html' %}
   {# 重写指定的块 #}
   {% block title %}首页{% endblock %}
   {% block head %}
       {# 保留父级模板中的内容 #}
       {{ super() }}
       <h1>添加的内容</h1>
   {% endblock %}
   {# 删除基础模板中的指定的块 #}
   {% block body %}{% endblock %}
   ```

   > 在子模板中可以删除、修改、覆盖基础模板中的block

### 使用bootstrap

安装：`pip install flask-bootstrap`

使用：在manage.py中

```python
# 导入类库
from flask_bootstrap import Bootstrap
# 创建对象
bootstrap = Bootstrap(app)
# 测试bootstrap
@app.route('/bootstrap/')
def bootstrap():
    return render_template('bootstrap.html', name='xiaomeng')
```

模板文件bootstrap.html

```html
{# 继承自bootstrap的基础模板 #}
{% extends 'bootstrap/base.html' %}

{% block title %}bootstrap测试{% endblock %}

{% block content %}
<div class="container">
    <h1>Hello {{ name }}</h1>
</div>
{% endblock %}
```

bootstrap的基础模板中定义了很多block，可以在衍生模板中直接使用：

| 块名      | 说明          |
| ------- | ----------- |
| doc     | 整个文档内容      |
| html    | html标签中的内容  |
| head    | head标签中的内容  |
| title   | title标签中的内容 |
| body    | body标签中的内容  |
| metas   | 一组meta标签    |
| styles  | 层叠样式表       |
| scripts | 加载JS代码      |
| content | 用户定义的页面内容   |
| navbar  | 用户定义的导航条    |

说明：上述的block在子模板中都可直接使用，但是可能会出现覆盖问题，当出现问题时，很多时候都是因为没有调用super()

### 定义基础模板

代码如下：

```html
{# 继承自bootstrap的基础模板 #}
{% extends 'bootstrap/base.html' %}

{% block title %}博客{% endblock %}

{% block navbar %}
<nav class="navbar navbar-inverse" style="border-radius: 0px;">
    <div class="container">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
            <button type="button" 
                    class="navbar-toggle collapsed" 
                    data-toggle="collapse"
                    data-target=".navbar-collapse" 
                    aria-expanded="false">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="#">首页</a>
        </div>
        <div class="collapse navbar-collapse">
            <ul class="nav navbar-nav">
                <li><a href="#">板块一</a></li>
                <li><a href="#">板块二</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <li><a href="#">登录</a></li>
                <li><a href="#">注册</a></li>
            </ul>
        </div><!-- /.navbar-collapse -->
    </div><!-- /.container -->
</nav>
{% endblock %}

{% block content %}
<div class="container">
    {% block page_content %}默认内容{% endblock %}
</div>
{% endblock %}
```

### 自定义错误页面

1. 添加视图函数

   ```python
   @app.errorhandler(404)
   def page_not_found(e):
       return render_template('404.html')
   ```

2. 创建模板文件404.html

   ```html
   {# 继承自项目的基础模板 #}
   {% extends 'base.html' %}
   {% block title %}出错了{% endblock %}
   {% block page_content %}大哥，你是不是搞错了@_@{% endblock %}
   ```

3. 自定义500错误显示