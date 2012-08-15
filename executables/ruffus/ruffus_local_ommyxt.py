#!/usr/bin/env python
'''
Created on Aug 15, 2012

@author: quandtan
'''

import os
import sys
from ruffus import *
from cStringIO import StringIO
from subprocess import Popen
from subprocess import PIPE
from applicake.framework.runner import IniFileRunner2, ApplicationRunner,CollectorRunner,WrapperRunner, IniFileRunner
from applicake.applications.commons.generator import DatasetcodeGenerator,\
    ParametersetGenerator
from applicake.applications.os.echo import Echo
from applicake.applications.commons.collector import GuseCollector
from applicake.applications.proteomics.searchengine.xtandem import Xtandem
from applicake.applications.proteomics.openbis.dss import Dss
from applicake.applications.proteomics.tpp.tandem2xml import Tandem2Xml
from applicake.applications.proteomics.tpp.xinteract import Xinteract
from applicake.applications.proteomics.tpp.interprophet import InterProphet
from applicake.applications.proteomics.openms.filehandling.idfileconverter import PepXml2IdXml
from applicake.applications.proteomics.openms.peptideproteinprocessing.falsediscoveryrate import FalseDiscoveryRate
from applicake.applications.proteomics.openms.peptideproteinprocessing.peptideindexer import PeptideIndexer
from applicake.applications.proteomics.openms.peptideproteinprocessing.idfilter import IdFilter
from applicake.applications.proteomics.openms.filehandling.fileconverter import Mzxml2Mzml
from applicake.applications.proteomics.openms.signalprocessing.peakpickerhighres import PeakPickerHighRes
from applicake.applications.proteomics.openms.quantification.featurefindercentroided import OrbiLessStrict
from applicake.applications.proteomics.sybit.pepxml2csv import Pepxml2Csv
from applicake.applications.proteomics.sybit.fdr2probability import Fdr2Probability
from applicake.applications.proteomics.tpp.proteinprophet import ProteinProphet
from applicake.applications.proteomics.sybit.protxml2spectralcount import ProtXml2SpectralCount
from applicake.applications.proteomics.sybit.protxml2modifications import ProtXml2Modifications
from applicake.applications.proteomics.sybit.protxml2openbis import ProtXml2Openbis
from applicake.applications.proteomics.openbis.dropbox import Copy2Dropbox,\
    Copy2IdentDropbox
from applicake.applications.commons.inifile import Unifier
from applicake.framework.interfaces import IApplication, IWrapper
from applicake.applications.proteomics.proteowizard.msconvert import Mzxml2Mgf
from applicake.applications.proteomics.searchengine.omssa import Omssa
from applicake.applications.proteomics.searchengine.myrimatch import Myrimatch

cwd = None


#helper function
def wrap(applic,  input_file_name, output_file_name,opts=None):
    argv = ['', '-i', input_file_name, '-o', output_file_name]
    if opts is not None:
        argv.extend(opts)
    application = applic()
    if isinstance(application, IApplication):
        runner = ApplicationRunner()
        print 'use application runner'
    elif isinstance(application, IWrapper):
        runner = WrapperRunner()
    else:
        raise Exception('could not identfy [%s]' % applic.__name__)    
    application = applic()
    exit_code = runner(argv, application)
    if exit_code != 0:
        raise Exception("[%s] failed [%s]" % (applic.__name__, exit_code)) 

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
        f.write("""BASEDIR = /cluster/home/biol/quandtan/test/workflows
LOG_LEVEL = DEBUG
STORAGE = file
TEMPLATE = template.tpl
DATASET_DIR = /cluster/scratch/malars/datasets
DATASET_CODE = 20120124102254267-296925,20120124121656335-296961
DBASE = /cluster/scratch/malars/biodb/ex_sp/current/decoy/ex_sp_9606.fasta
DECOY_STRING = DECOY_ 
FRAGMASSERR = 0.4
FRAGMASSUNIT = Da
PRECMASSERR = 15,25
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
ENZYME = Trypsin
STATIC_MODS = Carbamidomethyl (C)
THREADS = 4
XTANDEM_SCORE = k-score
XINTERACT_ARGS = -dDECOY_ -OAPdlIw
IPROPHET_ARGS = MINPROB=0
FDR=0.01
SPACE = QUANDTAN
PROJECT = TEST
DROPBOX = /cluster/scratch/malars/drop-box_prot_ident
WORKFLOW=ruffus_local_xtom
""" 
#,20120603165413998-510432,
# 20120606045538225-517638 -> b10-01219.p.mzxml
# 20120603160111752-510155 -> b10-01219.c.mzxml 
# 20120124102254267-296925,20120124121656335-296961 -> orbi silac hela from petri
)       
        

@follows(setup)
@split("input.ini", "generate.ini_*")
def generator(input_file_name, notused_output_file_names):
    argv = ['', '-i', input_file_name, '--GENERATORS', 'generate.ini','-o','generator.ini','-l','DEBUG']
    runner = IniFileRunner()
    application = DatasetcodeGenerator()
    exit_code = runner(argv, application)
    if exit_code != 0:
        raise Exception("generator failed [%s]" % exit_code) 
    
@transform(generator, regex("generate.ini_"), "dss.ini_")
@jobs_limit(1)
def dss(input_file_name, output_file_name):   
    wrap(Dss,input_file_name, output_file_name,['--PREFIX', 'getmsdata'])
        
@transform(dss, regex("dss.ini_"), "xtandem.ini_")
def tandem(input_file_name, output_file_name):
    wrap(Xtandem,input_file_name, output_file_name,['--PREFIX', 'tandem.exe','-s','file','-l','DEBUG'])

@transform(tandem, regex("xtandem.ini_"), "xtandem2xml.ini_")
def tandem2xml(input_file_name, output_file_name):
    wrap(Tandem2Xml,input_file_name, output_file_name)  

@transform(tandem2xml, regex("xtandem2xml.ini_"), "xinteract_xtandem.ini_")
def xinteract_xtandem(input_file_name, output_file_name):
    wrap(Xinteract,input_file_name, output_file_name,['-n','xinteract_xtandem'])  

@transform(dss, regex("dss.ini_"), "myrimatch.ini_")
def myrimatch(input_file_name, output_file_name):
    wrap(Myrimatch,input_file_name, output_file_name)

@transform(myrimatch, regex("myrimatch.ini_"), "xinteract_myrimatch.ini_")
def xinteract_myrimatch(input_file_name, output_file_name):
    wrap(Xinteract,input_file_name, output_file_name,['-n','xinteract_myrimatch']) 

@transform(dss, regex("dss.ini_"), "msconvert.ini_")
def msconvert(input_file_name, output_file_name):
    wrap(Mzxml2Mgf,input_file_name, output_file_name,['-s','file','-l','DEBUG'])
    
@transform(msconvert, regex("msconvert.ini_"), "omssa.ini_")
def omssa(input_file_name, output_file_name):
    wrap(Omssa,input_file_name, output_file_name)

@transform(omssa, regex("omssa.ini_"), "xinteract_omssa.ini_")
def xinteract_omssa(input_file_name, output_file_name):
    wrap(Xinteract,input_file_name, output_file_name,['-n','xinteract_omssa'])       
    
@merge([xinteract_xtandem,xinteract_myrimatch,xinteract_omssa], "collector.ini")
def collector(notused_input_file_names, output_file_name):
    argv = ['', '--COLLECTORS', 'xinteract_xtandem.ini','--COLLECTORS', 'xinteract_myrimatch.ini','--COLLECTORS', 'xinteract_omssa.ini', '-o', output_file_name,'-s','file']
    runner = CollectorRunner()
    application = GuseCollector()
    exit_code = runner(argv, application)
    if exit_code != 0:
        raise Exception("[%s] failed [%s]" % ('collector',exit_code))    

@follows(collector)
@split("collector.ini", "paramgenerate.ini_*")
def paramgenerator(input_file_name, notused_output_file_names):
    argv = ['', '-i', input_file_name, '--GENERATORS','paramgenerate.ini','-o','paramgenerator.ini']
    runner = IniFileRunner2()
    application = ParametersetGenerator()
    exit_code = runner(argv, application)
    if exit_code != 0:
        raise Exception("paramgenerator [%s]" % exit_code)  

@transform(paramgenerator, regex("paramgenerate.ini_"), "interprophet.ini_")
def interprophet(input_file_name, output_file_name):
    wrap(InterProphet,input_file_name, output_file_name)

@transform(interprophet, regex("interprophet.ini_"), "pepxml2csv.ini_")
def pepxml2csv(input_file_name, output_file_name):
    wrap(Pepxml2Csv,input_file_name, output_file_name)          
    
@transform(pepxml2csv, regex("pepxml2csv.ini_"), "fdr2probability.ini_")
def fdr2probability(input_file_name, output_file_name):
    wrap(Fdr2Probability,input_file_name, output_file_name)        

@transform(fdr2probability, regex("fdr2probability.ini_"), "proteinprophet.ini_") 
def proteinprophet(input_file_name, output_file_name):
    wrap(ProteinProphet,input_file_name, output_file_name)

@transform(proteinprophet, regex("proteinprophet.ini_"), "protxml2spectralcount.ini_") 
def protxml2spectralcount(input_file_name, output_file_name):
    wrap(ProtXml2SpectralCount,input_file_name, output_file_name)

@transform(protxml2spectralcount, regex("protxml2spectralcount.ini_"), "protxml2modifications.ini_")
def protxml2modifications(input_file_name, output_file_name):
    wrap(ProtXml2Modifications,input_file_name, output_file_name)

@transform(protxml2modifications, regex("protxml2modifications.ini_"), "protxml2openbis.ini_")
def protxml2openbis(input_file_name, output_file_name):
    wrap(ProtXml2Openbis,input_file_name, output_file_name)

@transform(protxml2openbis, regex("protxml2openbis.ini_"),"copy2dropbox.ini_")
def copy2dropbox(input_file_name, output_file_name):
    argv = ["", "-i", input_file_name, "-o",output_file_name,"-p"]
    runner = IniFileRunner()
    application = Copy2IdentDropbox()
    exit_code = runner(argv, application)
    if exit_code != 0:
        raise Exception("copy2dropbox [%s]" % exit_code)  


pipeline_run([copy2dropbox], multiprocess = 4)

#pipeline_printout_graph ('flowchart.png','png',[copy2dropbox],no_key_legend = False) #svg
