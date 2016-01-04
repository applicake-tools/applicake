# identification workflow for systeMHC

#!/usr/bin/env python
import os
import sys
import subprocess
from multiprocessing import freeze_support

from ruffus import *

from applicake.apps.examples.a_pyecho import PythonEcho
from applicake.apps.flow.merge import Merge
from applicake.apps.flow.split import Split
from toolscake.apps.tpp.dropbox import Copy2IdentDropbox
from toolscake.apps.tpp.interprophet import InterProphet
from toolscake.apps.tpp.peptideprophet import PeptideProphetSequence
from toolscake.apps.tpp.searchengines.comet import Comet
from toolscake.apps.tpp.searchengines.iprophetpepxml2csv import IprohetPepXML2CSV
from toolscake.apps.tpp.searchengines.myrimatch import Myrimatch

basepath = os.path.dirname(__file__) + '/../../'





@files("input.ini", "inputfix.ini")
def biopersdb(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    PythonEcho.main()

@follows(biopersdb)
@split("inputfix.ini", "split.ini_*")
def split_dataset(infile, unused_outfile):
    sys.argv = ['--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'MZXML']
    Split.main()
    #subprocess.check_call(['python', basepath + 'appliapps/flow/split.py',
    #                       '--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'MZXML'])

###################################################################################

@transform(split_dataset, regex("split.ini_"), "rawmyri.ini_")
def myri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Myrimatch.main()
    #subprocess.check_call(['python', basepath + 'appliapps/tpp/searchengines/myrimatch.py',
    #                       '--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4'])


@transform(myri, regex("rawmyri.ini_"), "myrimatch.ini_")
def peppromyri(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepmyri']
    PeptideProphetSequence.main()
    #subprocess.check_call(['python', basepath + 'appliapps/tpp/peptideprophet.py',
    #                      '--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepmyri'])

###################################################################################

@transform(split_dataset, regex("split.ini_"), "rawcomet.ini_")
def comet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4']
    Comet.main()
    #subprocess.check_call(['python', basepath + 'appliapps/tpp/searchengines/comet.py',
    #                       '--INPUT', infile, '--OUTPUT', outfile, '--THREADS', '4'])


@transform(comet, regex("rawcomet.ini_"), "comet.ini_")
def pepprocomet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepcomet']
    PeptideProphetSequence.main()
    #subprocess.check_call(['python', basepath + 'appliapps/tpp/peptideprophet.py',
    #                       '--INPUT', infile, '--OUTPUT', outfile, '--NAME', 'pepcomet'])


############################# TAIL: PARAMGENERATE ##################################

@merge([pepprocomet,peppromyri], "ecollate.ini")
def merge_datasets(unused_infiles, outfile):
    sys.argv = ['--MERGE', 'comet.ini', '--MERGED', outfile]
    Merge.main()
    #subprocess.check_call(['python', basepath + 'appliapps/flow/merge.py',
    #                       '--MERGE', 'engineiprophet.ini', '--MERGED', outfile])

@follows(merge_datasets)
@files("ecollate.ini_0", "datasetiprophet.ini")
def datasetiprophet(infile, outfile):
    sys.argv = ['--INPUT', infile, '--OUTPUT', outfile]
    InterProphet.main()
    #subprocess.check_call(['python', basepath + 'appliapps/tpp/interprophet.py',
    #                       '--INPUT', infile, '--OUTPUT', outfile])

@follows(datasetiprophet)
@files("datasetiprophet.ini", "copy2dropbox.ini")
def convert2csv(infile, outfile):
    sys.argv = [ '--INPUT', infile, '--OUTPUT', outfile]
    IprohetPepXML2CSV.main()




def setupWindows():
    if len(sys.argv) > 1 and sys.argv[1] == 'cont':
        print 'Continuing with existing input.ini (Ruffus should skip to the right place automatically)'
    else:
        print 'Starting from scratch by creating new input.ini'
        subprocess.call("rm *ini* *.log", shell=True)
        with open("input.ini", 'w+') as f:
            f.write("""
LOG_LEVEL = DEBUG
COMMENT = WFTEST - newUPS TPP

# Search parameters
FDR_CUTOFF = 0.01
FDR_TYPE = iprophet-pepFDR
FRAGMASSERR = 0.5
FRAGMASSUNIT = Da
PRECMASSERR = 15
PRECMASSUNIT = ppm
MISSEDCLEAVAGE = 0
ENZYME = Nonspecific
STATIC_MODS =
VARIABLE_MODS = Oxidation (M)

## TPP
DECOY_STRING = DECOY_
IPROPHET_ARGS = MINPROB=0


## Parameters
MZXML=D:/projects/p1958/data/datafiles/mzXML/PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep1_msms1_c.mzXML,D:/projects/p1958/data/datafiles/mzXML/PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep2_msms2_c.mzXML
#,D:/projects/p1958/data/datafiles/mzXML/PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep3_msms3_c.mzXML,D:/projects/p1958/data/datafiles/mzXML/PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep4_msms4_c.mzXML,D:/projects/p1958/data/datafiles/mzXML/PBMC1_Tubingen_120724_CB_Buffy18_W_20_Rep5_msms5_c.mzXML


DBASE=D:/projects/p1958/data/databases/CNCL_05640_2015_09_DECOY.fasta
COMET_DIR=C:/Users/wolski/prog/applicake-tools/SearchCake_Binaries/Comet/windows/windows_64bit
COMET_EXE=comet.exe
MYRIMATCH_DIR=C:/Users/wolski/prog/applicake-tools/SearchCake_Binaries/MyriMatch/windows/windows_64bit
MYRIMATCH_EXE=myrimatch.exe
TPPDIR=C:/Users/wolski/prog/applicake-tools/SearchCake_Binaries/tpp/windows/windows_64bit

""")


def runPipline():
    freeze_support()
    pipeline_run([convert2csv],multiprocess=3)

if __name__ == '__main__':
    setupWindows()
    runPipline()

#pipeline_printout_graph ('flowchart.png','png',[copy2dropbox],no_key_legend = False) #svg
