//   SMCTC: moveset.hh  
//
//   Copyright Adam Johansen, 2008.
// 
//   This file is part of SMCTC.
//
//   SMCTC is free software: you can redistribute it and/or modify
//   it under the terms of the GNU General Public License as published by
//   the Free Software Foundation, either version 3 of the License, or
//   (at your option) any later version.
//
//   SMCTC is distributed in the hope that it will be useful,
//   but WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//   GNU General Public License for more details.
//
//   You should have received a copy of the GNU General Public License
//   along with SMCTC.  If not, see <http://www.gnu.org/licenses/>.
//

//! \file
//! \brief Classes and functions which deal with collections of sampler proposal "moves".
//!
//! This file contains definitions of smc::moveset.
//! It deals with the collections of proposal moves (including initialisation and MCMC moves) which must be dealt with by the sampler.

#ifndef __SMC_MOVESET_PYTHON_HH
#define __SMC_MOVESET_PYTHON_HH 1.0

#include "particle_python.hh"
#include "rng.hh"
#include <boost/python.hpp>
#include <string>
#ifndef Particle
#define Particle smc::particle<boost::python::list>
#endif
namespace smc {
  /// A template class for a set of moves for use in an SMC samplers framework.
  class moveset_python_init_exception : std::exception
  {
    public:
      moveset_python_init_exception(const char* variable_name):
      variable_name_str(variable_name) {}
      char const* what() const throw() { return (variable_name_str + " must be function object").c_str(); }
      virtual ~moveset_python_init_exception() throw (){}    
    private:
      std::string variable_name_str;
  };
  class moveset_python
    {
    private:
      ///The number of moves which are present in the set
      long number;
      ///The function which initialises a particle.
      // Particle (*pfInitialise)(rng*);
      boost::python::object pfInitialise;
      ///The function which selects a move for a given particle at a given time.
      // long (*pfMoveSelect)(long , const Particle &, rng*);
      boost::python::object pfMoveSelect;
      ///The functions which perform actual moves.
      // void (**pfMoves)(long, Particle &, rng*);
      boost::python::object* pfMoves;
      ///A Markov Chain Monte Carlo move.
      // int (*pfMCMC)(long,Particle &, rng*);

    public:
      ///Create a completely unspecified moveset
      moveset_python();
      ///Create a reduced moveset with a single move
      moveset_python(const boost::python::object& pfInit, const boost::python::object& pfNewMoves);
      
      ///Initialise a particle
      Particle* DoInit(const rng& pRng) { 
        return new Particle(boost::python::call<Particle>(pfInitialise.ptr(),boost::ref(pRng)));
      }
      ///Select an appropriate move at time lTime and apply it to pFrom
      void DoMove(long lTime, Particle & pFrom, const rng& pRng);
      
      ///Free the memory used for the array of move pointers when deleting
      ~moveset_python();

      /// \brief Set the initialisation function.
      /// \param pfInit is a function which returns a particle generated according to the initial distribution 
      void SetInitialisor(const boost::python::object& pfInit)
      {
        PyObject *pfInit_ptr;
        pfInit_ptr = pfInit.ptr();
        if(!PyFunction_Check(pfInit_ptr)){ 
           throw moveset_python_init_exception("pfInit");
        }
        pfInitialise = pfInit;
      }

      ///Set the individual move functions to the supplied array of such functions
      void SetMoveFunctions(long nMoves, const boost::python::object* pfNewMoves);
      
      ///Moveset assignment should allocate buffers and deep copy all members.
      moveset_python & operator= (moveset_python & pFrom);
    };


  /// The argument free smc::moveset constructor simply sets the number of available moves to zero and sets
  /// all of the associated function pointers to NULL.
 moveset_python::moveset_python()
  {
    number = 0;
    pfMoves = NULL;
  }

  /// The three argument moveset constructor creates a new set of moves and sets all of the relevant function
  /// pointers to the supplied values. Only a single move should exist if this constructor is used.
  /// \param pfInit The function which should be used to initialise particles when the system is initialised
  /// \param pfNewMoves An functions which moves a particle at a specified time to a new location
  /// \param pfNewMCMC The function which should be called to apply an MCMC move (if any)
 moveset_python::moveset_python(const boost::python::object& pfInit, const boost::python::object& pfNewMoves)
  {
    SetInitialisor(pfInit);
    pfMoves = NULL; //This presents an erroneous deletion by the following call
    SetMoveFunctions(1, &pfNewMoves);
    // SetMCMCFunction(pfNewMCMC);
  }

 


 moveset_python::~moveset_python()
  {
    if(pfMoves)
      delete [] pfMoves;
  }

 
  
  void moveset_python::DoMove(long lTime, Particle & pFrom, const rng& pRng)
  {
    //  if(number > 1)
	  //     pfMoves[pfMoveSelect(lTime,pFrom,pRng)](lTime,pFrom,pRng);
    //  else
	    pfMoves[0](lTime,boost::ref(pFrom),boost::ref(pRng));
  }

  /// \param nMoves The number of moves which are defined in general.
  /// \param pfNewMoves An array of functions which move a particle at a specified time to a new location
  ///
  /// The move functions accept two arguments, the first of which corresponds to the system evolution time and the
  /// second to an initial particle position and the second to a weighted starting position. It returns a new 
  /// weighted position corresponding to the moved particle.
  
   void moveset_python::SetMoveFunctions(long nMoves, const boost::python::object* pfNewMoves)
    {
      number = nMoves;
      if(pfMoves)
	       delete [] pfMoves;
      pfMoves =  new boost::python::object[nMoves];
      for(int i = 0; i < nMoves; i++){
        if(!PyFunction_Check(pfNewMoves[i].ptr()))
            throw moveset_python_init_exception("pfNewMoves");
	      pfMoves[i] = pfNewMoves[i];
      }
      return;
    }

  
 moveset_python &moveset_python::operator= (moveset_python & pFrom)
  {
    SetInitialisor(pFrom.pfInitialise);
    SetMoveFunctions(pFrom.number, pFrom.pfMoves);        
    
    return *this;
  }
}
#endif
