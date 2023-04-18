#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "FSBMSE#11HCM Team 03"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import logging
from app import *

def main(args):
    """ Main entry point of the app """
    logging.info("********* Start App ***************")
    run()


if __name__ == "__main__":
    """ This is executed when run from the command line """

    main(None)