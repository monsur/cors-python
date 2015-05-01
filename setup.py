from setuptools import setup
from setuptools import find_packages

setup(
    name='cors-python',
    version='0.0.1',
    description='Python CORS Integration for WSGI Applications',
    author='Monsur Hossain',
    author_email='monsur@gmail.com',
    url='https://github.com/monsur/cors-python',
    packages=find_packages(exclude=('tests',)),
    requires=['WebOb']
)
