# yaxmake/yaxlib/ytarget.py

import os
import platform

import ymessage
import ynode

class YaxTarget(ynode.YaxNode):

    target_types = ('object', 'console_app', 'gui_app', 'static_library', 'dynamic_library')

    def __init__(self, target_type, target_name, target_sources):
        ynode.YaxNode.__init__(self)
        if target_type not in YaxTarget.target_types:
            ymessage.fatal('Invalid target type: %s' % target_type)
        self._type = target_type
        self._name = target_name
        self._sources = target_sources

    def getType(self):
        return self._type

    def getName(self):
        return self._name

    def getSources(self):
        return self._sources
    
    def _get_new_name_with_ext(self, filename, ext):
        new_name = filename
        names = os.path.splitext(filename)
        if not names[1]:
            new_name = '.'.join([names[0], ext])
        return new_name

    def getTargetFullName(self, toolkit):
        (filepath, filename) = os.path.split(self._name)
        
        if toolkit == 'msvc':
            ext_name = None
            if self._type.endswith('_app'):
                ext_name = 'exe'
            elif self._type == 'static_library':
                ext_name = 'lib'
            elif self._type == 'dynamic_library':
                ext_name = 'dll'
                
            if ext_name:
                filename = self._get_new_name_with_ext(filename, ext_name)

        elif toolkit == 'gnu':
            os_system = platform.system().upper()
            if (self._type.endswith('_app')) and (os_system=='WINDOWS'):
                filename = self._get_new_name_with_ext(filename, 'exe')
            elif self._type == 'static_library':
                filename = 'lib' + self._get_new_name_with_ext(filename, 'a')
            elif self._type == 'dynamic_library':
                dll_ext = 'so'
                if os_system == 'WINDOWS':
                    dll_ext = 'dll'
                filename = 'lib' + self._get_new_name_with_ext(filename, dll_ext)
        else:
            ymessage.fatal('Error at YaxTarget.getTargetFullName() with toolkit: %s' % toolkit)

        return os.path.join(filepath, filename)
