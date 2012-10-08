# yaxmake/yaxlib/ymessage.py

import sys

class YaxException(Exception):
    def __init__(self, value):
        self._value = value
    def __str__(self):
        return repr(self._value)

def vmessage(env, s):
    if env.getVerboseMode():
        print '[*]', s
    
def message(s):
    print '[*]', s

def warning(s):
    print '[!]', s

def fatal(s):
    print '[x]', s
    raise YaxException('Error')
#    sys.exit(-1)

    
