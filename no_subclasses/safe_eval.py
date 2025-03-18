import builtins,warnings,copy,traceback
import no_subclasses

__all__ = ["safe_exec","safe_eval"]

DEFAULT_SCOPE = {"__builtins__": {}} # 默认命名空间，不包含任何内置函数

def safe_exec(code, globals_=None, locals_=None):
    if globals_ is None:
        globals_ = copy.deepcopy(DEFAULT_SCOPE)
    if locals_ is None:
        locals_ = copy.deepcopy(DEFAULT_SCOPE)
    builtins.exec(code, globals_, locals_)

def safe_eval(expr, globals_=None, locals_=None):
    if globals_ is None:
        globals_ = copy.deepcopy(DEFAULT_SCOPE)
    if locals_ is None:
        locals_ = copy.deepcopy(DEFAULT_SCOPE)
    return builtins.eval(expr, globals_, locals_)

def safe_eval_shell():
    no_subclasses.init()
    # 测试创建新类是否会修改__subclasses__()
    class A:pass
    A2 = type("A2",(object,),{})
    A3 = type.__new__(type,"A3",(object,),{})
    if object.__subclasses__():
        warnings.warn("Test failed, object.__subclasses__() is not empty")

    print("Safe eval shell")
    print("""Example: (1).__class__.__base__.__subclasses__() \
(equivalent to object.__subclasses__())""")
    while True:
        try:
            code = input(">>> ").strip()
        except EOFError:
            break
        if code:
            try:
                print(repr(safe_eval(code)))
            except BaseException:
                traceback.print_exc()

if __name__=="__main__":safe_eval_shell()