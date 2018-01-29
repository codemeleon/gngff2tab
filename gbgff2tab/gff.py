#!/usr/bin/env python
"""
This code is modification of
---------------------------
GTF.py
Kamil Slowikowski
December 24, 2013

Read GFF/GTF files. Works with gzip compressed files and pandas.

    http://useast.ensembl.org/info/website/upload/gff.html

LICENSE

This is free and unencumbered software released into the public domain.
Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""
# Add information to remove comments

import gzip
import re
from collections import defaultdict
from os import path

import click
import pandas as pd
from Bio import Seq, SeqIO

GTF_HEADER = [
    'seqname', 'source', 'feature', 'start', 'end', 'score', 'strand', 'frame'
]
R_SEMICOLON = re.compile(r'\s*;\s*')
R_COMMA = re.compile(r'\s*,\s*')
R_KEYVALUE = re.compile(r'(\s+|\s*=\s*)')


def _get_value(value):
    if not value:
        return None

    # Strip double and single quotes.
    value = value.strip('"\'')

    # Return a list if the value has a comma.
    if ',' in value:
        value = re.split(R_COMMA, value)
    # These values are equivalent to None.
    elif value in ['', '.', 'NA']:
        return None

    return value


def parse(line):
    """Parse a single GTF line and return a dict.
    """
    result = {}

    fields = line.rstrip().split('\t')

    for i, col in enumerate(GTF_HEADER):
        result[col] = _get_value(fields[i])

    # INFO field consists of "key1=value;key2=value;...".
    infos = [x for x in re.split(R_SEMICOLON, fields[8]) if x.strip()]

    for i, info in enumerate(infos, 1):
        # It should be key="value".
        try:
            key, _, value = re.split(R_KEYVALUE, info, 1)
        # But sometimes it is just "value".
        except ValueError:
            key = 'INFO{}'.format(i)
            value = info
        # Ignore the field if there is no value.
        if value:
            result[key] = _get_value(value)
    return result


def lines(filename):
    """Open an optionally gzipped GTF file and generate a dict for each line.
    """
    fn_open = gzip.open if filename.endswith('.gz') else open
    seq_bool = False
    sequences = ""
    res_dicts = []
    with fn_open(filename) as fh:
        for line in fh:
            if "##FASTA" in line:
                seq_bool = True
                continue
                # break
            elif line.startswith('#'):
                continue
            elif seq_bool:
                sequences += line

            else:
                # yield parse(line)
                res_dicts.append(parse(line))
    sequences = sequences.split(">")[1:]
    seq_dict = {}
    for sequence in sequences:
        sequence_split = sequence.split("\n")
        seq = ''.join(sequence_split[1:])
        seq_dict[sequence_split[0]] = seq
    del sequences
    return res_dicts, seq_dict


def dataframe(filename):
    """Open an optionally gzipped GTF file and return a pandas.DataFrame.
    """
    # Each column is a list stored as a value in this dict.
    result = defaultdict(list)
    info, sequences = lines(filename)
    for i, line in enumerate(info):
        for key in line.keys():
            # This key has not been seen yet, so set it to None for all
            # previous lines.
            if key not in result:
                result[key] = [None] * i

        # Ensure this row has some value for each column.
        for key in result.keys():
            result[key].append(line.get(key, None))
    # print(pd.DataFrame(result))
    return pd.DataFrame(result), sequences


def toaa(table, seq):
    table = table[table['feature'] == "CDS"]
    table["start"] = pd.to_numeric(table["start"])  # list(map())
    table["end"] = pd.to_numeric(table["end"])
    for k in seq:
        seq[k] = Seq.Seq(seq[k])

    aa_dict = {}
    for i, row in table[["ID", "seqname", "start", "end",
                         "strand"]].iterrows():
        seqt = seq[row["seqname"]][row['start'] - 1:row["end"]]
        if row["strand"] == "-":
            seqt = seqt.reverse_complement()
        translates = str(seqt.translate()[:-1])
        aa_dict[row["ID"]] = translates
    return aa_dict

    #
    #
    # @click.command()
    # @click.option("-gtf", help="gtf/gff/gtf.gz/gff.gz input file", type=str,
    #               default=None, show_default=True)
    # @click.option("-csv", help="csv outputfile", type=str, default=None,
    #               show_default=True)
    # @click.option("-sep", help="Column separator", type=str, default="\t",
    #               show_default=True)
    # def run(gtf, csv, sep):
    #     """gtf/gff/gtf.gz/gff.gz to csv."""
    #     if not gtf:
    #         click.echo("Input file not given. Exiting ....")
    #         exit(1)
    #     if not path.isfile(gtf):
    #         click.echo("Given file doesn't exists. Exiting ....")
    #         exit()
    #     if not csv:
    #         click.echo("Ouput csv path not given. Exiting ...")
    #         exit(1)
    #     dtf = dataframe(gtf)
    #     # dtf.to_csv(csv, index=False, sep=sep)
    #
    #
    # if __name__ == '__main__':
    #     run()
