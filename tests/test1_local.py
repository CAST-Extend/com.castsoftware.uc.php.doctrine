'''
Created on May 27, 2019

@author: MMR
'''
import unittest
import cast.analysers.test

class Test(unittest.TestCase):
    
    def testRunAnalysis(self):
        
        # UA 
        analysis = cast.analysers.test.UATestAnalysis('PHP')
        analysis.add_selection('test1')
        analysis.set_verbose(True)
        analysis.run()
        
        
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()