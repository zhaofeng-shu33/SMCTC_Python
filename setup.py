import os
import sys
from setuptools import Extension, setup
DEBUG = False # if produce debug version, change False to True
if False: # for osx version<=9, change False to True
    osx_use_libc = '-stdlib=libc++'
else:
    osx_use_libc = ''
sources_list = ['smctc_ext.cpp']
link_flag_list = []
compile_flag_list = []
include_dir_list = ['./include']
if sys.platform == 'linux2':
    boost_py_lib = '-lboost_python-py' + sys.version[0] + sys.version[2] 
elif sys.platform == 'darwin':
    boost_py_lib = '-lboost_python' + sys.version[0] + sys.version[2]
    if(osx_use_libc):
        link_flag_list.append(osx_use_libc)
        compile_flag_list.append(osx_use_libc)
elif sys.platform == 'win32':
    boost_py_lib = ''
    sources_list.extend(['./include/history.cc','./include/rng.cc', './include/smc-exception.cc'])
else:
    raise Exception("Unsupported platform")

if sys.platform == 'win32':
    # for windows, we only support condas build
    conda_include = os.path.join(os.environ['CONDA_PREFIX'],'Library','include')
    conda_lib_path = os.path.join(os.environ['CONDA_PREFIX'],'Library','lib') 
    include_dir_list.append(conda_include)
    compile_flag_list.append('/EHsc')
    compile_flag_list.append('/DWIN32')
    compile_flag_list.append('/DGSL_DLL')
    link_flag_list.append('/LIBPATH:'+conda_lib_path)
    link_flag_list.append('libboost_exception.lib')
    link_flag_list.append('gsl.lib')
    link_flag_list.append('gslcblas.lib')
    if(DEBUG):
        compile_flag_list.append('/Od')    
else:
    # for other platforms, we only support system python build
    link_flag_list.extend(['-L./include', '-lsmctc','-lgsl', '-lgslcblas'])
    if(DEBUG):
        compile_flag_list.append('-O0')    
    
link_flag_list.append(boost_py_lib)

module = Extension('smctc', sources=sources_list, 
include_dirs = include_dir_list,
extra_link_args = link_flag_list,
extra_compile_args = compile_flag_list
)

setup(name='smctc', ext_modules = [module])
