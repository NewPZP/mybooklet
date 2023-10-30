### 属性标志
- 对象属性（properties），除 **`value`** 外，还有三个特殊的特性（attributes），也就是所谓的“标志”：
	- **`writable`** — 如果为 `true`，则值可以被修改，否则它是只可读的。
	- **`enumerable`** — 如果为 `true`，则会被在循环中列出，否则不会被列出。
	- **`configurable`** — 如果为 `true`，则此属性可以被删除，这些特性也可以被修改，否则不可以。
- [Object.getOwnPropertyDescriptor](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertyDescriptor) 方法允许查询有关属性的 **完整** 信息。
```javascript
let descriptor = Object.getOwnPropertyDescriptor(obj, propertyName);
```

- 为了修改标志，我们可以使用 [Object.defineProperty](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/defineProperty)。
```javascript
let user = {};

Object.defineProperty(user, "name", {
  value: "John"
});

let descriptor = Object.getOwnPropertyDescriptor(user, 'name');

alert( JSON.stringify(descriptor, null, 2 ) );
/*
{
  "value": "John",
  "writable": false,
  "enumerable": false,
  "configurable": false
}
 */
```
###  只读
- 只在严格模式下会出现 Errors
```javascript
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  writable: false
});

user.name = "Pete"; // Error: Cannot assign to read only property 'name'
```

- 针对的是属性不存在的情况
```javascript
let user = { };

Object.defineProperty(user, "name", {
  value: "John",
  // 对于新属性，我们需要明确地列出哪些是 true
  enumerable: true,
  configurable: true
});

alert(user.name); // John
user.name = "Pete"; // Error
```

### 不可枚举

```javascript
let user = {
  name: "John",
  toString() {
    return this.name;
  }
};

Object.defineProperty(user, "toString", {
  enumerable: false
});

// 现在我们的 toString 消失了：
for (let key in user) alert(key); // name
```

### 不可配置
- 不可配置的属性不能被删除，它的特性（attribute）不能被修改。
```javascript
let descriptor = Object.getOwnPropertyDescriptor(Math, 'PI');

alert( JSON.stringify(descriptor, null, 2 ) );
/*
{
  "value": 3.141592653589793,
  "writable": false,
  "enumerable": false,
  "configurable": false
}
*/
```

- 我们也无法将 `Math.PI` 改为 `writable`：
```javascript
// Error，因为 configurable: false
Object.defineProperty(Math, "PI", { writable: true });
```
- 使属性变成不可配置是一条单行道。我们无法通过 `defineProperty` 再把它改回来。
- **请注意：`configurable: false` 防止更改和删除属性标志，但是允许更改对象的值。**
```javascript
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  configurable: false
});

user.name = "Pete"; // 正常工作
delete user.name; // Error
```

- 设置为一个“永不可改”的常量，就像内建的 `Math.PI`：
```javascript
let user = {
  name: "John"
};

Object.defineProperty(user, "name", {
  writable: false,
  configurable: false
});

// 不能修改 user.name 或它的标志
// 下面的所有操作都不起作用：
user.name = "Pete";
delete user.name;
Object.defineProperty(user, "name", { value: "Pete" });
```

### Object.defineProperties
- 允许定义多个属性
```javascript
Object.defineProperties(user, {
  name: { value: "John", writable: false },
  surname: { value: "Smith", writable: false },
  // ...
});
```

### Object.getOwnPropertyDescriptors
- 克隆对象可以用这个 `Object.getOwnPropertyDescriptors` 返回包含 symbol 类型的和不可枚举的属性在内的 **所有** 属性描述符。
```javascript
let clone = Object.defineProperties({}, Object.getOwnPropertyDescriptors(obj));
```

### 设定一个全局的密封对象
- 属性描述符在单个属性的级别上工作。还有一些限制访问 **整个** 对象的方法：
	- [Object.preventExtensions(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/preventExtensions)禁止向对象添加新属性。
	- [Object.seal(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/seal)禁止添加/删除属性。为所有现有的属性设置 `configurable: false`
	- [Object.freeze(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze)禁止添加/删除/更改属性。为所有现有的属性设置 `configurable: false, writable: false`。
- 和对应的判断
	- [Object.isExtensible(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isExtensible) 
	- [Object.isSealed(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isSealed)
	- [Object.isFrozen(obj)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/isFrozen)
## 属性setter和getter

- 有两种类型的对象属性。
	- **数据属性**
	- **访问器属性（accessor property）**

### getter 和 setter
```javascript
let obj = {
  get propName() {
    // 当读取 obj.propName 时，getter 起作用
  },

  set propName(value) {
    // 当执行 obj.propName = value 操作时，setter 起作用
  }
};
```

```javascript
let user = {
  name: "John",
  surname: "Smith",

  get fullName() {
    return `${this.name} ${this.surname}`;
  },

  set fullName(value) {
    [this.name, this.surname] = value.split(" ");
  }
};

// set fullName 将以给定值执行
user.fullName = "Alice Cooper";

alert(user.name); // Alice
alert(user.surname); // Cooper
```

### 访问器描述符
- 所以访问器描述符可能有：
	- **`get`** —— 一个没有参数的函数，在读取属性时工作，
	- **`set`** —— 带有一个参数的函数，当属性被设置时调用，
	- **`enumerable`** —— 与数据属性的相同，
	- **`configurable`** —— 与数据属性的相同。
```javascript
let user = {
  name: "John",
  surname: "Smith"
};

Object.defineProperty(user, 'fullName', {
  get() {
    return `${this.name} ${this.surname}`;
  },

  set(value) {
    [this.name, this.surname] = value.split(" ");
  }
});

alert(user.fullName); // John Smith

for(let key in user) alert(key); // name, surname
```

- 一个属性要么是访问器（具有 `get/set` 方法），要么是数据属性（具有 `value`），但不能两者都是。

### 更聪明的 getter/setter
- getter/setter 可以用作“真实”属性值的包装器，以便对它们进行更多的控制。
```javascript
let user = {
  get name() {
    return this._name;
  },

  set name(value) {
    if (value.length < 4) {
      alert("Name is too short, need at least 4 characters");
      return;
    }
    this._name = value;
  }
};

user.name = "Pete";
alert(user.name); // Pete

user.name = ""; // Name 太短了……
```

### 兼容性

- 访问器的一大用途是，它们允许随时通过使用 getter 和 setter 替换“正常的”数据属性，来控制和调整这些属性的行为。

```javascript
function User(name, birthday) {
  this.name = name;
  this.birthday = birthday;

  // 年龄是根据当前日期和生日计算得出的
  Object.defineProperty(this, "age", {
    get() {
      let todayYear = new Date().getFullYear();
      return todayYear - this.birthday.getFullYear();
    }
  });
}

let john = new User("John", new Date(1992, 6, 1));

alert( john.birthday ); // birthday 是可访问的
alert( john.age );      // ……age 也是可访问的
```