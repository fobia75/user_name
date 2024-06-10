from asyncio.log import logger
from pathlib import Path, PurePath
from flask import Flask, abort, flash, make_response, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from markupsafe import escape


app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/')
def index():
    return render_template('index.html')
    

@app.route('/login', methods= ['POST','GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username','email')
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/greet')
def greet():
    username = request.cookies.get('username')
    if username:
        return render_template('greet.html', name = username)
    return redirect(url_for('index'))


@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/next')
def next_page():
    return f'привет вася'


@app.route('/load_img', methods=['GET','POST'])
def load_img():
    if request.method == 'POST': 
        file = request.files.get('file') 
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f'Файл {escape(file_name)} загружен на сервер' 

    context= {
        'task': 'задание 2'
    }
    return render_template('page_1.html', **context)


@app.route('/authorization', methods=['GET','POST'])
def authorization():
    users_dict = {
        'auth_emeil': '1@mail.ru',
        'auth_pass': '123'
    }
    context= {
        'task': 'задание 3'
    }
    if request.method == 'POST': 
        auth_emeil = request.form.get('auth_emeil')
        auth_pass = request.form.get('auth_pass')  
        if auth_emeil == users_dict['auth_emeil'] and auth_pass == users_dict['auth_pass']:
            return f'вход выполнен успешно' 
        else:
            return f'такого пользователя не существует'
    return render_template('authorization.html', **context)


@app.route('/counter', methods=['GET','POST'])
def counter():
    context= {
        'task': 'задание 4'
    }
    if request.method == 'POST': 
        text = request.form.get('text')
        return f'количество знаков: {len(text.split())}'
    return render_template('counter.html', **context)


@app.route('/calculator', methods=['GET','POST'])
def calculator():
    context= {
        'task': 'задание 5'
    }
    if request.method == 'POST': 
        number_1 = request.form.get('number_1')
        number_2 = request.form.get('number_2')
        operation = request.form.get('operation') 
        match operation:
            case 'add':
                return f'{int(number_1) + int(number_2)}'
            case 'subtract':
                return f'{int(number_1) - int(number_2)}'
            case 'multiply':
                return f'{int(number_1) * int(number_2)}'
            case 'divide':
                if number_2 == '0':
                    return f'нельзя делить на ноль'
                return f'{int(number_1) / int(number_2)}'
    return render_template('calculator.html', **context)


@app.errorhandler(403)
def page_not_found(e):
    logger.warning(e)
    context = {
        'title':'некоректный возраст',
        'url': request.base_url
    }
    return render_template('403.html',**context), 403
    

@app.route('/check_age', methods=['GET','POST'])
def check_age():
    MIN_AGE = 18
    MAX_AGE = 100
    context= {
        'task': 'задание 6'
    }
    if request.method == 'POST': 
        name = request.form.get('name')
        number_age = request.form.get('number_age')
        if MIN_AGE < int(number_age)  < MAX_AGE:
            return f'{name } доступ разрешён'
        abort(403)
    return render_template('check_age.html', **context)


@app.route('/quadro', methods=['GET','POST'])
def quadro():
    NUMBER = 5
    return redirect(url_for('quadro_result', number = int(NUMBER ** 2)))
    


@app.route('/quadro/<int:number>')
def quadro_result(number: int):
    return str(number)


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
# Проверка данных формы
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('form'))
        # Обработка данных формы
        flash('Форма успешно отправлена!', 'success')
        return redirect(url_for('form'))

    return render_template('form.html')


if __name__ == '__main__':
    app.run(debug=True)

