#!/usr/bin/env python
import os
import sys
import subprocess

from ruffus import *


basepath = os.path.dirname(__file__) + '/../../'


def setup():
    if len(sys.argv) > 1 and sys.argv[1] == 'cont':
        print 'Continuing with existing input.ini (Ruffus should skip to the right place automatically)'
    else:
        print 'Starting from scratch by creating new input.ini'
        subprocess.call("rm *ini* *.log", shell=True)
        with open("input.ini", 'w') as f:
            f.write("""
RUNSWATH2VIEWER = true
THREADS = 4
MODULE = imsbtools/20140808_swath
WORKFLOW = wf
LOG_LEVEL = DEBUG
BASEDIR = /cluster/scratch_xl/shareholder/imsb_ra/workflows/
DATASET_DIR = /cluster/scratch_xl/shareholder/imsb_ra/datasets/
DROPBOX = /cluster/scratch_xl/shareholder/imsb_ra/openbis_dropbox/
COMMENT = WFTEST - newUPS SWATH

IRTTRAML = /cluster/apps/imsbtools/stable/files/hroest_DIA_iRT.TraML
MIN_RSQ = 0.95
MIN_COVERAGE = 0.6
MIN_UPPER_EDGE_DIST = 1
EXTRACTION_WINDOW = 0.05
RT_EXTRACTION_WINDOW = 600
EXTRA_RT_EXTRACTION_WINDOW = 100
WINDOW_UNIT = Thomson
DO_CHROMML_REQUANT = true
USE_DIA_SCORES = true
USE_MS1_TRACES = false

MPR_NUM_XVAL = 10
#MPR_LDA_PATH = /cluster/apps/guse/stable/wftests/chludwig_L110830_20_SW_scorer.bin
MPR_MAINVAR = xx_swath_prelim_score
MPR_VARS = bseries_score elution_model_fit_score intensity_score isotope_correlation_score isotope_overlap_score library_corr library_rmsd log_sn_score massdev_score massdev_score_weighted norm_rt_score xcorr_coelution xcorr_coelution_weighted xcorr_shape xcorr_shape_weighted yseries_score
MPR_DSCORE_CUTOFF = 1

ALIGNER_FDR =
ALIGNER_MAX_FDRQUAL =
ALIGNER_TARGETFDR = 0.01
ALIGNER_MAX_RT_DIFF = 30
ALIGNER_FRACSELECTED = 0
ALIGNER_METHOD = best_overall
ALIGNER_REALIGN_METHOD = splineR_external

MATRIX_FORMAT = tsv
DB_SOURCE = PersonalDB
DATABASE_PACKAGE = LOBLUM
DATABASE_VERSION = newUPS1 ruffus reference
DATABASE_DB = 20130823112025
DBASE = 20130823112244490-872696

SPACE = LOBLUM
PROJECT = JUNK
DATASET_CODE = 20130110233329710-761850, 20130110232929822-761848, 20130110215707264-761830
""")


@follows(setup)
@files("input.ini", "biopersdb.ini")
def biopersdb(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/openbis/biopersdb.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@follows(biopersdb)
@files("biopersdb.ini", "tramltotsv.ini")
def tramltotsv(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/tramltotsv.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@follows(tramltotsv)
@split("tramltotsv.ini", "split.ini_*")
def split_dataset(infile, unused_outfile):
    subprocess.check_call(['python', basepath + 'appliapps/flow/split.py',
                           '--INPUT', infile, '--SPLIT', 'split.ini', '--SPLIT_KEY', 'DATASET_CODE'])


@transform(split_dataset, regex("split.ini_"), "dss.ini_")
def dss(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/openbis/dss.py',
                           '--INPUT', infile, '--OUTPUT', outfile, '--EXECUTABLE', 'getdataset'])


#debug_irt problem
@jobs_limit(1)
@transform(dss, regex("dss.ini_"), "osw.ini_")
def openswathworkflow(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/openswath.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@transform(openswathworkflow, regex("osw.ini_"), "pprophet.ini_")
def pprophet(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/pyprophet.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@merge(pprophet, "mergedataset.ini_0")
def merge_dataset(unused_infile, unused_outfile):
    subprocess.check_call(['python', basepath + 'appliapps/flow/merge.py',
                           '--MERGE', 'pprophet.ini', '--MERGED', 'mergedataset.ini'])


@follows(merge_dataset)
@files("mergedataset.ini_0", "featurealign.ini")
def featurealign(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/featurealign.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@follows(featurealign)
@split("featurealign.ini", "splitchrom.ini_*")
def split_chrom(infile, unused_outfile):
    subprocess.check_call(['python', basepath + 'appliapps/flow/split.py',
                           '--INPUT', infile, '--SPLIT', 'splitchrom.ini', '--SPLIT_KEY', 'CHROM_MZML'])


@transform(split_chrom, regex("splitchrom.ini_"), "requant.ini_")
def requant(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/requant.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@merge(requant, "mergerequant.ini_0")
def merge_chrom(unused_infile, unused_outfile):
    subprocess.check_call(['python', basepath + 'appliapps/flow/merge.py',
                           '--MERGE', 'requant.ini', '--MERGED', 'mergerequant.ini'])


@follows(merge_chrom)
@files("mergerequant.ini_0", "matrix.ini")
def matrix(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/matrix.py',
                           '--INPUT', infile, '--OUTPUT', outfile])


@follows(matrix)
@files("matrix.ini", "cp2dropbox.ini")
def cp2dropbox(infile, outfile):
    subprocess.check_call(['python', basepath + 'appliapps/swath/dropbox.py',
                           '--INPUT', infile, '--OUTPUT', outfile])

########################################################
pipeline_run([cp2dropbox], multiprocess=3, verbose=2)
    
