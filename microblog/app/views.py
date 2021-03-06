from forms import LoginForm, EditForm
from flask import render_template
from app import app, db

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(current_user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit.html',
        form = form)

if user is None:
        username = resp.username
        if username is None or username == "":
            username = resp.email.split('@')[0]
        username = User.make_unique_username(username)
        user = User(username = username, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
