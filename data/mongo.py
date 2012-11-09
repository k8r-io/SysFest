from mongokit import Connection, Document
from sysfest.data import BaseDB

class Host(Document):
	__collection__ = 'hosts'
	use_dot_notation = True
	structure = {
		'hostname': unicode,
		'description': unicode,
		'homes': [ {'ip':unicode,'hostnames':[unicode]} ],
		'tags' : [ unicode ] }
	
class MongoFest(BaseDB):
	def __init__(self,app):
		self.conn = Connection(app.config['MONGODB_HOST'],app.config['MONGODB_PORT'])	
		self.conn.register(Host)
	def find(self):
		return self.conn.sysfest.Host.find()
	def close(self):
		self.conn.disconnect()
		

