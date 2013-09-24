from distutils.core import setup

setup(
	name='SysFest',
	version='0.1.3',
	author='Kristopher Kirkland',
	author_email='kirkland@umn.edu',
	packages=['sysfest','sysfest.data'],
	url='https://github.com/ASCIIDuck/SysFest',
	description='Backend CRUD api used for tracking host inventory',
	install_requires=[
		'Flask',
		'MongoKit'
	]
)