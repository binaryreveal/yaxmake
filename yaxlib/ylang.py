# yaxmake/yaxlib/ylang.py

import ymessage

class YaxLanguage:
    """
    yaxmake language class
    """

    languages = ('c', 'c++')
    
    def __init__(self, lang):
        if lang not in YaxLanguage.languages:
            ymessage.fatal('Invalid language: %s' % lang)
        self._language = lang

    def getLanguage(self):
        return self._language

    @staticmethod
    def getDefaultLanguageValue():
        return YaxLanguage.languages[0]
