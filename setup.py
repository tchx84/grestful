from setuptools import setup

setup(name='grestful',
    keywords=['restful', 'pyobject']
    version='0.0.5',
    description='Integrate RESTful web services to your Glib2 code.',
    url='http://github.com/tchx84/grestful',
    author='Martin Abente Lahaye',
    author_email='martin.abente.lahaye@gmail.com',
    license='LGPL',
    packages=['grestful'],
    install_requires=[
        'pycurl'
    ],
    zip_safe=False)
