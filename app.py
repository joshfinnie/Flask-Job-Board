import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flaskext.seasurf import SeaSurf
from flaskext.bcrypt import Bcrypt

import settings

from mongoengine import connect, Document, StringField, EmailField, DateTimeField, URLField

app = Flask(__name__)
app.config.from_object(settings)

csrf = SeaSurf(app)
bcrypt = Bcrypt(app)

connect('app2312735', 
        host='staff.mongohq.com',
        port=10092, 
        username='heroku',
        password='ded467f4021d3ca1c394707cbb2a8760')

class User(Document):
	username = StringField(required=True)
	email = EmailField(required=True)
	first_name = StringField(max_length=50)
	last_name = StringField(max_length=50)
	location = StringField()
	homepage = StringField()
	passhash = StringField()
	created = DateTimeField()

	meta = {
        'ordering': ['-created']
    }

class Job(Document):
	company_name = StringField(required=True)
	company_location = StringField(required=True)
	company_url = URLField(required=True)
	job_title = StringField(required=True)
	job_posting = StringField(required=True)
	application_instructions = StringField(required=True)
	created = DateTimeField()

	meta = {
        'ordering': ['-created']
    }

@app.route("/")
def home():
	jobs = Job.objects.all()
	return render_template('home.html', jobs=jobs)

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/create', methods=['GET', 'POST'])
def create_job():
	if request.method == 'POST':
		job = Job(company_name=request.form['company_name'])
		job.company_location=request.form['company_location']
		job.company_url=request.form['company_url']
		job.job_title=request.form['job_title']
		job.job_posting=request.form['job_posting']
		job.application_instructions=request.form['application_instructions']
		job.created=datetime.utcnow()
		job.save()
		next_url = job.id
		flash(u'Job successfully created.', 'success')
		return redirect(url_for('show_job', job_id=next_url))
	else:
		return render_template('create_job.html')

@app.route('/signup', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		if request.form['password'] == request.form['password2']:
			user = User(username=request.form['username'])
			user.email=request.form['email']
			user.first_name=request.form['first_name']
			user.last_name=request.form['last_name']
			user.location='None'
			user.passhash=bcrypt.generate_password_hash(request.form['password'])
			user.homepage='None'
			user.created=datetime.utcnow()
			user.save()
			user_id=user.id
			flash(u'Successfully created new user.', 'success')
			return redirect(url_for('show_user', user_id=user_id))
		else:
			flash(u'Passwords do not match.', 'error')
			return render_template('create_user.html')
	else:
		return render_template('create_user.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		try:
			user = User.objects.get(username=request.form['username'])
		except User.DoesNotExist:
			flash(u'Password or Username is incorrect.', 'error')
			return render_template('login.html')
		else:
		 	if not bcrypt.check_password_hash(user.passhash, request.form['password']):
				flash(u'Password or Username is incorrect.', 'error')
				return render_template('login.html')
			else:
				session['username'] = user.username
				session['logged_in'] = True
				flash(u'You have been successfully logged in.', 'success')
				return redirect(url_for('home'))
	else:
		return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('logged_in', None)
    flash(u'You have been successfully logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/user/<user_id>')
def show_user(user_id):
	user = User.objects.with_id(user_id)
	return render_template('show_user.html', user=user)

@app.route('/job/<job_id>')
def show_job(job_id):
	job = Job.objects.with_id(job_id)
	return render_template('show_job.html', job=job)

@app.route('/users')
def show_all_users():
	users = User.objects.all()
	return render_template('show_all_users.html', users=users)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)