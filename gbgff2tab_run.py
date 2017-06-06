#!/usr/bin/env python

import click
from os import path
from gbgff2tab import gff

@click.command()
@click.option("-infile", help="Input file", type=str, default=None,
              show_default=True)
@click.option("-infmt", help="Input file format", default="gff",
              type=click.Choice(["gff", "gb"]), show_default=True)
@click.option("-outfile", help="Output file", type=str, default=None,
              show_default=True)
@click.option("-sep", help="Field Seprator", type=str, default=",",
              show_default=True)
def run(infile, infmt, outfile, sep):
    if not infile:
        click.echo("Input file not given. Exiting ....")
        exit(1)
    if not path.isfile(infile):
        click.echo("%s doesn't exit. exiting ...." % infile)
        exit(1)
    if not outfile:
        click.echo("Output file not given. Exiting ....")
        exit(1)
    table, seq = gff.dataframe(infile)
    table.to_csv(outfile, index=False, sep=sep)

if  __name__ == '__main__':
    run()
