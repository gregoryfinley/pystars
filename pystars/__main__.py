#!/usr/bin/env python

import sys
# import argparse

import pystars

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    pystars.run()

if __name__ == '__main__':
    main()
