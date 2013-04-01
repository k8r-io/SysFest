from flask import Flask,g,render_template,request,send_file,Response
from data import BaseDB
from os import environ
from data.mongo import MongoFest
import json
import bson
import logging
from logging import FileHandler, StreamHandler;

app = Flask(__name__)
stderr = StreamHandler()
app.logger.addHandler(stderr)
if 'SYSFEST_CONFIG' in environ:
	app.config.from_object(environ['SYSFEST_CONFIG'])
else:
	app.logger.critical("No SYSFEST_CONFIG environment variable found!")
	
file_handler = FileHandler(app.config["LOG_PATH"]+"sysfest.log")
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)
app.logger.removeHandler(stderr)

def _clean_oid(host):
	if isinstance(host["_id"], bson.objectid.ObjectId):
		host["_id"]={"_oid":str(host["_id"])}
	return host

@app.before_request
def open_db(): 
	g.db =  MongoFest(app)

@app.teardown_request
def close_db(exception): 
	g.db.close()

@app.route('/host',methods=['GET'])
@app.route('/host/',methods=['GET'])
def list_all():
	hosts = g.db.find()
	payload = {}
	payload['hosts'] = [ _clean_oid(h) for h in hosts ]
	payload['ok']=1
	resp = Response(json.dumps(payload), status=200,mimetype='application/json')
	return resp

@app.route('/host/<hostname>',methods=['GET'])
def show_host(hostname): 
	host = g.db.find_one(hostname=hostname)
	payload = {}
	payload['host'] = _clean_oid(host)
	payload['ok']=1
	resp = Response(json.dumps(payload), status=200,mimetype='application/json')
	return resp

