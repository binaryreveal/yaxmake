# yaxmake/yaxlib/ytk.py

import ymessage

class YaxToolkit:
    """
    yaxmake toolkit class
    """

    toolkits = ('gnu', 'msvc')

    def __init__(self, toolkit):
        if toolkit not in YaxToolkit.toolkits:
            ymessage.fatal('Invalid toolkit: %s' % toolkit)
        self._toolkit = toolkit

    def getToolkit(self):
        return self._toolkit

    @staticmethod
    def getDefaultToolkitValue():
        return YaxToolkit.toolkits[0]
