import copy
from .secrets import ConfigBase


# production configuration 
ConfigProduction = copy.deepcopy(ConfigBase)

# Development configuration
#
# alter any properties to reflect the development changes
# however, be wary that this file will be in source control
# override any of the IConfig properties required for development in the ConfigDevelopment object
#
# TLDR: don't add any sensitive information to this file (passwords, api keys, etc...)
ConfigDevelopment = copy.deepcopy(ConfigBase)

ConfigDevelopment.is_development = True

