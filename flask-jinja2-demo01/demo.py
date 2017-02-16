from flask import Flask, render_template, request, redirect, url_for
from werkzeug.routing import BaseConverter
from werkzeug.utils import secure_filename
import os


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter


@app.route('/')
def hello_world():
    return render_template('index.html', title='demo01')


@app.route('/services')
def services():
    return 'Service'


@app.route('/about')
@app.route('/aboutme')
def about():
    return 'About'


# @app.route('/user/<username>')
# def user(username):
#     return 'User %s' % username;

# 路由转换器
# int  float  path

# @app.route('/user/<int:user_id>')
# def user(user_id):
#     return 'User %d' % user_id;

@app.route('/user/<regex("[a-z]{3}"):user_id>')
def user(user_id):
    return 'User %s' % user_id;


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    elif request.method == 'GET':
        username = request.args['username']
    return render_template('login.html', method=request.method)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(basepath, 'static/uploads')
        f.save(upload_path, secure_filename(f.filename))
        return redirect(url_for('upload'))
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
