#!/usr/bin/env python2

from setuptools import setup, find_packages


def included_package(p):
	return p.startswith('spacq.') or p == 'spacq'


setup(
	name='SpanishAcquisition',
	version='3.0.0',
	author='Dmitri Iouchtchenko',
	author_email='diouchtc@uwaterloo.ca',
	maintainer='Paulo Miguel',
	maintainer_email='pmiguel@uwaterloo.ca',
	description='Package for interfacing with devices and building user '
			'interfaces.',
	license='BSD',
	url='http://ghwatson.github.com/SpanishAcquisitionIQC/',
	packages=[p for p in find_packages() if included_package(p)],
	classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: BSD License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
	],
)
