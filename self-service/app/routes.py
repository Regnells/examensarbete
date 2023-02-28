from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import LoginForm
from ad_tools import ad_tools

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='One Click IT')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    ad = ad_tools()

    if form.validate_on_submit():
        # Hacky workaround. Need to get this into portal in a better way.
        global global_username
        global global_password
        global_username = form.username.data
        global_password = form.password.data

        if ad.authenticate(form.username.data, form.password.data):
            # Create user session
            session['username'] = form.username.data
            return redirect(url_for('portal'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))
      
    return render_template('login.html', title='Login', form=form)

@app.route('/portal', methods=['GET', 'POST'])
def portal():
    # Pretty hacky workaround to checking priviliges. There is probably a way to do this with session.
    ad = ad_tools()

    try:
        ad.authenticate(global_username, global_password)
    except:
        flash('Please log in before accessing portal.')
        return redirect(url_for('login'))

    # Check if a user session has been established, else redirect to login
    if 'username' in session and ad.check_hr():
        return render_template('hrportal.html', title='HR Portal')
    elif 'username' in session and ad.check_it():
        return render_template('adminportal.html', title='Admin Portal')
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    # Remove user session
    session.pop('username', None)
    return redirect(url_for('index'))