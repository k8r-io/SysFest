from mongokit import Connection, Document
from sysfest.data import BaseDB
import pymongo
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
		self.logger = app.logger
	def find(self,hostname='',tags=''):
		if hostname == '':
			return [ self._clean_oid(h) for h in self.conn.sysfest.Host.find().sort("hostname", pymongo.ASCENDING) ]
		elif hostname != '':
			regx = re.compile(hostname)
			return [ self._clean_oid(h) for h in self.conn.sysfest.Host.find({"$or":[{'hostname':regx},{'homes.hostnames.val':regx}]}).sort("hostname", pymongo.DESCENDING) ]
	def search(self,query):
		tag_pattern = re.compile('tag:(\w+)')
		tags = tag_pattern.findall(query)
		query = tag_pattern.sub('',query)
		hostnames = query.split(' ')
		terms = [{"$or":[{'hostname':re.compile(x)},{'homes.hostnames.val':re.compile(x)}]} for x in hostnames]
		
		if tags: #pythonic (moronic) way to check if an array is empty
			terms = terms + [{"tags":{"$all":tags}}]

		return [ self._clean_oid(h) for h in self.conn.sysfest.Host.find({"$and":terms}).sort("hostname", pymongo.DESCENDING) ]

	def find_one(self,host_id):
		if isinstance(host_id, basestring):
			host_id=bson.objectid.ObjectId(host_id)
		host = self._clean_oid(self.conn.sysfest.Host.find_one({'_id':host_id}))
		return host
	def update(self,host_id,values):
		self.conn.sysfest.hosts.update({"_id":bson.objectid.ObjectId(host_id)},{"$set":values})
		return self.find_one(host_id)
	def create(self,values):
		oid = self.conn.sysfest.hosts.insert(values)
		return self.find_one(host_id=oid)
	def delete(self,host_id):
		return self.conn.sysfest.hosts.remove({'_id':bson.objectid.ObjectId(host_id)})

	def close(self):
		self.conn.disconnect()

	def _clean_oid(self,host):
		if host is not None and isinstance(host["_id"], bson.objectid.ObjectId):
			host["_id"]=str(host["_id"])
		return host
		

