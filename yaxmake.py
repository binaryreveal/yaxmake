#!/usr/bin/env python

############################################################################
# @author jIeZHaNG
# @contact binaryreveal@gmail.com
#
# @date 10/06/2012
#
# @history
#  10/04/2012 first draft version 0.1.0
#  10/06/2012 renew version
############################################################################

import os
import sys

from yaxlib import *

env = yenv.YaxEnvironment.create()

def main():
    """
    yaxmake main entry point
    """
    global env
    parser = ycl.YaxCommandLineParser()
    parser.parse(env)
    execfile(parser.getInputFile(), globals())

    for e in yenv.YaxEnvironment.env_list:
        e.make()

if __name__=='__main__':
    main()
