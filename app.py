import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, abort
from flaskext.seasurf import SeaSurf

import settings

from mongoengine import connect, Document, StringField, EmailField, BooleanField, DateTimeField, URLField

app = Flask(__name__)
app.config.from_object(settings)

csrf = SeaSurf(app)

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
	created = DateTimeField()

@app.route("/")
def home():
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
		job = Job(company_name=request.form['company_name'])
		job.company_location=request.form['company_location']
		job.company_url=request.form['company_url']
		job.job_posting=request.form['job_posting']
		job.application_instructions=request.form['application_instructions']
		job.created=datetime.utcnow()
		job.save()
		return redirect(url_for('home'))
	else:
		return render_template('create_job.html')

@app.route('/job/<job_id>')
def show_job(job_id):
	job = Job.objects.with_id(job_id)
	return render_template('show_job.html', job=job)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)