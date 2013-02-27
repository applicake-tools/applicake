#!/usr/bin/env python
'''
Created on Jun 19, 2012

@author: quandtan
'''

import sys
from applicake.framework.runner import IniFileRunner
from applicake.applications.proteomics.openbis.dropbox import Copy2DropboxQuant

runner = IniFileRunner()
application = Copy2DropboxQuant()
exit_code = runner(sys.argv,application)
print exit_code
sys.exit(exit_code)