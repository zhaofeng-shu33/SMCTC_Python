import os
import sys
from setuptools import Extension, setup

if False: # if necessay, change False to True
    osx_specific = '-stdlib=libc++'
else:
    osx_specific = ''
if sys.platform =='linux2':
	boost_py_lib = '-lboost_python-py' + sys.version[0] + sys.version[2] 
else:
	boost_py_lib = '-lboost_python' + sys.version[0] + sys.version[2]

module = Extension('smctc', sources=['smctc_ext.cpp'], 
include_dirs = ['./include'],
extra_link_args=[boost_py_lib, '-L./include', '-lsmctc','-lgsl', '-lgslcblas'],
extra_compile_args=['-O0']
)

setup(name='smctc', ext_modules = [module])
