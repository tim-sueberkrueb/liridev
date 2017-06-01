#!/usr/bin/env python3
# -*- coding: utf-8

import setuptools

setuptools.setup(
    name='liridev',
    version='0.1.0',
    description='Liri development tools',
    license='MIT',
    author='Tim Süberkrüb',
    author_email='dev@timsueberkrueb.io',
    url='https://www.github.com/tim-sueberkrueb',
    packages=setuptools.find_packages(),
    scripts=[
        'bin/liridev'
    ],
    install_requires=[
        'click'
    ]
)
