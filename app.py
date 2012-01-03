import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort
import settings

from mongoengine import connect, Document, StringField, EmailField, BooleanField, DateTimeField, URLField

app = Flask(__name__)
app.config.from_object(settings)

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

class Job(Document):
	company_name = StringField(required=True)
	company_location = StringField(required=True)
	company_url = URLField(required=True)
	job_posting = StringField(required=True)
	application_instructions = StringField(required=True)
	telework = BooleanField(required=True)
	created = DateTimeField(default = datetime.utcnow())

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = os.urandom(15)
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/create', methods=['GET', 'POST'])
def create_job():
	if request.method == 'POST':
		job = Job(company_name=request.form['company_name'],
		          company_location=request.form['company_location'], 
		          company_url=request.form['company_url'],
		          job_posting=request.form['job_posting'],
		          telework=request.form['telework'])
		job.save()
		redirect(url_for('/'))
	return render_template('create_job.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)