import cast_upgrade_1_6_4 # @UnusedImport
import unittest
from cast.analysers.test import UATestAnalysis
from cast.application.test import run
from cast.application import create_engine

class TestIntegration(unittest.TestCase):

    def test_basic(self):
        myengine = create_engine("postgresql+pg8000://operator:CastAIP@localhost:2282/postgres")
        run(kb_name='symf01_local', application_name='symf01', engine=myengine)
        
        
if __name__ == "__main__":
    unittest.main()
        