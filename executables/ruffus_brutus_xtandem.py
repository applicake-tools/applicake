#!/usr/bin/env python
'''
Created on Jun 5, 2012

@author: quandtan
'''

import os
import sys
from ruffus import *
from cStringIO import StringIO
from subprocess import Popen
from subprocess import PIPE
from applicake.framework.runner import GeneratorRunner
from applicake.framework.runner import CollectorRunner
from applicake.framework.runner import WrapperRunner
from applicake.applications.proteomics.openbis.generator import GuseGenerator
from applicake.applications.os.echo import Echo
from applicake.applications.commons.collector import GuseCollector
from applicake.applications.proteomics.searchengine.xtandem import Xtandem
from applicake.applications.proteomics.openms.filehandling.fileconverter import Mzxml2Mgf
from applicake.applications.proteomics.openbis.dss import Dss

cwd = None

def execute(command):
    p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)            
    output, error = p.communicate()                                                                                                                                                                            
    out_stream = StringIO(output)
    err_stream = StringIO(error) 


def setup():
    cwd = '.'
    os.chdir(cwd)
    execute("find . -type d -iname '[0-9]*' -exec rm -rf {} \;")
    execute('rm *.err')
    execute('rm *.out')
    execute('rm *.log')
    execute('rm *ini*')
#    execute('rm jobid.txt') 
    execute('rm flowchart.*')    
    with open("input.ini", 'w+') as f:
        f.write("""BASEDIR = /cluster/scratch/malars/workflows
LOG_LEVEL = DEBUG
STORAGE = file
TEMPLATE = template.tpl
DATASET_DIR = /cluster/scratch/malars/datasets
DATASET_CODE = 20120603160111752-510155,20120603165413998-510432,
DBASE = /cluster/scratch/malars/biodb/ex_sp/current/decoy/ex_sp_9606.fasta
FRAGMASSERR = 0.4
FRAGMASSUNIT = Da
PRECMASSERR = 15
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
STATIC_MODS = 'Carbamidomethyl (C)'
VARIABLE_MODS = 'Phospho (STY)'
THREADS = 4
""")       

@follows(setup)
@split("input.ini", "generate.ini_*")
def generator(input_file_name, notused_output_file_names):
    sys.argv = ['IGNORED', '-i', input_file_name, '--GENERATORS', 'generate.ini' ,'-l','DEBUG']
    runner = GeneratorRunner()
    application = GuseGenerator()
    exit_code = runner(sys.argv, application)
    if exit_code != 0:
        raise Exception("generator failed [%s]" % exit_code) 
    
@transform(generator, regex("generate.ini_"), "dssout.ini_")
def dss(input_file_name, output_file_name):
    sys.argv = ['IGNORED', '-i', input_file_name, '-o', output_file_name, '--PREFIX', 'getmsdata']
    runner = WrapperRunner()
    wrapper = Dss()
    exit_code = runner(sys.argv, wrapper)
    if exit_code != 0:
                raise Exception("dss failed [%s]" % exit_code)    
    
@transform(dss, regex("dssout.ini_"), "xtandemout.ini_")
def tandem(input_file_name, output_file_name):
    sys.argv = ['IGNORED', '-i', input_file_name, '-o', output_file_name, 
                '--TEMPLATE', 'xtandem.tpl',
                '--PREFIX', 'tandem','-l','DEBUG']
    runner = WrapperRunner()
    wrapper = Xtandem()
    exit_code = runner(sys.argv, wrapper)
    if exit_code != 0:
        raise Exception("echo failed [%s]" % exit_code) 
      
    
@merge(tandem, "output.ini")
def collector(notused_input_file_names, output_file_name):
    sys.argv = ['IGNORED', '--COLLECTORS', 'xtandemout.ini', '-o', output_file_name,'-s','file']
    runner = CollectorRunner()
    application = GuseCollector()
    exit_code = runner(sys.argv, application)
    if exit_code != 0:
        raise Exception("collector failed [%s]" % exit_code)    

pipeline_run([collector])


#pipeline_printout_graph ('flowchart.png','png',[collector],no_key_legend = False) #svg
