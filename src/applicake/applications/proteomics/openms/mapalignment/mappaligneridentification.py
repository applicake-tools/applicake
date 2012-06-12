'''
Created on Jun 12, 2012

@author: quandtan
'''

import os
from applicake.applications.proteomics.base import OpenMs
from applicake.framework.templatehandler import BasicTemplateHandler

class MapAlignerIdentification(OpenMs):
    """
    Wrapper for OpenMS tools MapAlignerIdentification.
    """

    _input_file = ''
    _result_file = ''

    def __init__(self):
        """
        Constructor
        """
        base = self.__class__.__name__
        self._input_file = '%s.ini' % base # application specific config file
        self._result_file = '%s.result' % base # result produced by the application

    def _get_prefix(self,info,log):
        if not info.has_key(self.PREFIX):
            info[self.PREFIX] = 'MapAlignerIdentification'
            log.debug('set [%s] to [%s] because it was not set before.' % (self.PREFIX,info[self.PREFIX]))
        return info[self.PREFIX],info

    def get_template_handler(self):
        """
        See interface
        """
        return MapAlignerIdentificationTemplate()

    def prepare_run(self,info,log):
        """
        See interface.

        - Read the a specific template and replaces variables from the info object.
        - Tool is executed using the pattern: [PREFIX] -ini [TEMPLATE].
        - If there is a result file, it is added with a specific key to the info object.
        """
        wd = info[self.WORKDIR]
        log.debug('reset path of application files from current dir to work dir [%s]' % wd)
        self._input_file = os.path.join(wd,self._input_file)
        info['TEMPLATE'] = self._input_file
        self._result_file = os.path.join(wd,self._result_file)
        info[params] = self._result_file
        log.debug('get template handler')
        th = self.get_template_handler()
        log.debug('modify template')
        mod_template,info = th.modify_template(info, log)
        prefix,info = self._get_prefix(info,log)
        command = '%s -ini %s' % (prefix,self._input_file)
        return command,info

    def set_args(self,log,args_handler):
        """
        See interface
        """
        args_handler = super(MapAlignerIdentification, self).set_args(log,args_handler)
        #args_handler.add_app_args(log, '', '')
        return args_handler


class MapAlignerIdentificationTemplate(BasicTemplateHandler):
    """
    Template handler for MapAlignerIdentification.
    """

    def read_template(self, info, log):
        """
        See super class.
        """
        template = """<?xml version="1.0" encoding="ISO-8859-1"?>
<PARAMETERS version="1.3" xsi:noNamespaceSchemaLocation="http://open-ms.sourceforge.net/schemas/Param_1_3.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NODE name="MapAlignerIdentification" description="Corrects retention time distortions between maps based on common peptide identifications.">
    <ITEM name="version" value="1.9.0" type="string" description="Version of the tool that generated this parameters file." tags="advanced" />
    <NODE name="1" description="Instance &apos;1&apos; section for &apos;MapAlignerIdentification&apos;">
      <ITEMLIST name="in" type="string" description="Input files separated by blanks (all must have the same file type)" tags="input file,required" restrictions="*.featureXML,*.consensusXML,*.idXML">
      </ITEMLIST>
      <ITEMLIST name="out" type="string" description="Output files separated by blanks" tags="output file" restrictions="*.featureXML,*.consensusXML,*.idXML">
      </ITEMLIST>
      <ITEMLIST name="trafo_out" type="string" description="Transformation output files separated by blanks" tags="output file" restrictions="*.trafoXML">
      </ITEMLIST>
      <ITEM name="log" value="" type="string" description="Name of log file (created only when specified)" tags="advanced" />
      <ITEM name="debug" value="0" type="int" description="Sets the debug level" tags="advanced" />
      <ITEM name="threads" value="1" type="int" description="Sets the number of threads allowed to be used by the TOPP tool" />
      <ITEM name="no_progress" value="false" type="string" description="Disables progress logging to command line" tags="advanced" restrictions="true,false" />
      <ITEM name="test" value="false" type="string" description="Enables the test mode (needed for internal use only)" tags="advanced" restrictions="true,false" />
      <NODE name="reference" description="Options to define a reference file">
        <ITEM name="file" value="" type="string" description="File to use as reference" tags="input file" restrictions="*.featureXML,*.consensusXML,*.idXML" />
        <ITEM name="index" value="0" type="int" description="Use one of the input files as reference (&apos;1&apos; for the first file, etc.).#br#If &apos;0&apos;, no explicit reference is set - the algorithm will use an average of all inputs as reference." restrictions="0:" />
      </NODE>
      <NODE name="algorithm" description="Algorithm parameters section">
        <ITEM name="peptide_score_threshold" value="0" type="float" description="Score threshold for peptide hits to be used in the alignment.#br#Select a value that allows only &apos;high confidence&apos; matches." />
        <ITEM name="min_run_occur" value="2" type="int" description="Minimum number of runs (incl. reference, if any) a peptide must occur in to be used for the alignment.#br#Unless you have very few runs or identifications, increase this value to focus on more informative peptides." restrictions="2:" />
        <ITEM name="max_rt_shift" value="0.5" type="float" description="Maximum realistic RT difference for a peptide (median per run vs. reference). Peptides with higher shifts (outliers) are not used to compute the alignment.#br#If 0, no limit (disable filter); if &gt; 1, the final value in seconds; if &lt;= 1, taken as a fraction of the range of the reference RT scale." restrictions="0:" />
        <ITEM name="use_unassigned_peptides" value="true" type="string" description="Should unassigned peptide identifications be used when computing an alignment of feature maps? If &apos;false&apos;, only peptide IDs assigned to features will be used." restrictions="true,false" />
        <ITEM name="use_feature_rt" value="false" type="string" description="When aligning feature maps, don&apos;t use the retention time of a peptide identification directly; instead, use the retention time of the centroid of the feature (apex of the elution profile) that the peptide was matched to. If different identifications are matched to one feature, only the peptide closest to the centroid in RT is used.#br#Precludes &apos;use_unassigned_peptides&apos;." restrictions="true,false" />
      </NODE>
      <NODE name="model" description="Options to control the modeling of retention time transformations from data">
        <ITEM name="type" value="b_spline" type="string" description="Type of model" restrictions="linear,b_spline,interpolated" />
        <NODE name="linear" description="Parameters for &apos;linear&apos; model">
          <ITEM name="symmetric_regression" value="false" type="string" description="Perform linear regression on &apos;y - x&apos; vs. &apos;y + x&apos;, instead of on &apos;y&apos; vs. &apos;x&apos;." restrictions="true,false" />
        </NODE>
        <NODE name="b_spline" description="Parameters for &apos;b_spline&apos; model">
          <ITEM name="num_breakpoints" value="5" type="int" description="Number of breakpoints of the cubic spline in the smoothing step. More breakpoints mean less smoothing. Reduce this number if the transformation has an unexpected shape." restrictions="2:" />
          <ITEM name="break_positions" value="uniform" type="string" description="How to distribute the breakpoints on the retention time scale. &apos;uniform&apos;: intervals of equal size; &apos;quantiles&apos;: equal number of data points per interval." restrictions="uniform,quantiles" />
        </NODE>
        <NODE name="interpolated" description="Parameters for &apos;interpolated&apos; model">
          <ITEM name="interpolation_type" value="cspline" type="string" description="Type of interpolation to apply." restrictions="linear,cspline,akima" />
        </NODE>
      </NODE>
    </NODE>
  </NODE>
</PARAMETERS>
"""
        log.debug('read template from [%s]' % self.__class__.__name__)
        return template,info

class OrbiLessStrict(BasicTemplateHandler):
    """
    Template handler for MapAlignerIdentification.
    """

    def read_template(self, info, log):
        """
        See super class.
        """
        template = """<?xml version="1.0" encoding="ISO-8859-1"?>
<PARAMETERS version="1.3" xsi:noNamespaceSchemaLocation="http://open-ms.sourceforge.net/schemas/Param_1_3.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NODE name="MapAlignerIdentification" description="Corrects retention time distortions between maps based on common peptide identifications.">
    <ITEM name="version" value="1.9.0" type="string" description="Version of the tool that generated this parameters file." tags="advanced" />
    <NODE name="1" description="Instance &apos;1&apos; section for &apos;MapAlignerIdentification&apos;">
      <ITEMLIST name="in" type="string" description="Input files separated by blanks (all must have the same file type)" tags="input file,required" restrictions="*.featureXML,*.consensusXML,*.idXML">
      </ITEMLIST>
      <ITEMLIST name="out" type="string" description="Output files separated by blanks" tags="output file" restrictions="*.featureXML,*.consensusXML,*.idXML">
      </ITEMLIST>
      <ITEMLIST name="trafo_out" type="string" description="Transformation output files separated by blanks" tags="output file" restrictions="*.trafoXML">
      </ITEMLIST>
      <ITEM name="log" value="" type="string" description="Name of log file (created only when specified)" tags="advanced" />
      <ITEM name="debug" value="0" type="int" description="Sets the debug level" tags="advanced" />
      <ITEM name="threads" value="$THREADS" type="int" description="Sets the number of threads allowed to be used by the TOPP tool" />
      <ITEM name="no_progress" value="false" type="string" description="Disables progress logging to command line" tags="advanced" restrictions="true,false" />
      <ITEM name="test" value="false" type="string" description="Enables the test mode (needed for internal use only)" tags="advanced" restrictions="true,false" />
      <NODE name="reference" description="Options to define a reference file">
        <ITEM name="file" value="" type="string" description="File to use as reference" tags="input file" restrictions="*.featureXML,*.consensusXML,*.idXML" />
        <ITEM name="index" value="0" type="int" description="Use one of the input files as reference (&apos;1&apos; for the first file, etc.).#br#If &apos;0&apos;, no explicit reference is set - the algorithm will use an average of all inputs as reference." restrictions="0:" />
      </NODE>
      <NODE name="algorithm" description="Algorithm parameters section">
        <ITEM name="peptide_score_threshold" value="0" type="float" description="Score threshold for peptide hits to be used in the alignment.#br#Select a value that allows only &apos;high confidence&apos; matches." />
        <ITEM name="min_run_occur" value="2" type="int" description="Minimum number of runs (incl. reference, if any) a peptide must occur in to be used for the alignment.#br#Unless you have very few runs or identifications, increase this value to focus on more informative peptides." restrictions="2:" />
        <ITEM name="max_rt_shift" value="0.5" type="float" description="Maximum realistic RT difference for a peptide (median per run vs. reference). Peptides with higher shifts (outliers) are not used to compute the alignment.#br#If 0, no limit (disable filter); if &gt; 1, the final value in seconds; if &lt;= 1, taken as a fraction of the range of the reference RT scale." restrictions="0:" />
        <ITEM name="use_unassigned_peptides" value="true" type="string" description="Should unassigned peptide identifications be used when computing an alignment of feature maps? If &apos;false&apos;, only peptide IDs assigned to features will be used." restrictions="true,false" />
        <ITEM name="use_feature_rt" value="false" type="string" description="When aligning feature maps, don&apos;t use the retention time of a peptide identification directly; instead, use the retention time of the centroid of the feature (apex of the elution profile) that the peptide was matched to. If different identifications are matched to one feature, only the peptide closest to the centroid in RT is used.#br#Precludes &apos;use_unassigned_peptides&apos;." restrictions="true,false" />
      </NODE>
      <NODE name="model" description="Options to control the modeling of retention time transformations from data">
        <ITEM name="type" value="b_spline" type="string" description="Type of model" restrictions="linear,b_spline,interpolated" />
        <NODE name="linear" description="Parameters for &apos;linear&apos; model">
          <ITEM name="symmetric_regression" value="false" type="string" description="Perform linear regression on &apos;y - x&apos; vs. &apos;y + x&apos;, instead of on &apos;y&apos; vs. &apos;x&apos;." restrictions="true,false" />
        </NODE>
        <NODE name="b_spline" description="Parameters for &apos;b_spline&apos; model">
          <ITEM name="num_breakpoints" value="5" type="int" description="Number of breakpoints of the cubic spline in the smoothing step. More breakpoints mean less smoothing. Reduce this number if the transformation has an unexpected shape." restrictions="2:" />
          <ITEM name="break_positions" value="uniform" type="string" description="How to distribute the breakpoints on the retention time scale. &apos;uniform&apos;: intervals of equal size; &apos;quantiles&apos;: equal number of data points per interval." restrictions="uniform,quantiles" />
        </NODE>
        <NODE name="interpolated" description="Parameters for &apos;interpolated&apos; model">
          <ITEM name="interpolation_type" value="cspline" type="string" description="Type of interpolation to apply." restrictions="linear,cspline,akima" />
        </NODE>
      </NODE>
    </NODE>
  </NODE>
</PARAMETERS>
"""
        log.debug('read template from [%s]' % self.__class__.__name__)
        return template,info        
