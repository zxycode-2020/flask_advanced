from flask import Flask, render_template, render_template_string, g
from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    # 渲染模板文件
    return render_template('index.html')


@app.route('/user/<name>')
def welcome(name):
    # g变量不需要分配就可以在模板文件中使用
    g.name = name
    # 将分类的变量直接写在渲染函数的后面，作为参数即可
    return render_template('user.html', name=name)
    #return render_template_string('<h1>Hello {{ name }} !</h1>', name=name)


@app.route('/usefunc/')
def use_func():
    #return render_template('use_func.html', var='xiaoming')
    return render_template('use_func.html', var='<b>xiaoming</b>')


@app.route('/control/')
def control():
    return render_template('control.html', name='xiaoming')


if __name__ == '__main__':
    manager.run()

