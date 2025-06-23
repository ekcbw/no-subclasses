<span class="badge-placeholder">[![Stars](https://img.shields.io/github/stars/ekcbw/no-subclasses)](https://img.shields.io/github/stars/ekcbw/no-subclasses)</span>
<span class="badge-placeholder">[![GitHub release](https://img.shields.io/github/v/release/ekcbw/no-subclasses)](https://github.com/ekcbw/no-subclasses/releases/latest)</span>
<span class="badge-placeholder">[![License: MIT](https://img.shields.io/github/license/ekcbw/no-subclasses)](https://github.com/ekcbw/no-subclasses/blob/main/LICENSE)</span>

[English | [中文](README_zh.md)]

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