## Class 基本语法

### class 语法
- 但在现代 JavaScript 中，还有一个更高级的“类（class）”构造方式
```javascript
class MyClass {
  // class 方法
  constructor() { ... }
  method1() { ... }
  method2() { ... }
  method3() { ... }
  ...
}
```
- 类的方法之间没有逗号

### 什么是 class？
- 在 JavaScript 中，类是一种函数。

```javascript
class User {
  constructor(name) { this.name = name; }
  sayHi() { alert(this.name); }
}

// class 是一个函数
alert(typeof User); // function

// ...或者，更确切地说，是 constructor 方法
alert(User === User.prototype.constructor); // true

// 方法在 User.prototype 中，例如：
alert(User.prototype.sayHi); // sayHi 方法的代码

// 在原型中实际上有两个方法
alert(Object.getOwnPropertyNames(User.prototype)); // constructor, sayHi
```
- 上面完成以下事情
	1. 创建一个名为 `User` 的函数，该函数成为类声明的结果。该函数的代码来自于 `constructor` 方法（如果我们不编写这种方法，那么它就被假定为空）。
	2. 存储类中的方法，例如 `User.prototype` 中的 `sayHi`。

### 不仅仅是语法糖
- 用函数方式重写
```javascript
// 用纯函数重写 class User

// 1. 创建构造器函数
function User(name) {
  this.name = name;
}
// 函数的原型（prototype）默认具有 "constructor" 属性，
// 所以，我们不需要创建它

// 2. 将方法添加到原型
User.prototype.sayHi = function() {
  alert(this.name);
};

// 用法：
let user = new User("John");
user.sayHi();
```
- 区别
	- 首先，通过 `class` 创建的函数具有特殊的内部属性标记 `[[IsClassConstructor]]: true`。因此，它与手动创建并不完全相同。
	- 类方法不可枚举。 类定义将 `"prototype"` 中的所有方法的 `enumerable` 标志设置为 `false`。
	-  类总是使用 `use strict`。 在类构造中的所有代码都将自动进入严格模式。
### 类表达式
- 就像函数一样，类可以在另外一个表达式中被定义，被传递，被返回，被赋值等。
```javascript
let User = class {
  sayHi() {
    alert("Hello");
  }
};
```

- 如果类表达式有名字，那么该名字仅在类内部可见：
```javascript
// “命名类表达式（Named Class Expression）”
// (规范中没有这样的术语，但是它和命名函数表达式类似)
let User = class MyClass {
  sayHi() {
    alert(MyClass); // MyClass 这个名字仅在类内部可见
  }
};

new User().sayHi(); // 正常运行，显示 MyClass 中定义的内容

alert(MyClass); // error，MyClass 在外部不可见
```

- 动态地“按需”创建类
```javascript
function makeClass(phrase) {
  // 声明一个类并返回它
  return class {
    sayHi() {
      alert(phrase);
    }
  };
}

// 创建一个新的类
let User = makeClass("Hello");

new User().sayHi(); // Hello
```

### Getters/setters

```javascript
class User {

  constructor(name) {
    // 调用 setter
    this.name = name;
  }

  get name() {
    return this._name;
  }

  set name(value) {
    if (value.length < 4) {
      alert("Name is too short.");
      return;
    }
    this._name = value;
  }

}

let user = new User("John");
alert(user.name); // John

user = new User(""); // Name is too short.
```

### 计算属性名称 `[…]`
```javascript
class User {

  ['say' + 'Hi']() {
    alert("Hello");
  }

}

new User().sayHi();
```

### class字段
- 旧的浏览器可能需要 polyfill
- “类字段”是一种允许添加任何属性的语法。
```javascript
class User {
  name = "John";

  sayHi() {
    alert(`Hello, ${this.name}!`);
  }
}

new User().sayHi(); // Hello, John!
```
- 类字段重要的不同之处在于，它们会在每个独立对象中被设好，而不是设在 `User.prototype`：

### 使用类字段制作绑定方法

- JavaScript 中的函数具有动态的 `this`。它取决于调用上下文。因此，如果一个对象方法被传递到某处，或者在另一个上下文中被调用，则 `this` 将不再是对其对象的引用。

```javascript
class Button {
  constructor(value) {
    this.value = value;
  }

  click() {
    alert(this.value);
  }
}

let button = new Button("hello");

setTimeout(button.click, 1000); // undefined
```

- 解决
```javascript
class Button {
  constructor(value) {
    this.value = value;
  }
  click = () => {
    alert(this.value);
  }
}

let button = new Button("hello");

setTimeout(button.click, 1000); // hello
```

## 类继承

### “extends” 关键字
```javascript
class Animal {
  constructor(name) {
    this.speed = 0;
    this.name = name;
  }
  run(speed) {
    this.speed = speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }
  stop() {
    this.speed = 0;
    alert(`${this.name} stands still.`);
  }
}

let animal = new Animal("My animal");
```
```javascript
class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }
}

let rabbit = new Rabbit("White Rabbit");

rabbit.run(5); // White Rabbit runs with speed 5.
rabbit.hide(); // White Rabbit hides!
```

- 在内部，关键字 `extends` 使用了很好的旧的原型机制进行工作。它将 `Rabbit.prototype.[[Prototype]]` 设置为 `Animal.prototype`。
- 在 `extends` 后允许任意表达式
```javascript
function f(phrase) {
  return class {
    sayHi() { alert(phrase); }
  };
}

class User extends f("Hello") {}

new User().sayHi(); // Hello
```

### 重写方法
```javascript
class Animal {

  constructor(name) {
    this.speed = 0;
    this.name = name;
  }

  run(speed) {
    this.speed = speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }

  stop() {
    this.speed = 0;
    alert(`${this.name} stands still.`);
  }

}

class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }

  stop() {
    super.stop(); // 调用父类的 stop
    this.hide(); // 然后 hide
  }
}

let rabbit = new Rabbit("White Rabbit");

rabbit.run(5); // White Rabbit runs with speed 5.
rabbit.stop(); // White Rabbit stands still. White Rabbit hides!
```
- 箭头函数没有 `super`

### 重写 constructor

- 根据 [规范](https://tc39.github.io/ecma262/#sec-runtime-semantics-classdefinitionevaluation)，如果一个类扩展了另一个类并且没有 `constructor`，那么将生成下面这样的“空” `constructor`：
```javascript
class Rabbit extends Animal {
  // 为没有自己的 constructor 的扩展类生成的
  constructor(...args) {
    super(...args);
  }
}
```

- **继承类的 constructor 必须调用 `super(...)`，并且 (!) 一定要在使用 `this` 之前调用。**
```javascript
class Animal {
  constructor(name) {
    this.speed = 0;
    this.name = name;
  }
  // ...
}

class Rabbit extends Animal {

  constructor(name, earLength) {
    this.speed = 0;
    this.name = name;
    this.earLength = earLength;
  }

  // ...
}

// 不工作！
let rabbit = new Rabbit("White Rabbit", 10); // Error: this is not defined.
```

- 在 JavaScript 中，继承类（所谓的“派生构造器”，英文为 “derived constructor”）的构造函数与其他函数之间是有区别的。派生构造器具有特殊的内部属性 `[[ConstructorKind]]:"derived"`。这是一个特殊的内部标签。
- 该标签会影响它的 `new` 行为：
	- 当通过 `new` 执行一个常规函数时，它将创建一个空对象，并将这个空对象赋值给 `this`。
	- 但是当继承的 constructor 执行时，它不会执行此操作。它期望父类的 constructor 来完成这项工作。

### 重写类字段: 一个棘手的注意要点
```javascript
class Animal {
  name = 'animal';

  constructor() {
    alert(this.name); // (*)
  }
}

class Rabbit extends Animal {
  name = 'rabbit';
}

new Animal(); // animal
new Rabbit(); // animal
```

- 这里，`Rabbit` 继承自 `Animal`，并且用它自己的值重写了 `name` 字段。因为 `Rabbit` 中没有自己的构造器，所以 `Animal` 的构造器被调用了。
- **换句话说，父类构造器总是会使用它自己字段的值，而不是被重写的那一个。**
```javascript
class Animal {
  showName() {  // 而不是 this.name = 'animal'
    alert('animal');
  }

  constructor() {
    this.showName(); // 而不是 alert(this.name);
  }
}

class Rabbit extends Animal {
  showName() {
    alert('rabbit');
  }
}

new Animal(); // animal
new Rabbit(); // rabbit
```
- 如果出问题了，我们可以通过使用方法或者 getter/setter 替代类字段，来修复这个问题。
### 深入：内部探究和 `[[HomeObject]]`

- JavaScript 为函数添加了一个特殊的内部属性：`[[HomeObject]]`。当一个函数被定义为类或者对象方法时，它的 `[[HomeObject]]` 属性就成为了该对象。
```javascript
let animal = {
  name: "Animal",
  eat() {         // animal.eat.[[HomeObject]] == animal
    alert(`${this.name} eats.`);
  }
};

let rabbit = {
  __proto__: animal,
  name: "Rabbit",
  eat() {         // rabbit.eat.[[HomeObject]] == rabbit
    super.eat();
  }
};

let longEar = {
  __proto__: rabbit,
  name: "Long Ear",
  eat() {         // longEar.eat.[[HomeObject]] == longEar
    super.eat();
  }
};

// 正确执行
longEar.eat();  // Long Ear eats.
```

#### 方法并不是“自由”的
- 函数通常都是“自由”的，并没有绑定到 JavaScript 中的对象。正因如此，它们可以在对象之间复制，并用另外一个 `this` 调用它。
- `[[HomeObject]]` 的存在违反了这个原则，因为方法记住了它们的对象。`[[HomeObject]]` 不能被更改，所以这个绑定是永久的。

```javascript
let animal = {
  sayHi() {
    alert(`I'm an animal`);
  }
};

// rabbit 继承自 animal
let rabbit = {
  __proto__: animal,
  sayHi() {
    super.sayHi();
  }
};

let plant = {
  sayHi() {
    alert("I'm a plant");
  }
};

// tree 继承自 plant
let tree = {
  __proto__: plant,
  sayHi: rabbit.sayHi // (*)
};

tree.sayHi();  // I'm an animal (?!?)
```

#### 方法，不是函数属性
- `[[HomeObject]]` 是为类和普通对象中的方法定义的。但是对于对象而言，方法必须确切指定为 `method()`，而不是 `"method: function()"`。

```javascript
let animal = {
  eat: function() { // 这里是故意这样写的，而不是 eat() {...
    // ...
  }
};

let rabbit = {
  __proto__: animal,
  eat: function() {
    super.eat();
  }
};

rabbit.eat();  // 错误调用 super（因为这里没有 [[HomeObject]]）
```

## 静态属性，静态方法

```javascript
class User {
  static staticMethod() {
    alert(this === User);
  }
}

User.staticMethod(); // true
```
```javascript
class User { }

User.staticMethod = function() {
  alert(this === User);
};

User.staticMethod(); // true
```

- 静态方法不适用于单个对象
```javascript
// ...
article.createTodays(); /// Error: article.createTodays is not a function
```

### 静态属性

```javascript
class Article {
  static publisher = "Levi Ding";
}

alert( Article.publisher ); // Levi Ding
```

### 继承静态属性和方法

```javascript
class Animal {
  static planet = "Earth";

  constructor(name, speed) {
    this.speed = speed;
    this.name = name;
  }

  run(speed = 0) {
    this.speed += speed;
    alert(`${this.name} runs with speed ${this.speed}.`);
  }

  static compare(animalA, animalB) {
    return animalA.speed - animalB.speed;
  }

}

// 继承于 Animal
class Rabbit extends Animal {
  hide() {
    alert(`${this.name} hides!`);
  }
}

let rabbits = [
  new Rabbit("White Rabbit", 10),
  new Rabbit("Black Rabbit", 5)
];

rabbits.sort(Rabbit.compare);

rabbits[0].run(); // Black Rabbit runs with speed 5.

alert(Rabbit.planet); // Earth
```

## 私有的和受保护的属性和方法

### 受保护的 “waterAmount”

```javascript
class CoffeeMachine {
  _waterAmount = 0;

  set waterAmount(value) {
    if (value < 0) {
      value = 0;
    }
    this._waterAmount = value;
  }

  get waterAmount() {
    return this._waterAmount;
  }

  constructor(power) {
    this._power = power;
  }

}

// 创建咖啡机
let coffeeMachine = new CoffeeMachine(100);

// 加水
coffeeMachine.waterAmount = -10; // _waterAmount 将变为 0，而不是 -10
```

### 只读的 “power”
- 要做到这一点，我们只需要设置 getter，而不设置 setter：
```javascript
class CoffeeMachine {
  // ...

  constructor(power) {
    this._power = power;
  }

  get power() {
    return this._power;
  }

}

// 创建咖啡机
let coffeeMachine = new CoffeeMachine(100);

alert(`Power is: ${coffeeMachine.power}W`); // 功率是：100W

coffeeMachine.power = 25; // Error（没有 setter）
```

- getter/setter 函数
	- 但大多数时候首选 `get.../set...` 函数，像这样：
	- 这看起来有点长，但函数更灵活。它们可以接受多个参数
```javascript
class CoffeeMachine {
  _waterAmount = 0;

  setWaterAmount(value) {
    if (value < 0) value = 0;
    this._waterAmount = value;
  }

  getWaterAmount() {
    return this._waterAmount;
  }
}

new CoffeeMachine().setWaterAmount(100);
```

- 受保护的字段是可以被继承的

### 私有的 “#waterLimit”
- 这是一个最近添加到 JavaScript 的特性。 JavaScript 引擎不支持（或部分支持），需要 polyfills。
```javascript
class CoffeeMachine {
  #waterLimit = 200;

  #fixWaterAmount(value) {
    if (value < 0) return 0;
    if (value > this.#waterLimit) return this.#waterLimit;
  }

  setWaterAmount(value) {
    this.#waterLimit = this.#fixWaterAmount(value);
  }
}

let coffeeMachine = new CoffeeMachine();

// 不能从类的外部访问类的私有属性和方法
coffeeMachine.#fixWaterAmount(123); // Error
coffeeMachine.#waterLimit = 1000; // Error
```

- 私有字段与公共字段不会发生冲突。我们可以同时拥有私有的 `#waterAmount` 和公共的 `waterAmount` 字段。
```javascript
class CoffeeMachine {

  #waterAmount = 0;

  get waterAmount() {
    return this.#waterAmount;
  }

  set waterAmount(value) {
    if (value < 0) value = 0;
    this.#waterAmount = value;
  }
}

let machine = new CoffeeMachine();

machine.waterAmount = 100;
alert(machine.#waterAmount); // Error
```

- 但是如果我们继承自 `CoffeeMachine`，那么我们将无法直接访问 `#waterAmount`。我们需要依靠 `waterAmount` getter/setter：
```javascript
class MegaCoffeeMachine extends CoffeeMachine {
  method() {
    alert( this.#waterAmount ); // Error: can only access from CoffeeMachine
  }
}
```

## 扩展内建类

- 内建的类，例如 `Array`，`Map` 等也都是可以扩展的（extendable）。
```javascript
// 给 PowerArray 新增了一个方法（可以增加更多）
class PowerArray extends Array {
  isEmpty() {
    return this.length === 0;
  }
}

let arr = new PowerArray(1, 2, 5, 10, 50);
alert(arr.isEmpty()); // false

let filteredArr = arr.filter(item => item >= 10);
alert(filteredArr); // 10, 50
alert(filteredArr.isEmpty()); // false
```

- 当 `arr.filter()` 被调用时，它的内部使用的是 `arr.constructor` 来创建新的结果数组，而不是使用原生的 `Array`。

```javascript
class PowerArray extends Array {
  isEmpty() {
    return this.length === 0;
  }

  // 内建方法将使用这个作为 constructor
  static get [Symbol.species]() {
    return Array;
  }
}

let arr = new PowerArray(1, 2, 5, 10, 50);
alert(arr.isEmpty()); // false

// filter 使用 arr.constructor[Symbol.species] 作为 constructor 创建新数组
let filteredArr = arr.filter(item => item >= 10);

// filteredArr 不是 PowerArray，而是 Array
alert(filteredArr.isEmpty()); // Error: filteredArr.isEmpty is not a function
```
### 内建类没有静态方法继承
- 当一个类扩展另一个类时，静态方法和非静态方法都会被继承
- 但内建类却是一个例外。它们相互间不继承静态方法。

`Array` 和 `Date` 都继承自 `Object`，所以它们的实例都有来自 `Object.prototype` 的方法。但 `Array.[[Prototype]]` 并不指向 `Object`，所以它们没有例如 `Array.keys()`（或 `Date.keys()`）这些静态方法。

## 类检查："instanceof"

```javascript
class Rabbit {}
let rabbit = new Rabbit();

// rabbit 是 Rabbit class 的对象吗？
alert( rabbit instanceof Rabbit ); // true
```

```javascript
// 这里是构造函数，而不是 class
function Rabbit() {}

alert( new Rabbit() instanceof Rabbit ); // true
```

```javascript
let arr = [1, 2, 3];
alert( arr instanceof Array ); // true
alert( arr instanceof Object ); // true
```

- `Symbol.hasInstance`

```javascript
    // 设置 instanceOf 检查
    // 并假设具有 canEat 属性的都是 animal
    class Animal {
      static [Symbol.hasInstance](obj) {
        if (obj.canEat) return true;
      }
    }
    
    let obj = { canEat: true };
    
    alert(obj instanceof Animal); // true：Animal[Symbol.hasInstance](obj) 被调用
    ```
- 大多数 class 没有 `Symbol.hasInstance`。在这种情况下，标准的逻辑是：使用 `obj instanceOf Class` 检查 `Class.prototype` 是否等于 `obj` 的原型链中的原型之一。
```javascript
obj.__proto__ === Class.prototype?
obj.__proto__.__proto__ === Class.prototype?
obj.__proto__.__proto__.__proto__ === Class.prototype?
...
// 如果任意一个的答案为 true，则返回 true
// 否则，如果我们已经检查到了原型链的尾端，则返回 false
```
-  [objA.isPrototypeOf(objB)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/object/isPrototypeOf)
如果 `objA` 处在 `objB` 的原型链中，则返回 `true`。所以，可以将 `obj instanceof Class` 检查改为 `Class.prototype.isPrototypeOf(obj)`。

```javascript
function Rabbit() {}
let rabbit = new Rabbit();

// 修改了 prototype
Rabbit.prototype = {};

// ...再也不是 rabbit 了！
alert( rabbit instanceof Rabbit ); // false
```

### 使用 Object.prototype.toString 方法来揭示类型

```javascript
// 方便起见，将 toString 方法复制到一个变量中
let objectToString = Object.prototype.toString;

// 它是什么类型的？
let arr = [];

alert( objectToString.call(arr) ); // [object Array]
```

```javascript
// 特定于环境的对象和类的 toStringTag：
alert( window[Symbol.toStringTag]); // Window
alert( XMLHttpRequest.prototype[Symbol.toStringTag] ); // XMLHttpRequest

alert( {}.toString.call(window) ); // [object Window]
alert( {}.toString.call(new XMLHttpRequest()) ); // [object XMLHttpRequest]
```
- 如果我们想要获取内建对象的类型，并希望把该信息以字符串的形式返回，而不只是检查类型的话，我们可以用 `{}.toString.call` 替代 `instanceof`。

## Mixin 模式
- js没有多继承， mixin可以帮助实现类似功能
### 一个 Mixin 实例

```javascript
// mixin
let sayHiMixin = {
  sayHi() {
    alert(`Hello ${this.name}`);
  },
  sayBye() {
    alert(`Bye ${this.name}`);
  }
};

// 用法：
class User {
  constructor(name) {
    this.name = name;
  }
}

// 拷贝方法
Object.assign(User.prototype, sayHiMixin);

// 现在 User 可以打招呼了
new User("Dude").sayHi(); // Hello Dude!
```

```javascript
let sayMixin = {
  say(phrase) {
    alert(phrase);
  }
};

let sayHiMixin = {
  __proto__: sayMixin, // (或者，我们可以在这儿使用 Object.setPrototypeOf 来设置原型)

  sayHi() {
    // 调用父类方法
    super.say(`Hello ${this.name}`); // (*)
  },
  sayBye() {
    super.say(`Bye ${this.name}`); // (*)
  }
};

class User {
  constructor(name) {
    this.name = name;
  }
}

// 拷贝方法
Object.assign(User.prototype, sayHiMixin);

// 现在 User 可以打招呼了
new User("Dude").sayHi(); // Hello Dude!
```

### EventMixin

```javascript
let eventMixin = {
  /**
   * 订阅事件，用法：
   *  menu.on('select', function(item) { ... }
  */
  on(eventName, handler) {
    if (!this._eventHandlers) this._eventHandlers = {};
    if (!this._eventHandlers[eventName]) {
      this._eventHandlers[eventName] = [];
    }
    this._eventHandlers[eventName].push(handler);
  },

  /**
   * 取消订阅，用法：
   *  menu.off('select', handler)
   */
  off(eventName, handler) {
    let handlers = this._eventHandlers?.[eventName];
    if (!handlers) return;
    for (let i = 0; i < handlers.length; i++) {
      if (handlers[i] === handler) {
        handlers.splice(i--, 1);
      }
    }
  },

  /**
   * 生成具有给定名称和数据的事件
   *  this.trigger('select', data1, data2);
   */
  trigger(eventName, ...args) {
    if (!this._eventHandlers?.[eventName]) {
      return; // 该事件名称没有对应的事件处理程序（handler）
    }

    // 调用事件处理程序（handler）
    this._eventHandlers[eventName].forEach(handler => handler.apply(this, args));
  }
};
```

```javascript
// 创建一个 class
class Menu {
  choose(value) {
    this.trigger("select", value);
  }
}
// 添加带有事件相关方法的 mixin
Object.assign(Menu.prototype, eventMixin);

let menu = new Menu();

// 添加一个事件处理程序（handler），在被选择时被调用：
menu.on("select", value => alert(`Value selected: ${value}`));

// 触发事件 => 运行上述的事件处理程序（handler）并显示：
// 被选中的值：123
menu.choose("123");
```