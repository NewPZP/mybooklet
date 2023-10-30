[PEP 484 -- Type Hints](https://www.python.org/dev/peps/pep-0484/) 
## Abstract 摘要
- pep 3107 介绍了函数类型声明（function annotation），但没有定义语义。现在已经有很多第三方关于静态类型分析的用法会从中受益
- 这个模块介绍了一个临时的模块，这个模块在类型声明不可用的情况下提供一些标准的定义和工具，和一些约定
- 它没有一个强制的规定，用或不用类型约束，只是为了更好的协作，就像pep333中对web framework的一些约定
- 下面这个例子，它对参数和返回值做了类型约束，这些约束在运行时可以通过`__annotations__`属性得到，约束不会在运行时候发生，是否进行约束全凭编程人员的意愿，由强大的linter工具实现。
```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```
- 这个提案，受到了 [mypy](http://mypy-lang.org/).的启发，如`Sequence[int]` 是一个自定义类型的Sequence类型，从纯python模块 typing 倒入，如果在metaclass中实现了`__getitem__()`,这个`Sequence[int]` 的约束就有效
- 类型系统还支持 unions ， generic types，一个特殊类型Any，这些新的特性的想法来自渐进类型， 渐进类型 和 全类型系统 在 PEP483 中有解释
- 其他我们借鉴的方法或比较参照的方法 我们在PEP482 中有说明
## 原理和目标
- PEP 3107添加了对函数定义 类型约束的支持， [implicit goal to use them for type hinting](https://www.artima.com/weblogs/viewpost.jsp?thread=85551) 罗列了在PEP中描述的可能用法
- PEP的目标是提供一个标准的 类型约束的语法，让python 代码更容易做静态分析，重构，运行时类型检查，代码生成
- 最重要的是提供让工具做静态分析，如mypy，还有可以让IDE做重构或代码提示
### 非目标
- python仍然是动态语言，作者没有想把类型约束作为强制性的命令或公约

## 类型约束的意义
- 没有类型约束的函数应视为最通用的类型，或忽略类型，有这个`@no_type_check` 修饰的函数被视为没有类型约束
- 函数的返回 和所有参数建议都有类型的约束，默认的类型约束是Any，除了类方法和实例方法的第一个参数
- 类型检查 检查函数体和所给的类型注解的一致性，还有校验调用时的正确性
- 类型检查器期望得到尽可能多的信息，最小的需要是要处理内建的装饰器 `@property`, `@staticmethod` and `@classmethod`.
## 类型定义语法
- 语法使用了 [PEP 3107](https://peps.python.org/pep-3107 "PEP 3107 – Function Annotations")-style，还有一些扩展，在下面的章节描述，最基础的形式如下
	- 参数的类型是str， 函数返回的类型是str, 
	- 指定参数类型的字类型也是可以被这个参数类型接受的
```python
def greeting(name: str) -> str:
    return 'Hello ' + name
```

### 可接受的类型约束
- 类型约束可以是 内建 类型，抽象基类，types 模块的类型，和用户自定义的类型
- 注解是实现类型约束最好的形式， 有时候使用 comment 或在一个别的stub 文件更适合
- 注解必须是 可行的表达式，在函数定义的时候不能抛出异常
- 注解必须是简单的，否则解释器无法解释它，例如注解不能是计算出来的动态类型，
- 另外，下面这些特殊的构造会很有用，`None`, `Any`, `Union`, `Tuple`, `Callable`，所有的 ABCs模块里的，typing导出的如Sequence Dict 和其他一些别名

### 使用None
- 使用 None 和 type(None) 约束类型是等效的
### 类型别名

```python
Url = str

def retry(url: Url, retry_count: int) -> None: ...
```
- 建议类型别名第一个大写
- 下面两段代码等价
```python
from typing import TypeVar, Iterable, Tuple

T = TypeVar('T', int, float, complex)
Vector = Iterable[Tuple[T, T]]

def inproduct(v: Vector[T]) -> T:
    return sum(x*y for x, y in v)
def dilate(v: Vector[T], scale: T) -> Vector[T]:
    return ((x * scale, y * scale) for x, y in v)
vec = []  # type: Vector[float]
```

```python
from typing import TypeVar, Iterable, Tuple

T = TypeVar('T', int, float, complex)

def inproduct(v: Iterable[Tuple[T, T]]) -> T:
    return sum(x*y for x, y in v)
def dilate(v: Iterable[Tuple[T, T]], scale: T) -> Iterable[Tuple[T, T]]:
    return ((x * scale, y * scale) for x, y in v)
vec = []  # type: Iterable[Tuple[float, float]]
```

### Callable 
- 框架中用到的 一些回调方法时 可以用 `Callable[[Arg1Type, Arg2Type], ReturnType]`
```python 
from typing import Callable

def feeder(get_next_item: Callable[[], str]) -> None:
    # Body

def async_query(on_success: Callable[[int], None],
                on_error: Callable[[int, Exception], None]) -> None:
    # Body
```
- ... 可以表示不限定的入参
```python 
def partial(func: Callable[..., str], *args) -> Callable[..., str]:
```
- 因为`typing.Callable` 替代了 collections.abc.Callable， isinstance来判断是否是Callable用哪个有变化

###  泛型Generics
- 抽象基类可以描述元素的类型
```python 
from typing import Mapping, Set

def notify_by_email(employees: Set[Employee], overrides: Mapping[str, str]) -> None: ...
```
- 泛型可以 使用 TypeVar 参数化
```python
from typing import Sequence, TypeVar

T = TypeVar('T')      # Declare type variable

def first(l: Sequence[T]) -> T:   # Generic function
    return l[0]
```

- 可以包含可能的元素类型, 注意 x y不能一个是Text 一个是bytes 
```python
from typing import TypeVar, Text

AnyStr = TypeVar('AnyStr', Text, bytes)

def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y
```
- 总的来说就是 基类约束的可以接受其子类约束的,下面方法是可行的，MyStr 是 str 子类
```python
class MyStr(str): ...

x = concat(MyStr('apple'), MyStr('pie'))
```
- Any 可以接受任何类型
### 用户自定义泛型
```python

from typing import TypeVar, Generic
from logging import Logger

T = TypeVar('T')

class LoggedVar(Generic[T]):
    def __init__(self, value: T, name: str, logger: Logger) -> None:
        self.name = name
        self.logger = logger
        self.value = value

    def set(self, new: T) -> None:
        self.log('Set ' + repr(self.value))
        self.value = new

    def get(self) -> T:
        self.log('Get ' + repr(self.value))
        return self.value

    def log(self, message: str) -> None:
        self.logger.info('{}: {}'.format(self.name, message))
# ----------------
from typing import Iterable

def zero_all_vars(vars: Iterable[LoggedVar[int]]) -> None:
    for var in vars:
        var.set(0)
        
```
- 泛型可以有多个类型变量
```python
from typing import TypeVar, Generic
...

T = TypeVar('T')
S = TypeVar('S')

class Pair(Generic[T, S]):
    ...
```
- 类型变量不能重名
```python
from typing import TypeVar, Generic
...

T = TypeVar('T')

class Pair(Generic[T, T]):   # INVALID
    ...
```
- 下面这种情况不用写 Generic
```python
from typing import TypeVar, Iterator

T = TypeVar('T')

class MyIter(Iterator[T]):
    ...

#等价的写法

class MyIter(Iterator[T], Generic[T]):
    ...
```
- 可以使用多继承
```python
from typing import TypeVar, Generic, Sized, Iterable, Container, Tuple

T = TypeVar('T')

class LinkedList(Sized, Generic[T]):
    ...

K = TypeVar('K')
V = TypeVar('V')

class MyMapping(Iterable[Tuple[K, V]],
                Container[Tuple[K, V]],
                Generic[K, V]):
    ...
```
- 泛型没有指明参数类型时，它的每个参数都是Any
```python
from typing import Iterable

class MyIterable(Iterable):  # Same as Iterable[Any]
    ...
```
### 类型变量范围

下面是在静态类型检查的一些特殊情况
- 同一块代码块中相同的 类型变量可能指不同的类型
```python
from typing import TypeVar, Generic
    
T = TypeVar('T')

def fun_1(x: T) -> T: ...  # T here
def fun_2(x: T) -> T: ...  # and here could be different

fun_1(1)                   # This is OK, T is inferred to be int
fun_2('a')                 # This is also OK, now T is str
```
- 泛型变量类里用的变量类型是一样的
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class MyClass(Generic[T]):
    def meth_1(self, x: T) -> T: ...  # T here
    def meth_2(self, x: T) -> T: ...  # and here are always the same

a = MyClass()  # type: MyClass[int]
a.meth_1(1)    # OK
a.meth_2('a')  # This is an error!
```
- 使用时如果没有指定类型，那么里面的函数会变成泛型函数
```python
T = TypeVar('T')
S = TypeVar('S')
class Foo(Generic[T]):
    def method(self, x: T, y: S) -> S:
        ...

x = Foo()               # type: Foo[int]
y = x.method(0, "abc")  # inferred type of y is str

```
- 泛型函数函数体内不能解绑类型变量，或者在类里面 ？？？ 不太明白
```python
T = TypeVar('T')
S = TypeVar('S')

def a_fun(x: T) -> None:
    # this is OK
    y = []  # type: List[T]
    # but below is an error!
    y = []  # type: List[S]

class Bar(Generic[T]):
    # this is also an error
    an_attr = []  # type: List[S]

    def do_something(x: S) -> S:  # this is OK though
```
- 泛型函数里的类不能像下面这么定义
```python
from typing import List

def a_fun(x: T) -> None:

    # This is OK
    a_list = []  # type: List[T]
    ...

    # This is however illegal
    class MyGeneric(Generic[T]):
        ...
```
- 泛型类里有泛型类的情况如下
```python
T = TypeVar('T')
S = TypeVar('S')

class Outer(Generic[T]):
    class Bad(Iterable[T]):       # Error
        ...
    class AlsoBad:
        x = None  # type: List[T] # Also an error

    class Inner(Iterable[S]):     # OK
        ...
    attr = None  # type: Inner[T] # Also OK
```

### 泛型类实例化和类型擦除
- 下面这个泛型类，我们用Node()去实例化，运行时态实例的类型是Node，而对于类型检查器是是什么类型，取决于在`__init__ `和`__new__`方法里T 用了什么类型，如果没有用，默认就是Any
```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Node(Generic[T]):
    ...
```

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Node(Generic[T]):
    x = None  # type: T # Instance attribute (see below)
    def __init__(self, label: T = None) -> None:
        ...

x = Node('')  # Inferred type is Node[str]
y = Node(0)   # Inferred type is Node[int]
z = Node()    # Inferred type is Node[Any]
```
- 可以用类型注解来指定类型 ？？
```python
# (continued from previous example)
a = Node()  # type: Node[int]
b = Node()  # type: Node[str]
```
- 这种方式也是可以的
```python
# (continued from previous example)
p = Node[int]()
q = Node[str]()
r = Node[int]('')  # Error
s = Node[str](0)   # Error
```
- 运行时态 是不区分 `Node[int]` 和`Node[str]`的，这个就叫做 类型擦除 “type erasure”，java和ts也有类似机制
- 属性的访问方式情况如下，要通过实例化后的对象访问
```python
# (continued from previous example)
Node[int].x = 1  # Error
Node[int].x      # Error
Node.x = 1       # Error
Node.x           # Error
type(p).x        # Error
p.x              # Ok (evaluates to None)
Node[int]().x    # Ok (evaluates to None)
p.x = 1          # Ok, but assigning to instance attribute

```
- Mapping Sequence List Dict Set FrozenSet 等抽象泛型类是不能实例化的
- 不要使用 `Node[int]`这种形式，而是通过别名` IntNode = Node[int]`, 前面这个有runtime cost，另外可以提高可读性
### 作为基类的泛型
- `Generic[T]` 只能作为基类
- 用户自定义的泛型可以作为基类也可以作为类型使用
```python
rom typing import Dict, List, Optional

class Node:
    ...

class SymbolTable(Dict[str, List[Node]]):
    def push(self, name: str, node: Node) -> None:
        self.setdefault(name, []).append(node)

    def pop(self, name: str) -> Node:
        return self[name].pop()

    def lookup(self, name: str) -> Optional[Node]:
        nodes = self.get(name)
        if nodes:
            return nodes[-1]
        return None
```
- SymbolTable 是 dict 的subclass 是`Dict[str, List[Node]]` 的subtype
- 如果基类里有类型参数，那么这个会把他变成泛型
```python
from typing import TypeVar, Iterable, Container

T = TypeVar('T')

class LinkedList(Iterable[T], Container[T]):
    ...


from typing import TypeVar, Mapping

T = TypeVar('T')

class MyDict(Mapping[str, T]):
    ...
```

### 抽象泛型类型
- 泛型用的metaclass是 abc.ABCMeta的子类，通过添加抽象方法或属性泛型类可以是一个 ABC，
泛型类也可以用ABCs作为基类，不会有metaclass的冲突
### 带bound类型变量
- 下面表示必须是Sized的子类，可以绑定 type constraints
```python
from typing import TypeVar, Sized

ST = TypeVar('ST', bound=Sized)

def longer(x: ST, y: ST) -> ST:
    if len(x) > len(y):
        return x
    else:
        return y

longer([1], [1, 2])  # ok, return type List[int]
longer({1}, {1, 2})  # ok, return type Set[int]
longer([1], {1, 2})  # ok, return type Collection[int]
```
### 协变与逆变
总之有种情况 函数参数标注了 父类类型，能不能把子类类型标注的变量穿进去，默认是不行的，但有个开关 如下
```python
from typing import TypeVar, Generic, Iterable, Iterator

T_co = TypeVar('T_co', covariant=True)

class ImmutableList(Generic[T_co]):
    def __init__(self, items: Iterable[T_co]) -> None: ...
    def __iter__(self) -> Iterator[T_co]: ...
    ...

class Employee: ...

class Manager(Employee): ...

def dump_employees(emps: ImmutableList[Employee]) -> None:
    for emp in emps:
        ...

mgrs = ImmutableList([Manager()])  # type: ImmutableList[Manager]
dump_employees(mgrs)  # OK
```
- covariant是泛型类的属性，不是类型变量的，只能在泛型类里使用 但可以用下面实现类似效果
```python
from typing import TypeVar

class Employee: ...

class Manager(Employee): ...

E = TypeVar('E', bound=Employee)

def dump_employee(e: E) -> None: ...

dump_employee(Manager())  # OK

```
下面这样是不行的
```python
B_co = TypeVar('B_co', covariant=True)

def bad_func(x: B_co) -> B_co:  # Flagged as error by a type checker
    ...
```

### numeric tower 数字类型的继承关系
- 标准库number实现了对应的ABCs(`Number`, `Complex`, `Real`, `Rational` , `Integral`) ,虽然有bug，但它们无处不在
- 我们不用写 import numbers 然后写numbers.Float 来使用，pep 提出了一个更简便的方法：但参数使用float 标注时，类型int的变量也是可以接受的 ...

### Forward references
- 如果类型约束 还没定义，可以先用字符串表示，否则像下面这样会报错
```python
class Tree:
    def __init__(self, left: Tree, right: Tree):
        self.left = left
        self.right = right
```
我们可以这么写
```python
class Tree:
    def __init__(self, left: 'Tree', right: 'Tree'):
        self.left = left
        self.right = right
```
泛型也可以这么用
```python
class Tree:
    ...
    def leaves(self) -> List['Tree']:
        ...
```
- 利用这个可以解决循环引用问题
```python
# File models/a.py
from models.b import B
class A(Model):
    def foo(self, b: B): ...

# File models/b.py
from models.a import A
class B(Model):
    def bar(self, a: A): ...

# File main.py
from models.a import A
from models.b import B
```
可以这么写
```python
# File models/a.py
from models import b
class A(Model):
    def foo(self, b: 'b.B'): ...

# File models/b.py
from models import a
class B(Model):
    def bar(self, a: 'a.A'): ...

# File main.py
from models.a import A
from models.b import B
```

### 联合类型 Union types
```python
from typing import Union

def handle_employees(e: Union[Employee, Sequence[Employee]]) -> None:
    if isinstance(e, Employee):
        e = [e]
    ...
```
- `Union[T1, None]` 和  `Optional[T1]`是等价的
```python
def handle_employee(e: Union[Employee, None]) -> None: ...

from typing import Optional
def handle_employee(e: Optional[Employee]) -> None: ...
```
- 早期版本的pep认为但一个参数赋值为None时类型是 optional
	```python
		def handle_employee(e: Employee = None): ...
	```
	与下面是等价的, 现在提倡下面这种
	```python
	def handle_employee(e: Optional[Employee] = None) -> None: ...
	```
### 联合类型支持单例
```python
from typing import Union
from enum import Enum

class Empty(Enum):
    token = 0
_empty = Empty.token

def func(x: Union[int, None, Empty] = _empty) -> int:

    boom = x * 42  # This fails type check

    if x is _empty:
        return 0
    elif x is None:
        return 1
    else:  # At this point typechecker knows that x can only have type int
        return x * 2
```

```python
class Reason(Enum):
    timeout = 1
    error = 2

def process(response: Union[str, Reason] = '') -> str:
    if response is Reason.timeout:
        return 'TIMEOUT'
    elif response is Reason.error:
        return 'ERROR'
    else:
        # response can be only str, all other possible values exhausted
        return 'PROCESSED: ' + response
```

### 任意类型 Any
- object 和Any的区别，object基本不可以调用所有方法，any可以
- 
```python
from typing import Mapping

def use_map(m: Mapping) -> None:  # Same as Mapping[Any, Any]
    ...
```
- Tuple等价`Tuple[Any, ...]`, `Callable`等价 `Callable[..., Any]` ......
```python
from typing import Tuple, List, Callable

def check_args(args: Tuple) -> bool:
    ...

check_args(())           # OK
check_args((42, 'abc'))  # Also OK
check_args(3.14)         # Flagged as error by a type checker

# A list of arbitrary callables is accepted by this function
def apply_callbacks(cbs: List[Callable]) -> None:
```

### NoReturn 类型
- 表示不返回，只能用在函数返回标识上
```python
from typing import NoReturn

def stop() -> NoReturn:
    raise RuntimeError('no way')
```
- 错误的使用
```python
import sys
from typing import NoReturn

  def f(x: int) -> NoReturn:  # Error, f(0) implicitly returns None
      if x != 0:
          sys.exit(1)

# continue from first example
def g(x: int) -> int:
    if x > 0:
        return x
    stop()
    return 'whatever works'  # Error might be not reported by some checkers
                             # that ignore errors in unreachable blocks

from typing import List, NoReturn

# All of the following are errors
def bad1(x: NoReturn) -> int:
    ...
bad2 = None  # type: NoReturn
def bad3() -> List[NoReturn]:
    ...
```

### 类对象类型，type of class object
一个例子
```python
class User: ...  # Abstract base for User classes
class BasicUser(User): ...
class ProUser(User): ...
class TeamUser(User): ...

def new_user(user_class: type) -> User:
    user = user_class()
    # (Here we could write the user object to a database)
    return user

U = TypeVar('U', bound=User)
def new_user(user_class: Type[U]) -> U:
    user = user_class()
    # (Here we could write the user object to a database)
    return user

def new_non_team_user(user_class: Type[Union[BasicUser, ProUser]]):
    user = new_user(user_class)
    ...

joe = new_user(BasicUser)  # Inferred type is BasicUser
new_non_team_user(ProUser)  # OK
new_non_team_user(TeamUser)  # Disallowed by type checker
```
- `Type[T]`T 是类型变量，可以在类方法的第一个参数标注
- 一些特殊的构造方法如 Tupe Callable 是不能作为Type的参数的

### 注解实例和类方法
```python
T = TypeVar('T', bound='Copyable')
class Copyable:
    def copy(self: T) -> T:
        # return a copy of self

class C(Copyable): ...
c = C()
c2 = c.copy()  # type here should be C

T = TypeVar('T', bound='C')
class C:
    @classmethod
    def factory(cls: Type[T]) -> T:
        # make a new instance of cls

class D(C): ...
d = D.factory()  # type here should be D
```
### 版本 和平台 校验
```python
import sys

if sys.version_info[0] >= 3:
    # Python 3 specific definitions
else:
    # Python 2 specific definitions

if sys.platform == 'win32':
    # Windows specific definitions
else:
    # Posix specific definitions
```

### 运行时态 还是 类型校验
typing 有个常量TYPE_CHECKING，建议在类型校验或其他静态分析阶段为True， 运行时设置为False
```python
import typing

if typing.TYPE_CHECKING:
    import expensive_mod

def a_func(arg: 'expensive_mod.SomeClass') -> None:
    a_var = arg  # type: expensive_mod.SomeClass
    ...
```
### 任意参数列表和默认参数值
```python
def foo(*args: str, **kwds: int): ...
```
- `args` 类型是 `Tuple[str, ...]`  `kwds` 类型是 `Dict[str, int]`.
- 下面是一个声明有默认值，而没有指定默认值的情况
```python
def foo(x: AnyStr, y: AnyStr = ...) -> AnyStr: ...
```

### 位置参数Positional-only arguments
- 只有前面带双下划线的参数，不能通过参数名给函数传递参数
```python
def quux(__x: int, __y__: int = 0) -> None: ...

quux(3, __y__=1)  # This call is fine.

quux(__x=3)  # This call is an error.
```

### 注解生成器和协程
返回是生成器的函数可用用typing模块的 `Generator[yield_type, send_type, return_type]` 注解，
```python
def echo_round() -> Generator[int, float, str]:
    res = yield
    while res:
        res = yield round(res)
    return 'OK'
```

- PEP492 介绍的协程 注解的语法和普通的函数一样, 对await表达式才有效
```python
async def spam(ignored: int) -> str:
    return 'spam'

async def foo() -> None:
    bar = await spam(42)  # type: str
```
- collections.abc.Coroutine 也支持send throw 方法的类型限制 
```python
from typing import List, Coroutine
c = None  # type: Coroutine[List[str], str, int]
...
x = c.send('hi')  # type: List[str]
async def bar() -> None:
    x = await c  # type: int
```
- 还提供了 `Awaitable`, `AsyncIterable`, and `AsyncIterator`
```python
def op() -> typing.Awaitable[str]:
    if cond:
        return spam(42)
    else:
        return asyncio.Future(...)
    
```

## 其他注解用法的兼容性
- 现存的潜在的函数注解用法有很多和类型约束不兼容，这会让类型校验器很困惑，
- 但是因为类型约束不在运行失态有效，它不会让程序错误，只是类型校验器会给出报警
- 可以用下面的标识，说明程序不使用类型约束
	- `# type: ignore`
	- `@no_type_check` 修饰类或方法
	- `@no_type_check_decorator`. 修饰自定义的类或方法

## 类型注释 Type comments
- 注释 也是 类型约束的一种方法
```python
x = []                # type: List[Employee]
x, y, z = [], [], []  # type: List[int], List[int], List[str]
x, y, z = [], [], []  # type: (List[int], List[int], List[str])
a, b, *c = range(5)   # type: float, float, List[float]
x = [1, 2]            # type: List[int]

with frobnicate() as foo:  # type: int
    # Here foo is an int
    ...

for x, y in points:  # type: float, float
    # Here x and y are floats
    ...
```
- in stubs  python3.5或更早的版本可以用下面那个
```python
from typing import IO
stream: IO[str]

from typing import IO
stream = None  # type: IO[str]
```
- `# type: ignore` 可以忽略错误
```python
import http.client
errors = {
    'not_found': http.client.NOT_FOUND  # type: ignore
}
```
	- # type: ignore # <comment or other marker> 可以放在文件最上面 会屏蔽所有错误

## 类型转换
```python
from typing import List, cast

def find_first_str(a: List[object]) -> str:
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    # We only get here if there's at least one string in a
    return cast(str, a[index])
```

## 新类型帮助函数

- `NewType('Derived', Base)` 等价于下面，非常方便去创建一些简单的类
```python
class Derived(Base):
    def __init__(self, _x: Base) -> None:
        ...
```
- 运行时期  `NewType('Derived', Base)` 返回一个dummy function 就返回它的参数，注意下面最后一行，但 类型是NewType的参数不能传入类型是Base的参数，除非转下类型
```python
UserId = NewType('UserId', int)

def name_by_id(user_id: UserId) -> str:
    ...

UserId('user')          # Fails type check

name_by_id(42)          # Fails type check
name_by_id(UserId(42))  # OK

num = UserId(5) + 1     # type: int
```
- NewType接受两个参数，第一个是名称，第二个必须是正确的类，不是类似类型构造器如 Union或其他由NewType构造的类型， NewType返回的函数只接受一个参数
```python
class PacketId:
    def __init__(self, major: int, minor: int) -> None:
        self._major = major
        self._minor = minor

TcpPacketId = NewType('TcpPacketId', PacketId)

packet = PacketId(100, 100)
tcp_packet = TcpPacketId(packet)  # OK

tcp_packet = TcpPacketId(127, 0)  # Fails in type checker and at runtime
```
- `isinstance` 和 `issubclass` 不能用在NewType
## Stub Files
- Stub Files 是包含类型约束的文件，供类型检查器使用
- 几个运用Stub File 的场景
	- 扩展模块
	- 第三方模块，还没有加类型约束
	- 还没有写类型约束的标准模块，
	- 必须兼容python2 python3的模块
	- 出于其他目的运用注解的模块
- stub files 和普通模块的语法差不多，`@overload` 这个特性有点不一样后面再说
- 类型检查器需要检查stub files 中标注的函数，sub file中的函数体 只有 ...
- 类型检查器去要一个可配置的路径找到stub file，一旦stubfile 找到了，就不找它真的模块在哪了
- .pyi 文件后缀的文件，在相同的模块路径下
- 其他一些注意点
	- stub中导入的模块和变量建议不要是其他stub中倒入的，除非用`import ... as ...` 或 `from ... import ... as ...`导入
	- 所有使用`from ... import *` 导入的对象，建议导出
	- 如下 当`__init__.pyi`包含`from . import ham`或 `from .ham import Ham`, 那么`ham` 是spam 的导出属性
	```
		spam/
		    __init__.pyi
		    ham.pyi
	```
	- stub file 是不完整的像下面这样
	```python
	def __getattr__(name) -> Any: ...
	```
### 函数方法 过载
```python
from typing import overload

class bytes:
    ...
    @overload
    def __getitem__(self, i: int) -> int: ...
    @overload
    def __getitem__(self, s: slice) -> bytes: ...
```
比下面这种方式更精确
```python
from typing import Union

class bytes:
    ...
    def __getitem__(self, a: Union[int, slice]) -> Union[int, bytes]: ...
```
- 另一种场景,处理内建的map函数
```python
from typing import Callable, Iterable, Iterator, Tuple, TypeVar, overload

T1 = TypeVar('T1')
T2 = TypeVar('T2')
S = TypeVar('S')

@overload
def map(func: Callable[[T1], S], iter1: Iterable[T1]) -> Iterator[S]: ...
@overload
def map(func: Callable[[T1, T2], S],
        iter1: Iterable[T1], iter2: Iterable[T2]) -> Iterator[S]: ...
# ... and we could add more items to support more than two iterables
```
- 不能直接调用 一个 `@overload`修饰的函数 
- 下面是一个不能用 union表示的情况
```python
@overload
def utf8(value: None) -> None:
    pass
@overload
def utf8(value: bytes) -> bytes:
    pass
@overload
def utf8(value: unicode) -> bytes:
    pass
def utf8(value):
    <actual implementation>
```
- TypeVar 可以实现过载的功能
```python
from typing import TypeVar, Text

AnyStr = TypeVar('AnyStr', Text, bytes)

def concat1(x: AnyStr, y: AnyStr) -> AnyStr: ...

@overload
def concat2(x: str, y: str) -> str: ...
@overload
def concat2(x: bytes, y: bytes) -> bytes: ...
```

### 保存和发布 stub files
- 早期是随着模块放在相同的目录，后来由于开发者不能自由的添加这些类型约束到他们的软件包里，所以我们分了三种情况 命名，版本和安装路径
- 对于第三方的模块的stub 文件 这个pep 没有提供 a naming scheme 
- 第三方模块stub 文件必须版本号必须是 软件包最低可以兼容的版本，比如FooPackage 包有1.0, 1.1, 1.2, 1.3, 2.0, 2.1, 2.2. 这么几个版本 1.1, 2.0 and 2.2. 的接口有变化， 所以1.3 版本的包选择的是1.1 版本的stub，
- 第三方的stub模块包可以用任意的路径去存储，类型检查器通过搜索 PYTHONPATH来找到它们，shared/typehints/pythonX.Y/ 这个路径很常用，setup.py 下很可能有这样的描述
```python
...
data_files=[
    (
        'shared/typehints/python{}.{}'.format(*sys.version_info[:2]),
        pathlib.Path(SRC_PATH).glob('**/*.pyi'),
    ),
],
...
```
- 2018年 stub 文件发布的规则有些变化 [PEP 561](https://peps.python.org/pep-0561 "PEP 561 – Distributing and Packaging Type Information").
### Typeshed Repo  typeshed 库

有一个共享库将有用的存根文件都搜集在了一起，那就是 [typeshed](https://www.python.org/dev/peps/pep-0484/#typeshed)。存根文件的收集策略是独立的，并在库文档中做了报告。注意，如果某个包的所有者明确要求忽略，则此包的存根文件将不会包含进来。

## 异常
针对本特性可引发的异常，没有语法上的建议。目前本特性唯一已知的应用场景就是作为文档记录，这时建议将信息放入文档字符串（docstring）中

## typing 模块
为了将静态类型检查特性开放给 Python 3.5 以下的版本使用，需要有一个统一的命名空间。为此，标准库中引入了一个名为 `typing` 的新模块。

`typing` 模块定义了用于构建类型的基础构件（如 `Any`）、表示内置集合类的泛型变体类型（如 `List`）、表示集合类的泛型抽象基类类型（如 `Sequence`）和一批便捷类定义。

请注意，只有在类型注解的上下文中才支持用 `TypeVar` 定义的特殊类型结构，比如 `Any`、`Union`和类型变量，而 `Generic` 则只能用作基类。如果出现在 `isinstance` 或 `issubclass` 中，所有这些（未参数化的泛型除外）都将引发 `TypeError` 异常。

基础构件：

-   Any，用法为 `def get(key: str) -> Any: ...`。
-   Union，用法为 `Union[Type1, Type2, Type3]`。
-   Callable，用法为 `Callable[[Arg1Type, Arg2Type], ReturnType]`。
-   Tuple，用于列出元素类型，比如 `Tuple[int, int, str]`。空元组类型可以表示为 `Tuple[()]`。可变长同构元组可以表示为一个类型和省略号，比如 `Tuple[int, ...]`，此处的 `...` 是语法的组成部分。
-   TypeVar，用法为 `X = TypeVar('X', Type1, Type2, Type3)` 或简化为 `Y = TypeVar('Y')`（详见上文）。
-   Generic，用于创建用户自定义泛型类。
-   Type，用于对类对象做类型注解。

内置集合类的泛型变体：

-   Dict，用法为 `Dict[key_type, value_type]`。
-   DefaultDict，用法为 `DefaultDict[key_type, value_type]`，是 `collections.defaultdict` 的泛型变体。
-   List，用法为 `List[element_type]`。
-   Set，用法为 `Set[element_type]`。参阅下文有关 `AbstractSet` 的备注信息。
-   FrozenSet，用法为 `FrozenSet[element_type]`。

**注意**：`Dict`、`DefaultDict`、`List`、`Set` 和 `FrozenSet` 主要用于对返回值做类型注解。而函数参数的注解，建议采用下述抽象集合类型，比如 `Mapping`、`Sequence` 或 `AbstractSet`。

容器类抽象基类的泛型变体（及一些非容器类）：

-   Awaitable
-   AsyncIterable
-   AsyncIterator
-   ByteString
-   Callable（详见上文）
-   Collection
-   Container
-   ContextManager
-   Coroutine
-   Generator，用法为 `Generator[yield_type, send_type, return_type]`，表示生成器函数的返回值。此为 `Iterable` 的子类型。并且为 `send()` 方法可接受的类型加入了类型变量（可逆变）。可逆变的意思是，在要求可发送 `Manager` 实例的上下文中，生成器允许发送 `Employee` 实例，并返回生成器的类型。
-   Hashable（非泛型）
-   ItemsView
-   Iterable
-   Iterator
-   KeysView
-   Mapping
-   MappingView
-   MutableMapping
-   MutableSequence
-   MutableSet
-   Sequence
-   Set，重命名为 `AbstractSet`。因为 `typing` 模块中的 `Set` 表示泛型 `set()`，所以需要改名。
-   Sized（非泛型）
-   ValuesView

一些用于测试某个方法的一次性类型，类似于 `Hashable` 或 `Sized`：

-   Reversible，用于测试 `__reversed__`
-   SupportsAbs，用于测试 `__abs__`
-   SupportsComplex，用于测试 `__complex__`
-   SupportsFloat，用于测试 `__float__`
-   SupportsInt，用于测试 `__int__`
-   SupportsRound，用于测试 `__round__`
-   SupportsBytes，用于测试 `__bytes__`

便捷类定义：

-   Optional，定义为 `Optional[t] == Union[t, None]`。
-   Text，只是 Python 3 中 `str`、Python 2 中 `unicode` 的别名。
-   AnyStr，定义为 `TypeVar('AnyStr', Text, bytes)`。
-   NamedTuple，用法为 `NamedTuple(type_name, [(field_name, field_type), ...])` 等价于 `collections.namedtuple(type_name, [field_name, ...])`。在为命名元组类型的字段进行类型声明时，这会很有用。
-   NewType，用于创建运行开销很小的唯一类型，如 `UserId = NewType('UserId', int)`。
-   cast()，如前所述。
-   @no_type_check，用于禁止对某个类或函数做类型检查的装饰器（参见下文）。
-   @no_type_check_decorator，用于创建自定义装饰器的装饰器，含义与 `@no_type_check` 相同（参见下文）。
-   @type_check_only，仅在对存根文件做类型检查时可用的装饰器，标记某个类或函数在运行时不可用。
-   @overload，如上所述。
-   get_type_hints()，用于获取函数或方法的类型提示信息的工具函数。给定一个函数或方法对象，它将以 `__annotations__` 的格式返回一个`dict`，向前引用将在原函数或方法定义的上下文中进行表达式求值。
-   TYPE_CHECKING，运行时为 `False`，而对类型检查器则为 `True`。

I/O相关的类型：

-   IO（基于 `AnyStr` 的泛型）
-   BinaryIO（只是 `IO[bytes]` 子类型)
-   TextIO（只是 `IO[str]` 子类型)

与正则表达式和 `re` 模块相关的类型：

-   `Match` 和 `Pattern`，`re.match()` 和 `re.compile()` 的结果类型（基于 `AnyStr` 的泛型）。

## Python 2.7 和跨版本代码的建议语法
某些工具软件可能想在必须与 Python 2.7 兼容的代码中支持类型注解。为此，本 PEP 在此给出建议性（而并非强制）扩展，其中函数的类型注解放入 `# type` 注释（comment）中。这种注释必须紧挨着函数头之后，但在文档字符串之前。举个例子，下述 Python 3 代码：

```python
def embezzle(self, account: str, funds: int = 1000000, *fake_receipts: str) -> None:
    """Embezzle funds from account using fake receipts."""
    <code goes here>
```

等价于以下代码：

```python
def embezzle(self, account, funds=1000000, *fake_receipts):
    # type: (str, int, *str) -> None
    """Embezzle funds from account using fake receipts."""
    <code goes here>
```

请注意，方法的 `self` 不需要注明类型。

无参数方法则应如下所示：

```python
def load_cache(self):
    # type: () -> bool
    <code>
```

有时需要仅为函数或方法指定返回类型，而暂不指定参数类型。为了明确这种需求，可以用省略号替换参数列表。例如：

```python
def send_email(address, sender, cc, bcc, subject, body):
    # type: (...) -> bool
    """Send an email message.  Return True if successful."""
    <code>
```

参数列表有时会比较长，难以用一条 `# type:` 注释来指定类型。为此可以每行给出一个参数，并在每个参数的逗号之后加上必要的 `# type:` 注释。返回类型可以用省略号语法指定。指定返回类型不是强制性要求，也不是每个参数都需要指定类型。带有 `# type:` 注释的行应该只包含一个参数。最后一个参数的类型注释应该在右括号之前。例如：

```python
def send_email(address,     # type: Union[str, List[str]]
               sender,      # type: str
               cc,          # type: Optional[List[str]]
               bcc,         # type: Optional[List[str]]
               subject='',
               body=None    # type: List[str]
               ):
    # type: (...) -> bool
    """Send an email message.  Return True if successful."""
    <code>
```

注意事项：

-   只要工具软件支持这种类型注释语法，就应该与 Python 版本无关。为了支持横跨 Python 2 和 Python 3 的代码，必须如此。
-   参数或返回值不得同时带有类型注解（annotation）和类型注释（comment）。
-   如果要采用简写格式（如 `# type: (str, int) -> None`），则每一个参数都必须如此，实例和类方法的第一个参数除外。这第一个参数通常会省略注释，但也允许带上。
-   简写格式必须带有返回类型。如果是 Python 3 则会省略某些参数或返回类型，而 Python 2 则应使用 `Any`。
-   采用简写格式时，`*args` 和 `**kwds` 的类型注解前面请对应放置1或2个星号。在用 Python 3 注解格式时，此处的注解表示的是每一个参数值​​的类型，而不是由特殊参数值 `args` 或 `kwds` 接收到的 `tuple`/`dict` 的类型。
-   与其他的类型注释相类似，类型注解中用到的任何名称都必须由包含注解的模块导入或定义。
-   采用简写格式时，整个注解必须在一行之内。
-   简写格式也可以与右括号处于同一行，例如：

```python
def add(a, b):  # type: (int, int) -> int
    return a + b
```

-   类型检查程序会将位置不对的类型注释标记为错误。如有必要，可以对此类注释作两次注释标记。例如：

```python
def f():
    '''Docstring'''
    # type: () -> None  # Error!

def g():
    '''Docstring'''
    # # type: () -> None  # This is OK
```

在对 Python 2.7 代码做类型检查时，类型检查程序应将 `int` 和 `long` 视为相同类型。对于注解为 `Text` 的参数，`str` 和 `unicode` 类型也应该是可接受的。

## 未被接受的替代方案（Rejected Alternatives）

在讨论本 PEP 的早期草案时，出现过各种反对意见，并提出过一些替代方案。在此讨论其中一些意见，并解释一下未被接受的原因。

下面是几个主要的反对意见。

### 泛型参数该用什么括号？（Which brackets for generic type parameters?）

大多数人都熟知，在C++、Java、C# 和 Swift 等语言当中，用尖括号（如 `List<int>`）来表示泛型的参数化。这种格式的问题是真的难以解析，尤其是对于像 Python 这种思维简单的解析器而言。在大多数语言中，通常只允许在特定的语法位置用尖括号来解决歧义，而这些位置不允许出现泛型表达式。并且还得采用非常强大的解析技术，可对任何一段代码进行重复解析（backtrack）。

但在 Python 中，更愿意让类型表达式（在语法上）与其他表达式一样，以便用变量赋值之类的操作就能创建类型别名。不妨看看下面这个简单的类型表达式：

```cpp
List<int>
```

从 Python 解析程序的角度来看，以4个短语（名称、小于、名称、大于）开头的表达式将视为连续（chained）比较：

```css
a < b > c  # I.e., (a < b) and (b > c)
```

甚至可以创建一个两种解析方式共存的示例：

```css
a < b > [ c ]
```

假设语言中包含尖括号，则以下两种解释都是可以的：

```css
(a<b>)[c]      # I.e., (a<b>).__getitem__(c)
a < b > ([c])  # I.e., (a < b) and (b > [c])
```

当然能够再提出一种规则来消除上述情况的歧义，但对于大多数用户而言，会觉得这些规则稍显随意和复杂。并且这还要将 CPython 解析程序（和其他所有Python 解析程序）做出很大的改动。有一点应该注意，Python 当前的解析程序是有意如此“愚蠢”的，这样用户很容易就能想到简单的语法。

因为上述所有原因，所以方括号（如 `List[int]`）是（长期以来都是）泛型参数的首选语法。这通过在元类上定义 `__getitem__()` 方法就可以实现，根本不需要引入新的语法。这种方案在所有较新版本的 Python（从 Python 2.2 开始）中均有效。并非只有 Python 才选择这种语法，Scala 中的泛型类也采用了方括号。

### 已在用的注解怎么办（What about existing uses of annotations?）

有一条观点指出，[PEP 3107](https://www.cnblogs.com/popapa/p/PEP3107.html) 明确支持在函数注解中使用任意表达式。因此，本条新提案被认为与 PEP 3107 规范不兼容。

对此的回应是，首先本提案没有引入任何直接的不兼容性，因此使用注解的程序在 Python 3.4 中仍然可以正确运行，在 Python 3.5 中也毫无影响。

类型提示确实期望能最终成为注解的唯一用途，但这需要再多些讨论，而且 Python 3.5 才首次推出 `typing` 模块，也需要一段时间实现废弃（deprecation）。直至 Python 3.6 发布之前，当前的 PEP 都将为临时（provisional）状态（参阅 [PEP 411](https://www.python.org/dev/peps/pep-0411)）。可能的方案最快将自 3.6 开始无提示地废弃非类型提示的注解，自 3.7 开始完全废弃，并在 Python 3.8 中将类型提示声明为唯一允许使用的注解。即便类型提示在一夜之间取得了成功，也应该让带注解程序包的作者有足够的时间去更换方案。

_更新_：2017年秋季，本 PEP 和 `type.py` 模块的临时状态终止计划已作更改，因此其他注解用法的弃用计划也已更改。更新过的时间计划请参阅 [PEP 563](https://www.python.org/dev/peps/pep-0563)。

另一种可能的结果是，类型提示最终将成为注解的默认含义，但将其禁用的选项也会一直保留。为此，本提案定义了一个装饰器 `@no_type_check`，该装饰器将禁止对给定类或函数中用作类型提示的注解作默认解释。这里还定义了一个元装饰器 `@no_type_check_decorator`，可用于对装饰器进行装饰，使得用其装饰的任何函数或类中的注解都会被类型检查程序忽略。

且还有 `# type: ignore` 注解呢，静态检查程序应支持对选中包禁止类型检查的配置项。

尽管有这么多选择可用，但允许类型提示和其他形式的注解共存于参数中的提案已经发布过了一些。有一项提案建议，如果某个参数的注解是字典字面量，则每个字典键都表示一种不同格式的注解，字典键“`type`”将用于类型提示。这种想法及其变体的问题在于，注解会变得非常“杂乱”，可读性会很差。而且大多数现有采用注解的库，几乎不需要与类型提示混合使用。因此，只要有选择地禁用类型提示就足够了。

### 前向声明的问题（The problem of forward declarations）

当类型提示必须包含向前引用时，当前提案无疑是次优选择。Python 要求所有变量在用到时再作定义。除了循环导入外，这不太会有问题：这里的“用到”表示“在运行时去作查找”，并且对于大多数“向前”引用而言，确保在用到名称的函数被调用之前定义名称就没有问题了。

类型提示的问题在于，在定义函数时会对注解进行求值（据 [PEP 3107](https://www.cnblogs.com/popapa/p/PEP3107.html)，类似于默认值），因此注解中使用的任何名称在定义函数时必须已经定义。常见的场景是类的定义，其方法需要在注解中引用类本身。更一般地说，在相互递归引用的类中也可能发生这种情况。对于容器类型而言这很自然，例如：

```python
class Node:
    """Binary tree node."""

    def __init__(self, left: Node, right: Node):
        self.left = left
        self.right = right
```

上述写法是行不通的，因为 Python 的特性就是，一旦类的全体代码执行完毕，类的名称就定义完成了。我们的解决方案不是特别优雅，但是可以完成任务，也就是允许在注解中使用字符串字面量。不过大多数时候都不必用到字符串，类型提示的大多数应用都应引用内置类型或其他模块中已定义的类型。

有一种答复将会修改类型提示的语义，以便根本不会在运行时对其进行求值。毕竟类型检查是脱机进行的，为什么要在运行时对类型提示进行求值呢。当然这与向下兼容有冲突，因为 Python 解释程序其实并不知道某个注解是要用作类型提示或是有其他用途。

有一种可行的折衷方案，就是用 `__future__` 导入可以将给定模块中的所有注解都转换为字符串字面量，如下所示：

```java
from __future__ import annotations

class ImSet:
    def add(self, a: ImSet) -> List[ImSet]: ...

assert ImSet.add.__annotations__ == {'a': 'ImSet', 'return': 'List[ImSet]'}
```

这种 `__future__` 导入语句可能会在单独的 PEP 中给出。

_更新_：[PEP 563](https://www.python.org/dev/peps/pep-0563) 中已讨论了 `__future__` 导入语句及其后果。

### 双冒号（The double colon）

一些有创造力的人已经尝试发明了多种解决方案。比如有人提议让类型提示采用双冒号（:😃，可以一次解决两个问题：消除类型提示与其他注解之间的歧义、修改语义避免运行时求值。但这种想法有以下几个问题。

-   难看（ugly）。在 Python 中单个冒号有很多用途，并且看起来都很熟悉，因为类似于英文中的冒号用法。这是一条普遍的经验法则，Python 会遵守标点符号的大多数使用格式，那些例外通常也是因其他编程语言而熟知的。但是 :: 的这种用法在英语中是闻所未闻的，而在其他语言（例如 C++）中是被用作作用域操作符的，这太与众不同了。相反，类型提示采用单个冒号读起来很自然，这不足为奇，因为这是为此目的而精心设计的（想法比 [PEP 3107](https://www.cnblogs.com/popapa/p/PEP3107.html) [gvr-artima](https://www.cnblogs.com/popapa/p/PEP484.html#gvr-artima) 要早得多）。从 Pascal 到 Swift，其他很多语言也采用了相同的风格。
-   该如何处理返回类型的注解？
-   实际上这是在运行时对类型提示进行求值的特性。
    -   让类型提示可用于运行时，使得能基于类型提示构建运行时的类型检查程序。
    -   即便代码尚未运行，类型检查程序仍能捕获错误。因为类型检查程序是一个单独的程序，所以用户可以选择不运行（甚至不安装），但仍可能想把类型提示用作简明的文档。错误的类型提示即便当作文档也没啥用处。
-   因为是新语法，所以把双冒号用于类型提示将会受到限制，只能适用于 Python 3.5 的代码。而利用现有的语法，本提案可以轻松应用于较低版本的Python 3。mypy 实际支持 Python 3.2 以上的版本。
-   如果类型提示获得成功，可能会决定在未来加入新的语法，用于声明变量的类型，比如 `var age: int = 42`。如果参数的类型提示采用双冒号，那么为了保持一致，未来的语法必须采用同样的约定，如此难看的语法将会一直流传下去。

### 其他一些新语法格式（Other forms of new syntax）

还有一些其他格式的语法也被提出来过，比如[引入 `where` 关键字](https://www.cnblogs.com/popapa/p/PEP484.html#roberge)，以及 Cobra-inspired `requires` 子句。但这些语法都和双冒号一样存在同样的问题，他们不适用于低版本的 Python 3。新的__future__ 导入语法也同样如此。

### 其他的向下兼容约定（Other backwards compatible conventions）

提出的想法有：

-   装饰器，比如 `@typehints(name=str, returns=str)`。这可能会有用，但太啰嗦了（增加一行代码，并且参数名称必须重复一遍），且与 [PEP 3107](https://www.cnblogs.com/popapa/p/PEP3107.html) 的注解方式相去甚远。
-   存根文件。存根文件确实有需要，但主要是用来把类型提示加入已有代码中，这些代码本身不适合添加类型提示，例如：第三方软件包、需同时支持 Python 2和 Python 3 的代码、（特别是）扩展模块。在大多数情况下，与函数定义放在一起的行内注解会更加有用。
-   文档字符串。文档字符串对注解已有约定，即基于 Sphinx 注解方式 `(:type arg1: description)`。这真有点啰嗦（每个参数增加一行代码），而且不太优雅。当然再创造一些新语法也是可以的，但很难超越注解语法（因为它是专为此目的而设计的）。

还有人提议，就坐等新的发行版本吧。但这能解决什么问题？只会是拖延下去罢了。