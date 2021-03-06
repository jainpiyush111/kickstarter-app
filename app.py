from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import flask_login
from models import User, Projects, Pledges
from flask.ext.login import *
import flask_login_auth


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)


# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('pages/placeholder.home.html')

@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.name.data
        password = form.password.data
        value = flask_login_auth.authenticate(username, password)
        if (value == 1):
            get_data = flask_login_auth.get_data(username, password)
            session['name'] = username
            session['usersid'] = get_data[0][0]
            project = flask_login_auth.show_project(session['usersid'])
            session['project'] = project
            return render_template('pages/placeholder.home.html', session=session)
    return render_template('forms/login.html', form=form)


@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateProject(request.form)
    if request.method == 'POST':
        project = Projects(session['usersid'], form.name.data, form.short_desc.data,
                           form.long_desc.data, form.goal_amount.data, form.time_end.data)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pages/placeholder.create.html', form=form)


@app.route('/index')
def index():
    project = flask_login_auth.show_project(session['usersid'])
    session['project'] = project
    return render_template('pages/placeholder.home.html', session=session)

@app.route('/showPledge', methods=['GET', 'POST'])
def showPledge():
    if request.method == 'POST':
        projectId = request.form['submit']
        session['projectId'] = projectId
        return redirect(url_for('newPledge'))


@app.route('/newPledge', methods=['GET', 'POST'])
def newPledge():
    form = NewPledge(request.form)
    if request.method == 'POST':
       pledge = Pledges(session['projectId'],session['usersid'],form.amount.data)
       db.session.add(pledge)
       db.session.commit()
       return redirect(url_for('home'))
    return render_template('pages/placeholder.pledge.html', form=form, session=session)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = User(form.name.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
