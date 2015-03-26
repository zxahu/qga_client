# 
# Get configration from ini file
#
# @author Litrin J.
#

from ConfigParser import ConfigParser
import re


class Configuration(object):

    # Instance for singleton
    __selfObject = None
    # Content cached.
    __cache = {}
    # The default config file path
    __filename = '/etc/qga_agent.conf'

    def __init__(self, sFile = ''):
        if sFile != '': 
            self.__filename = sFile

        self.__getConfig()
         
    def __getConfig(self):
        config = ConfigParser()
        config.read(self.__filename)
        
        for section in config.sections():
            self.__cache[section] = {}
            for option in config.options(section):
                tmp = config.get(section, option)
                if re.match(r"^'.*'$", tmp) or re.match(r'^".*"$', tmp): 
                    tmp = tmp[1:-1]
                self.__cache[section][option] = tmp

    def getSection(self, section):
        if self.__cache.has_key(section):
            return self.__cache[section]
        else:
            errorMessage = 'Section %s not found!' % (section)
            raise NameError, errorMessage

    def getOption(self, section, option):
        option = option.lower()
        if self.__cache.has_key(section) and self.__cache[section].has_key(option):
            return self.__cache[section][option]
        else:
            errorMessage = 'Option %s[%s] not found!' % (section, option)
            raise NameError, errorMessage

    def __repr__(self):
        filestring = open(self.__filename, 'r').read()
        string = '''Config File: %s
----------
%s
----------
        ''' % (self.__filename, filestring)

        return string


