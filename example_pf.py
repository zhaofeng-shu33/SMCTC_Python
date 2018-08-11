#!/usr/local/python
#@author: zhaofeng-shu33
from math import log, sqrt
import smctc
import pdb
var_s0 = 4
var_u0 = 1
var_s  = 0.02
var_u  = 0.001

scale_y = 0.1
nu_y = 10.0
Delta = 0.1
global y
y = [] # cv_obs_list

def logLikelihood(lTime, X):
    """
    The function corresponding to the log likelihood at specified time and position (up to normalisation)
    param: lTime[int] The current time (i.e. the index of the current distribution)
    param: X[list]     The state to consider 
    """
    global y
    return -0.5 * (nu_y + 1.0) * (log(1 + pow((X[0] - y[lTime][0])/scale_y,2) / nu_y) + log(1 + pow((X[1] - y[lTime][1])/scale_y, 2) / nu_y))

def fInitialise(pRng):
    """
    A function to initialise particles

    param: pRng[smctc.rng] A pointer to the random number generator which is to be used
    """
    value = [0.0]*4 # cv_state
  
    value[0] = pRng.Normal(0,sqrt(var_s0)) # x_pos
    value[1] = pRng.Normal(0,sqrt(var_s0)) # y_pos
    value[2] = pRng.Normal(0,sqrt(var_u0)) # x_vel
    value[3] = pRng.Normal(0,sqrt(var_u0)) # y_vel

    return smctc.particle(value,logLikelihood(0,value))


def fMove(lTime, pFrom, pRng):
    """
    The proposal function.

    param: lTime[int] The sampler iteration.
    param: pFrom[smc.particle] The particle to move.
    param: pRng[smc.rng]  A random number generator.
    """
    cv_to = pFrom.GetValue() # cv_state, list

    cv_to[0] += cv_to[2] * Delta + pRng.Normal(0,sqrt(var_s))
    cv_to[2]  += pRng.Normal(0,sqrt(var_u))
    cv_to[1]  += cv_to[3] * Delta + pRng.Normal(0,sqrt(var_s))
    cv_to[3]  += pRng.Normal(0,sqrt(var_u))

    pFrom.AddToLogWeight(logLikelihood(lTime, cv_to))

if __name__ == '__main__':
    # initialize observation list
    cv_obs_one = [1.1, 2.2]
    y.append(cv_obs_one)
    cv_state_tmp = [3.3, 4.4, 5.5, 6.6]
    logLikelihood(0, cv_state_tmp)
    rng_tmp = smctc.rng()
    particle_tmp = fInitialise(rng_tmp)
    pdb.set_trace()    
    fMove(0, particle_tmp, rng_tmp)
    pdb.set_trace()    
    # observe that particle_tmp.GetValue() is changed by calling `fmove`
    