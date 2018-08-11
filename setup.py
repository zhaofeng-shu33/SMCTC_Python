import os
from setuptools import Extension, setup

module = Extension('smctc', sources=['smctc_ext.cpp'], 
include_dirs = ['../include'],
extra_link_args=['-lboost_python37', '-L../lib', '-lsmctc','-lgslcblas', '-lgsl'])

setup(name='smctc', ext_modules = [module])