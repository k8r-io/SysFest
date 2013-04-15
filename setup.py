from distutils.core import setup

setup(
	name='SysFest',
	version='0.1.0',
	author='Kristopher Kirkland',
	author_email='kirkland@umn.edu',
	packages=['sysfest','sysfest.data','sysfest.config'],
	url='https://github.com/ASCIIDuck/SysFest',
	description='Backend CRUD api used for tracking host inventory',
	install_requires=[
		'Flask',
		'MongoKit'
	]
)