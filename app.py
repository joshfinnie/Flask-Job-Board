import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
import settings

from mongoengine import connect, Document, StringField, EmailField, BooleanField, DateTimeField, URLField
from wtforms import Form, BooleanField, TextField, validators, TextAreaField

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

class Job_Form(Form):
	company_name = TextField('Company Name', [validators.required()])
	company_location = TextField('Company Location', [validators.required()])
	company_url = TextField('Company URL', [validators.required()])
	job_posting = TextAreaField('Job Posting', [validators.required()])
	application_instructions = TextField("Application Instructions", [validators.required()])
	telework = BooleanField('Telework?')

@app.route("/")
def hello():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/contact')
def contact():
	return render_template('contact.html')

@app.route('/create')
def create_job():
	form = Job_Form()
	if form.validate_on_submit():
		job = Job(company_name=request.form['company_name'],
		          company_location=request.form['company_location'], 
		          company_url=request.form['company_url'],
		          job_posting=request.form['job_posting'],
		          telework=request.form['telework'])
		job.save()
		next_url = "/%s" % job._id
		redirect(url_for(next_url))	
	return render_template('create_job.html', form=form)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)