https://zh.javascript.info/

## 规范
- **ECMA-262**
	- [https://tc39.es/ecma262/](https://tc39.es/ecma262/)
- 最新提案草稿
	- [https://github.com/tc39/proposals](https://github.com/tc39/proposals)
- MDN
	- 一个带有用例和其他信息的主要的手册
	- [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)
	-  [https://google.com/search?q=MDN+parseInt](https://google.com/search?q=MDN+parseInt) 可以这样使用google搜索
- 兼容性表
	- [https://caniuse.com](https://caniuse.com/)
	- [https://kangax.github.io/compat-table](https://kangax.github.io/compat-table)



## “script” 标签
-  我们可以使用一个 `<script>` 标签将 JavaScript 代码添加到页面中。
-  `type` 和 `language` 特性（attribute）不是必需的。
- 外部的脚本可以通过 `<script src="path/to/script.js"></script> `的方式插入。

## 代码结构
### 分号
- 自动分号插入
- 最好不要省略，一种混淆的情况
```javascript
alert("Hello") 
[1, 2].forEach(alert);
// 和下面是一样的
alert("Hello")[1, 2].forEach(alert);

```
### 注释
- 和java 一样

## 现代模式 use strict
- ES5 为保证兼容性提出，使用use strict可以激活新特性
- 确保在顶部
```javascript
alert("some code"); 
// 下面的 "use strict" 会被忽略，必须在最顶部。 
"use strict"; 
// 严格模式没有被激活
```
- 浏览器控制台
	- 默认没有开启 现代模式
	- 开启方法
```javascript
'use strict'; <Shift+Enter 换行> 
// ...你的代码 
<按下 Enter 以运行>
```
```javascript
(function() { 
	'use strict'; 
	// ...你的代码... 
})()
```
- 是否使用
	- **目前我们欢迎将 `"use strict";` 写在脚本的顶部。稍后，当你的代码全都写在了 class 和 module 中时，你则可以将 `"use strict";` 这行代码省略掉。**
## 变量

- let ，多个变量定义最好是多行
```javascript
let user = 'John'; 
let age = 25;
let message = 'Hello';
```
- 一行多个用逗号
```javascript
let user = 'John', age = 25, message = 'Hello';
```
- 老脚本会用var
- 变量是存储数据的盒子
```javascript
let hello = 'Hello world!'; 
let message; 
// 将字符串 'Hello world' 从变量 hello 拷贝到 message
message = hello;
// 现在两个变量保存着相同的数据 
alert(hello); 
// Hello world! 
alert(message); 
// Hello world!
```
- 不要声明两次
### 命名
- 字母、数字、符号 `$` 和 `_`。
- 首字母不是数字
- 驼峰式命名法
- use strict 启用时，不声明会报错
### 常量
- const
- 一般用把常量当别名用
- 大写加下划线，一般只拿来作硬编码

## 数据类型
### Number
- 代表整数和浮点
- 包括 special numeric values  `Infinity`、`-Infinity` 和 `NaN`。
- NaN运算具有传播性，除`NaN ** 0 == 1` 其它情况计算都是NaN
- 数学运算是安全的，永远不会因为错误停止， 最坏情况就是的到NaN
###  BigInt
- number 的范围是`(2**53-1)`（即 `9007199254740991`）或小于 `-(2**53-1)` 的整数。
- BigInt用于表示任意长度的整数。
- 末尾加一个n表示 BigInt类型
```javascript
const bigInt = 1234567890123456789012345678901234567890n;
```

### String 
- 三种形式
	1.  双引号：`"Hello"`.
	2.  单引号：`'Hello'`.
	3.  反引号：`` `Hello` ``.
```javascript
let str = "Hello";
let str2 = 'Single quotes are ok too';
let phrase = `can embed another ${str}`;
```

- 反引号是 **功能扩展** 引号 允许我们通过将变量和表达式包装在 `${…}` 中，
```javascript
let name = "John";

// 嵌入一个变量
alert( `Hello, ${name}!` ); // Hello, John!

// 嵌入一个表达式
alert( `the result is ${1 + 2}` ); // the result is 3
```

### Boolean
- boolean 类型仅包含两个值：`true` 和 `false`。

### null
- 特殊的 `null` 值不属于上述任何一种类型。
- `null` 不是一个“对不存在的 `object` 的引用”或者 “null 指针”。JavaScript 中的 `null` 仅仅是一个代表“无”、“空”或“值未知”的特殊值。

### undefined
- 特殊值 `undefined` 和 `null` 一样自成类型。`undefined` 的含义是 `未被赋值`。
```javascript
let age;

alert(age); // 弹出 "undefined"
```
- 通常，使用 `null` 将一个“空”或者“未知”的值写入变量中，而 `undefined` 则保留作为未进行初始化的事物的默认初始值。

### Object 类型和 Symbol 类型
- `object` 则用于储存数据集合和更复杂的实体。除了object其他都是原始类型
- `symbol` 类型用于创建对象的唯一标识符。

### typeof 运算符
```javascript
typeof undefined // "undefined"

typeof 0 // "number"

typeof 10n // "bigint"

typeof true // "boolean"

typeof "foo" // "string"

typeof Symbol("id") // "symbol"

typeof Math // "object"  (1)

typeof null // "object"  (2)

typeof alert // "function"  (3)
```
1. `Math` 是一个提供数学运算的内建 `object`
2. `typeof null` 的结果为 `"object"`。这是官方承认的 `typeof` 的错误，这个问题来自于 JavaScript 语言的早期阶段，并为了兼容性而保留了下来。`null` 绝对不是一个 `object`。`null` 有自己的类型，它是一个特殊值。`typeof` 的行为在这里是错误的。
3. `typeof alert` 的结果是 `"function"`，因为 `alert` 在 JavaScript 语言中是一个函数。我们会在下一章学习函数，那时我们会了解到，在 JavaScript 语言中没有一个特别的 “function” 类型。函数隶属于 `object` 类型。但是 `typeof` 会对函数区分对待，并返回 `"function"`。这也是来自于 JavaScript 语言早期的问题。从技术上讲，这种行为是不正确的，但在实际编程中却非常方便。

- 你可能还会遇到另一种语法：`typeof(x)`。它与 `typeof x` 相同。简单点说：`typeof` 是一个操作符，不是一个函数。这里的括号不是 `typeof` 的一部分。它是数学运算分组的括号。

## 类型转换
- 大多数情况运算符和函数会自动进行转换

### 字符串类型转换

```javascript
let value = true;
alert(typeof value); // boolean

value = String(value); // 现在，值是一个字符串形式的 "true"
alert(typeof value); // string
```

### 数字转换
- 在算术函数和表达式中，会自动进行 number 类型转换。
```javascript
alert( "6" / "2" ); // 3, string 类型的值被自动转换成 number 类型后进行计算
```
- 使用Number显式转
```javascript
let str = "123";
alert(typeof str); // string

let num = Number(str); // 变成 number 类型 123

alert(typeof num); // number
```
- 转换失败时
```javascript
let age = Number("an arbitrary string instead of a number");
alert(age); // NaN，转换失败
```
- 例子
```javascript
alert( Number("   123   ") ); // 123
alert( Number("123z") );      // NaN（从字符串“读取”数字，读到 "z" 时出现错误）
alert( Number(true) );        // 1
alert( Number(false) );       // 0
```
- 请注意 `null` 和 `undefined` 在这有点不同：`null` 变成数字 `0`，`undefined` 变成 `NaN`。
### 布尔类型转换
转换规则如下：
-   直观上为“空”的值（如 `0`、空字符串、`null`、`undefined` 和 `NaN`）将变为 `false`。
-   其他值变成 `true`。

```javascript
alert( Boolean(1) ); // true
alert( Boolean(0) ); // false

alert( Boolean("hello") ); // true
alert( Boolean("") ); // false
```
## 基础运算符，数学运算

### 术语：“一元运算符”，“二元运算符”，“运算元”
- **运算元** —— 运算符应用的对象。比如说乘法运算 `5 * 2`，有两个运算元：左运算元 `5` 和右运算元 `2`。有时候人们也称其为“参数”而不是“运算元”。
- 如果一个运算符对应的只有一个运算元，那么它是 **一元运算符**。比如说一元负号运算符（unary negation）`-`，它的作用是对数字进行正负转换：
- 如果一个运算符拥有两个运算元，那么它是 **二元运算符**。

### 数学运算
-   加法 `+`,
-   减法 `-`,
-   乘法 `*`,
-   除法 `/`,
-   取余 `%`,
```javascript
alert( 5 % 2 ); // 1，5 除以 2 的余数
alert( 8 % 3 ); // 2，8 除以 3 的余数
```
-   求幂 `**`.
	```javascript
alert( 4 ** (1/2) ); // 2（1/2 次方与平方根相同)
alert( 8 ** (1/3) ); // 2（1/3 次方与立方根相同)
```
- 用二元运算符 + 连接字符串
```javascript
let s = "my" + "string";
alert(s); // mystring
```
- 只要任意一个运算元是字符串，那么另一个运算元也将被转化为字符串。
```javascript
alert( '1' + 2 ); // "12"
alert( 2 + '1' ); // "21"
```
- 运算符是按顺序工作 所以
```javascript
alert(2 + 2 + '1' ); // "41"，不是 "221"
alert('1' + 2 + 2); // "122"，不是 "14"
```
- **二元 `+` 是唯一一个以这种方式支持字符串的运算符。**其他算术运算符只对数字起作用，并且总是将其运算元转换为数字。
```javascript
alert( 6 - '2' ); // 4，将 '2' 转换为数字
alert( '6' / '2' ); // 3，将两个运算元都转换为数字
```

### 数字转化，一元运算符 +
- 加号 `+` 应用于单个值，对数字没有任何作用。但是如果运算元不是数字，加号 `+` 则会将其转化为数字。 它的效果和 `Number(...)` 相同，但是更加简短。
```javascript
// 对数字无效
let x = 1;
alert( +x ); // 1

let y = -2;
alert( +y ); // -2

// 转化非数字
alert( +true ); // 1
alert( +"" );   // 0
```

```javascript
let apples = "2";
let oranges = "3";

alert( apples + oranges ); // "23"，二元运算符加号合并字符串
```
```javascript
let apples = "2";
let oranges = "3";

// 在二元运算符加号起作用之前，所有的值都被转化为了数字
alert( +apples + +oranges ); // 5

// 更长的写法
// alert( Number(apples) + Number(oranges) ); // 5
```

### 运算符优先级
- 一元运算符优先级高于二元运算符


### 赋值运算符
- 赋值 = 返回一个值
	- 语句 `x = value` 将值 `value` 写入 `x` **然后返回 value**。
```javascript
let a = 1;
let b = 2;

let c = 3 - (a = b + 1);

alert( a ); // 3
alert( c ); // 0
```
- 链式赋值（Chaining assignments）
```javascript
let a, b, c;

a = b = c = 2 + 2;

alert( a ); // 4
alert( b ); // 4
alert( c ); // 4
```

### 原地修改
```javascript
let n = 2;
n += 5; // 现在 n = 7（等同于 n = n + 5）
n *= 2; // 现在 n = 14（等同于 n = n * 2）

alert( n ); // 14
```
- 所有算术和位运算符都有简短的“修改并赋值”运算符：`/=` 和 `-=` 等。
- 这类运算符的优先级与普通赋值运算符的优先级相同，所以它们在大多数其他运算之后执行

### 自增/自减
- 自增
	```javascript
    let counter = 2;
    counter++;      // 和 counter = counter + 1 效果一样，但是更简洁
    alert( counter ); // 3
    ```
- 自减
	```javascript
    let counter = 2;
    counter--;      // 和 counter = counter - 1 效果一样，但是更简洁
    alert( counter ); // 1
    ```
- 自增/自减只能应用于变量。试一下，将其应用于数值（比如 `5++`）则会报错。
- 前置与后置
	-   当运算符置于变量后，被称为“后置形式”：`counter++`。
	-   当运算符置于变量前，被称为“前置形式”：`++counter`。
-  `++/--` 运算符同样可以在表达式内部使用。它们的优先级比绝大部分的算数运算符要高。

### 位运算符

### 逗号运算符

- 逗号运算符能让我们处理多个语句，使用 `,` 将它们分开。每个语句都运行了，**但是只有最后的语句的结果会被返回。**
```javascript
let a = (1 + 2, 3 + 4);

alert( a ); // 7（3 + 4 的结果）
```
- 请注意逗号运算符的优先级非常低，比 `=` 还要低，因此上面你的例子中圆括号非常重要。
- 应用
```javascript
// 一行上有三个运算符
for (a = 1, b = 3, c = a * b; a < 10; a++) {
 ...
}
```

## 值的比较

### Boolean 比较
```javascript
alert( 2 > 1 );  // true（正确）
alert( 2 == 1 ); // false（错误）
alert( 2 != 1 ); // true（正确）
```
```javascript
let result = 5 > 4; // 把比较的结果赋值给 result
alert( result ); // true
```

### 字符串比较

- 使用“字典（dictionary）”或“词典（lexicographical）”顺序进行判定。
```javascript
alert( 'Z' > 'A' ); // true
alert( 'Glow' > 'Glee' ); // true
alert( 'Bee' > 'Be' ); // true
```

### 不同类型的比较
- 首先将其转化为数字（number）再判定大小。
```javascript
alert( '2' > 1 ); // true，字符串 '2' 会被转化为数字 2
alert( '01' == 1 ); // true，字符串 '01' 会被转化为数字 1
```
- 对于布尔类型值，`true` 会被转化为 `1`、`false` 转化为 `0`。
```javascript
alert( true == 1 ); // true
alert( false == 0 ); // true
```
- 注意
```javascript
let a = 0;
alert( Boolean(a) ); // false

let b = "0";
alert( Boolean(b) ); // true

alert(a == b); // true!
```

### 严格相等
- 普通的相等性检查 `==` 存在一个问题，它不能区分出 `0` 和 `false`：
```javascript
alert( 0 == false ); // true
```
```javascript
alert( '' == false ); // true
```

- **严格相等运算符 `===` 在进行比较时不会做任何的类型转换。**
```javascript
alert( 0 === false ); // false，因为被比较值的数据类型不同
```

- 同样的，与“不相等”符号 `!=` 类似，

### 对 null 和 undefined 进行比较

```javascript
alert( null === undefined ); // false
```

```javascript
alert( null == undefined ); // true
```

- 当使用数学式或其他比较方法 `< > <= >=` 时：
	-`null/undefined` 会被转化为数字：`null` 被转化为 `0`，`undefined` 被转化为 `NaN`。

### 奇怪的结果：null vs 0
```javascript
alert( null > 0 );  // (1) false
alert( null == 0 ); // (2) false
alert( null >= 0 ); // (3) true
```
为什么会出现这种反常结果，这是因为相等性检查 `==` 和普通比较符 `> < >= <=` 的代码逻辑是相互独立的。进行值的比较时，`null` 会被转化为数字，因此它被转化为了 `0`。这就是为什么（3）中 `null >= 0` 返回值是 true，（1）中 `null > 0` 返回值是 false。
另一方面，`undefined` 和 `null` 在相等性检查 `==` 中不会进行任何的类型转换，它们有自己独立的比较规则，所以除了它们之间互等外，不会等于任何其他的值。这就解释了为什么（2）中 `null == 0` 会返回 false。


### 特立独行的 undefined

- undefined 不应该被与其他值进行比较：
```javascript
alert( undefined > 0 ); // false (1)
alert( undefined < 0 ); // false (2)
alert( undefined == 0 ); // false (3)
```
-   `(1)` 和 `(2)` 都返回 `false` 是因为 `undefined` 在比较中被转换为了 `NaN`，而 `NaN` 是一个特殊的数值型值，它与任何值进行比较都会返回 `false`。
-   `(3)` 返回 `false` 是因为这是一个相等性检查，而 `undefined` 只与 `null` 相等，不会与其他值相等。

### 避免问题
- 除了严格相等 `===` 外，其他但凡是有 `undefined/null` 参与的比较，我们都需要格外小心。
- 除非你非常清楚自己在做什么，否则永远不要使用 `>= > < <=` 去比较一个可能为 `null/undefined` 的变量。对于取值可能是 `null/undefined` 的变量，请按需要分别检查它的取值情况。

## 条件分支 if 和 ？
### if
```javascript
if (year == 2015) {
  alert( "That's correct!" );
  alert( "You're so smart!" );
}
```

### 布尔转换
-   数字 `0`、空字符串 `""`、`null`、`undefined` 和 `NaN` 都会被转换成 `false`。因为它们被称为“假值（falsy）”。
-   其他值被转换为 `true`，所以它们被称为“真值（truthy）”。

### else
```javascript
let year = prompt('In which year was ECMAScript-2015 specification published?', '');

if (year == 2015) {
  alert( 'You guessed it right!' );
} else {
  alert( 'How can you be so wrong?' ); // 2015 以外的任何值
}
```

###  多个条件：“else if”
```javascript
let year = prompt('In which year was ECMAScript-2015 specification published?', '');

if (year < 2015) {
  alert( 'Too early...' );
} else if (year > 2015) {
  alert( 'Too late' );
} else {
  alert( 'Exactly!' );
}
```

### 条件运算符 ‘?’

```javascript
let accessAllowed;
let age = prompt('How old are you?', '');

if (age > 18) {
  accessAllowed = true;
} else {
  accessAllowed = false;
}

alert(accessAllowed);


```
等价于
```javascript
let accessAllowed = (age > 18) ? true : false;
```

### 多个 ‘?’
```javascript
let age = prompt('age?', 18);

let message = (age < 3) ? 'Hi, baby!' :
  (age < 18) ? 'Hello!' :
  (age < 100) ? 'Greetings!' :
  'What an unusual age!';

alert( message );
```

### ‘?’ 的非常规使用
- 可读性比较差，建议还是使用if
```javascript
let company = prompt('Which company created JavaScript?', '');

(company == 'Netscape') ?
   alert('Right!') : alert('Wrong.');
```

## 逻辑运算符
### || 或

### 或运算寻找第一个真值
```javascript
alert( 1 || 0 ); // 1（1 是真值）

alert( null || 1 ); // 1（1 是第一个真值）
alert( null || 0 || 1 ); // 1（第一个真值）

alert( undefined || null || 0 ); // 0（都是假值，返回最后一个值）
```
```javascript
let firstName = "";
let lastName = "";
let nickName = "SuperCoder";

alert( firstName || lastName || nickName || "Anonymous"); // SuperCoder
```
### 短路求职
```javascript
true || alert("not printed");
false || alert("printed");
```

### && 与

### 与运算寻找第一个假值
- 与运算返回第一个假值，如果没有假值就返回最后一个值。
```javascript
// 如果第一个操作数是真值，
// 与运算返回第二个操作数：
alert( 1 && 0 ); // 0
alert( 1 && 5 ); // 5

// 如果第一个操作数是假值，
// 与运算将直接返回它。第二个操作数会被忽略
alert( null && 5 ); // null
alert( 0 && "no matter what" ); // 0
```

### ！ 非
- 两个非运算 `!!` 有时候用来将某个值转化为布尔类型：
```javascript
alert( !!"non-empty string" ); // true
alert( !!null ); // false
```

也就是，第一个非运算将该值转化为布尔类型并取反，第二个非运算再次取反。最后我们就得到了一个任意值到布尔值的转化。与下面等同
```javascript
alert( Boolean("non-empty string") ); // true
alert( Boolean(null) ); // false
```

## 空值合并运算符 '??'
- 比较新的特性
-   如果 `a` 是已定义的，则结果为 `a`，
-   如果 `a` 不是已定义的，则结果为 `b`。
- 等同于
```javascript
result = (a !== null && a !== undefined) ? a : b;
```

- 例子
```javascript
let user;

alert(user ?? "匿名"); // 匿名（user 未定义）
```
```javascript
let firstName = null;
let lastName = null;
let nickName = "Supercoder";

// 显示第一个已定义的值：
alert(firstName ?? lastName ?? nickName ?? "匿名"); // Supercoder
```

### 与 ||比较
- 下面等同上面的效果
```javascript
let firstName = null;
let lastName = null;
let nickName = "Supercoder";

// 显示第一个真值：
alert(firstName || lastName || nickName || "Anonymous"); // Supercoder
```
- 它们之间重要的区别是：
	-   `||` 返回第一个 **真** 值。
	-   `??` 返回第一个 **已定义的** 值。
- 一种 情况 使用？？ 可能更好
```javascript
let height = 0;

alert(height || 100); // 100
alert(height ?? 100); // 0
```

### 优先级
- `??` 运算符的优先级与 `||` 相同，它们的的优先级都为 `4`，在 `=` 和 `?` 运算前计算，但在大多数其他运算（例如 `+` 和 `*`）之后计算。
### ?? 与 && 或 || 一起使用
- 出于安全原因，JavaScript 禁止将 `??` 运算符与 `&&` 和 `||` 运算符一起使用，除非使用括号明确指定了优先级。

## 循环 while / for
### while
```javascript
let i = 3;
while (i) { // 当 i 变成 0 时，条件为假，循环终止
  alert( i );
  i--;
}
```
```javascript
let i = 0;
do {
  alert( i );
  i++;
} while (i < 3);
```

### for
```javascript
for (let i = 0; i < 3; i++) { // 结果为 0、1、2
  alert(i);
}
```

### 跳出循环
- break
### 继续下次迭代
- continue

### break continue 标签

```javascript
outer: for (let i = 0; i < 3; i++) {

  for (let j = 0; j < 3; j++) {

    let input = prompt(`Value at coords (${i},${j})`, '');

    // 如果是空字符串或被取消，则中断并跳出这两个循环。
    if (!input) break outer; // (*)

    // 用得到的值做些事……
  }
}

alert('Done!');
```
## switch
- 要用break 
- `switch` 和 `case` 都允许任意表达式。
```javascript
let a = "1";
let b = 0;

switch (+a) {
  case b + 1:
    alert("this runs, because +a is 1, exactly equals b+1");
    break;

  default:
    alert("this doesn't run");
}
```
### “case” 分组
```javascript
let a = 3;

switch (a) {
  case 4:
    alert('Right!');
    break;

  case 3: // (*) 下面这两个 case 被分在一组
  case 5:
    alert('Wrong!');
    alert("Why don't you take a math class?");
    break;

  default:
    alert('The result is strange. Really.');
}
```

### 类型很关键
- 输入 `3`，因为 `prompt` 的结果是字符串类型的 `"3"`，不严格相等 `===` 于数字类型的 `3`，所以 `case 3` 不会执行！因此 `case 3` 部分是一段无效代码。所以会执行 `default` 分支。
```javascript
let arg = prompt("Enter a value?")
switch (arg) {
  case '0':
  case '1':
    alert( 'One or zero' );
    break;

  case '2':
    alert( 'Two' );
    break;

  case 3:
    alert( 'Never executes!' );
    break;
  default:
    alert( 'An unknown value' )
}
```
## 函数

### 声明
```javascript
function name(parameter1, parameter2, ... parameterN) {
  ...body...
}
```

### 局部变量
- 在函数中声明的变量只在该函数内部可见。
```javascript
function showMessage() {
  let message = "Hello, I'm JavaScript!"; // 局部变量

  alert( message );
}

showMessage(); // Hello, I'm JavaScript!

alert( message ); // <-- 错误！变量是函数的局部变量
```

### 外部变量
- 函数对外部变量拥有全部的访问权限。函数也可以修改外部变量。
```javascript
let userName = 'John';

function showMessage() {
  userName = "Bob"; // (1) 改变外部变量

  let message = 'Hello, ' + userName;
  alert(message);
}

alert( userName ); // John 在函数调用之前

showMessage();

alert( userName ); // Bob，值被函数修改了
```
- 如果在函数内部声明了同名变量，那么函数会 **遮蔽** 外部变量。
```javascript
let userName = 'John';

function showMessage() {
  let userName = "Bob"; // 声明一个局部变量

  let message = 'Hello, ' + userName; // Bob
  alert(message);
}

// 函数会创建并使用它自己的 userName
showMessage();

alert( userName ); // John，未被更改，函数没有访问外部变量。
```
### 参数
-   参数（parameter）是函数声明中括号内列出的变量（它是函数声明时的术语）。
-   参数（argument）是调用函数时传递给函数的值（它是函数调用时的术语）。
### 默认值
```javascript
function showMessage(from, text = "no text given") {
  alert( from + ": " + text );
}

showMessage("Ann"); // Ann: no text given
```

```javascript
function showMessage(from, text = anotherFunction()) {
  // anotherFunction() 仅在没有给定 text 时执行
  // 其运行结果将成为 text 的值
}
```

### 后备默认参数
```javascript
function showMessage(text) {
  // ...

  if (text === undefined) { // 如果参数未被传递进来
    text = 'empty message';
  }

  alert(text);
}

showMessage(); // empty message
```

```javascript
function showMessage(text) {
  // 如果 text 为 undefined 或者为假值，那么将其赋值为 'empty'
  text = text || 'empty';
  ...
}
```

```javascript
function showCount(count) {
  // 如果 count 为 undefined 或 null，则提示 "unknown"
  alert(count ?? "unknown");
}

showCount(0); // 0
showCount(null); // unknown
showCount(); // unknown
```

### 返回值

### 函数命名
- 函数就是行为（action）。所以它们的名字通常是动词。它应该简短且尽可能准确地描述函数的作用。这样读代码的人就能清楚地知道这个函数的功能。
```javascript
showMessage(..)     // 显示信息
getAge(..)          // 返回 age（gets it somehow）
calcSum(..)         // 计算求和并返回结果
createForm(..)      // 创建表单（通常会返回它）
checkPermission(..) // 检查权限并返回 true/false
```
- 一个函数 —— 一个行为
有了前缀，只需瞥一眼函数名，就可以了解它的功能是什么，返回什么样的值。

### 函数 == 注释
- 如果这个函数功能复杂，那么把该函数拆分成几个小的函数是值得的。
- 自描述的函数

```javascript
function showPrimes(n) {
  nextPrime: for (let i = 2; i < n; i++) {

    for (let j = 2; j < i; j++) {
      if (i % j == 0) continue nextPrime;
    }

    alert( i ); // 一个素数
  }
}
```
- 上面拆成下面更易理解
```javascript
function showPrimes(n) {

  for (let i = 2; i < n; i++) {
    if (!isPrime(i)) continue;

    alert(i);  // 一个素数
  }
}

function isPrime(n) {
  for (let i = 2; i < n; i++) {
    if ( n % i == 0) return false;
  }
  return true;
}
```

## 函数表达式
```javascript
let sayHi = function() {
  alert( "Hello" );
};
```

### 函数是一个值
```javascript
function sayHi() {
  alert( "Hello" );
}

alert( sayHi ); // 显示函数代码
```
- 可以复制
```javascript
function sayHi() {   // (1) 创建
  alert( "Hello" );
}

let func = sayHi;    // (2) 复制

func(); // Hello     // (3) 运行复制的值（正常运行）！
sayHi(); // Hello    //     这里也能运行（为什么不行呢）
```
- 一样的
```javascript
let sayHi = function() { // (1) 创建
  alert( "Hello" );
};

let func = sayHi;
// ...
```
- 注意 函数表达式后面有个分号
### 回调函数

```javascript
function ask(question, yes, no) {
  if (confirm(question)) yes()
  else no();
}

function showOk() {
  alert( "You agreed." );
}

function showCancel() {
  alert( "You canceled the execution." );
}

// 用法：函数 showOk 和 showCancel 被作为参数传入到 ask
ask("Do you agree?", showOk, showCancel);
```
- 简洁一点 使用匿名函数
```javascript
function ask(question, yes, no) {
  if (confirm(question)) yes()
  else no();
}

ask(
  "Do you agree?",
  function() { alert("You agreed."); },
  function() { alert("You canceled the execution."); }
);
```

### 函数表达式 vs 函数声明

- **函数表达式是在代码执行到达时被创建，并且仅从那一刻起可用。**
- **在函数声明被定义之前，它就可以被调用。**
```javascript
sayHi("John"); // Hello, John

function sayHi(name) {
  alert( `Hello, ${name}` );
}
```
```javascript
sayHi("John"); // error!

let sayHi = function(name) {  // (*) no magic any more
  alert( `Hello, ${name}` );
};
```

- **严格模式下，当一个函数声明在一个代码块内时，它在该代码块内的任何位置都是可见的。但在代码块外不可见。**
```javascript
let age = 16; // 拿 16 作为例子

if (age < 18) {
  welcome();               // \   (运行)
                           //  |
  function welcome() {     //  |
    alert("Hello!");       //  |  函数声明在声明它的代码块内任意位置都可用
  }                        //  |
                           //  |
  welcome();               // /   (运行)

} else {

  function welcome() {
    alert("Greetings!");
  }
}

// 在这里，我们在花括号外部调用函数，我们看不到它们内部的函数声明。


welcome(); // Error: welcome is not defined
```
- 使用函数表达式可以解决上面这个问题
```javascript
let age = prompt("What is your age?", 18);

let welcome;

if (age < 18) {

  welcome = function() {
    alert("Hello!");
  };

} else {

  welcome = function() {
    alert("Greetings!");
  };

}

welcome(); // 现在可以了
```

- 或者更简洁
```javascript
let age = prompt("What is your age?", 18);

let welcome = (age < 18) ?
  function() { alert("Hello!"); } :
  function() { alert("Greetings!"); };

welcome(); // 现在可以了
```

## 箭头函数基础知识

```javascript
let func = (arg1, arg2, ..., argN) => expression;
```
等同于
```javascript
let func = function(arg1, arg2, ..., argN) {
  return expression;
};
```

```javascript
let sum = (a, b) => a + b;

/* 这个箭头函数是下面这个函数的更短的版本：

let sum = function(a, b) {
  return a + b;
};
*/

alert( sum(1, 2) ); // 3
```

- 如果没有参数，括号则是空的（但括号必须保留）：
```javascript
    let sayHi = () => alert("Hello!");
    
    sayHi();
```
- 动态创建

```javascript
let age = prompt("What is your age?", 18);

let welcome = (age < 18) ?
  () => alert('Hello!') :
  () => alert("Greetings!");

welcome();
```

### 多行的箭头函数
```javascript
let sum = (a, b) => {  // 花括号表示开始一个多行函数
  let result = a + b;
  return result; // 如果我们使用了花括号，那么我们需要一个显式的 “return”
};

alert( sum(1, 2) ); // 3
```



