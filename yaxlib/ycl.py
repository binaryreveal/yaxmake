# yaxmake/yaxlib/ycl.py

import os
import sys

import ytk
import yver
import ylang
import ymessage

class YaxCommandLineParser:

    DEFAULT_INPUT_FILE_NAME = "yaxfile.py"

    def __init__(self):
        self._cmd = os.path.basename(sys.argv[0])
        self._args = sys.argv[1:]
        self._initialize()

    def _initialize(self):
        self._inputFile = YaxCommandLineParser.DEFAULT_INPUT_FILE_NAME
        self._toolkit = ytk.YaxToolkit.getDefaultToolkitValue()
        self._language = ylang.YaxLanguage.getDefaultLanguageValue()
        self._debug_mode = False
        self._clean_mode = False
        self._verbose_mode = False

    def _getOptionArgumentValue(self, arg, templ):
        optarg = self._getOptionArgument(arg)
        if optarg not in templ.keys():
            ymessage.fatal('Invalid argument: %s\n', arg)
        return templ[optarg]

    def _getOptionArgument(self, arg):
        items = arg.split('=', 1)
        if len(items)<2:
            ymessage.fatal('Option "%s" requires an argument' % arg)
        return items[1].strip()

    def _version(self):
        print "Yaxmake version %d.%d.%d" % (yver.yax_version[0], yver.yax_version[1], yver.yax_version[2])
        sys.exit(0)

    def _usage(self):
        print "Yaxmake is yet another cross make tool, written by jIeZHaNG."
        print "usage: %s <options>" % self._cmd
        print
        print "  options:"
        print "    -t or --toolkit=<toolkit>   : gnu or msvc, default is gnu"
        print "    -l or --language=<language> : c or c++, default is c"
        print "    -f or --file=<input file>   : default is 'yaxfile.py'"
        print "    -d or --debug               : debug mode on (not support yet)"
        print "    -c or --clean               : clean generated target files"
        print "    -V or --verbose             : verbose mode"
        print "    -v or --version             : version info"
        print "    -h or --help                : show this help info"
        print

        sys.exit(0)

    def parse(self, env):
        for arg in self._args:
            if arg.startswith("-t") or arg.startswith("--toolkit"):
                self._toolkit = self._getOptionArgument(arg)
            elif arg.startswith("-l") or arg.startswith("--language"):
                self._language = self._getOptionArgument(arg)
            elif arg.startswith("-f") or arg.startswith("--file"):
                self._inputFile = self._getOptionArgument(arg)
            elif arg in ('-d', '--debug'):
                self._debug_mode = True
            elif arg in ('-c', '--clean'):
                self._clean_mode = True
            elif arg in ('-V', '--verbose'):
                self._verbose_mode = True
            elif arg in ('-v', '--version'):
                self._version()
            elif arg in ('-h', '--help'):
                self._usage()
            else:
                print 'Invalid argument %s!\nTry -h or --help to view help info.' % arg
                sys.exit(-1)

        env.setLanguage(self._language)
        env.setToolkit(self._toolkit)
        env.setDebugMode(self._debug_mode)
        env.setCleanMode(self._clean_mode)
        env.setVerboseMode(self._verbose_mode)
        
        if not os.path.isfile(self._inputFile):
            ymessage.fatal("Missing input file!")

    def getInputFile(self):
        return self._inputFile

