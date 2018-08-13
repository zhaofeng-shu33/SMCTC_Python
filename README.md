# SMCTC_Python
[![Build Status](https://travis-ci.org/zhaofeng-shu33/SMCTC_Python.svg?branch=master)](https://travis-ci.org/zhaofeng-shu33/SMCTC_Python)
This project uses `boost_python` to wrap `C++` implementation of particle filter algorithms from [**Sequential Monte Carlo Template Class**](https://warwick.ac.uk/fac/sci/statistics/staff/academic-research/johansen/smctc).

## How to build(linux and mac)

Depedencies: `gsl`, `gslcblas`, `boost-python`

Use `Makefile` to build `libsmctc.a` and run `python setup.py build` to build the extension library.
