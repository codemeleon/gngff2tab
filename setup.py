#!/usr/bin/env python

from setuptools import setup

setup(name="gbgff2tab_run",
      version="0.0.1",
      description="Converts gff and genbank file to table",
      author="anmol M. Kiran",
      author_email="anmol@liv.ac.uk",
      url="https://github.com/codemeleon/gngff2tab",
      install_requires=['click',
                        'pandas',
                        'biopython'],
      license="GPLv3",
      scripts=["bin/gbgff2tab_run"],
      packages=["gbgff2tab"],
      zip_safe=False
     )
