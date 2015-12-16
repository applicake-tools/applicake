#!/usr/bin/env python
# -*- coding: utf-8  -*-

from __future__ import print_function

import sys
import os.path
import csv

from pyteomics import pepxml

def iprophetpepxml2csv(infile, outfile):
    # outfile = os.path.splitext(infile)[0] + '.csv'
    reader = pepxml.read(infile)
    f = open(outfile, 'wb')
    writer = csv.writer(f, delimiter='\t')

    # modifications_example = [{'position': 20, 'mass': 160.0306}]

    header_set = False

    result = {}
    for hit in reader:
        if not 'search_hit' in hit:
            continue
        #result = hit
        result['retention_time_sec'] = hit['retention_time_sec']
        result['assumed_charge'] = hit['assumed_charge']
        result['spectrum'] = hit['spectrum']
        result['nrhit'] = len(hit['search_hit'])
        search_hit = hit['search_hit'][0]

        result['modified_peptide'] = search_hit['modified_peptide']
        result['peptide'] = search_hit['peptide']
        analysis_result = search_hit['analysis_result'][1]
        iprophet_probability = analysis_result['interprophet_result'][ 'probability']
        result['iprophet_probability'] = iprophet_probability
        result['protein_id']= search_hit['proteins'][0]['protein']
        result['nrproteins'] = len(search_hit['proteins'])
        if not header_set:
            writer.writerow(result.keys())
            header_set = True
        writer.writerow(result.values())
    f.close()

if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = os.path.splitext(infile)[0] + '.tab'
    iprophetpepxml2csv(infile, outfile)


## MYRIMATCH
{
    'end_scan': 1380,
    'retention_time_sec': 5190.16999999998,
    'index': 160,
    'assumed_charge': 2,
    'spectrum': '5P_HDMSE_121214_20.1380.1380.2',
    'search_hit': [
        {
            'hit_rank': 1,
            'calc_neutral_pep_mass': 3123.6467143833,
            'modifications': [],
            'modified_peptide': 'GKFDFSGNLDLEAFVLMAAEIGLWVILR',
            'peptide': 'GKFDFSGNLDLEAFVLMAAEIGLWVILR',
            'massdiff': 0.05699714826,
            'search_score': {
                'mvh': 12.1394600401,
                'number of matched peaks': 4.0,
                'xcorr': 0.9391081889259687,
                'number of unmatched peaks': 51.0,
                'mzFidelity': 10.015543238385
            },
            'proteins': [
                {
                    'num_tol_term': 2,
                    'protein': 'sp|Q8IW92|GLBL2_HUMAN',
                    'peptide_next_aa': 'P',
                    'protein_descr': None,
                    'peptide_prev_aa': 'R',
                },
                {
                    'protein': 'sp|Q8NCI6|GLBL3_HUMAN'
                }
            ],
            'num_missed_cleavages': 1,
            'tot_num_ions': 55,
            'num_tot_proteins': 2,
            'num_matched_ions': 4
        }
    ],
    'precursor_neutral_mass': 3123.58971723504,
    'num_decoy_comparisons': '0',
    'start_scan': 1380,
    'num_target_comparisons': '936',
    'spectrumNativeID': 'controllerType=0 controllerNumber=1 scan=1380'
}


## X!Tandem

{'end_scan': 113,
 'retention_time_sec': 963.599,
 'index': 367,
 'assumed_charge': 2,
 'spectrum': '5P_HDMSE_121214_20.00113.00113.2',
 'search_hit':
     [{
         'hit_rank': 1,
         'calc_neutral_pep_mass': 3139.3787,
         'modifications': [{'position': 20, 'mass': 160.0306}],
         'modified_peptide': 'STDVDAVPYTGADSTQGTWCEDEPVGARR',
         'peptide': 'STDVDAVPYTGADSTQGTWCEDEPVGARR',
         'num_matched_ions': 1,
         'search_score': {
             'zscore': 0.0,
             'xscore': 0.0,
             'bscore': 1.0,
             'yscore': 0.0,
             'cscore': 0.0,
             'hyperscore': 229.0,
             'ascore': 0.0,
             'expect': 53.0,
             'nextscore': 277.0},
         'proteins': [{
             'num_tol_term': 2,
             'protein': 'DECOY_Q49AJ0',
             'peptide_next_aa': 'V',
             'protein_descr': None,
             'peptide_prev_aa': 'K'}],
         'num_missed_cleavages': 0,
         'tot_num_ions': 56,
         'num_tot_proteins': 1,
         'is_rejected': False,
         'massdiff': -0.03}],
 'precursor_neutral_mass': 3139.349,
 'start_scan': 113}

## OMSSA
{
    'end_scan': 1380,
    'index': 92,
    'assumed_charge': 2,
    'spectrum': '5P_HDMSE_121214_20.01380.01380.2',
    'search_hit': [{
        'hit_rank': 1,
        'calc_neutral_pep_mass': 3125.59204101562,
        'modifications': [],
        'modified_peptide':
            'DQALSISAMEELPRVLYLPLFMEAFSR',
        'peptide': 'DQALSISAMEELPRVLYLPLFMEAFSR',
        'num_matched_ions': 2,
        'search_score': {
            'pvalue': 129.44166834226553,
            'expect': 3883.250050267966},
        'proteins': [{
            'num_tol_term': 0,
            'protein': 'O95521',
            'peptide_next_aa': 'R',
            'protein_descr': 'PRAME family member 1 OS=Homo sapiens GN=PRAMEF1 PE=2 SV=2',
            'peptide_prev_aa': 'R'}],
        'tot_num_ions': 52,
        'num_tot_proteins': 1,
        'is_rejected': False,
        'massdiff': 0.014892578125}],
    'precursor_neutral_mass': 3125.60693359375,
    'start_scan': 1380}

{
    'end_scan': 1380,
    'index': 92,
    'assumed_charge': 2,
    'spectrum': '5P_HDMSE_121214_20.01380.01380.2',
    'search_hit': [{
        'hit_rank': 1,
        'calc_neutral_pep_mass': 3125.59204101562,
        'modifications': [],
        'modified_peptide':
            'DQALSISAMEELPRVLYLPLFMEAFSR',
        'peptide': 'DQALSISAMEELPRVLYLPLFMEAFSR',
        'num_matched_ions': 2,
        'search_score': {
            'pvalue': 129.44166834226553,
            'expect': 3883.250050267966},
        'proteins': [{
            'num_tol_term': 0,
            'protein': 'O95521',
            'peptide_next_aa': 'R',
            'protein_descr': 'PRAME family member 1 OS=Homo sapiens GN=PRAMEF1 PE=2 SV=2',
            'peptide_prev_aa': 'R'}],
        'tot_num_ions': 52,
        'num_tot_proteins': 1,
        'is_rejected': False,
        'massdiff': 0.014892578125}],
    'precursor_neutral_mass': 3125.60693359375,
    'start_scan': 1380
}
