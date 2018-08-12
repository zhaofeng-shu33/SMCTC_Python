#include <boost/python.hpp>
#include <exception>
#include <gsl/gsl_rng.h>

#include <cmath>
#include <cstdlib>
#include <iostream>

#include "rng.hh"
#include "history.hh"
#include "moveset_python.hh"
#include "sampler_python.hh"
using namespace boost::python;
#ifndef __SMC_TDSMC_HH
#define __SMC_TDSMC_HH 1.0
#endif
#ifndef Particle
#define Particle smc::particle<boost::python::list>
#endif
#define Sampler smc::sampler_python<list>


void translate(smc::moveset_python_init_exception const& e)
{
    PyErr_SetString(PyExc_TypeError, e.what());
}

BOOST_PYTHON_MODULE(smctc)
{
    scope().attr("__version__") = __SMC_TDSMC_HH;

    enum_<ResampleType>("ResampleType")
    .value("SMC_RESAMPLE_MULTINOMIAL", SMC_RESAMPLE_MULTINOMIAL)
    .value("SMC_RESAMPLE_RESIDUAL", SMC_RESAMPLE_RESIDUAL)
    .value("SMC_RESAMPLE_STRATIFIED", SMC_RESAMPLE_STRATIFIED)
    .value("SMC_RESAMPLE_SYSTEMATIC", SMC_RESAMPLE_SYSTEMATIC);

    enum_<HistoryType>("HistoryType")
    .value("SMC_HISTORY_NONE", SMC_HISTORY_NONE)
    .value("SMC_HISTORY_RAM", SMC_HISTORY_RAM);        

    class_<Particle>("particle", init<list,double>())
    .def(init<>())
    .def(init<Particle>())
    .def("SetLogWeight", &Particle::SetLogWeight)
    .def("GetLogWeight", &Particle::GetLogWeight)
    .def("SetValue",&Particle::SetValue)
    .def("GetValue", &Particle::GetValue, return_value_policy<copy_const_reference>())
    .def("AddToLogWeight", &Particle::AddToLogWeight);

    class_<Sampler, boost::noncopyable>("sampler", init<long, HistoryType>())
    .def("SetMoveSet", &Sampler::SetMoveSet)
    .def("Initialise", &Sampler::Initialise)
    .def("SetResampleParams", &Sampler::SetResampleParams)
    .def("Iterate", &Sampler::Iterate)
    .def("Integrate_Mean", &Sampler::Integrate_Mean);

    class_<smc::rng>("rng",init<>())
    .def("Normal", &smc::rng::Normal);

    register_exception_translator<smc::moveset_python_init_exception>(&translate);
    class_<smc::moveset_python>("moveset", init<object, object>())
    .def(init<>())
    .def("DoMove", &smc::moveset_python::DoMove)
    .def("DoInit", &smc::moveset_python::DoInit, return_value_policy<manage_new_object>());
}

