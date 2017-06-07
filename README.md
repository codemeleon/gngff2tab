# gbgff2tab
Converting Genbank and GFF file to pandas table to file.

# Installation
*Note*: _User might need to be a root_
## Suggested
> pip install git+https://github.com/codemeleon/gngff2tab.git

## Alternative
1. git clone https://github.com/codemeleon/gngff2tab.git
2. cd gngff2tab
3. python setup.py install

If the installation fails, please contact your system administrator. If you discover any bugs, please let us know by emailing anmol@liv.ac.uk

# Usage

## Stand alone
gbgff2tab_run --help

## Module
>>from gbgff2tab import gff
>>table, seq = gff.dataframe('gfffile')

*table*: pandas table
*saquences*: sequences dict for squences in gff file
