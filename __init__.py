from flask import Flask,g,render_template
from data import BaseDB
from os import environ
app = Flask(__name__)
app.config.from_object("sysfest.config")
if 'SYSFEST_CONFIG' in environ:
	app.config.from_object(environ['SYSFEST_CONFIG'])


@app.before_request
def open_db(): 
		if 'DB_MODULE' in app.config and 'DB_CLASS' in app.config:
				_temp = __import__(app.config['DB_MODULE'],globals(),locals(),[app.config['DB_CLASS']],-1)
				db_class = getattr(_temp,app.config['DB_CLASS'])
				g.db = db_class(app)
		else:
				g.db = BaseDB(app)
	

@app.teardown_request
def close_db(exception): 
	g.db.close()


@app.route('/')
@app.route('/hosts')
def list_all():
	hosts = g.db.find()
	return render_template('list_hosts.html',hosts=hosts)

@app.route('/hosts/<hostname>')
def show_host(): pass

