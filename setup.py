# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in whitelabel/__init__.py
from whitelabel import __version__ as version

setup(
	name='whitelabel',
	version=version,
	description='ERPNext Whitelabel',
	author='Bhavesh Maheshwari',
	author_email='maheshwaribhavesh95863@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
