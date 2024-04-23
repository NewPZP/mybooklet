## Proxy 和 Reflect
- 一个 `Proxy` 对象包装另一个对象并拦截诸如读取/写入属性和其他操作，可以选择自行处理它们，或者透明地允许该对象处理它们。

### Proxy

```javascript
let target = {};
let proxy = new Proxy(target, {}); // 空的 handler 对象

proxy.test = 5; // 写入 proxy 对象 (1)
alert(target.test); // 5，test 属性出现在了 target 中！

alert(proxy.test); // 5，我们也可以从 proxy 对象读取它 (2)

for(let key in proxy) alert(key); // test，迭代也正常工作 (3)
```

- `Proxy` 是一种特殊的“奇异对象（exotic object）”。它没有自己的属性。如果 `handler` 为空，则透明地将操作转发给 `target`。
- 要激活更多功能，让我们添加捕捉器。我们可以用它们拦截什么？
	- 它们在 [proxy 规范](https://tc39.es/ecma262/#sec-proxy-object-internal-methods-and-internal-slots) 和下表中被列出。

### 带有 “get” 捕捉器的默认值
- 要拦截读取操作，`handler` 应该有 `get(target, property, receiver)` 方法。
	- `target` —— 是目标对象，该对象被作为第一个参数传递给 `new Proxy`，
	- `property` —— 目标属性名，
	- `receiver` —— 如果目标属性是一个 getter 访问器属性，则 `receiver` 就是本次读取属性所在的 `this` 对象。通常，这就是 `proxy` 对象本身（或者，如果我们从 proxy 继承，则是从该 proxy 继承的对象）。现在我们不需要此参数，因此稍后我们将对其进行详细介绍。
```javascript
let dictionary = {
  'Hello': 'Hola',
  'Bye': 'Adiós'
};

dictionary = new Proxy(dictionary, {
  get(target, phrase) { // 拦截读取属性操作
    if (phrase in target) { //如果词典中有该短语
      return target[phrase]; // 返回其翻译
    } else {
      // 否则返回未翻译的短语
      return phrase;
    }
  }
});

// 在词典中查找任意短语！
// 最坏的情况也只是它们没有被翻译。
alert( dictionary['Hello'] ); // Hola
alert( dictionary['Welcome to Proxy']); // Welcome to Proxy（没有被翻译）
```

### 使用 “set” 捕捉器进行验证
- `set(target, property, value, receiver)`：
	- `target` —— 是目标对象，该对象被作为第一个参数传递给 `new Proxy`，
	- `property` —— 目标属性名称，
	- `value` —— 目标属性的值，
	- `receiver` —— 与 `get` 捕捉器类似，仅与 setter 访问器属性相关。
```javascript
let numbers = [];

numbers = new Proxy(numbers, { // (*)
  set(target, prop, val) { // 拦截写入属性操作
    if (typeof val == 'number') {
      target[prop] = val;
      return true;
    } else {
      return false;
    }
  }
});

numbers.push(1); // 添加成功
numbers.push(2); // 添加成功
alert("Length is: " + numbers.length); // 2

numbers.push("test"); // TypeError（proxy 的 'set' 返回 false）

alert("This line is never reached (error in the line above)");
```

- 别忘了返回 `true` 对于 `set` 操作，它必须在成功写入时返回 `true`。

### 用 “ownKeys” 和 “getOwnPropertyDescriptor” 进行迭代

- `Object.keys`，`for..in` 循环和大多数其他遍历对象属性的方法都使用内部方法 `[[OwnPropertyKeys]]`（由 `ownKeys` 捕捉器拦截) 来获取属性列表。

- 如果该属性在对象中不存在，那么我们只需要拦截 `[[GetOwnProperty]]`。
```javascript
let user = { };

user = new Proxy(user, {
  ownKeys(target) { // 一旦要获取属性列表就会被调用
    return ['a', 'b', 'c'];
  },

  getOwnPropertyDescriptor(target, prop) { // 被每个属性调用
    return {
      enumerable: true,
      configurable: true
      /* ...其他标志，可能是 "value:..." */
    };
  }

});

alert( Object.keys(user) ); // a, b, c 
```

### 具有 “deleteProperty” 和其他捕捉器的受保护属性

- 让我们使用代理来防止对以 `_` 开头的属性的任何访问。
	- `get` 读取此类属性时抛出错误，
	- `set` 写入属性时抛出错误，
	- `deleteProperty` 删除属性时抛出错误，
	- `ownKeys` 在使用 `for..in` 和像 `Object.keys` 这样的的方法时排除以 `_` 开头的属性。
```javascript
let user = {
  name: "John",
  _password: "***"
};

user = new Proxy(user, {
  get(target, prop) {
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    }
    let value = target[prop];
    return (typeof value === 'function') ? value.bind(target) : value; // (*)
  },
  set(target, prop, val) { // 拦截属性写入
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    } else {
      target[prop] = val;
      return true;
    }
  },
  deleteProperty(target, prop) { // 拦截属性删除
    if (prop.startsWith('_')) {
      throw new Error("Access denied");
    } else {
      delete target[prop];
      return true;
    }
  },
  ownKeys(target) { // 拦截读取属性列表
    return Object.keys(target).filter(key => !key.startsWith('_'));
  }
});

// "get" 不允许读取 _password
try {
  alert(user._password); // Error: Access denied
} catch(e) { alert(e.message); }

// "set" 不允许写入 _password
try {
  user._password = "test"; // Error: Access denied
} catch(e) { alert(e.message); }

// "deleteProperty" 不允许删除 _password
try {
  delete user._password; // Error: Access denied
} catch(e) { alert(e.message); }

// "ownKeys" 将 _password 过滤出去
for(let key in user) alert(key); // name
```


### 带有 “has” 捕捉器的 “in range”

- `has` 捕捉器会拦截 `in` 调用。`has(target, property)`
	- `target` —— 是目标对象，被作为第一个参数传递给 `new Proxy`，
	- `property` —— 属性名称。
```javascript
let range = {
  start: 1,
  end: 10
};

range = new Proxy(range, {
  has(target, prop) {
    return prop >= target.start && prop <= target.end;
  }
});

alert(5 in range); // true
alert(50 in range); // false
```

### 包装函数："apply"
- 我们也可以将代理（proxy）包装在函数周围。
- `apply(target, thisArg, args)` 捕捉器能使代理以函数的方式被调用：
	- `target` 是目标对象（在 JavaScript 中，函数就是一个对象），
	- `thisArg` 是 `this` 的值。
	- `args` 是参数列表。


```javascript
function delay(f, ms) {
  return function() {
    setTimeout(() => f.apply(this, arguments), ms);
  };
}

function sayHi(user) {
  alert(`Hello, ${user}!`);
}

alert(sayHi.length); // 1（函数的 length 是函数声明中的参数个数）

sayHi = delay(sayHi, 3000);

alert(sayHi.length); // 0（在包装器声明中，参数个数为 0)
```

- 但是包装函数不会转发属性读取/写入操作或者任何其他操作。进行包装后，就失去了对原始函数属性的访问，例如 `name`，`length` 和其他属性

```javascript
function delay(f, ms) {
  return new Proxy(f, {
    apply(target, thisArg, args) {
      setTimeout(() => target.apply(thisArg, args), ms);
    }
  });
}

function sayHi(user) {
  alert(`Hello, ${user}!`);
}

sayHi = delay(sayHi, 3000);

alert(sayHi.length); // 1 (*) proxy 将“获取 length”的操作转发给目标对象

sayHi("John"); // Hello, John!（3 秒后）
```

### Reflect
- `Reflect` 是一个内建对象，可简化 `Proxy` 的创建。
```javascript
let user = {};

Reflect.set(user, 'name', 'John');

alert(user.name); // John 
```

|操作|`Reflect` 调用|内部方法|
|---|---|---|
|`obj[prop]`|`Reflect.get(obj, prop)`|`[[Get]]`|
|`obj[prop] = value`|`Reflect.set(obj, prop, value)`|`[[Set]]`|
|`delete obj[prop]`|`Reflect.deleteProperty(obj, prop)`|`[[Delete]]`|
|`new F(value)`|`Reflect.construct(F, value)`|`[[Construct]]`|
|…|…|…|

#### 代理一个 getter
- 这里有个结果不符合期望
```javascript
let user = {
  _name: "Guest",
  get name() {
    return this._name;
  }
};

let userProxy = new Proxy(user, {
  get(target, prop, receiver) {
    return target[prop]; // (*) target = user
  }
});

let admin = {
  __proto__: userProxy,
  _name: "Admin"
};

// 期望输出：Admin
alert(admin.name); // 输出：Guest (?!?)
```

- `Reflect.get` 可以做到。如果我们使用它，一切都会正常运行。
```javascript
let user = {
  _name: "Guest",
  get name() {
    return this._name;
  }
};

let userProxy = new Proxy(user, {
  get(target, prop, receiver) { // receiver = admin
    return Reflect.get(target, prop, receiver); // (*)
  }
});


let admin = {
  __proto__: userProxy,
  _name: "Admin"
};

alert(admin.name); // Admin 
```

### Proxy 的局限性
#### 内建对象：内部插槽（Internal slot）
- 许多内建对象，例如 `Map`，`Set`，`Date`，`Promise` 等，都使用了所谓的“内部插槽”。
- 例如，`Map` 将项目（item）存储在 `[[MapData]]` 中。内建方法可以直接访问它们，而不通过 `[[Get]]/[[Set]]` 内部方法。所以 `Proxy` 无法拦截它们。
```javascript
let map = new Map();

let proxy = new Proxy(map, {});

proxy.set('test', 1); // Error
```

- 幸运的是，这有一种解决方法：
```javascript
let map = new Map();

let proxy = new Proxy(map, {
  get(target, prop, receiver) {
    let value = Reflect.get(...arguments);
    return typeof value == 'function' ? value.bind(target) : value;
  }
});

proxy.set('test', 1);
alert(proxy.get('test')); // 1（工作了！）
```

### 私有字段
- 类的私有字段也会发生类似的情况。
```javascript
class User {
  #name = "Guest";

  getName() {
    return this.#name;
  }
}

let user = new User();

user = new Proxy(user, {});

alert(user.getName()); // Error
```
- 解决
```javascript
class User {
  #name = "Guest";

  getName() {
    return this.#name;
  }
}

let user = new User();

user = new Proxy(user, {
  get(target, prop, receiver) {
    let value = Reflect.get(...arguments);
    return typeof value == 'function' ? value.bind(target) : value;
  }
});

alert(user.getName()); // Guest 
```
#### Proxy != target
```javascript
let allUsers = new Set();

class User {
  constructor(name) {
    this.name = name;
    allUsers.add(this);
  }
}

let user = new User("John");

alert(allUsers.has(user)); // true

user = new Proxy(user, {});

alert(allUsers.has(user)); // false
```
- 如我们所见，进行代理后，我们在 `allUsers` 中找不到 `user`，因为代理是一个不同的对象。
- Proxy 无法拦截严格相等性检查 `===`

### 可撤销 Proxy
- 一个 **可撤销** 的代理是可以被禁用的代理。
- 假设我们有一个资源，并且想随时关闭对该资源的访问。
```javascript
let object = {
  data: "Valuable data"
};

let {proxy, revoke} = Proxy.revocable(object, {});

// 将 proxy 传递到其他某处，而不是对象...
alert(proxy.data); // Valuable data

// 稍后，在我们的代码中
revoke();

// proxy 不再工作（revoked）
alert(proxy.data); // Error
```
- 对 `revoke()` 的调用会从代理中删除对目标对象的所有内部引用，因此它们之间再无连接。

```javascript
let revokes = new WeakMap();

let object = {
  data: "Valuable data"
};

let {proxy, revoke} = Proxy.revocable(object, {});

revokes.set(proxy, revoke);

// ...我们代码中的其他位置...
revoke = revokes.get(proxy);
revoke();

alert(proxy.data); // Error（revoked）
```

## Eval：执行代码字符串

- `eval` 内的代码在当前词法环境（lexical environment）中执行，因此它能访问外部变量：
```javascript
let a = 1;

function f() {
  let a = 2;

  eval('alert(a)'); // 2
}

f();
```

- `eval` 有属于自己的词法环境。因此我们不能从外部访问在 `eval` 中声明的函数和变量：
```javascript
// 提示：本教程所有可运行的示例都默认启用了严格模式 'use strict'

eval("let x = 5; function f() {}");

alert(typeof x); // undefined（没有这个变量）
// 函数 f 也不可从外部进行访问
```
- 如果不启用严格模式，`eval` 没有属于自己的词法环境，因此我们可以从外部访问变量 `x` 和函数 `f`。
### 使用 “eval”
- 现代编程中，已经很少使用 `eval` 了。人们经常说“eval 是魔鬼”。
- **如果 `eval` 中的代码没有使用外部变量，请以 `window.eval(...)` 的形式调用 `eval`：**通过这种方式，该代码便会在全局作用域内执行：

## 科里化
- 柯里化是一种函数的转换，它是指将一个函数从可调用的 `f(a, b, c)` 转换为可调用的 `f(a)(b)(c)`。
```javascript
function curry(f) { // curry(f) 执行柯里化转换
  return function(a) {
    return function(b) {
      return f(a, b);
    };
  };
}

// 用法
function sum(a, b) {
  return a + b;
}

let curriedSum = curry(sum);

alert( curriedSum(1)(2) ); // 3
```

- 柯里化更高级的实现，例如 lodash 库的 [_.curry](https://lodash.com/docs#curry)，会返回一个包装器，该包装器允许函数被正常调用或者以部分应用函数（partial）的方式调用：
```javascript
function sum(a, b) {
  return a + b;
}

let curriedSum = _.curry(sum); // 使用来自 lodash 库的 _.curry

alert( curriedSum(1, 2) ); // 3，仍可正常调用
alert( curriedSum(1)(2) ); // 3，以部分应用函数的方式调用
```

### 柯里化？目的是什么？

```javascript
// logNow 会是带有固定第一个参数的日志的部分应用函数
let logNow = log(new Date());

// 使用它
logNow("INFO", "message"); // [HH:mm] INFO message
```

### 高级柯里化实现

```javascript
function curry(func) {

  return function curried(...args) {
    if (args.length >= func.length) {
      return func.apply(this, args);
    } else {
      return function(...args2) {
        return curried.apply(this, args.concat(args2));
      }
    }
  };

}
```
```javascript
function sum(a, b, c) {
  return a + b + c;
}

let curriedSum = curry(sum);

alert( curriedSum(1, 2, 3) ); // 6，仍然可以被正常调用
alert( curriedSum(1)(2,3) ); // 6，对第一个参数的柯里化
alert( curriedSum(1)(2)(3) ); // 6，全柯里化
```

- 只允许确定参数长度的函数

### Reference Type

- 一个动态执行的方法调用可能会丢失 `this`。
```javascript
let user = {
  name: "John",
  hi() { alert(this.name); },
  bye() { alert("Bye"); }
};

user.hi(); // 正常运行

// 现在让我们基于 name 来选择调用 user.hi 或 user.bye
(user.name == "John" ? user.hi : user.bye)(); // Error!
```

### Reference type 解读
- 仔细看的话，我们可能注意到 `obj.method()` 语句中的两个操作：
	1. 首先，点 `'.'` 取了属性 `obj.method` 的值。
	2. 接着 `()` 执行了它。

```javascript
let user = {
  name: "John",
  hi() { alert(this.name); }
};

// 把获取方法和调用方法拆成两行
let hi = user.hi;
hi(); // 报错了，因为 this 的值是 undefined
```

这里 `hi = user.hi` 把函数赋值给了一个变量，接下来在最后一行它是完全独立的，所以这里没有 `this`。
**为确保 `user.hi()` 调用正常运行，JavaScript 玩了个小把戏 —— 点 `'.'` 返回的不是一个函数，而是一个特殊的 [Reference Type](https://tc39.github.io/ecma262/#sec-reference-specification-type) 的值。**

- Reference Type 的值是一个三个值的组合 `(base, name, strict)`，其中：
	- `base` 是对象。
	- `name` 是属性名。
	- `strict` 在 `use strict` 模式下为 true。
- 对属性 `user.hi` 访问的结果不是一个函数，而是一个 Reference Type 的值。
```javascript
// Reference Type 的值
(user, "hi", true)
```

- 任何例如赋值 `hi = user.hi` 等其他的操作，都会将 Reference Type 作为一个整体丢弃掉，而会取 `user.hi`（一个函数）的值并继续传递。所以任何后续操作都“丢失”了 `this`。
- `this` 的值仅在函数直接被通过点符号 `obj.method()` 或方括号 `obj['method']()` 语法（此处它们作用相同）调用时才被正确传递。

- 还有很多种解决这个问题的方式，例如 [func.bind()](https://zh.javascript.info/bind#solution-2-bind)。

## BigInt
- `BigInt` 是一种特殊的数字类型，它提供了对任意长度整数的支持。
```javascript
const bigint = 1234567890123456789012345678901234567890n;

const sameBigint = BigInt("1234567890123456789012345678901234567890");

const bigintFromNumber = BigInt(10); // 与 10n 相同
```

### 数学运算符

- 我们不可以把 bigint 和常规数字类型混合使用：
```javascript
alert(1n + 2); // Error: Cannot mix BigInt and other types
```
- 显示转换， 果 bigint 太大而数字类型无法容纳，则会截断多余的位
```javascript
let bigint = 1n;
let number = 2;

// 将 number 转换为 bigint
alert(bigint + BigInt(number)); // 3

// 将 bigint 转换为 number
alert(Number(bigint) + number); // 3
```
- BigInt 不支持一元加法
```javascript
let bigint = 1n;

alert( +bigint ); // error
```

### 比较运算符
- 比较运算符，例如 `<` 和 `>`，使用它们来对 bigint 和 number 类型的数字进行比较没有问题：
- 由于 number 和 bigint 属于不同类型，它们可能在进行 `==` 比较时相等，但在进行 `===`（严格相等）比较时不相等：


### 布尔运算

- 例如，在 `if` 中，bigint `0n` 为假，其他值为 `true`：
```javascript
alert( 1n || 2 ); // 1（1n 被认为是真）

alert( 0n || 2 ); // 2（0n 被认为是假）
```

### Polyfill
- 目前并没有一个众所周知的好用的 polyfill。
- 不过，[JSBI](https://github.com/GoogleChromeLabs/jsbi) 库的开发者提出了另一种解决方案。

## Unicode —— 字符串内幕

- JavaScript 允许我们通过下述三种表示方式之一将一个字符以其十六进制 Unicode 编码的方式插入到字符串中：
	- \xXX  `XX` 必须是介于 `00` 与 `FF` 之间的两位十六进制数，`\xXX` 表示 Unicode 编码为 `XX` 的字符。因为 `\xXX` 符号只支持两位十六进制数，所以它只能用于前 256 个 Unicode 字符。
	```javascript
		alert( "\x7A" ); // z
		alert( "\xA9" ); // © (版权符号)
	```
	- `\uXXXX` `XXXX` 必须是 4 位十六进制数，值介于 `0000` 和 `FFFF` 之间。此时，`\uXXXX` 便表示 Unicode 编码为 `XXXX` 的字符。
	```javascript
	    alert( "\u00A9" ); // ©, 等同于 \xA9，只是使用了四位十六进制数表示而已
	    alert( "\u044F" ); // я（西里尔字母）
	    alert( "\u2191" ); // ↑（上箭头符号）
	```
	- \u{X…XXXXXX} `X…XXXXXX` 必须是介于 `0` 和 `10FFFF`（Unicode 定义的最高码位）之间的 1 到 6 个字节的十六进制值。这种表示方式让我们能够轻松地表示所有现有的 Unicode 字符。
	 ```javascript
    alert( "\u{20331}" ); // 佫, 一个不常见的中文字符（长 Unicode）
    alert( "\u{1F60D}" ); // 😍, 一个微笑符号（另一个长 Unicode）
    ```

### 代理对
- 所有常用字符都有对应的 2 字节长度的编码（4 位十六进制数）
- 大多数欧洲语言的字母、数字、以及基本统一的 CJK 表意文字集（CJK —— 来自中文、日文和韩文书写系统）中的字母，均有对应的 2 字节长度的 Unicode 编码。
- 需要使用超过 2 个字节长度来表示的稀有符号，我们则使用一对 2 字节长度的字符编码，它被称为“代理对”（surrogate pair）。
- 这种做也有副作用 —— 这些符号的长度为 `2`：

```javascript
alert( '𝒳'.length ); // 2, 大写的数学符号 X
alert( '😂'.length ); // 2, 笑哭的表情
alert( '𩷶'.length ); // 2, 一个少见的中文字符
```

- JavaScript 新增了 [String.fromCodePoint](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/fromCodePoint) 和 [str.codePointAt](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/codePointAt) 这两个方法来处理代理对。
```javascript
// charCodeAt 不会考虑代理对，所以返回了 𝒳 前半部分的编码:

alert( '𝒳'.charCodeAt(0).toString(16) ); // d835

// codePointAt 可以正确处理代理对
alert( '𝒳'.codePointAt(0).toString(16) ); // 1d4b3，读取到了完整的代理对
```

- 注意：在任意点拆分字符串是很危险的
```javascript
alert( 'hi 😂'.slice(0, 4) ); //  hi [?]
```

### 变音符号和规范化
- 们在 `S` 后附加上特殊的“上方的点”字符（编码为 `\u0307`），则显示为 Ṡ。
```javascript
alert( 'S\u0307' ); // Ṡ
```
```javascript
alert( 'S\u0307\u0323' ); // Ṩ
```

- 一个有趣的问题：两个字符可能在视觉上看起来相同，但却使用的是不同的 Unicode 组合。
```javascript
let s1 = 'S\u0307\u0323'; // Ṩ, S + 上方点符号 + 下方点符号
let s2 = 'S\u0323\u0307'; // Ṩ, S + 下方点符号 + 上方点符号

alert( `s1: ${s1}, s2: ${s2}` );

alert( s1 == s2 ); // 尽管这两个字符在我们看来是相通的，但结果却是 false
```

- “Unicode 规范化”算法可以解决这个问题 可以借助 [str.normalize()](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/normalize) 实现这一点。
```javascript
alert( "S\u0307\u0323".normalize() == "S\u0323\u0307".normalize() ); // true
```

```javascript
alert( "S\u0307\u0323".normalize().length ); // 1

alert( "S\u0307\u0323".normalize() == "\u1e68" ); // true
```
