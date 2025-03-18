"""A library that removes the __subclasses__() list from all classes.\
一个清除所有类的__subclasses__()列表的库。"""
import sys
try:
    from no_subclasses.no_subclasses import *
    from no_subclasses.safe_eval import *
except ImportError:
    if "setup.py" not in sys.argv[0].lower():raise # 仅在setup.py导入本模块时，忽略错误

__version__ = "1.0.2"