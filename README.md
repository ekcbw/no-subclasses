<span class="badge-placeholder">[![Stars](https://img.shields.io/github/stars/ekcbw/no-subclasses)](https://img.shields.io/github/stars/ekcbw/no-subclasses)</span>
<span class="badge-placeholder">[![GitHub release](https://img.shields.io/github/v/release/ekcbw/no-subclasses)](https://github.com/ekcbw/no-subclasses/releases/latest)</span>
<span class="badge-placeholder">[![License: MIT](https://img.shields.io/github/license/ekcbw/no-subclasses)](https://github.com/ekcbw/no-subclasses/blob/main/LICENSE)</span>

**The English documentation is placed below the Chinese version.**  

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

---

In Python, all classes have a largely useless `__subclasses__()` method. This implementation not only incurs some memory overhead but also makes the code less secure. Users can access any built-in functions and classes through `object.__subclasses__()`, which undermines the complete security of `exec` and `eval` functions.  
The `no-subclasses` library is designed to remove the `__subclasses__()` method from all classes, thereby reducing Python's memory overhead and achieving **almost complete security** for `exec` and `eval` functions, preventing all `__subclasses__` attacks within `exec` and `eval`.  

## Usage Example

By default, Python's `__subclasses__()` can include almost any class. After enabling the `no_subclasses` library, `__subclasses__()` will always return an empty list, even if new classes are defined.  
```python
>>> import no_subclasses
>>> len(object.__subclasses__()) # Without no_subclasses library
313
>>> object.__subclasses__()[:5]
[<class 'type'>, <class 'async_generator'>, <class 'bytearray_iterator'>, <class 'bytearray'>, <class 'bytes_iterator'>]
>>>
>>> no_subclasses.init() # Enable no_subclasses library
>>> object.__subclasses__()
[]
>>> int.__subclasses__()
[]
>>> type.__subclasses__(type)
[]
```
Additionally, the library provides secure `exec` and `eval` functions, which cannot call any built-in functions or classes, nor can they be exploited by calling any class's `__subclasses__()` method.  
```python
>>> from no_subclasses import init,safe_eval
>>>
>>> safe_scope = {"__builtins__":{}} # Cannot call any built-in functions
>>> attack_expr = "(1).__class__.__base__.__subclasses__()"
>>> eval(attack_expr,safe_scope) # eval before enabling no_subclasses
[<class 'type'>, <class 'async_generator'>, <class 'int'>,
<class 'bytearray_iterator'>, <class 'bytearray'>,
<class 'bytes_iterator'>, <class 'bytes'>,
<class 'PyCapsule'>,<class 'classmethod'>,...] # Contains many built-in functions, insecure
>>>
>>> init()
>>> safe_eval(attack_expr) # or eval(attack_expr,safe_scope)
[]
```
## Detailed Usage

- `hack_class(cls)`: Clears the `__subclasses__()` list of a class.
- `hack_all_classes(start = object, ignored=())`: Starting from a root class (default is `object`), clears the `__subclasses__` list of all subclasses. `ignored` is a list or tuple of classes to be ignored, default is empty.
<br></br>

- `init_build_class_hook()`: Modifies the built-in `__build_class__` function so that executing a `class` statement does not modify the `__subclasses__()` list again, eliminating the need to re-call `hack_class()`.
- `init_type_hook()`: Modifies the built-in `type()` and `type.__new__()` so that calling `type()` or `type.__new__()` does not modify the `__subclasses__()` list again, eliminating the need to re-call `hack_class()`. (Requires `pydetour` library)
- **`init()`**: Initializes the entire `no_subclasses` library, calling `hack_all_classes`, `init_build_class_hook`, and `init_type_hook` together. **（Recommended）**

## Implementation Principle

The `hack_class` method is implemented based on the lower-level `pyobject` library's `get_type_subclasses` and `set_type_subclasses` methods. The `hack_all_classes` method uses BFS to deeply search all subclasses and then calls `hack_class` on each class.