import os
import sys
from setuptools import Extension, setup

if False:
    osx_specific = '-stdlib=libc++'
else:
    osx_specific = ''

boost_py_lib = '-lboost_python' + sys.version[0] + sys.version[2]

module = Extension('smctc', sources=['smctc_ext.cpp'], 
include_dirs = ['./include'],
extra_link_args=[boost_py_lib, '-L./include', '-lsmctc','-lgslcblas', '-lgsl', osx_specific],
extra_compile_args=['-O0', osx_specific])

setup(name='smctc', ext_modules = [module])