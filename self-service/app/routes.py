from app import app
from flask import render_template, flash, redirect, session, url_for
from app.forms import LoginForm, CreateUserForm, SearchUserForm
from ad_tools import ad_tools
import pythoncom

# Since we're checking perms everywhere this function should help with that.
def check_permissions(session, perm_it, perm_hr):
    session = session
    perm_it = perm_it
    perm_hr = perm_hr

    if 'username' in session:
        try:
            if perm_it:
                return "IT"
            elif perm_hr:
                return "HR"
            else:
                return False
        except:
            return False
    else:
        return False


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
        
        if auth:
            global is_it
            global is_hr
            is_it = ad.check_it()
            is_hr = ad.check_hr()

            if auth and is_it and is_hr:
                # Create user session
                session.permanent = False
                session['username'] = form.username.data
                return redirect(url_for('adminportal'))
            elif auth and is_hr:
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
                flash('User is not authorized to access this page.')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('login'))

      
    return render_template('login.html', title='Login', form=form)

@app.route('/portal')
def portal():
    try:
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))

    if check_perm == "IT":
        return redirect(url_for('adminportal'))
    elif check_perm == "HR":
        return redirect(url_for('hrportal'))
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))

@app.route('/hrportal', methods=['GET', 'POST'])
def hrportal():
    try :
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    if check_perm == "HR":
        return render_template('hrportal.html', title='HR Portal', is_hr=is_hr)
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))

@app.route('/hrportal/searchuser', methods=['GET', 'POST'])
def searchuser():
    try :
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))

    form = SearchUserForm()

    if check_perm == "HR":
        if form.validate_on_submit():
            found_user = ad.find_user(form.username.data)
            if found_user:
                return render_template('searchuser.html', title='HR Portal', is_hr=is_hr, form=form, found_user=found_user)
            else:
                flash('User not found.')
                return redirect(url_for('searchuser'))
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
        
    return render_template('searchuser.html', title='Test', form=form)

@app.route('/hrportal/groupsearch', methods=['GET', 'POST'])
def groupsearch():
    try:
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    
    form = SearchUserForm()
    
    if check_perm == "HR":
        if form.validate_on_submit():
            found_group = ad.find_groups(form.username.data)
            if found_group:
                return render_template('groupsearch.html', title='HR Portal', is_hr=is_hr, form=form, found_group=found_group)
            else:
                flash('User not found.')
                return redirect(url_for('groupsearch'))
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
        
    return render_template('groupsearch.html', title='Test', form=form)


@app.route('/adminportal', methods=['GET', 'POST'])
def adminportal():
    try:
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    
    if check_perm == "IT":
        return render_template('adminportal.html', title='Admin Portal', is_it=is_it)
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))

@app.route('/adminportal/createuser', methods=['GET', 'POST'])
def createuser():
    try:
        check_perm = check_permissions(session, is_it, is_hr)
    except:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    
    form = CreateUserForm()
    # Without this pyad does not work.
    pythoncom.CoInitialize()
    
    if check_perm == "IT":
        if form.validate_on_submit():
            try:
                ad.create_user(form.firstname.data, form.lastname.data, form.password.data, global_username, global_password)
                flash('User created successfully.')
                return render_template('createuser.html', title='Create User', form=form)
            except:
                flash('Error creating user.')
                return render_template('createuser.html', title='Create User', form=form)
    else:
        flash('You are not authorized to access this page.')
        return redirect(url_for('login'))
    
    return render_template('createuser.html', title='Create User', form=form)

@app.route('/logout')
def logout():
    # Remove user session
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for('index'))