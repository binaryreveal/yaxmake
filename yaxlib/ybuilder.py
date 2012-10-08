# yaxmake/yaxlib/ybuilder.py

import os

import ymessage
import ytarget

class base_builder:
    def __init__(self):
        self._templates = dict()
        self._template_handler_table = dict()
        self._object_extension_name = ''

    def _get_name_with_ext(self, filename, ext):
        names = os.path.splitext(filename)
        if names[1].lower()==ext:
            return None
        return '.'.join([names[0], ext])

    def _get_template_item(self, x, target):
        if x in self._template_handler_table.keys():
            return self._template_handler_table[x](self._env, target)
        return x

    def _expand_template(self, target_name, target):
        cmdq = list()
        q = self._templates[target.getType()].split(' ')
        for x in q:
            if x == '$(SOURCE)':
                s = ' '.join(target.getSources())
            elif x == '$(TARGET)':
                s = target_name
            elif x == '/Fo$(TARGET)':
                s = '/Fo' + target_name
            elif x == '/OUT:$(TARGET)':
                s = '/OUT:' + target_name
            elif x == '$(IMPLIB)':
                lib_name = self._get_name_with_ext(target_name, 'lib')
                if not lib_name:
                    lib_name = target_name
                s = '/IMPLIB:' + lib_name
            elif x == '$(CFLAGS)':
                s = ' '.join([self._env.getCompileFlags(), target.getCompileFlags()])
            elif x == '$(LFLAGS)':
                s = ' '.join([self._env.getLinkFlags(), target.getLinkFlags()])
            else:
                s = self._get_template_item(x, target)

            if s:
                cmdq.append(s)
        return ' '.join(cmdq)

    def _safe_remove(self, filename):
        if os.path.exists(filename):
            ymessage.message('Delete file: %s' % filename)
            os.unlink(filename)

    def _execute_template(self, target):
        target_name = target.getTargetFullName(self._env.getToolkit())
        if target.getType() != 'object':
            (filepath, filename) = os.path.split(target_name)
            if filepath and (not os.path.exists(filepath)):
                os.mkdir(filepath)
            (name, ext) = os.path.splitext(filename)
            name = self._env.getPrefix() + target.getPrefix() + name + target.getSuffix() + self._env.getSuffix()
            filename = ''.join([name, ext])
            target_name = os.path.join(filepath, filename)
            
        # clean mode
        if self._env.getCleanMode():
            self._safe_remove(target_name)
            return

        # build mode
        if os.path.isfile(target_name):
            need_update = False
            target_mtime = os.path.getmtime(target_name)
            for source in target.getSources():
                if os.path.getmtime(source) >= target_mtime:
                    need_update = True
                    break
            if not need_update:
                ymessage.message('Target %s is up to date.' % target_name)
                return

        cmd_line = self._expand_template(target_name, target)
        ymessage.message(cmd_line)
        if not self._env.execute(cmd_line):
            ymessage.fatal('Failed to execute command!')

    def _build_target(self, target):
        objects = list()
        for source in target.getSources():
            obj_name = self._get_name_with_ext(source, self._object_extension_name)
            if not obj_name:
                obj_name = source
            else:
                obj_target = ytarget.YaxTarget('object', obj_name, [source])
                obj_target.copy(target)
                self._execute_template(obj_target)
                
            objects.append(obj_name)

        if target.getType()!='object':
            new_target = ytarget.YaxTarget(target.getType(), target.getName(), objects)
            new_target.copy(target)
            self._execute_template(new_target)

    def _get_action(self):
        if self._env.getCleanMode():
            return 'Clean'
        return 'Build'
        
    def build(self, env):
        self._env = env
        targets = env.getTargetList()
        for target in targets:
            ymessage.vmessage(env, '%s target %s: %s' % (self._get_action(), target.getType(), target.getName()))
            self._build_target(target)            

def _super_join(array, prefix):
    return ' '.join(map(lambda x: prefix+x, array))

def _unique_list(array):
    return list(set(array))

#def _real_path(array):
#    return map(lambda x: os.path.realpath(x), array)
    
##############################################################################
# gnu builder and helper procedures
##############################################################################

def gnu_get_cc(env, target):
    cc = 'gcc'
    if env.getLanguage()=='c++':
        cc = 'g++'
    return cc

def gnu_get_ar(env, target):
    return 'ar'

def gnu_get_config(env, target):
    if env.getDebugMode():
        return '-g'
    return '-O2'

def gnu_get_defs(env, target):
    defs = _super_join(_unique_list(env.getDefinitionList() + target.getDefinitionList()), '-D')
    return defs

def gnu_get_ipaths(env, target):
    ipaths = _super_join(_unique_list(env.getIncludePathList() + target.getIncludePathList()), '-I')
    return ipaths
    
def gnu_get_lpaths(env, target):
    lpaths = _super_join(_unique_list(env.getLibraryPathList() + target.getLibraryPathList()), '-L')
    return lpaths

def gnu_get_libs(env, target):
    libs = _super_join(_unique_list(env.getLibraryList() + target.getLibraryList()), '-l')
    return libs

class gnu_builder(base_builder):
    def __init__(self):
        self._templates = {
            'object' : '$(CC) $(CONFIG) $(CFLAGS) $(DEFS) $(IPATHS) -c -o $(TARGET) $(SOURCE)',
            'static_library' : '$(AR) rcs $(TARGET) $(SOURCE)',
            'dynamic_library' : '$(CC) $(LFLAGS) $(LPATHS) $(LIBS) -fPIC -shared -o $(TARGET) $(SOURCE)',
            'console_app' : '$(CC) -o $(TARGET) $(SOURCE) $(LFLAGS) $(LPATHS) $(LIBS)',
            'gui_app' : '$(CC) -mwindows -o $(TARGET) $(SOURCE) $(LFLAGS) $(LPATHS) $(LIBS)',
        }

        self._template_handler_table = {
            '$(CC)' : gnu_get_cc,
            '$(AR)' : gnu_get_ar,
            '$(CONFIG)' : gnu_get_config,
            '$(DEFS)' : gnu_get_defs,
            '$(IPATHS)' : gnu_get_ipaths,
            '$(LPATHS)' : gnu_get_lpaths,
            '$(LIBS)' : gnu_get_libs,
        }

        self._object_extension_name = 'o'

##############################################################################
# msvc builder and helper procedures
##############################################################################

def msvc_get_cc(env, target):
    return 'cl'

def msvc_get_ar(env, target):
    return 'lib'

def msvc_get_config(env, target):
    if env.getDebugMode():
        return '/Od'
    return '/O2'

def msvc_get_link(env, target):
    return 'link'

def msvc_get_defs(env, target):
    defs = _super_join(_unique_list(env.getDefinitionList() + target.getDefinitionList()), '/D')
    return defs

def msvc_get_ipaths(env, target):
    ipaths = _super_join(_unique_list(env.getIncludePathList() + target.getIncludePathList()), '/I')
    return ipaths

def msvc_get_lpaths(env, target):
    lpaths = _super_join(_unique_list(env.getLibraryPathList() + target.getLibraryPathList()), '/LIBPATH:')
    return lpaths

def _make_sure_lib(s):
    filename = s
    names = os.path.splitext(s)
    if not names[1]:
        filename = '.'.join([names[0], 'lib'])
    return filename

def msvc_get_libs(env, target):
    libs = ' '.join(map(_make_sure_lib, env.getLibraryList() + target.getLibraryList()))
    return libs

class msvc_builder(base_builder):
    def __init__(self):
        self._templates = {
            'object' : '$(CC) /nologo $(CONFIG) $(CFLAGS) $(DEFS) $(IPATHS) /Fo$(TARGET) /c $(SOURCE)',
            'static_library' : '$(AR) /nologo /OUT:$(TARGET) $(SOURCE)',
            'dynamic_library' : '$(LINK) /nologo $(LFLAGS) $(LPATHS) $(LIBS) $(IMPLIB) /DLL /OUT:$(TARGET) $(SOURCE)',
            'console_app' : '$(LINK) /nologo /SUBSYSTEM:CONSOLE $(LFLAGS) $(LPATHS) /OUT:$(TARGET) $(SOURCE) $(LIBS)',
            'gui_app' : '$(LINK) /nologo /SUBSYSTEM:WINDOWS $(LFLAGS) $(LPATHS) /OUT:$(TARGET) $(SOURCE) $(LIBS)',
        }

        self._template_handler_table = {
            '$(CC)' : msvc_get_cc,
            '$(AR)' : msvc_get_ar,
            '$(CONFIG)' : msvc_get_config,
            '$(LINK)' : msvc_get_link,
            '$(DEFS)' : msvc_get_defs,
            '$(IPATHS)' : msvc_get_ipaths,
            '$(LPATHS)' : msvc_get_lpaths,
            '$(LIBS)' : msvc_get_libs,
        }

        self._object_extension_name = 'obj'

