# -*- coding: utf-8 -*-
import os
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, EditForm
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User
from werkzeug.urls import url_parse
from flask import Flask
from flask import render_template
from flask import redirect


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/index')
def index():
    if request.form:
        ticket = Ticket(place=request.form.get("place"))
        db.session.add(ticket)
        db.session.commit()
    user = current_user
    user = {'username': 'Name'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Moskow'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Chelyabinsk'
        },
        {
            'author': {'username': 'Blok'},
            'body': 'Petersburg'
        }
    ]

    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route("/update", methods=["POST"])
def update():
    newplace = request.form.get("newplace")
    oldplace = request.form.get("oldplace")
    ticket = Ticket.query.filter_by(place=oldplace).first()
    ticket.place = newplace
    db.session.commit()
    return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
    place = request.form.get("place")
    ticket = Ticket.query.filter_by(place=place).first()
    db.session.delete(ticket)
    db.session.commit()
    return redirect("/")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'City1'},
        {'author': user, 'body': 'City2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
     
    
    
 


    
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from sweater import app, db
from sweater.models import User, hisoriTickets, Tickets


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/history')
@login_required
def history():
    user_id = current_user.get_id()

    try:
        user_data = hisoriTickets.query.filter_by(login_id=user_id).order_by(hisoriTickets.date.desc()).all()
    except:
        user_data = False
    return render_template('history.html', user_data=user_data)

@app.route('/history/<int:id>')
@login_required
def history_del(id):

    data = hisoriTickets.query.get_or_404(id)
    try:

        db.session.delete(data)
        db.session.commit()
    except:
        return "Ошибка при удалении"
    return redirect(url_for('history'))

@app.route('/sign_up', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('hello_world'))
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password) or user and user.password == password:
            login_user(user)
            user_id = current_user.get_id()
            if user_id == '1':
                return redirect('admin')
            next_page = request.args.get('next')
            if next_page is None:
                next_page = url_for('hello_world')
            return redirect(next_page)
        else:
            flash('Логин или пароль неверны')
    else:
        flash('Пожалуйста, заполните поля логин и пароль')
    return render_template('sign-in.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    name = request.form.get('name')
    surname = request.form.get('surname')
    date = request.form.get('date')
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not (login or password or password2):
            flash('Пожалуйста, заполните все поля!')
        elif password != password2:
            flash('Пароли не равны!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(name=name, surname=surname, login=login, password=hash_pwd, date=date)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))
    return render_template('register.html')
# @app.route('/admin')
# def admin():
#     return render_template('admin')

@app.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule():
    schedules = True
    from_city = request.form.get('from_city')
    to_city = request.form.get('to_city')
    print(request.method)
    if request.method == 'POST':


        schedules = Tickets.query.filter_by(from_city=from_city,to_city=to_city).all()
        if schedules:
            return render_template('poisk.html', schedules=schedules)
        else:
            schedules = False

    return render_template('schedule.html', schedules=schedules)

@app.route('/schedule/<int:id>')
@login_required
def schedule_add(id):
    user_id = current_user.get_id()

    data = Tickets.query.get_or_404(id)
    date = data.date
    from_city = data.from_city
    to_city = data.to_city
    price = data.price
    new_hisoriTickets = hisoriTickets(date=date, from_city=from_city, to_city=to_city, price=price, login_id=user_id)
    db.session.add(new_hisoriTickets)
    db.session.commit()
    return redirect(url_for('history'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello_world'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response
