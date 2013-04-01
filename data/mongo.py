from mongokit import Connection, Document
from sysfest.data import BaseDB

class Host(Document):
	__collection__ = 'hosts'
	use_dot_notation = True
	structure = {
		'hostname': unicode,
		'description': unicode,
		'homes': [ {'ip':unicode,'hostnames':[{'val': unicode}]} ],
		'tags' : [ unicode ] }
	
class MongoFest(BaseDB):
	def __init__(self,app):
		self.conn = Connection(app.config['MONGODB_HOST'],app.config['MONGODB_PORT'])	
		self.conn.register(Host)
	def find(self,hostname=''):
		if hostname == '':
			return self.conn.sysfest.Host.find()
		else:
			return self.conn.sysfest.Host.find({'hostname':hostname})
	def find_one(self,hostname):
			return self.conn.sysfest.Host.find_one({'hostname':hostname})
	def close(self):
		self.conn.disconnect()
		

