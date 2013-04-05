from mongokit import Connection, Document
from sysfest.data import BaseDB
import re
import bson

class Host(Document):
	__collection__ = 'hosts'
	use_dot_notation = True
	structure = {
		'hostname': unicode,
		'description': unicode,
		'homes': [ {'name':unicode,'ip':unicode,'hostnames':[{'val': unicode}]} ],
		'tags' : [ unicode ] }
	
class MongoFest(BaseDB):
	def __init__(self,app):
		self.conn = Connection(app.config['MONGODB_HOST'],app.config['MONGODB_PORT'])	
		self.conn.register(Host)
	def find(self,hostname=''):
		if hostname == '':
			return [ self._clean_oid(h) for h in self.conn.sysfest.Host.find() ]
		elif hostname != '':
			regx = re.compile(hostname)
			return [ self._clean_oid(h) for h in self.conn.sysfest.Host.find({"$or":[{'hostname':regx},{'homes.hostnames.val':regx}]}) ]
	def find_one(self,host_id):
		return self._clean_oid(self.conn.sysfest.Host.find_one({'_id':bson.objectid.ObjectId(host_id)}))
	def update(self,host_id,values):
		self.conn.sysfest.Host.update("_id":ObjectId(host_id),{"$set":values})

	def close(self):
		self.conn.disconnect()

	def _clean_oid(self,host):
		if isinstance(host["_id"], bson.objectid.ObjectId):
			host["_id"]={"_oid":str(host["_id"])}
		return host
		

