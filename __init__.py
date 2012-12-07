from flask import Flask,g,render_template,request,send_file,Response
from data import BaseDB
from os import environ
import json
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
def index():
	return send_file(filename_or_fp='static/index.html')

@app.route('/host',methods=['GET'])
@app.route('/host/',methods=['GET'])
def list_all():
	hosts = g.db.find()
	data = ""
	for h in hosts:
		data += h.to_json()
	resp = Response(data, status=200,mimetype='application/json')
	return resp

@app.route('/host/<hostname>',methods=['GET'])
def show_host(hostname): 
	host = g.db.find_one(hostname=hostname)
	data = host.to_json()
	return Response(data, status=200,mimetype='application/json')

