from app import app
from flask import render_template, flash, redirect, session
from app.forms import LoginForm
from ad_tools import ad_tools

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Barebones Flask App')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        ad = ad_tools()
        if ad.authenticate(form.username.data, form.password.data):

            # Create user session
            session['username'] = form.username.data
            return redirect('/portal')
        else:
            return redirect('/login')
        
    return render_template('login.html', title='Login', form=form)

@app.route('/portal')
def portal():
    if 'username' in session:
        return render_template('portal.html', title='Portal')
    else:
        return redirect('/login')