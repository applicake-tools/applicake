'''
Created on Mar 20, 2012

@author: quandtan
'''

import itertools
from applicake.framework.confighandler import ConfigHandler
from applicake.framework.interfaces import IApplication
from applicake.utils.sequenceutils import SequenceUtils
from applicake.utils.dictutils import DictUtils
from applicake.framework.informationhandler import BasicInformationHandler


class Generator(IApplication):
    """   
    A basic Generator creates all possible value combinations from the input file if it contains keys with multiple values.
    The results are stored in files which are named in dependency input file name and the pattern accepted 
    by the applied worklfow manager.
    """
    
    def write_files(self,info,log,dicts,idx_sep='_'): 
        """
        Generates ini files from a list of dictionaries
        
        @type info: dict 
        @param info: Dictionary with information about the application. The created output files are added to the key [%s]
        @type dicts: list
        @type dicts: List of dictionaries used to create ini files
        """ % self.COPY_TO_WD
             
        for idx,dic in enumerate(dicts):
            path = "%s%s%s" % (dic[self.GENERATOR],idx_sep,idx) 
            log.debug(path)          
            dic[self.OUTPUT] = path
            BasicInformationHandler().write_info(dic, log)
            log.debug('create file [%s]' % path)
            info[self.COPY_TO_WD].append(path)

class DatasetcodeGenerator(Generator):
    """
    Generator that rely on the existence of a specific dataset-code key that is retrieved from an OpenBIS instance.
    
    The generator splits the input file by the all possible parameter combinations and then by all defined dataset-codes.
    """


    def main(self,info,log):
        """
        Generate the cartesian product of all values from info and writes them to files. 
        
        There is a distinction between dataset codes and parameters. For every parameter combination
        a new key [%s] is added. Dataset combinations are indexed using another key [%s]. 
        
        @precondition: 'info' object has to contain key [%s]
        @type info: see super class
        @param info: see super class
        @type log: see super class
        @param log: see super class 
        """ % (self.PARAM_IDX,self.DATASET_CODE,self.DATASET_CODE)
        
        # prepare a basedic to produced input files for inner workflow
        log.debug('create work copy of "info"')   
        basedic = info.copy()        
        #check if value DATASE_CODE is defined as list
        dsc = basedic[self.DATASET_CODE]
        if not isinstance(dsc,list):
            log.fatal('found value of [%s] not to be a list [%s]' % (self.DATASET_CODE,dsc))
            return(1,info) 
        log.debug('need to remove some keys from the work copy for a "clean" start ;-)')
        remove_keys = [self.COPY_TO_WD,self.NAME]        
        for key in remove_keys:
            try:
                del basedic[key]
                log.debug('removed key [%s] from work copy' % key)
            except:
                log.debug('work copy did not have key [%s]' % key)            
        # prepare first the product of a parameter combinations
        escape_keys = [self.DATASET_CODE]
        param_dicts = DictUtils.get_product_dicts(basedic, log, escape_keys,idx_key=self.PARAM_IDX)
        log.debug('param_dicts: [%s]' % param_dicts)
        log.debug('created [%s] dictionaries based on parameter combinations' % len(param_dicts))
        # prepare combinations based on files
        param_file_dicts = []
        escape_keys = []
        for dic in  param_dicts:            
            file_dicts = DictUtils.get_product_dicts(dic, log, escape_keys,idx_key=self.FILE_IDX)
            param_file_dicts.extend(file_dicts)
        log.debug('created [%s] dictionaries based on parameter and file combinations' % len(param_file_dicts))
        # write ini files
        self.write_files(info,log,param_file_dicts)
        return (0,info)   
    
    def set_args(self,log,args_handler):
        """
        See interface
        """        
        args_handler.add_app_args(log, self.GENERATOR, 'Base name for generating output files (such as for a parameter sweep)',action='append')
        args_handler.add_app_args(log, self.DATASET_CODE, 'Dataset code from OpenBIS)')
        args_handler.add_app_args(log, self.COPY_TO_WD, 'Files which are created by this application', action='append')       
        return args_handler       
        
#class PgradeDatasetcodeGenerator(DatasetcodeGenerator):
#    """
#    Dataset-code generator for the P-Grade workflow manager.
#    
#    It creates output files of the format [INPUTFILENAME].[INDEX]
#    """
#    
#    def write_files(self,info,log,dicts): 
#        """
#        see super class
#        """       
#        super(PgradeDatasetcodeGenerator,self).write_files(info,log,dicts,idx_sep='.')
        
class ParametersetGenerator(Generator):
    """
    Generator that runs after a collector to split the information by the parameter sets.
    """

    def main(self,info,log):
        """
        Generate the cartesian product of all values from info and writes them to files. 
        
        There is a distinction between dataset codes and parameters. For every parameter combination
        a new key [%s] is added. Dataset combinations are indexed using another key [%s]. 
        
        @precondition: 'info' object has to contain key [%s]
        @type info: see super class
        @param info: see super class
        @type log: see super class
        @param log: see super class 
        """ 
        
        if not isinstance(info[self.PARAM_IDX],list):
            log.error('value [%s] of key [%s] was no list' % (self.PARAM_IDX, info[self.PARAM_IDX]))
            return 1,info
        remove_keys = [self.INPUT,self.FILE_IDX,self.PRINT_LOG]
#        remove_keys = BasicInformationHandler().remove_keys
#        remove_keys.append(self.FILE_IDX) 
        basedic = DictUtils.extract(info, remove_keys, include=False)
        param_dicts = []
        if len(SequenceUtils.unify(basedic[self.PARAM_IDX], reduce = True)) ==1:                        
            for key in info.keys():
                if isinstance(basedic[key], list):
                    basedic[key] = SequenceUtils.unify(info[key], reduce = True)
            param_dicts.append(basedic)            
        else:
            param_dict = {}
            keys = basedic.keys()
            param_idxs = basedic[self.PARAM_IDX]
            # loops of unique list of found parameter idices
            for param_idx in SequenceUtils.unify(param_idxs):
                # gets the positions in the value list of the key
                log.debug('process parameter index [%s]' % param_idx)
                positions = SequenceUtils.get_indices(param_idxs, lambda x: x ==param_idx)
                log.debug('found it at positions [%s] in original array [%s]' % (positions,basedic[self.PARAM_IDX]))
                # extracts for every key of the info object the values that match these positions
                # and writes them into a new dictionary
                log.debug('start splitting values for every key in info object')
                for key in keys:
                    value = basedic[key]   
                    log.debug('value [%s] for key [%s]' % (value,key)) 
                    if not isinstance(value, list):
                        log.info('found value is not a list')
                        param_dict[key] = value
                    else:                
                        param_dict[key] = [value[pos] for pos in positions]
                param_dicts.append(param_dict)    
        # write ini files
        self.write_files(info,log,param_dicts)
        return (0,info)           
            
    
    def set_args(self,log,args_handler):
        """
        See interface
        """        
        args_handler.add_app_args(log, self.GENERATOR, 'Base name for generating output files (such as for a parameter sweep)',action='append')
        args_handler.add_app_args(log, self.COPY_TO_WD, 'Files which are created by this application', action='append')       
        return args_handler     