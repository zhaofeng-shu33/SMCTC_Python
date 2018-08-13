import os
from setuptools import Extension, setup

module = Extension('smctc', sources=['smctc_ext.cpp'], 
include_dirs = ['./include'],
extra_link_args=['-lboost_python', '-L./include', '-lsmctc','-lgslcblas', '-lgsl'],
extra_compile_args=['-O0'])

setup(name='smctc', ext_modules = [module])