'''
Created on Aug 10, 2012

@author: lorenz
'''

import shutil
import os
import time
from applicake.utils.fileutils import FileUtils
from applicake.framework.informationhandler import BasicInformationHandler
from applicake.applications.proteomics.openbis.dropbox import Copy2Dropbox

class Copy2SwathDropbox(Copy2Dropbox):
    """
    Copy files to an Openbis-openswath_dropbox.
    
    """
    def _get_dropboxdir(self, info):
        space = info['SPACE']
        project = info['PROJECT']
        prefix = ''
        if info.has_key(self.JOB_IDX):
            prefix = info[self.JOB_IDX]
        if info.has_key(self.PARAM_IDX):
            prefix = '%s.%s' % (prefix,info[self.PARAM_IDX])
        if info.has_key(self.FILE_IDX):
            prefix = '%s.%s' % (prefix,info[self.FILE_IDX])
        dirname = '%s+%s+%s' % (space, project, prefix)
        return os.path.join(info['DROPBOX'],dirname)
            
    def set_args(self,log,args_handler):
        args_handler.add_app_args(log, 'MPROPHET_STATS', 'mprophet stats')
        args_handler.add_app_args(log, 'COMPRESS_OUT', 'compressed featureXMLwithMprophet')
        args_handler.add_app_args(log, 'MPROPHET_TSV', 'mprophet allpeakgroups tsv soutput')
        args_handler.add_app_args(log, 'FEATURETSV', 'featuretsv')
        return super(Copy2SwathDropbox, self).set_args(log,args_handler)
    
    def main(self,info,log):
        
        path = self._get_dropboxdir(info)
        FileUtils.makedirs_safe(log, path,clean=True)
        
        keys = ['MPROPHET_TSV','MPROPHET_STATS','COMPRESS_OUT','FEATURETSV']
        files = []
        for key in keys:
            log.warn(key)
            if isinstance(info[key], list):
                files = info[key]
            else:
                files = [info[key]]
            for file in files:
                try:
                    shutil.copy(file,path)
                    log.debug('Copy [%s] to [%s]' % (file,path))
                except:
                    if FileUtils.is_valid_file(log, file):
                        log.warn('Could not copy, file [%s] already exists' % file)
                    else:
                        log.fatal('Stop program because could not copy [%s] to [%s]' % (file,path))
                        return(1,info,log)
        
        #SPACE PROJECT given
        dsinfo = {}
        dsinfo['SPACE'] = info['SPACE']
        dsinfo['PROJECT'] = info['PROJECT']
        dsinfo['PARENT_DATASETS']= info[self.DATASET_CODE]
        dsinfo['DATASET_TYPE'] = 'SWATH_RESULT'
        dsinfo['EXPERIMENT_TYPE'] = 'SWATH_SEARCH'
        #%.4 is just to have fixed num of digits in experiment
        dsinfo['EXPERIMENT'] = 'E%.4f' % time.time()
        dsinfo[self.OUTPUT] = os.path.join(path,'dataset.attributes')
        BasicInformationHandler().write_info(dsinfo, log)
        
        expinfo = {}
        expinfo['PARENT-DATA-SET-CODES'] = info[self.DATASET_CODE]
        for key in ['COMMENT','TRAML','EXTRACTION_WINDOW','RT_EXTRACTION_WINDOW','MIN_UPPER_EDGE_DIST','MPR_NUM_XVAL','IRTTRAML','MIN_RSQ']:
            if key in info:
                expinfo[key] = info[key]
        expinfo[self.OUTPUT] = os.path.join(path,'experiment.properties')
        BasicInformationHandler().write_info(expinfo, log)
        
        return 0,info
        