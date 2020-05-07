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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



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
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/ticket/<date>/<place>')
def show_ticket(place, date):
    ticket = Ticket.query.filter_by(place=place, date=date).first_or_404()
    return render_template('show_ticket.html', ticket=ticket)
