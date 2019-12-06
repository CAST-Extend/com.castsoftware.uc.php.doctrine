import cast_upgrade_1_6_4 # @UnusedImport
from cast.application import ApplicationLevelExtension, ReferenceFinder, create_link
import logging 
import sys
import re
import traceback

"""
class PHPDoctrineExtensionApplication
    
"""
    
class PHPDoctrineExtensionApplication(ApplicationLevelExtension):

    ###################################################################################################        

    
    def __init__(self):
        self.nbPHPFileScanned = 0
        self.nbYAMLFileScanned = 0
        self.nbYAMLFileWithSymfonyServices = 0
        self.nbSymfonyService = 0
        
        self.nbLinksDoctrineTableAnnotation = 0 
        self.nbLinksMethodToClass = 0         
        self.nbLinksDoctrineRepositoryClass = 0
        self.nbLinksSymfonyServiceToServiceClass = 0
        self.nbLinksPHPToSymfonyService = 0
        
        self.tables = {}        
        self.phpClassesList = []
        self.phpSymfonyServices = {}
        self.phpClassesByName = {}
        self.mappingSectionClass = {}
        
        self.currentSymfonyServiceName = None
        
    ###################################################################################################        
 
    def end_app_log(self):
        # Final reporting
        logging.info("end_app_log###################################################################################")
        logging.info("Number of PHP files scanned : " +  str(self.nbPHPFileScanned))
        logging.info("Number of YAML files scanned : " +  str(self.nbYAMLFileScanned))
        logging.info("Number of YAML files containing Symfony services : " +  str(self.nbYAMLFileWithSymfonyServices))
        logging.info("Number of Symfony services found : " +  str(self.nbSymfonyService))
        
        logging.info("Doctrine - Number of links to Tables from annotations : " +  str(self.nbLinksDoctrineTableAnnotation))
        logging.info("Doctrine - Number of links to repository class from entity annotation : " + str(self.nbLinksDoctrineRepositoryClass))
        logging.info("Number of links created from methods to class : " +  str(self.nbLinksMethodToClass))
        logging.info("Number of links created from Symfony services to Symfony service class : " + str(self.nbLinksSymfonyServiceToServiceClass))
        logging.info("Number of links created from php to Symfony service : " + str(self.nbLinksPHPToSymfonyService))
        logging.info("###################################################################################")
  
    ###################################################################################################        
  
    def end_application(self, application):
        logging.info("*********************************************************************************") 
        logging.info("PHPDoctrineExtensionApplication : running code at the end of an application")

        # tables found in the analysis (SQL analyzer + Oracle analyzer)
        for oTable in application.objects().has_type(['SQLScriptTable', 'CAST_Oracle_RelationalTable',]):
            logging.debug("Table " + oTable.get_fullname())
            self.tables[oTable.get_name()] = oTable

        # PHP classes found in the analysis (SQL analyzer + Oracle analyzer)
        for oClass in application.objects().has_type(['phpClass', ]):
            logging.debug("Class " + oClass.get_fullname())
            self.phpClassesByName[oClass.get_name()] = oClass
            self.phpClassesList.append(oClass)

        # PHP sections found in the analysis (SQL analyzer + Oracle analyzer)
        for oSection in application.objects().has_type(['phpSection', ]):
            logging.debug("Section " + oSection.get_fullname())
            # identify the class for each section, if any
            for oClass in self.phpClassesList:
                if oSection.get_fullname() in oClass.get_fullname():
                    self.mappingSectionClass[oSection.get_fullname()] = oClass
                    break

        # Symfony service
        for oSymfonyService in application.objects().has_type(['phpSymfonyService', ]): 
            self.nbSymfonyService += 1
            logging.debug("Symfony service " + oSymfonyService.get_fullname())
            self.phpSymfonyServices[oSymfonyService.get_name()] = oSymfonyService

        ############################################################################################
        #looking through PHP files
        files = application.get_files(['sourceFile'])        
        logging.debug("parsing files")

        for o in files:
            #logging.debug("parsing file > " + o.get_path())
            # check if file is analyzed source code, or if it generated (Unknown)
            if not o.get_path():
                continue
            #         <attribute name="extensions" stringValue="*.php;*.php4;*.php5;*.php6;*.inc;*.phtml;*.yml;*.yaml"/>
            
            # php files
            if re.match('.*\.[pP][hH][pP][0-9]*|.*\.[iI][nN][cC]|.*\.[pP][tT][hH][mM][lL]',o.get_path()):
                logging.debug("parsing file > " + o.get_path())
                self.scan_phpfile(application, o)               
                self.nbPHPFileScanned += 1

            # yaml files
            if re.match('.*\.[yY][mM][lL]|.*\.[yY][aA][mM][lL]',o.get_path()):
            #         <attribute name="extensions" stringValue="*.php;*.php4;*.php5;*.php6;*.inc;*.phtml;*.yml;*.yaml"/>
                logging.debug("parsing file > " + o.get_path())
                self.scan_yamlfile(application, o)      
                self.nbYAMLFileScanned += 1

        self.end_app_log()

    ###################################################################################################        

    def scan_yamlfile(self, application, yfile):
        logging.debug("INIT scan_yamlfile > " +str(yfile.name))
        bContainsService = False 
        # one RF for multiples patterns
        rfCall = ReferenceFinder()
        # to make sure this file contains Symfony services
        rfCall.add_pattern('containsService', before='', element = 'services:', after='')
        # to collect the Symfony service name
        rexSymfonyServiceName = '^[ ][ ][ ][ ]([A-Za-z0-9_\.-]+)[:]'
        rfCall.add_pattern('SymfonyServiceName', before='', element = rexSymfonyServiceName, after='')
        # to collect the service clas name
        rexSymfonyServiceClassName = '^[ ][ ][ ][ ][ ][ ][ ][ ][cC][lL][aA][sS][sS][:][\t ]*[A-Za-z0-9\-_\\\\]+[\\\\]([A-Za-z0-9\-_]+)'
        rfCall.add_pattern('SymfonyServiceClassName', before='', element = rexSymfonyServiceClassName, after='')
        
        try:
            references = [reference for reference in rfCall.find_references_in_file(yfile)]
        except FileNotFoundError:
            logging.warning("Wrong file or file path, from Vn-1 or previous " + str(yfile))
        else:
            # for debugging and traversing the results
            for reference in references:
                #logging.debug("  DONE: reference found: >" +str(reference))
                
                # identify the boolmark and parent object
                bk_line_code = reference.bookmark.begin_line  
                most_specific_object = yfile.find_most_specific_object(bk_line_code , 1)
                   
                # Service name
                if  reference.pattern_name=='containsService':
                    logging.debug("\t\t  containsService>" +reference.value)                   
                    bContainsService = True
                    self.nbYAMLFileWithSymfonyServices += 1
                   
                # Service name
                if bContainsService and reference.pattern_name=='SymfonyServiceName':
                    logging.debug("\t\t  SymfonyServiceName>" + str(reference))
                    m0 = re.search(rexSymfonyServiceName, reference.value)
                    if m0:
                        self.currentSymfonyServiceName = m0.group(1)

                # Service class name
                if bContainsService and reference.pattern_name=='SymfonyServiceClassName':
                    logging.debug("\t\t\t  SymfonyServiceClassName>" + str(reference))
                    logging.debug("\t\t\t\t  self.currentSymfonyServiceName>" + self.currentSymfonyServiceName)
                    m0 = re.search(rexSymfonyServiceClassName, reference.value)
                    if m0:
                        symfonyServiceClassName = m0.group(1)
                        try:
                            oclass = self.phpClassesByName[symfonyServiceClassName]
                            osymfonyservice = self.phpSymfonyServices[self.currentSymfonyServiceName] 
                            logging.debug("\t\t\t\t  creating link betwween SymfonyService " + osymfonyservice.get_fullname() + " and class " + oclass.get_fullname())
                            create_link("useLink", osymfonyservice, oclass, reference.bookmark)
                            self.nbLinksSymfonyServiceToServiceClass += 1
                        except KeyError:
                            logging.warning('Not able to find class ' + symfonyServiceClassName)
                    

    ###################################################################################################        
  
  
    def scan_phpfile(self, application, phpfile):
        logging.debug("INIT scan_phpfile > " +str(phpfile.name))
                
        # one RF for multiples patterns
        rfCall = ReferenceFinder()
        # Be careful, the order here is important !!!!!!
        
        # lines comments in PHP files
        rfCall.add_pattern('CSCOMMENTEDline',before = '', element = r'^[\t ]*//.*$|^[\t ]*#.*$', after = '')     # requires application_1_4_7 or above
        
        # Mapping class
        # example : @ORM\Table(name="affaire_r"
        #/**
        # * AffaireR
        # * @ORM\Table(name="affaire_r")
        # * @ORM\Entity(repositoryClass="NatachaBundle\Repository\AffaireRRepository")
        # * @ORM\Entity
        # * @ORM\Table(name="affaire_r")
        #*/
        rexTableAnnotation = '@ORM\\\\Table\(name=[\'"]([A-Za-z0-9\-_]+)[\'"]'
        rfCall.add_pattern('DoctrineTableAnnotation', before='', element = rexTableAnnotation, after='')

        # Repository class
        #rexRepositoryClass = '@ORM\\\\Entity\(repositoryClass="[A-Za-z0-9\-_\\\\]([A-Za-z0-9\-_]+)"'
        rexRepositoryClass = '@ORM\\\\Entity\(repositoryClass=[\'"][A-Za-z0-9\-_\\\\]+[\\\\]([A-Za-z0-9\-_]+)[\'"]'
        rfCall.add_pattern('DoctrineRepositoryClass', before='', element = rexRepositoryClass, after='') 
        
        # Class from methods to Classes
        # looking for class name after a namespace 
        # examples :
        #    -> LeftJoin("NatachaBundle:AffaireC",'ac','WITH','a.id=ac.ic'
        #    . "JOIN AppBundle:AuditLog audit "
        #    -> getRepository("AppTdexBundle:TCasier");
        #    $commune = $em-> getRepository('AppBundle:Commune')->getAutocomplete();
        #    ->from('NatachaBundle:AffaireC'
        rexClass = '[\'"].*[A-Za-z0-9\-_]+[:]([A-Za-z0-9\-_]+)'

        # examples :
        #    ->join('u.AffaireR', 'ar', 'WITH', 'a.id = ar.id')
        rexClass =  rexClass + '|' + '\([\'"][A-Za-z0-9]+[.]([A-Za-z0-9_-]+)'

        # examples :
        #    ->from('AffaireR'
        rexClass = rexClass + '|' +  '([fF][rR][oO][mM]|[jJ][oO][iI][nN])\([\'"]([A-Za-z0-9]+)[\'"]'
        rfCall.add_pattern('MethodToClassLink', before='', element = rexClass, after='')

        # PHP to symfony services 
        # examples : 
        rexphpToSymfonyService = '[gG][eE][tT]\(["\']([A-Za-z0-9_\.-]+)["\']'
        rfCall.add_pattern('PhpToSymfonyService', before='', element = rexphpToSymfonyService, after='')

        try:
            references = [reference for reference in rfCall.find_references_in_file(phpfile)]
        except FileNotFoundError:
            logging.warning("Wrong file or file path, from Vn-1 or previous " + str(phpfile))
        else:
            # for debugging and traversing the results
            for reference in references:
                #logging.debug("  DONE: reference found: >" +str(reference))
                
                # identify the boolmark and parent object
                bk_line_code = reference.bookmark.begin_line  
                most_specific_object = phpfile.find_most_specific_object(bk_line_code , 1)
                   
                # Pattern 1 - Looking for the @ORM\Table Doctrine annotation
                if  reference.pattern_name=='DoctrineTableAnnotation':
                    logging.debug("\t\t  DoctrineTableAnnotation>" +reference.value)
                    m0 = re.search(rexTableAnnotation, reference.value)
                    if m0:
                        tablename = m0.group(1)
                        try:
                            tableObject = self.tables[tablename]
                            try:
                                # get the class name
                                parentObject = self.mappingSectionClass[most_specific_object.get_fullname()]
                            except KeyError:
                                #if there is no php class in the php section we keep the section as parent object
                                parentObject = most_specific_object
                            create_link("useLink", parentObject, tableObject, reference.bookmark)
                            self.nbLinksDoctrineTableAnnotation += 1
                        except KeyError:
                            logging.warning("\t\t  Couldn't find table in local schema : " +tablename)
                
                #  Pattern 2 - Looking for the repository class
                if  reference.pattern_name=='DoctrineRepositoryClass':
                    logging.debug("\t\t  DoctrineRepositoryClass>" +reference.value)
                    m0 = re.search(rexRepositoryClass, reference.value)
                    if m0:
                        repositoryClassName = m0.group(1)
                        try:
                            repositoryClassObject = self.phpClassesByName[repositoryClassName]
                            try:
                                # get the class name for this section
                                parentObject = self.mappingSectionClass[most_specific_object.get_fullname()]
                            except KeyError:
                                #if there is no php class in the php section we keep the section as parent object
                                parentObject = most_specific_object
                            create_link("useLink", parentObject, repositoryClassObject, reference.bookmark)
                            self.nbLinksDoctrineRepositoryClass += 1
                        except KeyError:
                            logging.warning("\t\t  Couldn't find phpClass in local schema (DoctrineRepositoryClass) : " +repositoryClassName)

                # Pattern 3 - Looking for method with namespace to class link to create
                if  reference.pattern_name=='MethodToClassLink':
                    logging.debug("\t\t  MethodToClassLink>" +reference.value)
                    m0 = re.search(rexClass, reference.value)
                    if m0:
                        classname = m0.group(1)
                        if classname == None: classname = m0.group(2)
                        if classname == None: classname = m0.group(4)
                        logging.debug("\t\t  classname>" +classname)    
                        
                        try:
                            classObject = self.phpClassesByName[classname]
                            parentObject = most_specific_object
                            create_link("useLink", parentObject, classObject, reference.bookmark)
                            self.nbLinksMethodToClass += 1
                        except KeyError:
                            logging.warning("\t\t  Couldn't find phpClass in local schema (MethodToClassLink) : " +classname)

                if  reference.pattern_name=='PhpToSymfonyService':
                    logging.debug("\t\t  PhpToSymfonyService>" +reference.value)
                    m0 = re.search(rexphpToSymfonyService, reference.value)
                    if m0:
                        servicename = m0.group(1)
                        try:
                            serviceObject = self.phpSymfonyServices[servicename]
                            parentObject = most_specific_object
                            create_link("callLink", parentObject, serviceObject, reference.bookmark)                            
                            self.nbLinksPHPToSymfonyService += 1
                        except KeyError:
                            logging.warning("\t\t  Couldn't find symfony service in local schema (PhpToSymfonyService) : " +servicename)

    ###################################################################################################        


      