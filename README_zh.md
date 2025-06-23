[[English](README.md) | 中文]

在Python中，所有类都有一个基本无用的`__subclasses__()`方法，这个实现不仅有一定内存开销，还使得代码变得不再安全，用户可以通过`object.__subclasses__()`访问任何内置函数和类，使得彻底安全的`exec`、`eval`函数不复存在。  
`no-subclasses`库是一个清除所有类的`__subclasses__()`列表的库，既减小了Python的内存开销，也实现了几乎**彻底安全**的`exec`和`eval`函数，阻止了`exec`和`eval`中的所有`__subclasses__`攻击。  

## 使用示例

Python的`__subclasses__()`默认几乎可以包含任何的类。启用`no_subclasses`库后，`__subclasses__()`总是会返回空列表，即使定义了新的类，也不例外。  
```python
>>> import no_subclasses
>>> len(object.__subclasses__()) # 不启用no_subclasses库时
313
>>> object.__subclasses__()[:5]
[<class 'type'>, <class 'async_generator'>, <class 'bytearray_iterator'>, <class 'bytearray'>, <class 'bytes_iterator'>]
>>>
>>> no_subclasses.init() # 启用no_subclasses库
>>> object.__subclasses__()
[]
>>> int.__subclasses__()
[]
>>> type.__subclasses__(type)
[]
```
另外，库提供了安全的`exec`和`eval`函数，函数中不能调用任何内置函数和类，也不能通过调用任何类的`__subclasses__()`实现攻击。  
```python
>>> from no_subclasses import init,safe_eval
>>>
>>> safe_scope = {"__builtins__":{}} # 不能调用任何内置函数
>>> attack_expr = "(1).__class__.__base__.__subclasses__()"
>>> eval(attack_expr,safe_scope) # 启用no_subclasses之前的eval
[<class 'type'>, <class 'async_generator'>, <class 'int'>,
<class 'bytearray_iterator'>, <class 'bytearray'>,
<class 'bytes_iterator'>, <class 'bytes'>,
<class 'PyCapsule'>,<class 'classmethod'>,...] # 包含大量的内置函数，不安全
>>>
>>> init()
>>> safe_eval(attack_expr) # 或eval(attack_expr,safe_scope)
[]
```
## 详细用法

- `hack_class(cls)`: 清除一个类的`__subclasses__()`列表。
- `hack_all_classes(start = object, ignored=())`: 从一个根类（默认为`object`)开始，清除所有子类的`__subclasses__`列表。`ignored`为一个列表或元组，表示要忽略的类，默认为空。
<br></br>

- `init_build_class_hook()`: 修改内置的`__build_class__`函数，使得执行`class`语句时不会再次修改`__subclasses__()`列表，不需要重新调用`hack_class()`。
- `init_type_hook()`: 修改内置的`type()`和`type.__new__()`，使得调用`type()`乃至`type.__new__()`时不会再次修改`__subclasses__()`，不需要重新调用`hack_class()`。(需要`pydetour`库)
- **`init()`**: 初始化整个`no_subclasses`库，一并调用`hack_all_classes`、`init_build_class_hook`和`init_type_hook`。**（推荐使用）**

## 实现原理

`hack_class`方法基于更底层的`pyobject`库的`get_type_subclasses`和`set_type_subclasses`方法实现，
而`hack_all_classes`通过用BFS深入查找子类，再对每个类调用`hack_class`实现。
