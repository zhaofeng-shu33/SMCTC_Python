#!/usr/bin/python
# author:zhaofeng-shu33
# file-description: unit-test of smctc module
import unittest
import smctc
def fInitialise(pRng):
    value = [0.0]*2 # state
    value[0] = pRng.Normal(0, 1) # pos
    value[1] = pRng.Normal(0, 1) # vel
    return smctc.particle(value, 1.0)
def fMove(lTime, pFrom, pRng):
    cv_to = pFrom.GetValue() # state, list
    cv_to[0] += cv_to[1] + pRng.Normal(0, 0.1)
    cv_to[1]  += pRng.Normal(0, 0.1)
    pFrom.AddToLogWeight(0.1)

class TestMoveSet(unittest.TestCase):
    def test_Constructor(self):
        smctc.moveset()
        smctc.moveset(fInitialise, fMove)
    def test_DoInit(self):
        fmove = smctc.moveset(fInitialise, fMove)
        mrng = smctc.rng()
        pp = fmove.DoInit(mrng)
    def test_DoMove(self):
        a = smctc.particle([1,2.0],2.3)        
        mrng = smctc.rng()
        fmove = smctc.moveset(fInitialise, fMove)
        fmove.DoMove(0, a, mrng)
        self.assertAlmostEquals(a.GetLogWeight(),2.4)
        
class TestRandomNumberGenerator(unittest.TestCase):
    def test_Normal(self):
        smctc.rng().Normal(0,1)

class TestSampler(unittest.TestCase):
    def test_Init(self):
        smctc.sampler(100,smctc.HistoryType.SMC_HISTORY_NONE)
class TestEnumType(unittest.TestCase):
    def test_ResampleType(self):
        smctc.ResampleType.SMC_RESAMPLE_MULTINOMIAL
        smctc.ResampleType.SMC_RESAMPLE_RESIDUAL
        smctc.ResampleType.SMC_RESAMPLE_STRATIFIED
        smctc.ResampleType.SMC_RESAMPLE_SYSTEMATIC
    def test_HistoryType(self):
        smctc.HistoryType.SMC_HISTORY_NONE
        smctc.HistoryType.SMC_HISTORY_RAM
        
class TestModuleLevelClass(unittest.TestCase):
    def test_version(self):
        smctc.__version__
    
class TestParticleClass(unittest.TestCase):
    def test_init_default(self):
        smctc.particle()
    def test_init_value(self):
        a = smctc.particle([1,2.0],2.3)
    def test_init_copy(self):
        a = smctc.particle([1,2.0],2.3)
        b = smctc.particle(a)
    def test_get_log_weight(self):
        a = smctc.particle([1,2.0],2.3)
        self.assertEqual(a.GetLogWeight(), 2.3)
    def test_get_value(self):
        a = smctc.particle([1,2.0],2.3)
        self.assertEqual(a.GetValue(), [1,2.0])
    def test_set_log_weight(self):
        a = smctc.particle()
        a.SetLogWeight(2.3)
        self.assertEqual(a.GetLogWeight(),2.3)
    def test_set_value(self):
        a = smctc.particle()
        a.SetValue([1,2.0])
        self.assertEqual(a.GetValue(),[1,2.0])
if __name__ == '__main__':
    unittest.main()