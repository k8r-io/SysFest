from distutils.core import setup

setup(
	name='SysFest',
<<<<<<< HEAD
	version='0.1.1',
=======
	version='0.1.2',
>>>>>>> development
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