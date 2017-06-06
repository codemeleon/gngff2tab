#!/usr/bin/env python

from setuptools import setup

setup(name="gbgff2tab",
      version="0.0.1",
      description="Converts gff and genbank file to table",
      author="anmol M. Kiran",
      author_email="anmol@liv.ac.uk",
      url="https://github.com/codemeleon/gngff2tab.git",
      install_requires=['click',
                        'pandas',
                        'biopython'],
      license="GPLv3",
      script="gbgff2tab.py",
      packages=["gbgff2tab"],
      zip_safe=False
     )
