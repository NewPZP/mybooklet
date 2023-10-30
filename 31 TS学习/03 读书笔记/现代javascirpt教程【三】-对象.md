## 对象
- 我们可以用下面两种语法中的任一种来创建一个空的对象（“空柜子”）：
```javascript
let user = new Object(); // “构造函数” 的语法
let user = {};  // “字面量” 的语法
```
### 文本属性
```javascript
let user = {     // 一个对象
  name: "John",  // 键 "name"，值 "John"
  age: 30        // 键 "age"，值 30
};
```

- 访问
```javascript
// 读取文件的属性：
alert( user.name ); // John
alert( user.age ); // 30
```
- 添加
```javascript
user.isAdmin = true;
```
- 移除
```javascript
delete user.age;
```
- 多字符名作为属性
```javascript
let user = {
  name: "John",
  age: 30,
  "likes birds": true  // 多词属性名必须加引号
};
```
### 方括号
- 对于多词属性，点操作就不能用了
- 所以用方括号
```javascript
let user = {};

// 设置
user["likes birds"] = true;

// 读取
alert(user["likes birds"]); // true

// 删除
delete user["likes birds"];

```
- 点是不能像下面这样用的
```javascript
let key = "likes birds";

// 跟 user["likes birds"] = true; 一样
user[key] = true;
```
### 计算属性

- 当创建一个对象时，我们可以在对象字面量中使用方括号。这叫做 **计算属性**。
```javascript
let fruit = prompt("Which fruit to buy?", "apple");

let bag = {
  [fruit]: 5, // 属性名是从 fruit 变量中得到的
};

alert( bag.apple ); // 5 如果 fruit="apple"
```

```javascript
let fruit = 'apple';
let bag = {
  [fruit + 'Computers']: 5 // bag.appleComputers = 5
};
```

### 属性值简写

```javascript
function makeUser(name, age) {
  return {
    name: name,
    age: age,
    // ……其他的属性
  };
}

let user = makeUser("John", 30);
alert(user.name); // John
```
- 上面可简写成
```javascript
function makeUser(name, age) {
  return {
    name, // 与 name: name 相同
    age,  // 与 age: age 相同
    // ...
  };
}
```

### 属性名称限制

- 变量名不能是编程语言的某个保留字，如 “for”、“let”、“return” 等…… 但对象的属性名并不受此限制
- 其他类型会被自动地转换为字符串。
```javascript
let obj = {
  0: "test" // 等同于 "0": "test"
};

// 都会输出相同的属性（数字 0 被转为字符串 "0"）
alert( obj["0"] ); // test
alert( obj[0] ); // test (相同的属性)
```
- 一个名为 `__proto__` 的属性。我们不能将它设置为一个非对象的值：
```javascript
let obj = {};
obj.__proto__ = 5; // 分配一个数字
alert(obj.__proto__); // [object Object] —— 值为对象，与预期结果不同
```

### 属性存在性测试 in
```javascript
let user = { name: "John", age: 30 };

alert( "age" in user ); // true，user.age 存在
alert( "blabla" in user ); // false，user.blabla 不存在。
```
- 大部分情况下与 `undefined` 进行比较来判断就可以了，下面是例外
```javascript
let obj = {
  test: undefined
};

alert( obj.test ); // 显示 undefined，所以属性不存在？

alert( "test" in obj ); // true，属性存在！
```

### "for..in" 循环

```javascript
let user = {
  name: "John",
  age: 30,
  isAdmin: true
};

for (let key in user) {
  // keys
  alert( key );  // name, age, isAdmin
  // 属性键的值
  alert( user[key] ); // John, 30, true
}
```

### 像对象一样排序

- “有特别的顺序”：整数属性会被进行排序，其他属性则按照创建的顺序显示。
```javascript
let codes = {
  "49": "Germany",
  "41": "Switzerland",
  "44": "Great Britain",
  // ..,
  "1": "USA"
};

for(let code in codes) {
  alert(code); // 1, 41, 44, 49
}
```
```javascript
let user = {
  name: "John",
  surname: "Smith"
};
user.age = 25; // 增加一个

// 非整数属性是按照创建的顺序来排列的
for (let prop in user) {
  alert( prop ); // name, surname, age
}
```
- 解决电话号码前缀安装期望顺序排序
```javascript
let codes = {
  "+49": "Germany",
  "+41": "Switzerland",
  "+44": "Great Britain",
  // ..,
  "+1": "USA"
};

for (let code in codes) {
  alert( +code ); // 49, 41, 44, 1
}
```

## 对象引用复制

- **赋值了对象的变量存储的不是对象本身，而是该对象“在内存中的地址” —— 换句话说就是对该对象的“引用”。**
```javascript
let user = { name: 'John' };

let admin = user;

admin.name = 'Pete'; // 通过 "admin" 引用来修改

alert(user.name); // 'Pete'，修改能通过 "user" 引用看到
```

### 通过引用来比较

```javascript
let a = {};
let b = a; // 复制引用

alert( a == b ); // true，都引用同一对象
alert( a === b ); // true
```
```javascript
let a = {};
let b = {}; // 两个独立的对象

alert( a == b ); // false
```
### 克隆与合并，Object.assign

```javascript
let user = {
  name: "John",
  age: 30
};

let clone = {}; // 新的空对象

// 将 user 中所有的属性拷贝到其中
for (let key in user) {
  clone[key] = user[key];
}

// 现在 clone 是带有相同内容的完全独立的对象
clone.name = "Pete"; // 改变了其中的数据

alert( user.name ); // 原来的对象中的 name 属性依然是 John
```
- 我们也可以使用 [Object.assign](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/assign) 方法来达成同样的效果。
```javascript
Object.assign(dest, [src1, src2, src3...])
```
- 用它来合并多个对象：
```javascript
let user = { name: "John" };

let permissions1 = { canView: true };
let permissions2 = { canEdit: true };

// 将 permissions1 和 permissions2 中的所有属性都拷贝到 user 中
Object.assign(user, permissions1, permissions2);

// 现在 user = { name: "John", canView: true, canEdit: true }
```

- 如果被拷贝的属性的属性名已经存在，那么它会被覆盖：
```javascript
let user = { name: "John" };

Object.assign(user, { name: "Pete" });

alert(user.name); // 现在 user = { name: "Pete" }
```
其他克隆对象的方法，例如使用 [spread 语法](https://zh.javascript.info/rest-parameters-spread) `clone = {...user}`

### 深层克隆
- 当对象的属性不都是原始类型时

```javascript
let user = {
  name: "John",
  sizes: {
    height: 182,
    width: 50
  }
};

let clone = Object.assign({}, user);

alert( user.sizes === clone.sizes ); // true，同一个对象

// user 和 clone 分享同一个 sizes
user.sizes.width++;       // 通过其中一个改变属性值
alert(clone.sizes.width); // 51，能从另外一个获取到变更后的结果
```
- 为了解决这个问题，并让 `user` 和 `clone` 成为两个真正独立的对象，我们应该使用一个拷贝循环来检查 `user[key]` 的每个值，如果它是一个对象，那么也复制它的结构。这就是所谓的“深拷贝”。
- 可以采用现有的实现，例如 [lodash](https://lodash.com/) 库的 [_.cloneDeep(obj)](https://lodash.com/docs#cloneDeep)。

## 垃圾回收
### 可达性
- “可达”值是那些以某种方式可访问或可用的值。它们一定是存储在内存中的。
1.  这里列出固有的可达值的基本集合，这些值明显不能被释放。
    比方说：
    -   当前执行的函数，它的局部变量和参数。
    -   当前嵌套调用链上的其他函数、它们的局部变量和参数。
    -   全局变量。
    -   （还有一些内部的）
    这些值被称作 **根（roots）**。
2. 如果一个值可以通过引用链从根访问任何其他值，则认为该值是可达的。   
### 互相关联的对象
```javascript
function marry(man, woman) {
  woman.husband = man;
  man.wife = woman;

  return {
    father: man,
    mother: woman
  }
}

let family = marry({
  name: "John"
}, {
  name: "Ann"
});
```
```javascript
delete family.father;
delete family.mother.husband;
```
- John 现在是不可达的，并且将被从内存中删除
### 无法到达的岛屿
```javascript
family = null;
```
- John 和 Ann 仍然连着，都有传入的引用。但是，这样还不够。前面说的 `"family"` 对象已经不再与根相连，没有了外部对其的引用，所以它变成了一座“孤岛”，并且将被从内存中删除。

### 内部算法   
- “mark-and-sweep”
- 大致就是 遍历整棵树，标记起来，没有标记的就会被回收
- 优化
	- **分代收集（Generational collection）**
	- **增量收集（Incremental collection）**
	- **闲时收集（Idle-time collection）**

### 深入请参考
-  [V8 之旅：垃圾回收](http://jayconrod.com/posts/55/a-tour-of-v8-garbage-collection)。
- 《The Garbage Collection Handbook: The Art of Automatic Memory Management》
- [V8 博客](http://v8project.blogspot.com/)
-  [Vyacheslav Egorov](http://mrale.ph/)

## 对象方法 与this
### 方法
```javascript
let user = {
  name: "John",
  age: 30
};

user.sayHi = function() {
  alert("Hello!");
};

user.sayHi(); // Hello!
```
- 声明方式
```javascript
let user = {
  // ...
};

// 首先，声明函数
function sayHi() {
  alert("Hello!");
}

// 然后将其作为一个方法添加
user.sayHi = sayHi;

user.sayHi(); // Hello!
```

### 方法简写
```javascript
// 这些对象作用一样

user = {
  sayHi: function() {
    alert("Hello");
  }
};

// 方法简写看起来更好，对吧？
let user = {
  sayHi() { // 与 "sayHi: function(){...}" 一样
    alert("Hello");
  }
};
```

### 方法中的this
```javascript
let user = {
  name: "John",
  age: 30,

  sayHi() {
    // "this" 指的是“当前的对象”
    alert(this.name);
  }

};

user.sayHi(); // John
```
- 也可以在不使用 `this` 的情况下，通过外部变量名来引用它，但这样的代码是不可靠的。如果我们决定将 `user` 复制给另一个变量.....
```javascript
let user = {
  name: "John",
  age: 30,

  sayHi() {
    alert(user.name); // "user" 替代 "this"
  }

};
```

### this 不受限制

- `this` 的值是在代码运行时计算出来的，它取决于代码上下文。
```javascript
let user = { name: "John" };
let admin = { name: "Admin" };

function sayHi() {
  alert( this.name );
}

// 在两个对象中使用相同的函数
user.f = sayHi;
admin.f = sayHi;

// 这两个调用有不同的 this 值
// 函数内部的 "this" 是“点符号前面”的那个对象
user.f(); // John（this == user）
admin.f(); // Admin（this == admin）

admin['f'](); // Admin（使用点符号或方括号语法来访问这个方法，都没有关系。）
```
- 没有对象的情况下调用， 严格模式下的 `this` 值为 `undefined`。如果我们尝试访问 `this.name`，将会报错。在非严格模式的情况下，`this` 将会是 **全局对象**
```javascript
function sayHi() {
  alert(this);
}

sayHi(); // undefined
```
### 箭头函数没有自己的 “this”
- 箭头函数有些特别：它们没有自己的 `this`。如果我们在这样的函数中引用 `this`，`this` 值取决于外部“正常的”函数。
```javascript
let user = {
  firstName: "Ilya",
  sayHi() {
    let arrow = () => alert(this.firstName);
    arrow();
  }
};

user.sayHi(); // Ilya
```


## 构造器和 new

### 构造函数
构造函数在技术上是常规函数。不过有两个约定：
1.  它们的命名以大写字母开头。
2.  它们只能由 `"new"` 操作符来执行。

```javascript
function User(name) {
  this.name = name;
  this.isAdmin = false;
}

let user = new User("Jack");

alert(user.name); // Jack
alert(user.isAdmin); // false
```
当一个函数被使用 `new` 操作符执行时，它按照以下步骤：
1.  一个新的空对象被创建并分配给 `this`。
2.  函数体执行。通常它会修改 `this`，为其添加新的属性。
3.  返回 `this` 的值。
```javascript
function User(name) {
  // this = {};（隐式创建）

  // 添加属性到 this
  this.name = name;
  this.isAdmin = false;

  // return this;（隐式返回）
}
```

- 不重用时可以使用 new function
```javascript
// 创建一个函数并立即使用 new 调用它
let user = new function() {
  this.name = "John";
  this.isAdmin = false;

  // ……用于用户创建的其他代码
  // 也许是复杂的逻辑和语句
  // 局部变量等
};
```

### 构造器模式测试 new.target
在一个函数内部，我们可以使用 `new.target` 属性来检查它是否被使用 `new` 进行调用了。
```javascript
function User(name) {
  if (!new.target) { // 如果你没有通过 new 运行我
    return new User(name); // ……我会给你添加 new
  }

  this.name = name;
}

let john = User("John"); // 将调用重定向到新用户
alert(john.name); // John
```

### 构造器return
- 带有对象的 `return` 返回该对象，在所有其他情况下返回 `this`。
```javascript
function BigUser() {

  this.name = "John";

  return { name: "Godzilla" };  // <-- 返回这个对象
}

alert( new BigUser().name );  // Godzilla，得到了那个对象
```
- 这里有一个 `return` 为空的例子（或者我们可以在它之后放置一个原始类型，没有什么影响）：
```javascript
function SmallUser() {

  this.name = "John";

  return; // <-- 返回 this
}

alert( new SmallUser().name );  // John
```
- 如果没有参数，我们可以省略 `new` 后的括号， 但不是一个好风格：
```javascript
let user = new User; // <-- 没有参数
// 等同于
let user = new User();
```

### 构造器中的方法

```javascript
function User(name) {
  this.name = name;

  this.sayHi = function() {
    alert( "My name is: " + this.name );
  };
}

let john = new User("John");

john.sayHi(); // My name is: John

/*
john = {
   name: "John",
   sayHi: function() { ... }
}
*/
```


## 可选链 ？
- 可选链 `?.` 是一种访问嵌套对象属性的安全的方式。即使中间的属性不存在，也不会出现错误。
- 如果可选链 ?. 前面的值为 undefined 或者 null，它会停止运算并返回 undefined。
```javascript
let user = {}; // user 没有 address 属性

alert( user?.address?.street ); // undefined（不报错）
```
- 不要过度使用可选链
- `?.` 前的变量必须已声明
### 短路效应

```javascript
let user = null;
let x = 0;

user?.sayHi(x++); // 没有 "user"，因此代码执行没有到达 sayHi 调用和 x++

alert(x); // 0，值没有增加
```

### 其它变体  ?.()，?.[]

- 将 `?.()` 用于调用一个可能不存在的函数。
```javascript
let userAdmin = {
  admin() {
    alert("I am admin");
  }
};

let userGuest = {};

userAdmin.admin?.(); // I am admin

userGuest.admin?.(); // 啥都没发生（没有这样的方法）
```
- 语法 `?.[]` 也可以使用。跟前面的例子类似，它允许从一个可能不存在的对象上安全地读取属性。
```javascript
let key = "firstName";

let user1 = {
  firstName: "John"
};

let user2 = null;

alert( user1?.[key] ); // John
alert( user2?.[key] ); // undefined
```
- delete中使用
```javascript
delete user?.name; // 如果 user 存在，则删除 user.name
```
- 我们可以使用 `?.` 来安全地读取或删除，但不能写入
```javascript
let user = null;

user?.name = "John"; // Error，不起作用
// 因为它在计算的是：undefined = "John"
```

## symbol类型
根据规范，只有两种原始类型可以用作对象属性键：
-   字符串类型
-   symbol 类型
否则，如果使用另一种类型，例如数字，它会被自动转换为字符串。

### symbol
- “symbol” 值表示唯一的标识符。
- symbol 保证是唯一的。即使我们创建了许多具有相同描述的 symbol，它们的值也是不同。描述只是一个标签，不影响任何东西。
```javascript
// id 是描述为 "id" 的 symbol
let id = Symbol("id");
```
```javascript
let id1 = Symbol("id");
let id2 = Symbol("id");

alert(id1 == id2); // false
```
- symbol 不会被自动转换为字符串
```javascript
let id = Symbol("id");
alert(id); // 类型错误：无法将 symbol 值转换为字符串。
```

### “隐藏”属性
```javascript
let user = { // 属于另一个代码
  name: "John"
};

let id = Symbol("id");

user[id] = 1;

alert( user[id] ); // 我们可以使用 symbol 作为键来访问数据
```
- 由于 `user` 对象属于另一个代码库，所以向它们添加字段是不安全的，因为我们可能会影响代码库中的其他预定义行为。但 symbol 属性不会被意外访问到。第三方代码不会知道新定义的 symbol，因此将 symbol 添加到 `user` 对象是安全的。
- 可以避免下面这种情况
```javascript
let user = { name: "John" };

// 我们的脚本使用了 "id" 属性。
user.id = "Our id value";

// ……另一个脚本也想将 "id" 用于它的目的……

user.id = "Their id value"
// 砰！无意中被另一个脚本重写了 id！
```
### 对象字面量中的 symbol
- 要在对象字面量 `{...}` 中使用 symbol，则需要使用方括号把它括起来。
```javascript
let id = Symbol("id");

let user = {
  name: "John",
  [id]: 123 // 而不是 "id"：123
};
```
### symbol 在 for…in 中会被跳过
```javascript
let id = Symbol("id");
let user = {
  name: "John",
  age: 30,
  [id]: 123
};

for (let key in user) alert(key); // name, age（没有 symbol）

// 使用 symbol 任务直接访问
alert("Direct: " + user[id]); // Direct: 123
```
-  相反，Object.assign 会同时复制字符串和 symbol 属性：
```javascript
let id = Symbol("id");
let user = {
  [id]: 123
};

let clone = Object.assign({}, user);

alert( clone[id] ); // 123
```
### 全局 symbol

```javascript
// 从全局注册表中读取
let id = Symbol.for("id"); // 如果该 symbol 不存在，则创建它

// 再次读取（可能是在代码中的另一个位置）
let idAgain = Symbol.for("id");

// 相同的 symbol
alert( id === idAgain ); // true
```

注册表内的 symbol 被称为 **全局 symbol**。如果我们想要一个应用程序范围内的 symbol，可以在代码中随处访问 —— 这就是它们的用途。

### Symbol.keyFor
- 对于全局 symbol，`Symbol.for(key)` 按名字返回一个 symbol。相反，通过全局 symbol 返回一个名字，我们可以使用 `Symbol.keyFor(sym)`：
```javascript
// 通过 name 获取 symbol
let sym = Symbol.for("name");
let sym2 = Symbol.for("id");

// 通过 symbol 获取 name
alert( Symbol.keyFor(sym) ); // name
alert( Symbol.keyFor(sym2) ); // id
```
- 只适用于全局Symbol
```javascript
let globalSymbol = Symbol.for("name");
let localSymbol = Symbol("name");

alert( Symbol.keyFor(globalSymbol) ); // name，全局 symbol
alert( Symbol.keyFor(localSymbol) ); // undefined，非全局

alert( localSymbol.description ); // name
```
### 系统 symbol
它们都被列在了 [众所周知的 symbol](https://tc39.github.io/ecma262/#sec-well-known-symbols) 表的规范中：
-   `Symbol.hasInstance`
-   `Symbol.isConcatSpreadable`
-   `Symbol.iterator`
-   `Symbol.toPrimitive`
-   ……等等。
## 对象 原始值转换
- 限制 无法实现对象的相加相减等运算符操作

### 转换规则

### hint
类型转换在各种情况下有三种变体。它们被称为 “hint”，在 [规范](https://tc39.github.io/ecma262/#sec-toprimitive) 所述：
- "string"
```javascript
// 输出
alert(obj);

// 将对象作为属性键
anotherObj[obj] = 123;
```

- "number"
```javascript
// 显式转换
let num = Number(obj);

// 数学运算（除了二元加法）
let n = +obj; // 一元加法
let delta = date1 - date2;

// 小于/大于的比较
let greater = user1 > user2;
```

- `"default"`

```javascript
// 二元加法使用默认 hint
let total = obj1 + obj2;

// obj == number 使用默认 hint
if (user == 1) { ... };
```
- **为了进行转换，JavaScript 尝试查找并调用三个对象方法：**
	1.  调用 `obj[Symbol.toPrimitive](hint)` —— 带有 symbol 键 `Symbol.toPrimitive`（系统 symbol）的方法，如果这个方法存在的话，
	2.  否则，如果 hint 是 `"string"` —— 尝试调用 `obj.toString()` 或 `obj.valueOf()`，无论哪个存在。
	3.  否则，如果 hint 是 `"number"` 或 `"default"` —— 尝试调用 `obj.valueOf()` 或 `obj.toString()`，无论哪个存在。

### Symbol.toPrimitive

```javascript
let user = {
  name: "John",
  money: 1000,

  [Symbol.toPrimitive](hint) {
    alert(`hint: ${hint}`);
    return hint == "string" ? `{name: "${this.name}"}` : this.money;
  }
};

// 转换演示：
alert(user); // hint: string -> {name: "John"}
alert(+user); // hint: number -> 1000
alert(user + 500); // hint: default -> 1500
```

### toString/valueOf
- 如果没有 `Symbol.toPrimitive`，那么 JavaScript 将尝试寻找 `toString` 和 `valueOf` 方法：
	-   对于 `"string"` hint：调用 `toString` 方法，如果它不存在，则调用 `valueOf` 方法（因此，对于字符串转换，优先调用 `toString`）。
	-   对于其他 hint：调用 `valueOf` 方法，如果它不存在，则调用 `toString` 方法（因此，对于数学运算，优先调用 `valueOf` 方法）。


```javascript
let user = {name: "John"};

alert(user); // [object Object]
alert(user.valueOf() === user); // true
```

```javascript
let user = {
  name: "John",
  money: 1000,

  // 对于 hint="string"
  toString() {
    return `{name: "${this.name}"}`;
  },

  // 对于 hint="number" 或 "default"
  valueOf() {
    return this.money;
  }

};

alert(user); // toString -> {name: "John"}
alert(+user); // valueOf -> 1000
alert(user + 500); // valueOf -> 1500
```

- 如果没有 `Symbol.toPrimitive` 和 `valueOf`，`toString` 将处理所有原始转换。

### 转换可以返回任何原始类型
- 唯一强制性的事情是：这些方法必须返回一个原始值，而不是对象。

### 进一步的转换

如果我们将对象作为参数传递，则会出现两个运算阶段：
1.  对象被转换为原始值（通过前面我们描述的规则）。
2.  如果还需要进一步计算，则生成的原始值会被进一步转换。

```javascript
let obj = {
  // toString 在没有其他方法的情况下处理所有转换
  toString() {
    return "2";
  }
};

alert(obj * 2); // 4，对象被转换为原始值字符串 "2"，之后它被乘法转换为数字 2。
```
- 二元加法在同样的情况下会将其连接成字符串，因为它更愿意接受字符串：
```javascript
let obj = {
  toString() {
    return "2";
  }
};

alert(obj + 2); // 22（"2" + 2）被转换为原始值字符串 => 级联
```