import builtins,weakref
from collections import deque
from warnings import warn
from pyobject import set_type_subclasses
try:import pydetour
except (ImportError, AttributeError):pydetour = None

__all__ = ["hack_class","hack_all_classes","init_build_class_hook",
           "init_type_hook","init"]

Py_TPFLAGS_HEAPTYPE = 1 << 9 # 来自object.h
Py_TPFLAGS_IMMUTABLETYPE = 1 << 8
NULL = 0 # 来自pyobject
_hacked_classes = weakref.WeakSet()
_refs = set()
IGNORED = () # (type,)

def get_cls_name(cls):
    return f"""{cls.__module__ + "." if cls.__module__  else ""}\
{cls.__qualname__}"""

def hack_class(cls):
    set_type_subclasses(cls,{})

def hack_all_classes(start = object, ignored = IGNORED):
    que = deque()
    que.append(start)
    while que:
        cls = que.popleft()
        _refs.add(cls)
        subcls_meth = getattr(cls,"__subclasses__",None)
        if subcls_meth not in (None,type.__subclasses__):
            for subcls in subcls_meth():
                que.append(subcls)

        if cls in ignored:continue
        #print("Hacking:",cls.__name__)
        hack_class(cls)

def init_build_class_hook():
    _internal_build_cls = builtins.__build_class__

    def __build_class__(func, name, *bases, metaclass=None, **kwds):
        if metaclass is None:
            result = _internal_build_cls(func, name, *bases, **kwds)
        else:
            result = _internal_build_cls(func, name, *bases, metaclass=metaclass,**kwds)

        for cls in result.__mro__:
            if cls is result:continue
            hack_class(cls)
            #assert cls.__subclasses__() == []
        return result

    builtins.__build_class__ = __build_class__

def init_type_hook():
    def _type(arg,bases=None,dct=None):
        nonlocal unhook_func
        if bases is None and dct is None:
            return arg.__class__
        else:
            unhook_func()
            result = type(arg,bases,dct)
            unhook_func = pydetour.hook(type, lambda hookee:_type)
            for cls in result.__mro__:
                if cls is result:continue
                hack_class(cls)
            return result
    def _type_new(type_,arg,bases=None,dct=None):
        if not isinstance(type_,type):
            raise TypeError(f"type.__new__: {type_} is not a subtype of type")
        return _type(arg,bases,dct)

    unhook_func = pydetour.hook(type, lambda hookee:_type)
    pydetour.hook(type.__new__, lambda hookee:_type_new)

def init():
    hack_all_classes()
    init_build_class_hook()
    if pydetour:
        try:init_type_hook()
        except Exception as err:
            warn(f"""Failed to initialize hooks for type() and type.__new__() \
with pydetour: {err} ({type(err).__name__})""")
    else:
        warn("Install pydetour to hook type() and type.__new__() for better effects")