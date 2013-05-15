from flask import Flask,g,render_template,request,send_file,Response
from data import BaseDB
from os import environ
from data.mongo import MongoFest
import json
import logging
from logging import FileHandler, StreamHandler;

app = Flask(__name__)
stderr = StreamHandler()
app.logger.addHandler(stderr)
app.config.from_object('sysfest.default_config')
if 'SYSFEST_CONFIG' in environ:
	app.config.from_envvar('SYSFEST_CONFIG')
	
app.logger.removeHandler(stderr)

if 'LOG_FILE' in app.config and app.config['LOG_FILE'] != '':
	file_handler = FileHandler(app.config["LOG_FILE"])
	file_handler.setLevel(logging.DEBUG)
	app.logger.addHandler(file_handler)


@app.before_request
def open_db(): 
	g.db =  MongoFest(app)

@app.teardown_request
def close_db(exception): 
	g.db.close()

@app.route('/host',methods=['GET'])
def list_all():
	hosts = g.db.find()
	resp = Response(json.dumps(hosts), status=200,mimetype='application/json')
	return resp

@app.route('/host',methods=['POST'])
def update_host(): 
	data = request.json
	if "_id" in data:
		host_id = data["_id"]
		data.pop("_id")
		host = g.db.update(host_id=host_id,values=data)
	else:
		host = g.db.create(data)

	resp = Response(json.dumps(host),status=200,mimetype='application/json')
	return resp

@app.route('/host/hostname/<hostname>',methods=['GET'])
def find_by_hostname(hostname): 
	hosts = g.db.find(hostname=hostname)
	resp = Response(json.dumps(hosts), status=200,mimetype='application/json')
	return resp


@app.route('/host/<host_id>',methods=['GET'])
def show_host(host_id): 
	host = g.db.find_one(host_id=host_id)
	resp = Response(json.dumps(host), status=200,mimetype='application/json')
	return resp

@app.route('/host/<host_id>',methods=['DELETE'])
def delete_host(host_id): 
	g.db.delete(host_id=host_id)
	resp = Response("", status=200,mimetype='application/json')
	return resp

