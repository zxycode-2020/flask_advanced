from flask import Flask, render_template, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timedelta


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    #return url_for('register', _external=True)
    #return url_for('welcome', name='xiaohan', page=2, _external=True)
    #return render_template('base.html')
    return render_template('index.html')


@app.route('/moment/')
def show_time():
    current_time = datetime.utcnow() + timedelta(seconds=-3600)
    return render_template('moment.html', current_time=current_time)


@app.route('/register/')
def register():
    return '欢迎注册'


@app.route('/user/<name>')
def welcome(name):
    pass

if __name__ == '__main__':
    manager.run()