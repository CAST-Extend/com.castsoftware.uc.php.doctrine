import cast_upgrade_1_6_4 # @UnusedImport
from cast.analysers import log, CustomObject, create_link, external_link, Bookmark
import cast.analysers.ua

"""
class PHPDoctrineExtensionAnalysis
"""
    
class PHPDoctrineExtensionAnalysis(cast.analysers.ua.Extension):

    def __init__(self):
        self.currentphpsectionObject = None
        self.currentphpclassObject = None

    ###################################################################################################        
    def end_object(self, object):
        log.info('PHPDoctrineExtensionAnalysis end_object ' + object)   
        
    ###################################################################################################        
    def end_file(self, file):
        log.info('PHPDoctrineExtensionAnalysis end_file ' + file)   
 