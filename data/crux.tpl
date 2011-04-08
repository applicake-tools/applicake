fragment-mass=mono
isotopic-mass=average
precursor-window-type=$PRECMASSUNIT
precursor-window=$PRECMASSERR
mass-precision=4
custom-enzyme=__NULL_STR
C=57.021464
mz-bin-width=1.000508
version=FALSE
min-length=6
digestion=full-digest
overwrite=TRUE
parameter-file=__NULL_STR
min-peaks=20
xcorr-var-bin=FALSE
max-rank-preliminary=500
max-mods=4
spectrum-charge=all
print-search-progress=1000
use-mstoolkit=TRUE
fileroot=__NULL_STR
compute-sp=FALSE
verbosity=30
mz-bin-offset=0.680000
display-summed-mod-masses=TRUE
peptide-list=FALSE
print-theoretical-spectrum=FALSE
num-decoys-per-target=0
scan-number=__NULL_STR
max-aas-modified=255
reverse-sequence=FALSE
missed-cleavages=FALSE
search-decoy-pvalue-file=search.decoy.p.txt
spectrum-min-mass=0.000000
output-dir=crux-output
max-length=50
max-ion-charge=peptide
max-mass=7200.000000
min-mass=200.000000
precision=8
decoy-location=target-file
enzyme=trypsin
compute-p-values=FALSE
top-match=3
spectrum-max-mass=1000000000.000000
mod=NO MODS
nmod=NO MODS
cmod=NO MODS




#####################################################################
# Sample parameter file
#
# Lines starting with '#' will be ignored.  Don't leave any space
# before or after a parameter setting.  The format is
#
# <parameter-name>=<value>
#
#####################################################################

# Which isotopes to use in calculating fragment ion mass.
# <string>=average|mono. Default=mono.
# Parameter file only.  Used by crux-search-for-matches and
# crux-predict-peptide-ions.
#fragment-mass=mono

# Print to stdout additional information about the spectrum.
# Avaliable only for crux-get-ms2-spectrum.  Does not affect contents of
# the output file.
#stats=FALSE

# Minimum number of points for estimating the Weibull parameters. 
# Default=4000.
# Available for crux search-for-xlinks
#min-weibull-points=4000

# Predict the given number of isotope peaks (0|1|2). Default=0.
# Only available for crux-predict-peptide-ion.  Automatically set to 0
# for Sp scoring and 1 for xcorr scoring.
#isotope=0

# Sort peptides according to which property (mass, length, lexical,
# none).  Default=none.
# Only available for crux-generate-peptides.
#sort=none

# Window type to use for selecting decoy peptides from precursor mz.
# <string>=mass|mz|ppm. Default=mass.
# Available for crux search-for-matches
#precursor-window-type-decoy=mass

# The ion series to predict (b,y,by). Default='by' (both b and y ions).
# Only available for crux-predict-peptide-ions.  Set automatically to
# 'by' for searching.
#primary-ions=by

# Predict neutral loss ions (none, h20, nh3, all). Default='all'.
# Only available for crux-predict-peptide-ions. Set to 'all' for sp and
# xcorr scoring.
#neutral-losses=all

# Which isotopes to use in calcuating peptide mass.
# <string>=average|mono. Default=average.
# Used from command line or parameter file by crux-create-index and
# crux-generate-peptides.  Parameter file only for
# crux-search-for-matches.
#isotopic-mass=average

# Include self-loop peptides in the database.  Default=T.
# Available for crux search-for-xlinks program.
#xlink-include-selfloops=TRUE

# Window type to use for selecting candidate peptides. 
# <string>=mass|mz|ppm. Default=mass.
# Available for search-for-matches, search-for-xlinks.
#precursor-window-type=ppm
#precursor-window-type=mass

# Search peptides within +/- 'precursor-window' of the spectrum mass. 
# Definition of precursor window depends upon precursor-window-type.
# Default=3.0.
# Available from the parameter file only for crux-search-for-matches,
# crux-create-index, and crux-generate-peptides.
#precursor-window=15
#precursor-window=15
#precursor-window=3.000000

# Set the precision for masses and m/z written to sqt and .txt files. 
# Default=4
# Available from parameter file for all commands.
#mass-precision=4

# Specify rules for in silico digestion of proteins. See HTML
# documentation for syntax. Default is trypsin.
# Overrides the enzyme option.  Two lists of residues are given enclosed
# in square brackets or curly braces and separated by a |. The first
# list contains residues required/prohibited before the cleavage site
# and the second list is residues after the cleavage site.  If the
# residues are required for digestion, they are in square brackets, '['
# and ']'.  If the residues prevent digestion, then they are enclosed in
# curly braces, '{' and '}'.  Use X to indicate all residues.  For
# example, trypsin cuts after R or K but not before P which is
# represented as [RK]|{P}.  AspN cuts after any residue but only before
# D which is represented as [X]|[D].
#custom-enzyme=__NULL_STR

# Predict flanking peaks for b and y ions (T,F). Default=F.
# Only available for crux-predict-peptide-ion.
#flanking=FALSE

# Change the mass of all amino acids 'A' by the given amount.
# For parameter file only.  Default=no mass change.
#A=0.000000

# Change the mass of all amino acids 'C' by the given amount.
# For parameter file only.  Default=+57.0214637206.
#C=57.021464

# Change the mass of all amino acids 'D' by the given amount.
# For parameter file only.  Default=no mass change.
#D=0.000000

# Change the mass of all amino acids 'E' by the given amount.
# For parameter file only.  Default=no mass change.
#E=0.000000

# Specify the width of the bins used to discretize the m/z axis.  Also
# used as tolerance for assigning ions.  Default=1.0005079 for
# monoisotopic mass or 1.0011413 for average mass.
# Available for crux-search-for-matches and xlink-assign-ions.
#mz-bin-width=1.000508

# Change the mass of all amino acids 'F' by the given amount.
# For parameter file only.  Default=no mass change.
#F=0.000000

# Change the mass of all amino acids 'G' by the given amount.
# For parameter file only.  Default=no mass change.
#G=0.000000

# Change the mass of all amino acids 'H' by the given amount.
# For parameter file only.  Default=no mass change.
#H=0.000000

# Change the mass of all amino acids 'I' by the given amount.
# For parameter file only.  Default=no mass change.
#I=0.000000

# Change the mass of all amino acids 'K' by the given amount.
# For parameter file only.  Default=no mass change.
#K=0.000000

# Change the mass of all amino acids 'L' by the given amount.
# For parameter file only.  Default=no mass change.
#L=0.000000

# Change the mass of all amino acids 'M' by the given amount.
# For parameter file only.  Default=no mass change.
#M=0.000000

# Change the mass of all amino acids 'N' by the given amount.
# For parameter file only.  Default=no mass change.
#N=0.000000

# Change the mass of all amino acids 'P' by the given amount.
# For parameter file only.  Default=no mass change.
#P=0.000000

# Change the mass of all amino acids 'Q' by the given amount.
# For parameter file only.  Default=no mass change.
#Q=0.000000

# Change the mass of all amino acids 'R' by the given amount.
# For parameter file only.  Default=no mass change.
#R=0.000000

# Change the mass of all amino acids 'S' by the given amount.
# For parameter file only.  Default=no mass change.
#S=0.000000

# Change the mass of all amino acids 'T' by the given amount.
# For parameter file only.  Default=no mass change.
#T=0.000000

# Change the mass of all amino acids 'V' by the given amount.
# For parameter file only.  Default=no mass change.
#V=0.000000

# Change the mass of all amino acids 'W' by the given amount.
# For parameter file only.  Default=no mass change.
#W=0.000000

# Change the mass of all amino acids 'Y' by the given amount.
# For parameter file only.  Default=no mass change.
#Y=0.000000

# Print version number and quit.
# Available for all crux programs.  On command line use '--version T'.
#version=FALSE

# The minimum length of peptides to consider. Default=6.
# Used from the command line or parameter file by crux-create-index and
# crux-generate-peptides.  Parameter file only for
# crux-search-for-matches.
#min-length=6

# Predict the precursor ions, and all associated ions (neutral-losses,
# multiple charge states) consistent with the other specified options.
# (T,F) Default=F.
# Only available for crux-predict-peptide-ions.
#precursor-ions=FALSE

# Degree of digestion used to generate peptides.
# <string>=full-digest|partial-digest. Either both ends or one end of a
# peptide must conform to enzyme specificity rules. Default=full-digest.
# Used in conjunction with enzyme option when enzyme is not set to to
# 'no-enzyme'.  Available from command line or parameter file for
# crux-generate-peptides and crux create-index.  Available from
# parameter file for crux search-for-matches.  Digestion rules are as
# follows: enzyme name [cuts after one of these residues][but not before
# one of these residues].  trypsin [RK][P], elastase [ALIV][P],
# chymotrypsin [FWY][P].
#digestion=full-digest

# Replace existing files (T) or exit if attempting to overwrite (F).
# Default=F.
# Available for all crux programs.  Applies to parameter file as well as
# index, search, and analysis output files.
#overwrite=TRUE

# Set additional options with values in the given file.
# Available for all crux programs. Any options specified on the command
# line will override values in the parameter file.
#parameter-file=__NULL_STR

# The minimum number of peaks a spectrum must have for it to be
# searched. Default=20.
# Parameter file only for search-for-matches and sequest-search.
#min-peaks=20

# Predict peaks with the given maximum number of nh3 neutral loss
# modifications. Default=0.
# Only available for crux-predict-peptide-ions.
#nh3=0

# Use variable binning for XCORR.  If set to true, mz-bin-width, and
# mz-bin-offset parameters are utilized
# Available for crux-search-for-matches.
#xcorr-var-bin=FALSE

# Number of psms per spectrum to score with xcorr after preliminary
# scoring with Sp. Set to 0 to score all psms with xcorr. Default=500.
# Used by crux-search-for-matches.  For positive values, the Sp
# (preliminary) score acts as a filter; only high scoring psms go on to
# be scored with xcorr.  This saves some time.  If set to 0, all psms
# are scored with both scores. 
#max-rank-preliminary=500

# The maximum number of modifications that can be applied to a single
# peptide.  Default=no limit.
# Available from parameter file for crux-search-for-matches.
#max-mods=8

# Spectrum charge states to search. <string>=1|2|3|all. Default=all.
# Used by crux-search-for-matches to limit the charge states considered
# in the search.  With 'all' every spectrum will be searched and spectra
# with multiple charge states will be searched once at each charge
# state.  With 1, 2 ,or 3 only spectra with that that charge will be
# searched.
#spectrum-charge=all

# Show search progress by printing every n spectra searched. 
# Default=10.
# Set to 0 to show no search progress.  Available for crux
# search-for-matches from parameter file.
#print-search-progress=10

# Use MSToolkit to parse spectra. Default=F.
# Available for crux-search-for-matches
#use-mstoolkit=TRUE

# The estimated percent of target scores that are drawn from the null
# distribution.
# Used by compute-q-values, percolator and q-ranker
#pi-zero=1.000000

# Prefix added to output file names. Default=none. 
# Used by crux search-for-matches, crux sequest-search, crux percolator
# crux compute-q-values, and crux q-ranker.
#fileroot=__NULL_STR

# Turn off cross-validation to select hyperparameters.
# Available for q-ranker.
#no-xval=FALSE

# Compute the Sp score for all candidate peptides.  Default=F
# Available for search-for-matches.  Sp scoring is always done for
# sequest-search.
#compute-sp=FALSE

# Set level of output to stderr (0-100).  Default=30.
# Available for all crux programs.  Each level prints the following
# messages, including all those at lower verbosity levels: 0-fatal
# errors, 10-non-fatal errors, 20-warnings, 30-information on the
# progress of execution, 40-more progress information, 50-debug info,
# 60-detailed debug info.
#verbosity=30

# Specify the location of the left edge of the first bin used to
# discretize the m/z axis. Default=0.68
# Available for crux-search-for-matches.
#mz-bin-offset=0.680000

# When a residue has multiple modifications, print the sum of those
# modifications rather than listing each in a comma-separated list. 
# Default=T.
# Available in the parameter file for any command that prints peptides
# sequences.  Example: TRUE is SE[12.40]Q and FALSE is SE[10.00,2.40]Q
#display-summed-mod-masses=TRUE

# Create an ASCII version of the peptide list.  Default=F.
# Creates an ASCII file in the output directory containing one peptide
# per line.
#peptide-list=FALSE

# Print the theoretical spectrum
# Available for xlink-predict-peptide-ions (Default=F).
#print-theoretical-spectrum=FALSE

# Use MGF file format for parsing files
# Available for search-for-xlinks program (Default=F).
#use-mgf=FALSE

# Number of decoy peptides to search for every target peptide searched.
# Default=2.
# Use --decoy-location to control where they are returned (which
# file(s)).  Available only from the command line for
# search-for-matches. 
#num-decoys-per-target=0

# Search only select spectra specified as a single scan number or as a
# range as in x-y.  Default=search all.
# The search range x-y is inclusive of x and y.
#scan-number=__NULL_STR

# The maximum number of modified amino acids that can appear in one
# peptide.  Each aa can be modified multiple times.  Default=no limit.
# Available from parameter file for search-for-matches.
#max-aas-modified=255

# Generate decoys by reversing the peptide string rather than shuffling.
# Default=F.
# The first and last residues of the sequence are not changed.  If the
# reversed decoy sequence is the same as the target then the decoy is
# generated by shuffling.
#reverse-sequence=FALSE

# Include peptides with missed cleavage sites. Default=F.
# Available from command line or parameter file for crux-create-index
# and crux-generate-peptides.  Parameter file only for
# crux-search-for-matches.  When used with
# enzyme=<trypsin|elastase|chymotrpysin>  includes peptides containing
# one or more potential cleavage sites.
#missed-cleavages=FALSE

# Output filename for complete list of decoy p-values. 
# Default='search.decoy.p.txt'
# Only available for crux search-for-matches. The location of this file
# is controlled by --output-dir.
#search-decoy-pvalue-file=search.decoy.p.txt

# Search decoy-peptides within +/-  'mass-window-decoy' of the spectrum
# mass.  Default=20.0.
# Available for crux search-for-xlinks. 
#precursor-window-decoy=20.000000

# Minimum mass of spectra to be searched. Default=0.
# Available for crux-search-for-matches.
#spectrum-min-mass=0.000000

# Folder to which results will be written. Default='crux-output'.
# Used by crux create-index, crux search-for-matches, crux
# compute-q-values, and crux percolator.
#output-dir=crux-output

# Include dead-end peptides in the database.  Default=T.
# Available for crux search-for-xlinks program.
#xlink-include-deadends=TRUE

# The maximum length of peptides to consider. Default=50.
# Available from command line or parameter file for crux-create-index 
# and crux-generate-peptides. Parameter file only for
# crux-search-for-matches.
#max-length=50

# Generate peptides only once, even if they appear in more than one
# protein (T,F).  Default=F.
# Available from command line or parameter file for
# crux-genereate-peptides. Returns one line per peptide when true or one
# line per peptide per protein occurence when false.  
#unique-peptides=TRUE

# Predict ions up to max charge state (1,2,...,6) or up to the charge
# state of the peptide (peptide).  If the max-ion-charge is greater than
# the charge state of the peptide, then the max is the peptide charge.
# Default='peptide'.
# Available for predict-peptide-ions and search-for-xlinks. Set to
# 'peptide' for search.
#max-ion-charge=peptide

# The maximum mass of peptides to consider. Default=7200.
# Available from command line or parameter file for crux-create-index
# and crux-generate-peptides. Parameter file only for
# crux-search-for-matches.
#max-mass=7200.000000

# The minimum mass of peptides to consider. Default=200.
# Available from command line or parameter file for crux-create-index
# and crux-generate-peptides. Parameter file only for
# crux-search-for-matches.
#min-mass=200.000000

# Set the precision for scores written to sqt and text files. Default=8.
# Available from parameter file for crux search-for-matches, percolator,
# and compute-q-values.
#precision=8

# Specify location of decoy search results.
# <string>=target-file|one-decoy-file|separate-decoy-files.
# Default=separate-decoy-files.
# Applies when num-decoys-per-target > 0.  Use 'target-file' to mix
# target and decoy search results in one file. 'one-decoy-file' will
# return target results in one file and all decoys in another.
# 'separate-decoy-files' will create as many decoy files as
# num-decoys-per-target.
#decoy-location=target-file

# Optional file into which psm features are printed. Default=F.
# Available for percolator and q-ranker.  File will be named
# <fileroot>.percolator.features.txt or <fileroot>.qranker.features.txt.
#feature-file=FALSE

# Enzyme to use for in silico digestion of proteins.
# <string>=trypsin|chymotrypsin|elastase|clostripain|
# cyanogen-bromide|iodosobenzoate|proline-endopeptidase|
# staph-protease|aspn|modified-chymotrypsin|no-enzyme. Default=trypsin.
# Used in conjunction with the options digestion and missed-cleavages.
# Use 'no-enzyme' for non-specific digestion.  Available from command
# line or parameter file for crux-generate-peptides and crux
# create-index.  Available from parameter file for crux
# search-for-matches.   Digestion rules: enzyme name [cuts after one of
# these residues]|{but not before one of these residues}.  trypsin
# [RK]|{P}, elastase [ALIV]|{P}, chymotrypsin [FWY]|{P}, clostripain
# [R]|[], cyanogen-bromide [M]|[], iodosobenzoate [W]|[],
# proline-endopeptidase [P]|[], staph-protease [E]|[],
# modified-chymotrypsin [FWYL]|{P}, elastase-trypsin-chymotrypsin
# [ALIVKRWFY]|{P},aspn []|[D] (cuts before D).
#enzyme=trypsin

# Use flank peaks in xcorr theoretical spectrum
# Available for crux search-for-xlinks program (Default=T).
#xcorr-use-flanks=TRUE

# Predict peaks with the given maximum number of h2o neutral loss
# modifications. Default=0.
# Only available for crux-predict-peptide-ions.
#h2o=0

# Compute p-values for the main score type. Default=F.
# Currently only implemented for XCORR.
#compute-p-values=FALSE

# The number of PSMs per spectrum writen to the output  file(s). 
# Default=5.
# Available from parameter file for crux-search-for-matches.
#top-match=5

# Maximum mass of spectra to search. Default no maximum.
# Available for crux-search-for-matches.
#spectrum-max-mass=1000000000.000000

# Include linear peptides in the database.  Default=T.
# Available for crux search-for-xlinks program (Default=T).
#xlink-include-linears=TRUE

# Print peptide sequence (T,F). Default=F.
# Available only for crux-generate-peptides.
#output-sequence=FALSE

# Specify a variable modification to apply to peptides.  <mass
# change>:<aa list>:<max per peptide>:<prevents cleavage>:<prevents
# cross-link>.  Sub-parameters prevents cleavage and prevents cross-link
# are optional (T|F).Default=no mods.
# Available from parameter file for crux-generate-peptides and
# crux-search-for-matches and the the same must be used for crux
# compute-q-value.
#mod=NO MODS

# Specify a variable modification to apply to N-terminus of peptides. 
# <mass change>:<max distance from protein n-term (-1 for no max)>
# Available from parameter file for crux-generate-peptides and
# crux-search-for-matches and the the same must be used for crux
# compute-q-value.
#nmod=NO MODS

# Specify a variable modification to apply to C-terminus of peptides.
# <mass change>:<max distance from protein c-term (-1 for no max)>.
# Default=no mods.
# Available from parameter file for crux-generate-peptides and
# crux-search-for-matches and the the same must be used for crux
# compute-q-value.
#cmod=NO MODS

