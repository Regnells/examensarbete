from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import LoginForm, CreateUserForm, SearchUserForm
from ad_tools import ad_tools

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='One Click IT')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    global ad
    ad = ad_tools()

    if form.validate_on_submit():
        # Hacky globals to the rescue once again. Im' sure there is a way to use session for this.
        global global_username
        global global_password
        global_username = form.username.data
        global_password = form.password.data

        global auth
        auth = ad.authenticate(form.username.data, form.password.data)
        
        global is_it
        global is_hr
        is_it = ad.check_it()
        is_hr = ad.check_hr()

        if auth and is_hr:
            # Create user session
            session.permanent = False
            session['username'] = form.username.data
            return redirect(url_for('hrportal'))
        elif auth and is_it:
            # Create user session
            session.permanent = False
            session['username'] = form.username.data
            return redirect(url_for('adminportal'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

      
    return render_template('login.html', title='Login', form=form)

@app.route('/portal')
def portal():
    if 'username' in session:
        try:
            if is_hr:
                return redirect(url_for('hrportal'))
            elif is_it:
                return redirect(url_for('adminportal'))
            else:
                flash('You are not authorized to access this page.')
                return redirect(url_for('login'))
        except:
            flash('You are not authorized to access this page.')
            return redirect(url_for('login'))
    
    flash('You are not authorized to access this page.')
    return redirect(url_for('login'))

@app.route('/hrportal', methods=['GET', 'POST'])
def hrportal():
    return render_template('hrportal.html', title='HR Portal', is_hr=is_hr)

@app.route('/adminportal', methods=['GET', 'POST'])
def adminportal():
    return render_template('adminportal.html', title='Admin Portal', is_it=is_it)

@app.route('/hrportal/searchuser', methods=['GET', 'POST'])
def searchuser():
    form = SearchUserForm()

    if form.validate_on_submit():
        found_user = ad.find_user(form.username.data)
        if found_user:
            return render_template('searchuser.html', title='HR Portal', is_hr=is_hr, form=form, found_user=found_user)
        else:
            flash('User not found.')
            return redirect(url_for('hrportal'))
        
    return render_template('searchuser.html', title='Test', form=form)

@app.route('/hrportal/groupsearch', methods=['GET', 'POST'])
def groupsearch():
    form = SearchUserForm()

    if form.validate_on_submit():
        found_group = ad.find_groups(form.username.data)
        if found_group:
            return render_template('groupsearch.html', title='HR Portal', is_hr=is_hr, form=form, found_group=found_group)
        else:
            flash('User not found.')
            return redirect(url_for('hrportal'))
        
    return render_template('groupsearch.html', title='Test', form=form)

@app.route('/logout')
def logout():
    # Remove user session
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))