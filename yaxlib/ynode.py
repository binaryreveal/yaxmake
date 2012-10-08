# yaxmake/yaxlib/ynode.py

class YaxNode:
    def __init__(self):
        self._cflags = ''
        self._lflags = ''
        self._ipaths = list()
        self._lpaths = list()
        self._defs = list()
        self._libs = list()
        self._prefix = ''
        self._suffix = ''
    
    def copy(self, node):
        self.setCompileFlags(node.getCompileFlags())
        self.setLinkFlags(node.getLinkFlags())
        self.addIncludePathList(node.getIncludePathList())
        self.addLibraryPathList(node.getLibraryPathList())
        self.addDefinitionList(node.getDefinitionList())
        self.addLibraryList(node.getLibraryList())
        self.setPrefix(node.getPrefix())
        self.setSuffix(node.getSuffix())

    def getCompileFlags(self):
        return self._cflags

    def setCompileFlags(self, flags):
        self._cflags = flags

    def addCompileFlags(self, flags):
        self._cflags += flags

    def getLinkFlags(self):
        return self._lflags

    def setLinkFlags(self, flags):
        self._lflags = flags

    def addLinkFlags(self, flags):
        self._lflags += flags

    def _unique_list(self, l):
        return list(set(l))

    def getIncludePathList(self):
        return self._unique_list(self._ipaths)

    def addIncludePathList(self, paths):
        self._ipaths.extend(paths)

    def addIncludePaths(self, *paths):
        self.addIncludePathList(paths)

    def getLibraryPathList(self):
        return self._unique_list(self._lpaths)

    def addLibraryPathList(self, paths):
        self._lpaths.extend(paths)

    def addLibraryPaths(self, *paths):
        self.addLibraryPathList(paths)

    def getDefinitionList(self):
        return self._unique_list(self._defs)

    def addDefinitionList(self, defs):
        self._defs.extend(defs)

    def addDefinitions(self, *defs):
        self.addDefinitionList(defs)

    def getLibraryList(self):
        return self._unique_list(self._libs)

    def addLibraryList(self, libs):
        self._libs.extend(libs)

    def addLibraries(self, *libs):
        self.addLibraryList(libs)

    def getPrefix(self):
        return self._prefix

    def setPrefix(self, prefix):
        self._prefix = prefix

    def getSuffix(self):
        return self._suffix

    def setSuffix(self, suffix):
        self._suffix = suffix
