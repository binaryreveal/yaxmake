# yaxmake/yaxlib/yenv.py
# YaxEnvironment module

import os
import platform

import ymessage
import ytk
import ylang
import ynode
import ytarget
import ybuilder

class YaxEnvironment(ynode.YaxNode):
    """
    yaxmake environment class.
    """

    env_list = list()

    def __init__(self):
        ynode.YaxNode.__init__(self)
        self._do_init()

    def _do_init(self):
        self._toolkit = ytk.YaxToolkit.getDefaultToolkitValue()
        self._language = ylang.YaxLanguage.getDefaultLanguageValue()
        self._targets = list()
        self._debug_mode = False
        self._clean_mode = False
        self._verbose_mode = False

    @staticmethod
    def create():
        env = YaxEnvironment()
        YaxEnvironment.env_list.append(env)
        return env

    def clone(self):
        env = YaxEnvironment.create()
        env.setToolkit(self.getToolkit())
        env.setLanguage(self.getLanguage)
        env.copy(self)
        # env.addTargetList(self._targets)
        env.setDebugMode(self._debug_mode)
        env.setCleanMode(self._clean_mode)
        return env

    def _getToolkit(self):
        return self._toolkit

    def _setToolkit(self, toolkit):
        self._toolkit = toolkit

    def getToolkit(self):
        return self._getToolkit().getToolkit()

    def setToolkit(self, toolkit):
        self._setToolkit(ytk.YaxToolkit(toolkit))

    def _getLanguage(self):
        return self._language

    def _setLanguage(self, lang):
        self._language = lang

    def getLanguage(self):
        return self._getLanguage().getLanguage()

    def setLanguage(self, lang):
        self._setLanguage(ylang.YaxLanguage(lang))
        
    def getTargetList(self):
        return self._targets

    def addTargetList(self, targets):
        self._targets.extend(targets)

    def addTargets(self, *targets):
        self.addTargetList(targets)
        
    def getDebugMode(self):
        return self._debug_mode

    def setDebugMode(self, b):
        self._debug_mode = b

    def getCleanMode(self):
        return self._clean_mode

    def setCleanMode(self, b):
        self._clean_mode = b

    def getVerboseMode(self):
        return self._verbose_mode
        
    def setVerboseMode(self, b):
        self._verbose_mode = b
        
    def message(self, s):
        ymessage.message(s)

    def warning(self, s):
        ymessage.warning(s)

    def fatal(self, s):
        ymessage.fatal(s)

    def execute(self, cmd):
        return os.system(cmd)==0

    def captureExecute(self, cmd):
        chunks = list()
        pp = os.popen(cmd, 'r')
        while True:
            chunk = pp.read(0x1000)
            if not chunk:
                break
            chunks.append(chunk)
        pp.close()
        return ''.join(chunks)

    def getPlatform(self):
        return platform.system().upper()
        
    def captureExecuteFlatten(self, cmd):
        return ' '.join(self.captureExecute(cmd).split('\n'))

    def object(self, target, sources, cflags='', lflags='', prefix='', suffix='', defs=[], ipaths=[], lpaths=[], libs=[]):
        self._add_target('object', target, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs)

    def console_app(self, target, sources, cflags='', lflags='', prefix='', suffix='', defs=[], ipaths=[], lpaths=[], libs=[]):
        self._add_target('console_app', target, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs)

    def gui_app(self, target, sources, cflags='', lflags='', prefix='', suffix='', defs=[], ipaths=[], lpaths=[], libs=[]):
        self._add_target('gui_app', target, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs)

    def static_library(self, target, sources, cflags='', lflags='', prefix='', suffix='', defs=[], ipaths=[], lpaths=[], libs=[]):
        self._add_target('static_library', target, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs)

    def dynamic_library(self, target, sources, cflags='', lflags='', prefix='', suffix='', defs=[], ipaths=[], lpaths=[], libs=[]):
        self._add_target('dynamic_library', target, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs)
                
    def _add_target(self, target_type, target_name, sources, cflags, lflags, prefix, suffix, defs, ipaths, lpaths, libs):
        ymessage.vmessage(self, 'Add target %s: %s' % (target_type, target_name))
        target = ytarget.YaxTarget(target_type, target_name, sources)
        target.setCompileFlags(cflags)
        target.setLinkFlags(lflags)
        target.setPrefix(prefix)
        target.setSuffix(suffix)
        target.addDefinitionList(defs)
        target.addIncludePathList(ipaths)
        target.addLibraryPathList(lpaths)
        target.addLibraryList(libs)
        if target_type != 'object':
            target_definition = '_' + target_type.upper()
            if target_definition not in target.getDefinitionList():
                target.addDefinitions(target_definition)
        self.addTargets(target)
        
    def _addGlobalDefinitionList(self, defs):
        defs = map(lambda x: '_' + x, defs)
        for d in defs:
            if d not in self.getDefinitionList():
                self.addDefinitions(d)
                
    def make(self):
        ymessage.vmessage(self, 'Toolkit: %s' % self.getToolkit())
        builder = eval('ybuilder.%s_builder()' % self.getToolkit())
        self._addGlobalDefinitionList([self.getPlatform(), self.getToolkit().upper()])
        builder.build(self)
