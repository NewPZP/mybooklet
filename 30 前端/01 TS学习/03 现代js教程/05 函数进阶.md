## 递归 和堆栈
- 引擎在最大迭代深度为 10000 及以下时是可靠的，有些引擎可能允许更大的最大深度，但是对于大多数引擎来说，100000 可能就超出限制了。

### 执行上下文和堆栈

当一个函数进行嵌套调用时，将发生以下的事儿：
-   当前函数被暂停；
-   与它关联的执行上下文被一个叫做 **执行上下文堆栈** 的特殊数据结构保存；
-   执行嵌套调用；
-   嵌套调用结束后，从堆栈中恢复之前的执行上下文，并从停止的位置恢复外部函数。
-
### 递归遍历

### 递归结构

#### 链表


## Rest 参数与 Spread 语法

### Rest 参数 ...
- Rest 参数必须放到参数列表的末尾
```javascript
function showName(firstName, lastName, ...titles) {
  alert( firstName + ' ' + lastName ); // Julius Caesar

  // 剩余的参数被放入 titles 数组中
  // i.e. titles = ["Consul", "Imperator"]
  alert( titles[0] ); // Consul
  alert( titles[1] ); // Imperator
  alert( titles.length ); // 2
}

showName("Julius", "Caesar", "Consul", "Imperator");
```
### “arguments” 变量

```javascript
function showName() {
  alert( arguments.length );
  alert( arguments[0] );
  alert( arguments[1] );

  // 它是可遍历的
  // for(let arg of arguments) alert(arg);
}

// 依次显示：2，Julius，Caesar
showName("Julius", "Caesar");

// 依次显示：1，Ilya，undefined（没有第二个参数）
showName("Ilya");
```
- 箭头函数没有 `"arguments"`
	- 如果我们在箭头函数中访问 `arguments`，访问到的 `arguments` 并不属于箭头函数，而是属于箭头函数外部的“普通”函数。
```javascript
function f() {
  let showArg = () => alert(arguments[0]);
  showArg();
}

f(1); // 1
```

### Spread 语法
- spread语法解决下面这个问题
```javascript
alert( Math.max(3, 5, 1) ); // 5

let arr = [3, 5, 1];
alert( Math.max(arr) ); // NaN

alert( Math.max(...arr) ); // 5（spread 语法把数组转换为参数列表）

let arr1 = [1, -2, 3, 4]; 
let arr2 = [8, 3, -8, 1];
alert( Math.max(...arr1, ...arr2) ); // 8

let merged = [0, ...arr1, 2, ...arr2];
alert(merged)
```
- spread 语法这样操作任何可迭代对象。
```javascript
let str = "Hello";

alert( [...str] ); // H,e,l,l,o
alert( Array.from(str) ); // H,e,l,l,o

```
### 复制 array/object
- spread 语法 可以浅拷贝
```javascript
let arr = [1, 2, 3];

let arrCopy = [...arr]; // 将数组 spread 到参数列表中
                        // 然后将结果放到一个新数组

// 两个数组中的内容相同吗？
alert(JSON.stringify(arr) === JSON.stringify(arrCopy)); // true

// 两个数组相等吗？
alert(arr === arrCopy); // false（它们的引用是不同的）

// 修改我们初始的数组不会修改副本：
arr.push(4);
alert(arr); // 1, 2, 3, 4
alert(arrCopy); // 1, 2, 3
```
- 对象也可以操作
```javascript
let obj = { a: 1, b: 2, c: 3 };

let objCopy = { ...obj }; // 将对象 spread 到参数列表中
                          // 然后将结果返回到一个新对象

// 两个对象中的内容相同吗？
alert(JSON.stringify(obj) === JSON.stringify(objCopy)); // true

// 两个对象相等吗？
alert(obj === objCopy); // false (not same reference)

// 修改我们初始的对象不会修改副本：
obj.d = 4;
alert(JSON.stringify(obj)); // {"a":1,"b":2,"c":3,"d":4}
alert(JSON.stringify(objCopy)); // {"a":1,"b":2,"c":3}
```

## 变量作用域，闭包
### 代码块
- 如果在代码块 `{...}` 内声明了一个变量，那么这个变量只在该代码块内可见。下面没有隔离会报错
```javascript
{
  // 显示 message
  let message = "Hello";
  alert(message);
}

{
  // 显示另一个 message
  let message = "Goodbye";
  alert(message);
}
```

- 对于 `if`，`for` 和 `while` 等，在 `{...}` 中声明的变量也仅在内部可见：

### 嵌套函数
- 可以访问外部变量
```javascript
function sayHiBye(firstName, lastName) {

  // 辅助嵌套函数使用如下
  function getFullName() {
    return firstName + " " + lastName;
  }

  alert( "Hello, " + getFullName() );
  alert( "Bye, " + getFullName() );

}
```
### 词法环境
#### step1. 变量
- 在 JavaScript 中，每个运行的**函数**，**代码块** `{...}` 以及**整个脚本**，都有一个被称为 **词法环境（Lexical Environment）** 的内部（隐藏）的关联对象。
- 词法环境
	1.  **环境记录（Environment Record）** —— 一个存储所有局部变量作为其属性（包括一些其他信息，例如 `this` 的值）的对象。
	2.  对 **外部词法环境** 的引用，与外部代码相关联。

#### Step 2. 函数声明
- 一个函数其实也是一个值，就像变量一样。
- **不同之处在于函数声明的初始化会被立即完成。** （不像 `let` 那样直到声明处才可用）。

#### Step 3. 内部和外部的词法环境


### 垃圾收集
- 通常，函数调用完成后，会将词法环境和其中的所有变量从内存中删除。
- 可达的
```javascript
function f() {
  let value = Math.random();

  return function() { alert(value); };
}

// 数组中的 3 个函数，每个都与来自对应的 f() 的词法环境相关联
let arr = [f(), f(), f()];
```
- 不可达的，被清理
```javascript
function f() {
  let value = 123;

  return function() {
    alert(value);
  }
}

let g = f(); // 当 g 函数存在时，该值会被保留在内存中

g = null; // ……现在内存被清理了
```

#### 实际开发中的优化
- 理论上当函数可达时，它外部的所有变量也都将存在。
- 但在实际中，JavaScript 引擎会试图优化它。它们会分析变量的使用情况，如果从代码中可以明显看出有未使用的外部变量，那么就会将其删除。
- **在 V8（Chrome，Edge，Opera）中的一个重要的副作用是，此类变量在调试中将不可用。**

```javascript
function f() {
  let value = Math.random();

  function g() {
    debugger; // 在 Console 中：输入 alert(value); No such variable! 理论上，它应该是可以访问的，但引擎把它优化掉了。
  }

  return g;
}

let g = f();
g();
```
- 这可能会导致有趣的（如果不是那么耗时的）调试问题。其中之一 —— 我们可以看到的是一个同名的外部变量，而不是预期的变量：
```javascript
let value = "Surprise!";

function f() {
  let value = "the closest value";

  function g() {
    debugger; // 在 console 中：输入 alert(value); Surprise!
  }

  return g;
}

let g = f();
g();
```

## 老旧的var
- 现在一般用let不用var

### var没有块级作用域
```javascript
if (true) {
  var test = true; // 使用 "var" 而不是 "let"
}

alert(test); // true，变量在 if 结束后仍存在
```

```javascript
for (var i = 0; i < 10; i++) {
  var one = 1;
  // ...
}

alert(i);   // 10，"i" 在循环结束后仍可见，它是一个全局变量
alert(one); // 1，"one" 在循环结束后仍可见，它是一个全局变量
```
- 如果一个代码块位于函数内部，那么 `var` 声明的变量的作用域将为函数作用域：
```javascript
function sayHi() {
  if (true) {
    var phrase = "Hello";
  }

  alert(phrase); // 能正常工作
}

sayHi();
alert(phrase); // ReferenceError: phrase is not defined
```

### “var” 允许重新声明
### “var” 声明的变量，可以在其声明语句前被使用

```javascript
function sayHi() {
  phrase = "Hello"; // (*)

  if (false) {
    var phrase;
  }

  alert(phrase);
}
sayHi();
```
- 所有的 `var` 都被“提升”到了函数的顶部。所以，在上面的例子中，`if (false)` 分支永远都不会执行，但没关系，它里面的 `var` 在函数刚开始时就被处理了，所以在执行 `(*)` 那行代码时，变量是存在的。
- **声明会被提升，但是赋值不会。**

### IIFE 立即调用函数表达式
- 这里，创建了一个函数表达式并立即调用。因此，代码立即执行并拥有了自己的私有变量。
```javascript
// 创建 IIFE 的方法

(function() {
  alert("Parentheses around the function");
})();

(function() {
  alert("Parentheses around the whole thing");
}());

!function() {
  alert("Bitwise NOT operator starts the expression");
}();

+function() {
  alert("Unary plus starts the expression");
}();
```
- 现在我们没有累呦编写这种代码

## 全局对象
- 在浏览器中，它的名字是 “window”，对 Node.js 而言，它的名字是 “global”，其它环境可能用的是别的名字。
- 最近`globalThis` 被作为全局对象的标准名称加入到了 JavaScript 中，所有环境都应该支持该名称。所有主流浏览器都支持它。
- 全局对象的所有属性都可以被直接访问：
```javascript
alert("Hello");
// 等同于
window.alert("Hello");
```

- 在浏览器中，使用 `var`（而不是 `let/const`！）声明的全局函数和变量会成为全局对象的属性。
```javascript
var gVar = 5;

alert(window.gVar); // 5（成为了全局对象的属性）
```

- 如果一个值非常重要，以至于你想使它在全局范围内可用，那么可以直接将其作为属性写入
```javascript
// 将当前用户信息全局化，以允许所有脚本访问它
window.currentUser = {
  name: "John"
};

// 代码中的另一个位置
alert(currentUser.name);  // John

// 或者，如果我们有一个名为 "currentUser" 的局部变量
// 从 window 显式地获取它（这是安全的！）
alert(window.currentUser.name); // John
```

### 使用 polyfills
- 我们使用全局对象来测试对现代语言功能的支持。
- 测试是否存在内建的 `Promise` 对象
```javascript
if (!window.Promise) {
  alert("Your browser is really old!");
  window.Promise = ... // 定制实现现代语言功能
}
```

## 函数对象 NFE
- 在 JavaScript 中，函数的类型是对象。
- 一个容易理解的方式是把函数想象成可被调用的“行为对象（action object）”。我们不仅可以调用它们，还能把它们当作对象来处理：增/删属性，按引用传递等。
### 属性name
```javascript
function sayHi() {
  alert("Hi");
}

alert(sayHi.name); // sayHi
```

```javascript
let user = {

  sayHi() {
    // ...
  },

  sayBye: function() {
    // ...
  }

}

alert(user.sayHi.name); // sayHi
alert(user.sayBye.name); // sayBye
```

### 属性 “length”

- 还有另一个内建属性 “length”，它返回函数入参的个数，rest 参数不参与计数。
```javascript
function f1(a) {}
function f2(a, b) {}
function many(a, b, ...more) {}

alert(f1.length); // 1
alert(f2.length); // 2
alert(many.length); // 2
```

-  [内省/运行时检查（introspection）](https://zh.wikipedia.org/wiki/%E5%86%85%E7%9C%81_(%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6))。
```javascript
function ask(question, ...handlers) {
  let isYes = confirm(question);

  for(let handler of handlers) {
    if (handler.length == 0) {
      if (isYes) handler();
    } else {
      handler(isYes);
    }
  }

}

// 对于肯定的回答，两个 handler 都会被调用
// 对于否定的回答，只有第二个 handler 被调用
ask("Question?", () => alert('You said yes'), result => alert(result));
```

### 自定义属性

```javascript
function sayHi() {
  alert("Hi");

  // 计算调用次数
  sayHi.counter++;
}
sayHi.counter = 0; // 初始值

sayHi(); // Hi
sayHi(); // Hi

alert( `Called ${sayHi.counter} times` ); // Called 2 times
```

- 属性不是变量
	- 被赋值给函数的属性，比如 `sayHi.counter = 0`，**不会** 在函数内定义一个局部变量 `counter`。换句话说，属性 `counter` 和变量 `let counter` 是毫不相关的两个东西。
- 函数属性有时会用来替代闭包
```javascript
function makeCounter() {
  // 不需要这个了
  // let count = 0

  function counter() {
    return counter.count++;
  };

  counter.count = 0;

  return counter;
}

let counter = makeCounter();
alert( counter() ); // 0
alert( counter() ); // 1
```

```javascript
function makeCounter() {

  function counter() {
    return counter.count++;
  };

  counter.count = 0;

  return counter;
}

let counter = makeCounter();

counter.count = 10;
alert( counter() ); // 10
```
### 命名函数表达式 NFE
名字 `func` 有两个特殊的地方，这就是添加它的原因：
1. 它允许函数在内部引用自己。
2. 它在函数外是不可见的。
```javascript
let sayHi = function func(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    func("Guest"); // 使用 func 再次调用函数自身
  }
};

sayHi(); // Hello, Guest

// 但这不工作：
func(); // Error, func is not defined（在函数外不可见）
```
- 我们为什么使用 `func` 呢？为什么不直接使用 `sayHi` 进行嵌套调用？像下面这样
	- 问题在于 `sayHi` 的值可能会被函数外部的代码改变。如果该函数被赋值给另外一个变量（译注：也就是原变量被修改），那么函数就会开始报错：
```javascript
let sayHi = function(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    sayHi("Guest"); // Error: sayHi is not a function
  }
};

let welcome = sayHi;
sayHi = null;

welcome(); // Error，嵌套调用 sayHi 不再有效！
```
```javascript
let sayHi = function func(who) {
  if (who) {
    alert(`Hello, ${who}`);
  } else {
    func("Guest"); // 现在一切正常
  }
};

let welcome = sayHi;
sayHi = null;

welcome(); // Hello, Guest（嵌套调用有效）
```

## "new Function" 语法
- 语法
```javascript
let func = new Function ([arg1, arg2, ...argN], functionBody);
```
```javascript
let sum = new Function('a', 'b', 'return a + b');

alert( sum(1, 2) ); // 3
```

### 闭包
- 如果我们使用 `new Function` 创建一个函数，那么该函数的 `[[Environment]]` 并不指向当前的词法环境，而是指向全局环境。
- 因此，此类函数无法访问外部（outer）变量，只能访问全局变量。
```javascript
function getFunc() {
  let value = "test";

  let func = new Function('alert(value)');

  return func;
}

getFunc()(); // error: value is not defined
```
- 在将 JavaScript 发布到生产环境之前，需要使用 **压缩程序（minifier）** 对其进行压缩 —— 一个特殊的程序，通过删除多余的注释和空格等压缩代码 —— 更重要的是，将局部变量命名为较短的变量。这种情况下，如果使 `new Function` 可以访问自身函数以外的变量，它也很有可能无法找到重命名的 `userName`，这是因为新函数的创建发生在代码压缩以后，变量名已经被替换了。
- 当我们需要向 `new Function` 创建出的新函数传递数据时，我们必须显式地通过参数进行传递。

## 调度：setTimeout 和 setInterval
- `setTimeout` 允许我们将函数推迟到一段时间间隔之后再执行。
- `setInterval` 允许我们重复运行一个函数，从一段时间间隔之后开始运行，之后以该时间间隔连续重复运行该函数。

### setTimeout
```javascript
let timerId = setTimeout(func|code, [delay], [arg1], [arg2], ...)
```

```javascript
function sayHi(phrase, who) {
  alert( phrase + ', ' + who );
}

setTimeout(sayHi, 1000, "Hello", "John"); // Hello, John
```
```javascript
setTimeout(() => alert('Hello'), 1000);
```

#### 用 clearTimeout 来取消调度

```javascript
let timerId = setTimeout(() => alert("never happens"), 1000);
alert(timerId); // 定时器标识符

clearTimeout(timerId);
alert(timerId); // 还是这个标识符（并没有因为调度被取消了而变成 null）
```

### setInterval
```javascript
let timerId = setInterval(func|code, [delay], [arg1], [arg2], ...)
```

```javascript
// 每 2 秒重复一次
let timerId = setInterval(() => alert('tick'), 2000);

// 5 秒之后停止
setTimeout(() => { clearInterval(timerId); alert('stop'); }, 5000);
```

### 嵌套的 setTimeout
- 周期调度也可以用setTimeout，嵌套的 `setTimeout` 要比 `setInterval` 灵活得多。采用这种方式可以根据当前执行结果来调度下一次调用，因此下一次调用可以与当前这一次不同。
```javascript
/** instead of:
let timerId = setInterval(() => alert('tick'), 2000);
*/

let timerId = setTimeout(function tick() {
  alert('tick');
  timerId = setTimeout(tick, 2000); // (*)
}, 2000);
```

- **嵌套的 `setTimeout` 相较于 `setInterval` 能够更精确地设置两次执行之间的延时。**
- setTimeout是在完成调度后再调度，setInterval是调用时间间隔是一样的

### 零延时的 setTimeout
这儿有一种特殊的用法：`setTimeout(func, 0)`，或者仅仅是 `setTimeout(func)`。该函数被调度在当前脚本执行完成“之后”立即执行。

- 例如，下面这段代码会先输出 “Hello”，然后立即输出 “World”：
```javascript
setTimeout(() => alert("World"));

alert("Hello");
```

## 装饰器模式和转发，call/apply

### 透明缓存
```javascript
function slow(x) {
  // 这里可能会有重负载的 CPU 密集型工作
  alert(`Called with ${x}`);
  return x;
}

function cachingDecorator(func) {
  let cache = new Map();

  return function(x) {
    if (cache.has(x)) {    // 如果缓存中有对应的结果
      return cache.get(x); // 从缓存中读取结果
    }

    let result = func(x);  // 否则就调用 func

    cache.set(x, result);  // 然后将结果缓存（记住）下来
    return result;
  };
}

slow = cachingDecorator(slow);

alert( slow(1) ); // slow(1) 被缓存下来了，并返回结果
alert( "Again: " + slow(1) ); // 返回缓存中的 slow(1) 的结果

alert( slow(2) ); // slow(2) 被缓存下来了，并返回结果
alert( "Again: " + slow(2) ); // 返回缓存中的 slow(2) 的结果
```
- 在上面的代码中，`cachingDecorator` 是一个 **装饰器（decorator）**

### 使用 “func.call” 设定上下文
- 上面提到的缓存装饰器不适用于对象方法
```javascript
// 我们将对 worker.slow 的结果进行缓存
let worker = {
  someMethod() {
    return 1;
  },

  slow(x) {
    // 可怕的 CPU 过载任务
    alert("Called with " + x);
    return x * this.someMethod(); // (*)
  }
};

// 和之前例子中的代码相同
function cachingDecorator(func) {
  let cache = new Map();
  return function(x) {
    if (cache.has(x)) {
      return cache.get(x);
    }
    let result = func(x); // (**)
    cache.set(x, result);
    return result;
  };
}

alert( worker.slow(1) ); // 原始方法有效

worker.slow = cachingDecorator(worker.slow); // 现在对其进行缓存

alert( worker.slow(2) ); // 蛤！Error: Cannot read property 'someMethod' of undefined
```
- 有一个特殊的内建函数方法 [func.call(context, …args)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Function/call)，它允许调用一个显式设置 `this` 的函数。
```javascript
func.call(context, arg1, arg2, ...)
//它运行 `func`，提供的第一个参数作为 `this`，后面的作为参数（arguments）。
```
- 使用func.call()的装饰器
```javascript
let worker = {
  someMethod() {
    return 1;
  },

  slow(x) {
    alert("Called with " + x);
    return x * this.someMethod(); // (*)
  }
};

function cachingDecorator(func) {
  let cache = new Map();
  return function(x) {
    if (cache.has(x)) {
      return cache.get(x);
    }
    let result = func.call(this, x); // 现在 "this" 被正确地传递了
    cache.set(x, result);
    return result;
  };
}

worker.slow = cachingDecorator(worker.slow); // 现在对其进行缓存

alert( worker.slow(2) ); // 工作正常
alert( worker.slow(2) ); // 工作正常，没有调用原始函数（使用的缓存）
```

### 传递多个参数
```javascript
let worker = {
  slow(min, max) {
    alert(`Called with ${min},${max}`);
    return min + max;
  }
};

function cachingDecorator(func, hash) {
  let cache = new Map();
  return function() {
    let key = hash(arguments); // (*)
    if (cache.has(key)) {
      return cache.get(key);
    }

    let result = func.call(this, ...arguments); // (**)

    cache.set(key, result);
    return result;
  };
}

function hash(args) {
  return args[0] + ',' + args[1];
}

worker.slow = cachingDecorator(worker.slow, hash);

alert( worker.slow(3, 5) ); // works
alert( "Again " + worker.slow(3, 5) ); // same (cached)
```

### func.apply
- 我们可以使用 `func.apply(this, arguments)` 代替 `func.call(this, ...arguments)`。

- 只有一个关于 `args` 的细微的差别：
	- Spread 语法 `...` 允许将 **可迭代对象** `args` 作为列表传递给 `call`。
	- `apply` 只接受 **类数组** `args`。
- `apply` 可能会更快，因为大多数 JavaScript 引擎在内部对其进行了优化。

### 借用一种方法
```javascript
function hash() {
  alert( [].join.call(arguments) ); // 1,2
}

hash(1, 2);
```
- 这个技巧被称为 **方法借用（method borrowing）**。我们从常规数组 `[].join` 中获取（借用）join 方法，并使用 `[].join.call` 在 `arguments` 的上下文中运行它。

### 装饰器和函数属性
- 存在一种创建装饰器的方法，该装饰器可保留对函数属性的访问权限，但这需要使用特殊的 `Proxy` 对象来包装函数。后面深入

## 函数绑定
- 当将对象方法作为回调进行传递，例如传递给 `setTimeout`，这儿会存在一个常见的问题：“丢失 `this`”。
### 丢失this
```javascript
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

setTimeout(user.sayHi, 1000); // Hello, undefined!
```

### 解决方案 1：包装器
```javascript
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

setTimeout(function() {
  user.sayHi(); // Hello, John!
}, 1000);
```

```javascript
setTimeout(() => user.sayHi(), 1000); // Hello, John!
```

- 如果在 `setTimeout` 触发之前（有一秒的延迟！）`user` 的值改变了怎么办？那么，突然间，它将调用错误的对象！

### 解决方案 2：bind
- 函数提供了一个内建方法 [bind](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)，它可以绑定 `this`。
```javascript
let user = {
  firstName: "John",
  sayHi() {
    alert(`Hello, ${this.firstName}!`);
  }
};

let sayHi = user.sayHi.bind(user); // (*)

// 可以在没有对象（译注：与对象分离）的情况下运行它
sayHi(); // Hello, John!

setTimeout(sayHi, 1000); // Hello, John!

// 即使 user 的值在不到 1 秒内发生了改变
// sayHi 还是会使用预先绑定（pre-bound）的值，该值是对旧的 user 对象的引用
user = {
  sayHi() { alert("Another user in setTimeout!"); }
};
```

### 部分（应用）函数（Partial functions）
- 我们不仅可以绑定 `this`，还可以绑定参数（arguments）
```javascript
function mul(a, b) {
  return a * b;
}

let double = mul.bind(null, 2);

alert( double(3) ); // = mul(2, 3) = 6
alert( double(4) ); // = mul(2, 4) = 8
alert( double(5) ); // = mul(2, 5) = 10
```

### 在没有上下文情况下的 partial
- 当我们想绑定一些参数（arguments），但是不想绑定上下文 `this`，应该怎么办？
```javascript
function partial(func, ...argsBound) {
  return function(...args) { // (*)
    return func.call(this, ...argsBound, ...args);
  }
}

// 用法：
let user = {
  firstName: "John",
  say(time, phrase) {
    alert(`[${time}] ${this.firstName}: ${phrase}!`);
  }
};

// 添加一个带有绑定时间的 partial 方法
user.sayNow = partial(user.say, new Date().getHours() + ':' + new Date().getMinutes());

user.sayNow("Hello");
// 类似于这样的一些内容：
// [10:00] John: Hello!
```
## 深入理解箭头函数

### 箭头函数没有 “this”
- 箭头函数没有 `this`。如果访问 `this`，则会从外部获取。

```javascript
let group = {
  title: "Our Group",
  students: ["John", "Pete", "Alice"],

  showList() {
    this.students.forEach(
      student => alert(this.title + ': ' + student)
    );
  }
};

group.showList();
```
```javascript
let group = {
  title: "Our Group",
  students: ["John", "Pete", "Alice"],

  showList() {
    this.students.forEach(function(student) {
      // Error: Cannot read property 'title' of undefined
      alert(this.title + ': ' + student);
    });
  }
};

group.showList();
```

- 箭头函数 VS bind
	 - `.bind(this)` 创建了一个该函数的“绑定版本”。
	- 箭头函数 `=>` 没有创建任何绑定。箭头函数只是没有 `this`。`this` 的查找与常规变量的搜索方式完全相同：在外部词法环境中查找。

### 箭头函数没有 “arguments”

```javascript
function defer(f, ms) {
  return function() {
    setTimeout(() => f.apply(this, arguments), ms);
  };
}

function sayHi(who) {
  alert('Hello, ' + who);
}

let sayHiDeferred = defer(sayHi, 2000);
sayHiDeferred("John"); // 2 秒后显示：Hello, John
```

```javascript
function defer(f, ms) {
  return function(...args) {
    let ctx = this;
    setTimeout(function() {
      return f.apply(ctx, args);
    }, ms);
  };
}
```