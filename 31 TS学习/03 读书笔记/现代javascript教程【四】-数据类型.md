## 原始类型方法
- 一个原始值：
	-   是原始类型中的一种值。
	-   在 JavaScript 中有 7 种原始类型：`string`，`number`，`bigint`，`boolean`，`symbol`，`null` 和 `undefined`。
- 一个对象
	-   能够存储多个值作为属性。
	-   可以使用大括号 `{}` 创建对象，例如：`{name: "John", age: 30}`。JavaScript 中还有其他种类的对象，例如函数就是对象。
	- 关于对象的最好的事儿之一是，我们可以把一个函数作为对象的属性存储到对象中。

### 当作对象的原始类型

-   人们可能想对诸如字符串或数字之类的原始类型执行很多操作。最好使用方法来访问它们。
-   原始类型必须尽可能的简单轻量。

解决：
	1.  原始类型仍然是原始的。与预期相同，提供单个值
	2.  JavaScript 允许访问字符串，数字，布尔值和 symbol 的方法和属性。
	3.  为了使它们起作用，创建了提供额外功能的特殊“对象包装器”，使用后即被销毁。

“**对象包装器**”对于每种原始类型都是不同的，它们被称为 `String`、`Number`、`Boolean`、`Symbol` 和 `BigInt`。因此，它们提供了不同的方法。

```javascript
let str = "Hello";

alert( str.toUpperCase() ); // HELLO
```
以下是 `str.toUpperCase()` 中实际发生的情况：
1.  字符串 `str` 是一个原始值。因此，在访问其属性时，会创建一个包含字符串字面值的特殊对象，并且具有可用的方法，例如 `toUpperCase()`。
2.  该方法运行并返回一个新的字符串（由 `alert` 显示）。
3.  特殊对象被销毁，只留下原始值 `str`。

- 所以原始类型可以提供方法，但它们依然是轻量级的。

-  构造器 `String/Number/Boolean` 仅供内部使用
-  null/undefined 没有任何方法


## 数字类型

###  数字（number）有两种类型：
- “双精度浮点数”, 常规数字以 64 位的格式 [IEEE-754](https://en.wikipedia.org/wiki/IEEE_754) 存储，
- BigInt, 用于表示任意长度的整数

### 编写数字的更多方法
```javascript
let billion = 1_000_000_000;
```

```javascript
let billion = 1e9;  // 10 亿，字面意思：数字 1 后面跟 9 个 0

alert( 7.3e9 );  // 73 亿（与 7300000000 和 7_300_000_000 相同）
```
```javascript
1e3 === 1 * 1000; // e3 表示 *1000
1.23e6 === 1.23 * 1000000; // e6 表示 *1000000
```

```javascript
let mcs = 1e-6; // 1 的左边有 6 个 0
```

### 十六进制，二进制和八进制数字

```javascript
alert( 0xff ); // 255
alert( 0xFF ); // 255（一样，大小写没影响）
```

```javascript
let a = 0b11111111; // 二进制形式的 255
let b = 0o377; // 八进制形式的 255

alert( a == b ); // true，两边是相同的数字，都是 255
```

### toString(base)

```javascript
let num = 255;

alert( num.toString(16) );  // ff
alert( num.toString(2) );   // 11111111
```
- 注意下方两个点没有写错 ，也可以写成 `(123456).toString(36)`。
```javascript
    alert( 123456..toString(36) ); // 2n9c
```

### 舍入

`Math.floor`
向下舍入：`3.1` 变成 `3`，`-1.1` 变成 `-2`。
`Math.ceil`
向上舍入：`3.1` 变成 `4`，`-1.1` 变成 `-1`。
`Math.round`
向最近的整数舍入：`3.1` 变成 `3`，`3.6` 变成 `4`，中间值 `3.5` 变成 `4`。
`Math.trunc`（IE 浏览器不支持这个方法）
移除小数点后的所有内容而没有舍入：`3.1` 变成 `3`，`-1.1` 变成 `-1`。

- 们想将数字舍入到小数点后 `n` 位，该怎么办？
```javascript
let num = 1.23456;
alert( Math.round(num * 100) / 100 ); // 1.23456 -> 123.456 -> 123 -> 1.23
```
```javascript
let num = 12.34;
alert( num.toFixed(1) ); // "12.3"
```
```javascript
let num = 12.36;
alert( num.toFixed(1) ); // "12.4"

```
```javascript
let num = 12.34;
alert( num.toFixed(5) ); // "12.34000"，在结尾添加了 0，以达到小数点后五位
```
### 不精确计算
- 溢出
```javascript
alert( 1e500 ); // Infinity
```
- 精度损失
```javascript
alert( 0.1 + 0.2 == 0.3 ); // false
```
- 这是一个普遍的问题 使用二进制数字系统无法 **精确** 存储 _0.1_ 或 _0.2_，
	- 在十进制数字系统中，这样的数字表示起来很容易。将其与三分之一进行比较：`1/3`。三分之一变成了无限循环小数 `0.33333(3)`。
	- 在二进制数字系统中，可以保证以 `2` 的整数次幂作为除数时能够正常工作，但 `1/10` 就变成了一个无限循环的二进制小数。
- 解决精度问题
```javascript
let sum = 0.1 + 0.2;
alert( sum.toFixed(2) ); // "0.30"
```

- 有 64 位来表示该数字，其中 52 位可用于存储数字，
```javascript
// Hello！我是一个会自我增加的数字！
alert( 9999999999999999 ); // 显示 10000000000000000
```

- 两个零
	- 数字内部表示的另一个有趣结果是存在两个零：`0` 和 `-0`。

### 测试：isFinite 和 isNaN

-   `Infinity`（和 `-Infinity`）是一个特殊的数值，比任何数值都大（小）。
-   `NaN` 代表一个 error。
- 它们属于 `number` 类型，但不是“普通”数字

- `isNaN(value)` 将其参数转换为数字，然后测试它是否为 `NaN`：
```javascript
alert( isNaN(NaN) ); // true
alert( isNaN("str") ); // true
```
- 值 “NaN” 是独一无二的，它不等于任何东西，包括它自身：
```javascript
    alert( NaN === NaN ); // false
```

- `isFinite(value)` 将其参数转换为数字，如果是常规数字而不是 `NaN/Infinity/-Infinity`，则返回 `true`：
```javascript
    alert( isFinite("15") ); // true
    alert( isFinite("str") ); // false，因为是一个特殊的值：NaN
    alert( isFinite(Infinity) ); // false，因为是一个特殊的值：Infinity
```

- 有时 `isFinite` 被用于验证字符串值是否为常规数字：
```javascript
let num = +prompt("Enter a number", '');

// 结果会是 true，除非你输入的是 Infinity、-Infinity 或不是数字
alert( isFinite(num) );
```

- 在所有数字函数中，包括 `isFinite`，空字符串或仅有空格的字符串均被视为 `0`。

-  `Object.is`
	- 它类似于 `===` 一样对值进行比较，但它对于两种边缘情况更可靠：
		- 它适用于 `NaN`：`Object.is(NaN, NaN) === true`，这是件好事。
		- 值 `0` 和 `-0` 是不同的：`Object.is(0, -0) === false`，从技术上讲这是对的，因为在内部，数字的符号位可能会不同，即使其他所有位均为零。
	- 在所有其他情况下，`Object.is(a, b)` 与 `a === b` 相同。

### parseInt 和 parseFloat

- 使用加号 `+` 或 `Number()` 的数字转换是严格的。如果一个值不完全是一个数字，就会失败：
```javascript
alert( +"100px" ); // NaN
```
- 提取数字
```javascript
alert( parseInt('100px') ); // 100
alert( parseFloat('12.5em') ); // 12.5

alert( parseInt('12.3') ); // 12，只有整数部分被返回了
alert( parseFloat('12.3.4') ); // 12.3，在第二个点出停止了读取
```

- 不提取的情况
```javascript
alert( parseInt('a123') ); // NaN，第一个符号停止了读取
```

- 第二个参数
```javascript
alert( parseInt('0xff', 16) ); // 255
alert( parseInt('ff', 16) ); // 255，没有 0x 仍然有效

alert( parseInt('2n9c', 36) ); // 123456
```

### 其他数学函数

- Math.random()  //返回一个从 0 到 1 的随机数（不包括 1）。
-  `Math.max(a, b, c...)` 和 `Math.min(a, b, c...)`  从任意数量的参数中返回最大值和最小值。
```javascript
alert( Math.max(3, 5, -10, 0, 1) ); // 5
alert( Math.min(1, 2) ); // 1
```
- Math.pow(n, power)
```javascript
alert( Math.pow(2, 10) ); // 2 的 10 次幂 = 1024
```

## 字符串
- 字符串的内部格式始终是 [UTF-16](https://en.wikipedia.org/wiki/UTF-16)，它不依赖于页面编码。

### 引号（Quotes）
```javascript
let single = 'single-quoted';
let double = "double-quoted";

let backticks = `backticks`;
```
- 单引号和双引号基本相同。但是，反引号允许我们通过 `${…}` 将任何表达式嵌入到字符串中：
```javascript
function sum(a, b) {
  return a + b;
}

alert(`1 + 2 = ${sum(1, 2)}.`); // 1 + 2 = 3.
```
- 使用反引号的另一个优点是它们允许字符串跨行：
```javascript
let guestList = `Guests:
 * John
 * Pete
 * Mary
`;

alert(guestList); // 客人清单，多行
```

- 反引号还允许我们在第一个反引号之前指定一个“模版函数”
### 特殊字符
- 换行符
```javascript
let str1 = "Hello\nWorld"; // 使用“换行符”创建的两行字符串

// 使用反引号和普通的换行创建的两行字符串
let str2 = `Hello
World`;

alert(str1 == str2); // true
```
- unicode 
```javascript
alert( "\u00A9" ); // ©
alert( "\u{20331}" ); // 佫，罕见的中国象形文字（长 Unicode）
alert( "\u{1F60D}" ); // 😍，笑脸符号（另一个长 Unicode）
```
- 转义
```javascript
alert( 'I\'m the Walrus!' ); // I'm the Walrus!
```
```javascript
alert( `I'm the Walrus!` ); // I'm the Walrus!
```
```javascript
alert( `The backslash: \\` ); // The backslash: \
```

### 字符串长度
- `length` 是一个属性
```javascript
alert( `My\n`.length ); // 3
```
### 访问字符

```javascript
let str = `Hello`;

// 第一个字符
alert( str[0] ); // H
alert( str.charAt(0) ); // H

// 最后一个字符
alert( str[str.length - 1] ); // o
```
```javascript
let str = `Hello`;

alert( str[1000] ); // undefined
alert( str.charAt(1000) ); // ''（空字符串）
```
- for of
```javascript
for (let char of "Hello") {
  alert(char); // H,e,l,l,o（char 变为 "H"，然后是 "e"，然后是 "l" 等）
}
```
### 字符串不可变
```javascript
let str = 'Hi';

str[0] = 'h'; // error
alert( str[0] ); // 无法运行
```

```javascript
let str = 'Hi';

str = 'h' + str[1];  // 替换字符串

alert( str ); // hi
```
### 改变大小写
```javascript
alert( 'Interface'.toUpperCase() ); // INTERFACE
alert( 'Interface'.toLowerCase() ); // interface
```
```javascript
alert( 'Interface'[0].toLowerCase() ); // 'i'
```

### 查找字符串

- str.indexOf 第二个参数是开始查找位置
```javascript
let str = "As sly as a fox, as strong as an ox";
let target = "as";

let pos = -1;
while ((pos = str.indexOf(target, pos + 1)) != -1) {
  alert( pos );
}
``````
- str.lastIndexOf(substr, pos) 从末尾开始查找
- 按位（bitwise）NOT 技巧
	- 对于 32-bit 整数，`~n` 等于 `-(n+1)`。
	- 只要记住：`if (~str.indexOf(...))` 读作 “if found”。
```javascript
let str = "Widget";

if (~str.indexOf("Widget")) {
  alert( 'Found it!' ); // 正常运行
}
```

- includes，startsWith，endsWith
```javascript
alert( "Widget".includes("id") ); // true
alert( "Widget".includes("id", 3) ); // false, 从位置 3 开始没有 "id"
```
```javascript
alert( "Widget".startsWith("Wid") ); // true，"Widget" 以 "Wid" 开始
alert( "Widget".endsWith("get") ); // true，"Widget" 以 "get" 结束
```
### 获取子字符串
- `str.slice(start [, end])`
```javascript
let str = "stringify";
alert( str.slice(0, 5) ); // 'strin'，从 0 到 5 的子字符串（不包括 5）
alert( str.slice(0, 1) ); // 's'，从 0 到 1，但不包括 1，所以只有在 0 处的字符
```
```javascript
let str = "stringify";
alert( str.slice(2) ); // 从第二个位置直到结束
```

```javascript
let str = "stringify";

// 从右边的第四个位置开始，在右边的第一个位置结束
alert( str.slice(-4, -1) ); // 'gif'
```

- `str.substring(start [, end])`
	- 这与 `slice` 几乎相同，但它允许 `start` 大于 `end`。
	- 不支持负参数（不像 slice），它们被视为 `0`。
```javascript
let str = "stringify";

// 这些对于 substring 是相同的
alert( str.substring(2, 6) ); // "ring"
alert( str.substring(6, 2) ); // "ring"

// ……但对 slice 是不同的：
alert( str.slice(2, 6) ); // "ring"（一样）
alert( str.slice(6, 2) ); // ""（空字符串）
```
- `str.substr(start [, length])`
	- 与以前的方法相比，这个允许我们指定 `length` 而不是结束位置
```javascript
let str = "stringify";
alert( str.substr(2, 4) ); // 'ring'，从位置 2 开始，获取 4 个字符
```
```javascript
let str = "stringify";
alert( str.substr(-4, 2) ); // 'gi'，从倒数第 4 位获取 2 个字符
```
### 比较字符串
- 字符串按字母顺序逐字比较
- 奇怪的地方
	- 小写字母总是大于大写字母：
	```javascript
		    alert( 'a' > 'Z' ); // true
	```
	- 带变音符号的字母存在“乱序”的情况：
		```javascript
			alert( 'Österreich' > 'Zealand' ); // true
		```
- `str.codePointAt(pos)`
```javascript
// 不同的字母有不同的代码
alert( "z".codePointAt(0) ); // 122
alert( "Z".codePointAt(0) ); // 90
```

- String.fromCodePoint(code)
```javascript
alert( String.fromCodePoint(90) ); // Z
```
```javascript
// 在十六进制系统中 90 为 5a
alert( '\u005a' ); // Z
```
```javascript
let str = '';

for (let i = 65; i <= 220; i++) {
  str += String.fromCodePoint(i);
}
alert( str );
// ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
// ¡¢£¤¥¦§¨©ª«¬­®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜ
```

### 正确的比较
所有现代浏览器（IE10- 需要额外的库 [Intl.JS](https://github.com/andyearnshaw/Intl.js/)) 都支持国际化标准 [ECMA-402](http://www.ecma-international.org/ecma-402/1.0/ECMA-402.pdf)。

调用 [str.localeCompare(str2)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/String/localeCompare) 会根据语言规则返回一个整数，这个整数能指示字符串 `str` 在排序顺序中排在字符串 `str2` 前面、后面、还是相同：

-   如果 `str` 排在 `str2` 前面，则返回负数。
-   如果 `str` 排在 `str2` 后面，则返回正数。
-   如果它们在相同位置，则返回 `0`。
```javascript
alert( 'Österreich'.localeCompare('Zealand') ); // -1
```

### 内部，Unicode
- 所有常用的字符都是一个 2 字节的代码。2 字节只允许 65536 个组合，这对于表示每个可能的符号是不够的。所以稀有的符号被称为“代理对”的一对 2 字节的符号编码。

```javascript
alert( '𝒳'.length ); // 2，大写数学符号 X
alert( '😂'.length ); // 2，笑哭表情
alert( '𩷶'.length ); // 2，罕见的中国象形文字
```

```javascript
alert( '𝒳'[0] ); // 奇怪的符号……
alert( '𝒳'[1] ); // ……代理对的一块
```

```javascript
// charCodeAt 不理解代理对，所以它给出了代理对的代码

alert( '𝒳'.charCodeAt(0).toString(16) ); // d835，在 0xd800 和 0xdbff 之间
alert( '𝒳'.charCodeAt(1).toString(16) ); // dcb3, 在 0xdc00 和 0xdfff 之间
```
- 处理可参考后面的的可迭代对象
### 变音符号与规范化
- UTF-16 允许我们使用多个 Unicode 字符：基本字符紧跟“装饰”它的一个或多个“标记”字符。
```javascript
let s1 = 'S\u0307\u0323'; // Ṩ，S + 上点 + 下点
let s2 = 'S\u0323\u0307'; // Ṩ，S + 下点 + 上点

alert( `s1: ${s1}, s2: ${s2}` );

alert( s1 == s2 ); // false，尽管字符看起来相同（?!）
```
- Unicode 规范化
```javascript
alert( "S\u0307\u0323".normalize() == "S\u0323\u0307".normalize() ); // true
```
```javascript
alert( "S\u0307\u0323".normalize().length ); // 1

alert( "S\u0307\u0323".normalize() == "\u1e68" ); // true
```
- [Unicode 规范化形式](http://www.unicode.org/reports/tr15/)

## 数组
### 声明
- 两种方法
```javascript
let arr = new Array();
let arr = [];
```
- 增删改查
```javascript
let fruits = ["Apple", "Orange", "Plum"];

alert( fruits[0] ); // Apple
alert( fruits[1] ); // Orange
alert( fruits[2] ); // Plum

fruits[2] = 'Pear'; // 现在变成了 ["Apple", "Orange", "Pear"]

fruits[3] = 'Lemon'; // 现在变成 ["Apple", "Orange", "Pear", "Lemon"]

alert( fruits.length ); // 4

alert( fruits ); // Apple,Orange,Plum,Lemon

```
- 存储任意类型
```javascript
// 混合值
let arr = [ 'Apple', { name: 'John' }, true, function() { alert('hello'); } ];

// 获取索引为 1 的对象然后显示它的 name
alert( arr[1].name ); // John

// 获取索引为 3 的函数并执行
arr[3](); // hello
```
### 使用 “at” 获取最后一个元素
```javascript
let fruits = ["Apple", "Orange", "Plum"];

// 与 fruits[fruits.length-1] 相同
alert( fruits.at(-1) ); // Plum
```
-   如果 `i >= 0`，则与 `arr[i]` 完全相同。
-   对于 `i` 为负数的情况，它则从数组的尾部向前数。

### pop/push, shift/unshift 方法
- 队列
	-   `push` 在末端添加一个元素.
	-   `shift` 取出队列首端的一个元素，整个队列往前移，这样原先排第二的元素现在排在了第一。

- 栈
	-   `push` 在末端添加一个元素.
	-   `pop` 从末端取出一个元素.
- **作用于数组末端的方法：**
	- pop
	```javascript
	let fruits = ["Apple", "Orange", "Pear"];
	
	alert( fruits.pop() ); // 移除 "Pear" 然后 alert 显示出来
	
	alert( fruits ); // Apple, Orange
	```
	- push
	```javascript
	let fruits = ["Apple", "Orange"];
	
	fruits.push("Pear");
	
	alert( fruits ); // Apple, Orange, Pear
	```
- **作用于数组首端的方法：**
	- shift 取出数组的第一个元素并返回它：
	```javascript
	let fruits = ["Apple", "Orange", "Pear"];
	
	alert( fruits.shift() ); // 移除 Apple 然后 alert 显示出来
	
	alert( fruits ); // Orange, Pear
	```
	- `unshift`
	```javascript
	let fruits = ["Orange", "Pear"];
	
	fruits.unshift('Apple');
	
	alert( fruits ); // Apple, Orange, Pear
	```
	```javascript
	let fruits = ["Orange", "Pear"];
	
	fruits.unshift('Apple');
	
	alert( fruits ); // Apple, Orange, Pear
	```
### 内部
- 数组是一个对象，因此其行为也像一个对象。
- 数组误用的几种方式:
	-   添加一个非数字的属性，比如 `arr.test = 5`。
	-   制造空洞，比如：添加 `arr[0]`，然后添加 `arr[1000]` (它们中间什么都没有)。
	-   以倒序填充数组，比如 `arr[1000]`，`arr[999]` 等等。
### 性能
- `push/pop` 方法运行的比较快，而 `shift/unshift` 比较慢。

### 循环
- 老方式
```javascript
let arr = ["Apple", "Orange", "Pear"];

for (let i = 0; i < arr.length; i++) {
  alert( arr[i] );
}
```
- for of
```javascript
let fruits = ["Apple", "Orange", "Plum"];

// 遍历数组元素
for (let fruit of fruits) {
  alert( fruit );
}
```
- for in
	- - `for..in` 循环会遍历 **所有属性**，不仅仅是这些数字属性。
	- `for..in` 循环适用于普通对象，并且做了对应的优化。但是不适用于数组，因此速度要慢 10-100 倍。
```javascript
let arr = ["Apple", "Orange", "Pear"];

for (let key in arr) {
  alert( arr[key] ); // Apple, Orange, Pear
}
```
### 关于 “length”

```javascript
let fruits = [];
fruits[123] = "Apple";

alert( fruits.length ); // 124
```
- 截断 ，清空数组最简单的方法就是：`arr.length = 0;`。
```javascript
let arr = [1, 2, 3, 4, 5];

arr.length = 2; // 截断到只剩 2 个元素
alert( arr ); // [1, 2]

arr.length = 5; // 又把 length 加回来
alert( arr[3] ); // undefined：被截断的那些数值并没有回来
```
### new Array()
```javascript
let arr = new Array("Apple", "Pear", "etc");
```
```javascript
let arr = new Array(2); // 会创建一个 [2] 的数组吗？

alert( arr[0] ); // undefined！没有元素。

alert( arr.length ); // length 2
```

### 多维数组

```javascript
let matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
];

alert( matrix[1][1] ); // 最中间的那个数
```
### toString
- 数组有自己的 `toString` 方法的实现，会返回以逗号隔开的元素列表。
```javascript
let arr = [1, 2, 3];

alert( arr ); // 1,2,3
alert( String(arr) === '1,2,3' ); // true
```
```javascript
alert( [] + 1 ); // "1"
alert( [1] + 1 ); // "11"
alert( [1,2] + 1 ); // "1,21"
```
- 数组没有 `Symbol.toPrimitive`，也没有 `valueOf`，它们只能执行 `toString` 进行转换，所以这里 `[]` 就变成了一个空字符串，`[1]` 变成了 `"1"`，`[1,2]` 变成了 `"1,2"`。

### 不要使用 == 比较数组
- 如果我们使用 `==` 来比较数组，除非我们比较的是两个引用同一数组的变量，否则它们永远不相等。
```javascript
alert( [] == [] ); // false
alert( [0] == [0] ); // false
```

```javascript
alert( 0 == [] ); // true

alert('0' == [] ); // false
```

- 我们应该如何对数组进行比较呢
	- 可以在循环中或者使用下一章中我们将介绍的迭代方法逐项地比较它们。

## 数组方法

### 添加/移除数组元素
#### splice
- 用delete 删除了长度不变 
```javascript
let arr = ["I", "go", "home"];

delete arr[1]; // remove "go"

alert( arr[1] ); // undefined

// now arr = ["I",  , "home"];
alert( arr.length ); // 3
```
- splice删除
```javascript
let arr = ["I", "study", "JavaScript"];

arr.splice(1, 1); // 从索引 1 开始删除 1 个元素

alert( arr ); // ["I", "JavaScript"]
```
- splice 替换
```javascript
let arr = ["I", "study", "JavaScript", "right", "now"];

// 删除数组的前三项，并使用其他内容代替它们
arr.splice(0, 3, "Let's", "dance");

alert( arr ) // 现在 ["Let's", "dance", "right", "now"]
```
- splice 返回删除元素
```javascript
let arr = ["I", "study", "JavaScript", "right", "now"];

// 删除前两个元素
let removed = arr.splice(0, 2);

alert( removed ); // "I", "study" <-- 被从数组中删除了的元素
```
- 插入元素
```javascript
let arr = ["I", "study", "JavaScript"];

// 从索引 2 开始
// 删除 0 个元素
// 然后插入 "complex" 和 "language"
arr.splice(2, 0, "complex", "language");

alert( arr ); // "I", "study", "complex", "language", "JavaScript"
```
- splice 负向索引
```javascript
let arr = [1, 2, 5];

// 从索引 -1（尾端前一位）
// 删除 0 个元素，
// 然后插入 3 和 4
arr.splice(-1, 0, 3, 4);

alert( arr ); // 1,2,3,4,5
```
#### spice
```javascript
let arr = ["t", "e", "s", "t"];

alert( arr.slice(1, 3) ); // e,s（复制从位置 1 到位置 3 的元素）

alert( arr.slice(-2) ); // s,t（复制从位置 -2 到尾端的元素）
```

#### concat
```javascript
let arr = [1, 2];

// 从 arr 和 [3,4] 创建一个新数组
alert( arr.concat([3, 4]) ); // 1,2,3,4

// 从 arr、[3,4] 和 [5,6] 创建一个新数组
alert( arr.concat([3, 4], [5, 6]) ); // 1,2,3,4,5,6

// 从 arr、[3,4]、5 和 6 创建一个新数组
alert( arr.concat([3, 4], 5, 6) ); // 1,2,3,4,5,6
```
```javascript
let arr = [1, 2];

let arrayLike = {
  0: "something",
  length: 1
};

alert( arr.concat(arrayLike) ); // 1,2,[object Object]
```
- 其他对象
```javascript
let arr = [1, 2];

let arrayLike = {
  0: "something",
  1: "else",
  [Symbol.isConcatSpreadable]: true,
  length: 2
};

alert( arr.concat(arrayLike) ); // 1,2,something,else
```

### foreach
```javascript
arr.forEach(function(item, index, array) {
  // ... do something with item
});
```
```javascript
// 对每个元素调用 alert
["Bilbo", "Gandalf", "Nazgul"].forEach(alert);
```
```javascript
["Bilbo", "Gandalf", "Nazgul"].forEach((item, index, array) => {
  alert(`${item} is at index ${index} in ${array}`);
});
```

### 在数组中搜索
#### indexOf/lastIndexOf 和 includes
-   `arr.indexOf(item, from)` —— 从索引 `from` 开始搜索 `item`，如果找到则返回索引，否则返回 `-1`。
- `arr.includes(item, from)` —— 从索引 `from` 开始搜索 `item`，如果找到则返回 `true`（译注：如果没找到，则返回 `false`）。
- 方法 `includes` 可以正确的处理 `NaN`
```javascript
const arr = [NaN];
alert( arr.indexOf(NaN) ); // -1（错，应该为 0）
alert( arr.includes(NaN) );// true（正确）
```
#### find 和 findIndex/findLastIndex

```javascript
let result = arr.find(function(item, index, array) {
  // 如果返回 true，则返回 item 并停止迭代
  // 对于假值（falsy）的情况，则返回 undefined
});
```
```javascript
let users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"},
  {id: 4, name: "John"}
];

// 寻找第一个 John 的索引
alert(users.findIndex(user => user.name == 'John')); // 0

// 寻找最后一个 John 的索引
alert(users.findLastIndex(user => user.name == 'John')); // 3
```
#### filter
```javascript
let results = arr.filter(function(item, index, array) {
  // 如果 true item 被 push 到 results，迭代继续
  // 如果什么都没找到，则返回空数组
});
```
```javascript
let users = [
  {id: 1, name: "John"},
  {id: 2, name: "Pete"},
  {id: 3, name: "Mary"}
];

// 返回前两个用户的数组
let someUsers = users.filter(item => item.id < 3);

alert(someUsers.length); // 2
```

### 转换数组
#### map
- 它对数组的每个元素都调用函数，并返回结果数组。

```javascript
let result = arr.map(function(item, index, array) {
  // 返回新值而不是当前元素
})
```
```javascript
let lengths = ["Bilbo", "Gandalf", "Nazgul"].map(item => item.length);
alert(lengths); // 5,7,6
```

#### sort
对数组进行 **原位（in-place）** 排序，
```javascript
let arr = [ 1, 2, 15 ];

// 该方法重新排列 arr 的内容
arr.sort();

alert( arr );  // 1, 15, 2
```
```javascript
function compareNumeric(a, b) {
  if (a > b) return 1;
  if (a == b) return 0;
  if (a < b) return -1;
}

let arr = [ 1, 2, 15 ];

arr.sort(compareNumeric);

alert(arr);  // 1, 2, 15
```
- 用箭头函数
```javascript
arr.sort( (a, b) => a - b );
```

- localeCompare
```javascript
let countries = ['Österreich', 'Andorra', 'Vietnam'];

alert( countries.sort( (a, b) => a > b ? 1 : -1) ); // Andorra, Vietnam, Österreich（错的）

alert( countries.sort( (a, b) => a.localeCompare(b) ) ); // Andorra,Österreich,Vietnam（对的！）
```
#### reverse
```javascript
let arr = [1, 2, 3, 4, 5];
arr.reverse();

alert( arr ); // 5,4,3,2,1
```

#### split  join
- 二个数字参数 —— 对数组长度的限制。如果提供了，那么额外的元素会被忽略。
```javascript
let names = 'Bilbo, Gandalf, Nazgul';

let arr = names.split(', ');

for (let name of arr) {
  alert( `A message to ${name}.` ); // A message to Bilbo（和其他名字）
}

let arr = 'Bilbo, Gandalf, Nazgul, Saruman'.split(', ', 2); 
alert(arr); // Bilbo, Gandalf
```
- 拆分为字母
```javascript
let str = "test";
alert( str.split('') ); // t,e,s,t
```
- join 与split 相反
```javascript
let arr = ['Bilbo', 'Gandalf', 'Nazgul'];

let str = arr.join(';'); // 使用分号 ; 将数组粘合成字符串

alert( str ); // Bilbo;Gandalf;Nazgul
```
#### reduce/reduceRight
- 当我们需要遍历一个数组时 —— 我们可以使用 `forEach`，`for` 或 `for..of`。
- 当我们需要遍历并返回每个元素的数据时 —— 我们可以使用 `map`。
- reduce 它们用于根据数组计算单个值  reduce和reduceRight 遍历方向不一样
```javascript
let value = arr.reduce(function(accumulator, item, index, array) {
  // ...
}, [initial]);
```
- 该函数一个接一个地应用于所有数组元素，并将其结果“搬运（carry on）”到下一个调用。
	-   `accumulator` —— 是上一个函数调用的结果，第一次等于 `initial`（如果提供了 `initial` 的话）。
	-   `item` —— 当前的数组元素。
	-   `index` —— 当前索引。
	-   `arr` —— 数组本身。

```javascript
let arr = [1, 2, 3, 4, 5];

let result = arr.reduce((sum, current) => sum + current, 0);

alert(result); // 15
```

### Array.isArray
- type 不能区分数组类型
```javascript
alert(typeof {}); // object
alert(typeof []); // object（相同）
```
```javascript
alert(Array.isArray({})); // false
alert(Array.isArray([])); // true
```

### 大多数方法都支持 “thisArg”

```javascript
let army = {
  minAge: 18,
  maxAge: 27,
  canJoin(user) {
    return user.age >= this.minAge && user.age < this.maxAge;
  }
};

let users = [
  {age: 16},
  {age: 20},
  {age: 23},
  {age: 30}
];

// 找到 army.canJoin 返回 true 的 user
let soldiers = users.filter(army.canJoin, army);

alert(soldiers.length); // 2
alert(soldiers[0].age); // 20
alert(soldiers[1].age); // 23
```
- 如果在上面的示例中我们使用了 `users.filter(army.canJoin)`，那么 `army.canJoin` 将被作为独立函数调用，并且这时 `this=undefined`，从而会导致即时错误。
- 可以用 `users.filter(user => army.canJoin(user))` 替换对 `users.filter(army.canJoin, army)` 的调用。前者的使用频率更高，因为对于大多数人来说，它更容易理解。
## Iterable object（可迭代对象）
- 它是数组的泛化
- 这个概念是说任何对象都可以被定制为可在 `for..of` 循环中使用的对象。

### Symbol.iterator
```javascript
let range = {
  from: 1,
  to: 5
};

// 我们希望 for..of 这样运行：
// for(let num of range) ... num=1,2,3,4,5
```
- 有注释的 `range` 的完整实现：
```javascript
let range = {
  from: 1,
  to: 5
};

// 1. for..of 调用首先会调用这个：
range[Symbol.iterator] = function() {

  // ……它返回迭代器对象（iterator object）：
  // 2. 接下来，for..of 仅与下面的迭代器对象一起工作，要求它提供下一个值
  return {
    current: this.from,
    last: this.to,

    // 3. next() 在 for..of 的每一轮循环迭代中被调用
    next() {
      // 4. 它将会返回 {done:.., value :...} 格式的对象
      if (this.current <= this.last) {
        return { done: false, value: this.current++ };
      } else {
        return { done: true };
      }
    }
  };
};

// 现在它可以运行了！
for (let num of range) {
  alert(num); // 1, 然后是 2, 3, 4, 5
}
```

### 字符串是可迭代的
```javascript
for (let char of "test") {
  // 触发 4 次，每个字符一次
  alert( char ); // t, then e, then s, then t
}
```
对于代理对 也能工作
```javascript
let str = '𝒳😂';
for (let char of str) {
    alert( char ); // 𝒳，然后是 😂
}
```

### 显式调用迭代器
```javascript
let str = "Hello";

// 和 for..of 做相同的事
// for (let char of str) alert(char);

let iterator = str[Symbol.iterator]();

while (true) {
  let result = iterator.next();
  if (result.done) break;
  alert(result.value); // 一个接一个地输出字符
}
```
### 可迭代（iterable）和类数组（array-like）
-   **Iterable** 如上所述，是实现了 `Symbol.iterator` 方法的对象。
-   **Array-like** 是有索引和 `length` 属性的对象，所以它们看起来很像数组。
-   字符串即是可迭代的（`for..of` 对它们有效），又是类数组的（它们有数值索引和 `length` 属性）
- 下面这个是类数组，但不是可迭代
```javascript
let arrayLike = { // 有索引和 length 属性 => 类数组对象
  0: "Hello",
  1: "World",
  length: 2
};

// Error (no Symbol.iterator)
for (let item of arrayLike) {}
```

### Array.from
- 有一个全局方法 [Array.from](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Array/from) 可以接受一个可迭代或类数组的值，并从中获取一个“真正的”数组。然后我们就可以对其调用数组方法了。
```javascript
let arrayLike = {
  0: "Hello",
  1: "World",
  length: 2
};

let arr = Array.from(arrayLike); // (*)
alert(arr.pop()); // World（pop 方法有效）
```

```javascript
// 假设 range 来自上文的例子中
let arr = Array.from(range);
alert(arr); // 1,2,3,4,5 （数组的 toString 转化方法生效）
```
- 可选的第二个参数 `mapFn` 可以是一个函数，该函数会在对象中的元素被添加到数组前，被应用于每个元素，此外 `thisArg` 允许我们为该函数设置 `this`。
```javascript
// 假设 range 来自上文例子中

// 求每个数的平方
let arr = Array.from(range, num => num * num);

alert(arr); // 1,4,9,16,25
```
- 创建代理感知（surrogate-aware）的`slice` 方法
```javascript
function slice(str, start, end) {
  return Array.from(str).slice(start, end).join('');
}

let str = '𝒳😂𩷶';

alert( slice(str, 1, 3) ); // 😂𩷶

// 原生方法不支持识别代理对（译注：UTF-16 扩展字符）
alert( str.slice(1, 3) ); // 乱码（两个不同 UTF-16 扩展字符碎片拼接的结果）
```
## Map and Set（映射和集合）

### Map
[Map](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Map) 是一个带键的数据项的集合，就像一个 `Object` 一样。 但是它们最大的差别是 `Map` 允许任何类型的键（key）。
#### 方法 属性
-   `new Map()` —— 创建 map。
-   `map.set(key, value)` —— 根据键存储值。
-   `map.get(key)` —— 根据键来返回值，如果 `map` 中不存在对应的 `key`，则返回 `undefined`。
-   `map.has(key)` —— 如果 `key` 存在则返回 `true`，否则返回 `false`。
-   `map.delete(key)` —— 删除指定键的值。
-   `map.clear()` —— 清空 map。
-   `map.size` —— 返回当前元素个数。
```javascript
let map = new Map();

map.set('1', 'str1');   // 字符串键
map.set(1, 'num1');     // 数字键
map.set(true, 'bool1'); // 布尔值键

// 还记得普通的 Object 吗? 它会将键转化为字符串
// Map 则会保留键的类型，所以下面这两个结果不同：
alert( map.get(1)   ); // 'num1'
alert( map.get('1') ); // 'str1'

alert( map.size ); // 3
```

- `map[key]` 不是使用 `Map` 的正确方式
	虽然 `map[key]` 也有效，例如我们可以设置 `map[key] = 2`，这样会将 `map` 视为 JavaScript 的 plain object，因此它暗含了所有相应的限制（仅支持 string/symbol 键等）。
	所以我们应该使用 `map` 方法：`set` 和 `get` 等。

- **Map 还可以使用对象作为键。**
	```javascript
	let john = { name: "John" };
	
	// 存储每个用户的来访次数
	let visitsCountMap = new Map();
	
	// john 是 Map 中的键
	visitsCountMap.set(john, 123);
	
	alert( visitsCountMap.get(john) ); // 123
	```
- `Map` 是怎么比较键的？
	`Map` 使用 [SameValueZero](https://tc39.github.io/ecma262/#sec-samevaluezero) 算法来比较键是否相等。它和严格等于 `===` 差不多，但区别是 `NaN` 被看成是等于 `NaN`。所以 `NaN` 也可以被用作键。
- 链式调用
	 map.set('1', 'str1') .set(1, 'num1') .set(true, 'bool1');
### Map 迭代
```javascript
let recipeMap = new Map([
  ['cucumber', 500],
  ['tomatoes', 350],
  ['onion',    50]
]);

// 遍历所有的键（vegetables）
for (let vegetable of recipeMap.keys()) {
  alert(vegetable); // cucumber, tomatoes, onion
}

// 遍历所有的值（amounts）
for (let amount of recipeMap.values()) {
  alert(amount); // 500, 350, 50
}

// 遍历所有的实体 [key, value]
for (let entry of recipeMap) { // 与 recipeMap.entries() 相同
  alert(entry); // cucumber,500 (and so on)
}

// 对每个键值对 (key, value) 运行 forEach 函数
recipeMap.forEach( (value, key, map) => {
  alert(`${key}: ${value}`); // cucumber: 500 etc
});

```
### Object.entries：从对象创建 Map
- 从数组创建Map
```javascript
// 键值对 [key, value] 数组
let map = new Map([
  ['1',  'str1'],
  [1,    'num1'],
  [true, 'bool1']
]);

alert( map.get('1') ); // str1
```

- 从对象创建map
```javascript
let obj = {
  name: "John",
  age: 30
};

let map = new Map(Object.entries(obj));

alert( map.get('name') ); // John
```

### Object.fromEntries：从 Map 创建对象

```javascript
let prices = Object.fromEntries([
  ['banana', 1],
  ['orange', 2],
  ['meat', 4]
]);

// 现在 prices = { banana: 1, orange: 2, meat: 4 }

alert(prices.orange); // 2
```
```javascript
let map = new Map();
map.set('banana', 1);
map.set('orange', 2);
map.set('meat', 4);

let obj = Object.fromEntries(map.entries()); // 创建一个普通对象（plain object）(*)

// 完成了！
// obj = { banana: 1, orange: 2, meat: 4 }

alert(obj.orange); // 2
```

### Set
- `Set` 是一个特殊的类型集合 —— “值的集合”（没有键），它的每一个值只能出现一次。
#### 主要方法属性
-   `new Set(iterable)` —— 创建一个 `set`，如果提供了一个 `iterable` 对象（通常是数组），将会从数组里面复制值到 `set` 中。
-   `set.add(value)` —— 添加一个值，返回 set 本身
-   `set.delete(value)` —— 删除值，如果 `value` 在这个方法调用的时候存在则返回 `true` ，否则返回 `false`。
-   `set.has(value)` —— 如果 `value` 在 set 中，返回 `true`，否则返回 `false`。
-   `set.clear()` —— 清空 set。
-   `set.size` —— 返回元素个数。
```javascript
let set = new Set();

let john = { name: "John" };
let pete = { name: "Pete" };
let mary = { name: "Mary" };

// visits，一些访客来访好几次
set.add(john);
set.add(pete);
set.add(mary);
set.add(john);
set.add(mary);

// set 只保留不重复的值
alert( set.size ); // 3

for (let user of set) {
  alert(user.name); // John（然后 Pete 和 Mary）
}
```

### Set 迭代
```javascript
let set = new Set(["oranges", "apples", "bananas"]);

for (let value of set) alert(value);

// 与 forEach 相同：
set.forEach((value, valueAgain, set) => {
  alert(value);
});
```
- `Map` 中用于迭代的方法在 `Set` 中也同样支持：
	-   `set.keys()` —— 遍历并返回一个包含所有值的可迭代对象，
	-   `set.values()` —— 与 `set.keys()` 作用相同，这是为了兼容 `Map`，
	-   `set.entries()` —— 遍历并返回一个包含所有的实体 `[value, value]` 的可迭代对象，它的存在也是为了兼容 `Map`。


## WeakMap and WeakSet（弱映射和弱集合）

### WeakMap 
- `WeakMap` 和 `Map` 的第一个不同点就是，`WeakMap` 的键必须是对象，不能是原始值：
```javascript
let weakMap = new WeakMap();

let obj = {};

weakMap.set(obj, "ok"); // 正常工作（以对象作为键）

// 不能使用字符串作为键
weakMap.set("test", "Whoops"); // Error，因为 "test" 不是一个对象
```
- 如果我们在 weakMap 中使用一个对象作为键，并且没有其他对这个对象的引用 —— 该对象将会被从内存（和map）中自动清除。
```javascript
let john = { name: "John" };

let weakMap = new WeakMap();
weakMap.set(john, "...");

john = null; // 覆盖引用

// john 被从内存中删除了！
```
- `WeakMap` 不支持迭代以及 `keys()`，`values()` 和 `entries()` 方法。所以没有办法获取 `WeakMap` 的所有键或值。
- `WeakMap` 只有以下的方法：
	-   `weakMap.get(key)`
	-   `weakMap.set(key, value)`
	-   `weakMap.delete(key)`
	-   `weakMap.has(key)`
### 使用案例：额外的数据
- 假如我们正在处理一个“属于”另一个代码的一个对象，也可能是第三方库，并想存储一些与之相关的数据，那么这些数据就应该与这个对象共存亡
```javascript
weakMap.set(john, "secret documents");
// 如果 john 消失，secret documents 将会被自动清除
```
- 计数函数的例子
```javascript
// 📁 visitsCount.js
let visitsCountMap = new WeakMap(); // weakmap: user => visits count

// 递增用户来访次数
function countUser(user) {
  let count = visitsCountMap.get(user) || 0;
  visitsCountMap.set(user, count + 1);
}
```
```javascript
// 📁 main.js
let john = { name: "John" };

countUser(john); // count his visits

// 不久之后，john 离开了
john = null;
```
### 使用案例：缓存
#### map方案
```javascript
// 📁 cache.js
let cache = new Map();

// 计算并记住结果
function process(obj) {
  if (!cache.has(obj)) {
    let result = /* calculations of the result for */ obj;

    cache.set(obj, result);
  }

  return cache.get(obj);
}

// 现在我们在其它文件中使用 process()

// 📁 main.js
let obj = {/* 假设我们有个对象 */};

let result1 = process(obj); // 计算完成

// ……稍后，来自代码的另外一个地方……
let result2 = process(obj); // 取自缓存的被记忆的结果

// ……稍后，我们不再需要这个对象时：
obj = null;

alert(cache.size); // 1（啊！该对象依然在 cache 中，并占据着内存！）
```
#### WeakMap 方案
```javascript
// 📁 cache.js
let cache = new WeakMap();

// 计算并记结果
function process(obj) {
  if (!cache.has(obj)) {
    let result = /* calculate the result for */ obj;

    cache.set(obj, result);
  }

  return cache.get(obj);
}

// 📁 main.js
let obj = {/* some object */};

let result1 = process(obj);
let result2 = process(obj);

// ……稍后，我们不再需要这个对象时：
obj = null;

// 无法获取 cache.size，因为它是一个 WeakMap，
// 要么是 0，或即将变为 0
// 当 obj 被垃圾回收，缓存的数据也会被清除
```

### WeakSet
-   与 `Set` 类似，但是我们只能向 `WeakSet` 添加对象（而不能是原始值）。
-   对象只有在其它某个（些）地方能被访问的时候，才能留在 `WeakSet` 中。
-   跟 `Set` 一样，`WeakSet` 支持 `add`，`has` 和 `delete` 方法，但不支持 `size` 和 `keys()`，并且不可迭代。
```javascript
let visitedSet = new WeakSet();

let john = { name: "John" };
let pete = { name: "Pete" };
let mary = { name: "Mary" };

visitedSet.add(john); // John 访问了我们
visitedSet.add(pete); // 然后是 Pete
visitedSet.add(john); // John 再次访问

// visitedSet 现在有两个用户了

// 检查 John 是否来访过？
alert(visitedSet.has(john)); // true

// 检查 Mary 是否来访过？
alert(visitedSet.has(mary)); // false

john = null;

// visitedSet 将被自动清理(即自动清除其中已失效的值 john)
```


## Object.keys，values，entries

```javascript
let user = {
  name: "John",
  age: 30
};
```
-   `Object.keys(user) = ["name", "age"]`
-   `Object.values(user) = ["John", 30]`
-   `Object.entries(user) = [ ["name","John"], ["age",30] ]`
```javascript
let user = {
  name: "John",
  age: 30
};

// 遍历所有的值
for (let value of Object.values(user)) {
  alert(value); // John, then 30
}
```

- Object.keys/values/entries 会忽略 symbol 属性
	- 但是，如果我们也想要 Symbol 类型的键，那么这儿有一个单独的方法 [Object.getOwnPropertySymbols](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols)，它会返回一个只包含 Symbol 类型的键的数组。另外，还有一种方法 [Reflect.ownKeys(obj)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Reflect/ownKeys)，它会返回 **所有** 键。


### 转换对象

- 对象缺少数组存在的许多方法，例如 `map` 和 `filter` 等。如果我们想应用它们，那么我们可以使用 `Object.entries`，然后使用 `Object.fromEntries`：
```javascript
let prices = {
  banana: 1,
  orange: 2,
  meat: 4,
};

let doublePrices = Object.fromEntries(
  // 将价格转换为数组，将每个键/值对映射为另一对
  // 然后通过 fromEntries 再将结果转换为对象
  Object.entries(prices).map(entry => [entry[0], entry[1] * 2])
);

alert(doublePrices.meat); // 8
```

## 解构赋值
- 函数可能不需要整个对象/数组，而只需要其中一部分。**解构赋值** 是一种特殊的语法，它使我们可以将数组或对象“拆包”至一系列变量中
### 数组解构

```javascript
// 我们有一个存放了名字和姓氏的数组
let arr = ["John", "Smith"]

// 解构赋值
// 设置 firstName = arr[0]
// 以及 surname = arr[1]
let [firstName, surname] = arr;

alert(firstName); // John
alert(surname);  // Smith
```
```javascript
let [firstName, surname] = "John Smith".split(' ');
alert(firstName); // John
alert(surname);  // Smith
```

- 忽略使用逗号的元素
```javascript
// 不需要第二个元素
let [firstName, , title] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

alert( title ); // Consul
```

- 等号右侧可以是任何可迭代对象
```javascript
let [a, b, c] = "abc"; // ["a", "b", "c"]
let [one, two, three] = new Set([1, 2, 3]);
```

- 赋值给等号左侧的任何内容
```javascript
let user = {};
[user.name, user.surname] = "John Smith".split(' ');

alert(user.name); // John
alert(user.surname); // Smith
```
- 与 .entries() 方法进行循环操作
```javascript
let user = {
  name: "John",
  age: 30
};

// 使用循环遍历键—值对
for (let [key, value] of Object.entries(user)) {
  alert(`${key}:${value}`); // name:John, then age:30
}
```
- 用于 `Map`
```javascript
let user = new Map();
user.set("name", "John");
user.set("age", "30");

// Map 是以 [key, value] 对的形式进行迭代的，非常便于解构
for (let [key, value] of user) {
  alert(`${key}:${value}`); // name:John, then age:30
}
```
- 交换变量值的技巧
```javascript
let guest = "Jane";
let admin = "Pete";

// 让我们来交换变量的值：使得 guest = Pete，admin = Jane
[guest, admin] = [admin, guest];

alert(`${guest} ${admin}`); // Pete Jane（成功交换！）
```
- 其余的 ‘…’
```javascript
let [name1, name2] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

alert(name1); // Julius
alert(name2); // Caesar
// 其余数组项未被分配到任何地方
```
- 以使用三个点 `"..."` 来再加一个参数以获取其余数组项：
```javascript
let [name1, name2, ...rest] = ["Julius", "Caesar", "Consul", "of the Roman Republic"];

// rest 是包含从第三项开始的其余数组项的数组
alert(rest[0]); // Consul
alert(rest[1]); // of the Roman Republic
alert(rest.length); // 2
```
- 默认值
```javascript
// 默认值
let [name = "Guest", surname = "Anonymous"] = ["Julius"];

alert(name);    // Julius（来自数组的值）
alert(surname); // Anonymous（默认值被使用了）
```
### 对象解构
```javascript
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

let {title, width, height} = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
```
- 顺序不重要
```javascript
let {height, width, title} = { title: "Menu", height: 200, width: 100 }
```
- 改变变量名
```javascript
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

// { sourceProperty: targetVariable }
let {width: w, height: h, title} = options;

// width -> w
// height -> h
// title -> title

alert(title);  // Menu
alert(w);      // 100
alert(h);      // 200
```

- 默认值
```javascript
let options = {
  title: "Menu"
};

let {width = 100, height = 200, title} = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
```
- 提取部分
```javascript
let options = {
  title: "Menu",
  width: 100,
  height: 200
};

// 仅提取 title 作为变量
let { title } = options;

alert(title); // Menu
```
- 剩余模式 ...
```javascript
let options = {
  title: "Menu",
  height: 200,
  width: 100
};

// title = 名为 title 的属性
// rest = 存有剩余属性的对象
let {title, ...rest} = options;

// 现在 title="Menu", rest={height: 200, width: 100}
alert(rest.height);  // 200
alert(rest.width);   // 100
```
### 嵌套结构
```javascript
let options = {
  size: {
    width: 100,
    height: 200
  },
  items: ["Cake", "Donut"],
  extra: true
};

// 为了清晰起见，解构赋值语句被写成多行的形式
let {
  size: { // 把 size 赋值到这里
    width,
    height
  },
  items: [item1, item2], // 把 items 赋值到这里
  title = "Menu" // 在对象中不存在（使用默认值）
} = options;

alert(title);  // Menu
alert(width);  // 100
alert(height); // 200
alert(item1);  // Cake
alert(item2);  // Donut
```

### 智能函数参数
```javascript
// 我们传递一个对象给函数
let options = {
  title: "My menu",
  items: ["Item1", "Item2"]
};

// ……然后函数马上把对象解构成变量
function showMenu({title = "Untitled", width = 200, height = 100, items = []}) {
  // title, items – 提取于 options，
  // width, height – 使用默认值
  alert( `${title} ${width} ${height}` ); // My Menu 200 100
  alert( items ); // Item1, Item2
}

showMenu(options);
```

```javascript
function showMenu({ title = "Menu", width = 100, height = 200 } = {}) {
  alert( `${title} ${width} ${height}` );
}

showMenu(); // Menu 100 200
```

## 日期和时间

### 创建
- new Date()
```javascript
let now = new Date();
alert( now ); // 显示当前的日期/时间
```
- new Date(milliseconds)
```javascript
// 0 表示 01.01.1970 UTC+0
let Jan01_1970 = new Date(0);
alert( Jan01_1970 );

// 现在增加 24 小时，得到 02.01.1970 UTC+0
let Jan02_1970 = new Date(24 * 3600 * 1000);
alert( Jan02_1970 );


// 31 Dec 1969
let Dec31_1969 = new Date(-24 * 3600 * 1000);
alert( Dec31_1969 );
```

- `new Date(datestring)`
```javascript
let date = new Date("2017-01-26");
alert(date);
// 未指定具体时间，所以假定时间为格林尼治标准时间（GMT）的午夜零点
// 并根据运行代码时的用户的时区进行调整
// 因此，结果可能是
// Thu Jan 26 2017 11:00:00 GMT+1100 (Australian Eastern Daylight Time)
// 或
// Wed Jan 25 2017 16:00:00 GMT-0800 (Pacific Standard Time)
```
- `new Date(year, month, date, hours, minutes, seconds, ms)`
```javascript
new Date(2011, 0, 1, 0, 0, 0, 0); // 1 Jan 2011, 00:00:00
new Date(2011, 0, 1); // 同样，时分秒等均为默认值 0
```
	时间度量最大精确到 1 毫秒（1/1000 秒）：
```javascript
let date = new Date(2011, 0, 1, 2, 3, 4, 567);
alert( date ); // 1.01.2011, 02:03:04.567
```
### 访问日期组件
```javascript
//  当前日期
let date = new Date();

// 当地时区的小时数
alert( date.getHours() );

// 在 UTC+0 时区的小时数（非夏令时的伦敦时间）
alert( date.getUTCHours() );
```
```javascript
// 如果你在时区 UTC-1，输出 60
// 如果你在时区 UTC+3，输出 -180
alert( new Date().getTimezoneOffset() );
```
### 设置日期组件

-   [`setFullYear(year, [month], [date])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setFullYear)
-   [`setMonth(month, [date])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMonth)
-   [`setDate(date)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setDate)
-   [`setHours(hour, [min], [sec], [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setHours)
-   [`setMinutes(min, [sec], [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMinutes)
-   [`setSeconds(sec, [ms])`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setSeconds)
-   [`setMilliseconds(ms)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setMilliseconds)
-   [`setTime(milliseconds)`](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/setTime)（使用自 1970-01-01 00:00:00 UTC+0 以来的毫秒数来设置整个日期）
以上方法除了 `setTime()` 都有 UTC 变体
```javascript
let today = new Date();

today.setHours(0);
alert(today); // 日期依然是今天，但是小时数被改为了 0

today.setHours(0, 0, 0, 0);
alert(today); // 日期依然是今天，时间为 00:00:00。
```

### 自动校准
- **自动校准** 是 `Date` 对象的一个非常方便的特性。我们可以设置超范围的数值，它会自动校准。
```javascript
let date = new Date(2013, 0, 32); // 32 Jan 2013 ?!?
alert(date); // ……是 1st Feb 2013!
```
```javascript
let date = new Date(2016, 1, 28);
date.setDate(date.getDate() + 2);

alert( date ); // 1 Mar 2016
```
- 我们还可以设置 0 甚至可以设置负值。例如：
```javascript
let date = new Date(2016, 0, 2); // 2016 年 1 月 2 日

date.setDate(1); // 设置为当月的第一天
alert( date );

date.setDate(0); // 天数最小可以设置为 1，所以这里设置的是上一月的最后一天
alert( date ); // 31 Dec 2015
```
### 日期转化为数字，日期差值
```javascript
let date = new Date();
alert(+date); // 以毫秒为单位的数值，与使用 date.getTime() 的结果相同

```
- 可用于测量时间
```javascript
let start = new Date(); // 开始测量时间

// do the job
for (let i = 0; i < 100000; i++) {
  let doSomething = i * i * i;
}

let end = new Date(); // 结束测量时间

alert( `The loop took ${end - start} ms` );
```
### Date.now()
- 有一个特殊的方法 `Date.now()`，它会返回当前的时间戳。它相当于 `new Date().getTime()`，但它不会创建中间的 `Date` 对象。因此它更快，而且不会对垃圾回收造成额外的压力。
```javascript
let start = Date.now(); // 从 1 Jan 1970 至今的时间戳

// do the job
for (let i = 0; i < 100000; i++) {
  let doSomething = i * i * i;
}

let end = Date.now(); // 完成

alert( `The loop took ${end - start} ms` ); // 相减的是时间戳，而不是日期
```
### 基准测试（Benchmarking）

```javascript
function diffSubtract(date1, date2) {
  return date2 - date1;
}

function diffGetTime(date1, date2) {
  return date2.getTime() - date1.getTime();
}

function bench(f) {
  let date1 = new Date(0);
  let date2 = new Date();

  let start = Date.now();
  for (let i = 0; i < 100000; i++) f(date1, date2);
  return Date.now() - start;
}

let time1 = 0;
let time2 = 0;

// 交替运行 bench(diffSubtract) 和 bench(diffGetTime) 各 10 次
for (let i = 0; i < 10; i++) {
  time1 += bench(diffSubtract);
  time2 += bench(diffGetTime);
}

alert( 'Total time for diffSubtract: ' + time1 );
alert( 'Total time for diffGetTime: ' + time2 );
```
```javascript
// 在主循环中增加预热环节
bench(diffSubtract);
bench(diffGetTime);

// 开始度量
for (let i = 0; i < 10; i++) {
  time1 += bench(diffSubtract);
  time2 += bench(diffGetTime);
}
```

### 对字符串调用 Date.parse

[Date.parse(str)](https://developer.mozilla.org/zh/docs/Web/JavaScript/Reference/Global_Objects/Date/parse) 方法可以从一个字符串中读取日期。
字符串的格式应该为：`YYYY-MM-DDTHH:mm:ss.sssZ`，其中：
-   `YYYY-MM-DD` —— 日期：年-月-日。
-   字符 `"T"` 是一个分隔符。
-   `HH:mm:ss.sss` —— 时间：小时，分钟，秒，毫秒。
-   可选字符 `'Z'` 为 `+-hh:mm` 格式的时区。单个字符 `Z` 代表 UTC+0 时区。
简短形式也是可以的，比如 `YYYY-MM-DD` 或 `YYYY-MM`，甚至可以是 `YYYY`。
- 如果给定字符串的格式不正确，则返回 `NaN`。

```javascript
let date = new Date( Date.parse('2012-01-26T13:51:50.417-07:00') );

alert(date);
```

## JSON 方法，toJSON

### JSON.stringify
JavaScript 提供了如下方法：
-   `JSON.stringify` 将对象转换为 JSON。
-   `JSON.parse` 将 JSON 转换回对象。

```javascript
let student = {
  name: 'John',
  age: 30,
  isAdmin: false,
  courses: ['html', 'css', 'js'],
  spouse: null
};

let json = JSON.stringify(student);

alert(typeof json); // we've got a string!

alert(json);
/* JSON 编码的对象：
{
  "name": "John",
  "age": 30,
  "isAdmin": false,
  "courses": ["html", "css", "js"],
  "spouse": null
}
*/
```

JSON 支持以下数据类型：
-   Objects `{ ... }`
-   Arrays `[ ... ]`
-   Primitives：
    -   strings，
    -   numbers，
    -   boolean values `true/false`，
    -   `null`。
- JSON 是语言无关的纯数据规范，因此一些特定于 JavaScript 的对象属性会被 `JSON.stringify` 跳过。
	-   函数属性（方法）。
	-   Symbol 类型的键和值。
	-   存储 `undefined` 的属性。
```javascript
let user = {
  sayHi() { // 被忽略
    alert("Hello");
  },
  [Symbol("id")]: 123, // 被忽略
  something: undefined // 被忽略
};

alert( JSON.stringify(user) ); // {}（空对象）
```
- 支持嵌套对象转换
```javascript
let meetup = {
  title: "Conference",
  room: {
    number: 23,
    participants: ["john", "ann"]
  }
};

alert( JSON.stringify(meetup) );
/* 整个结构都被字符串化了
{
  "title":"Conference",
  "room":{"number":23,"participants":["john","ann"]},
}
*/
```
- 重要的限制：不得有循环引用。
```javascript
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: ["john", "ann"]
};

meetup.place = room;       // meetup 引用了 room
room.occupiedBy = meetup; // room 引用了 meetup

JSON.stringify(meetup); // Error: Converting circular structure to JSON
```

### 排除和转换：replacer
- 语法
```javascript
let json = JSON.stringify(value[, replacer, space])

```
- 这里去掉循环引用
```javascript
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: [{name: "John"}, {name: "Alice"}],
  place: room // meetup 引用了 room
};

room.occupiedBy = meetup; // room 引用了 meetup

alert( JSON.stringify(meetup, ['title', 'participants', 'place', 'name', 'number']) );
/*
{
  "title":"Conference",
  "participants":[{"name":"John"},{"name":"Alice"}],
  "place":{"number":23}
}
*/
```
- 我们可以使用一个函数代替数组作为 `replacer`。该函数会为每个 `(key,value)` 对调用并返回“已替换”的值，该值将替换原有的值。如果值被跳过了，则为 `undefined`。
```javascript
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  participants: [{name: "John"}, {name: "Alice"}],
  place: room // meetup 引用了 room
};

room.occupiedBy = meetup; // room 引用了 meetup

alert( JSON.stringify(meetup, function replacer(key, value) {
  alert(`${key}: ${value}`);
  return (key == 'occupiedBy') ? undefined : value;
}));

/* key:value pairs that come to replacer:
:             [object Object]
title:        Conference
participants: [object Object],[object Object]
0:            [object Object]
name:         John
1:            [object Object]
name:         Alice
place:        [object Object]
number:       23
occupiedBy: [object Object]
*/
```
### 格式化：space
- `JSON.stringify(value, replacer, spaces)` 的第三个参数是用于优化格式的空格数量。
```javascript
let user = {
  name: "John",
  age: 25,
  roles: {
    isAdmin: false,
    isEditor: true
  }
};

alert(JSON.stringify(user, null, 2));
/* 两个空格的缩进：
{
  "name": "John",
  "age": 25,
  "roles": {
    "isAdmin": false,
    "isEditor": true
  }
}
*/

/* 对于 JSON.stringify(user, null, 4) 的结果会有更多缩进：
{
    "name": "John",
    "age": 25,
    "roles": {
        "isAdmin": false,
        "isEditor": true
    }
}
*/
```

### 自定义 “toJSON”

- 像 `toString` 进行字符串转换，对象也可以提供 `toJSON` 方法来进行 JSON 转换。如果可用，`JSON.stringify` 会自动调用它。
```javascript
let room = {
  number: 23
};

let meetup = {
  title: "Conference",
  date: new Date(Date.UTC(2017, 0, 1)),
  room
};

alert( JSON.stringify(meetup) );
/*
  {
    "title":"Conference",
    "date":"2017-01-01T00:00:00.000Z",  // (1)
    "room": {"number":23}               // (2)
  }
*/
```
- 自定义 toJSON
```javascript
let room = {
  number: 23,
  toJSON() {
    return this.number;
  }
};

let meetup = {
  title: "Conference",
  room
};

alert( JSON.stringify(room) ); // 23

alert( JSON.stringify(meetup) );
/*
  {
    "title":"Conference",
    "room": 23
  }
*/
```

### JSON.parse
```javascript
// 字符串化数组
let numbers = "[0, 1, 2, 3]";

numbers = JSON.parse(numbers);

alert( numbers[1] ); // 1
```

```javascript
let userData = '{ "name": "John", "age": 35, "isAdmin": false, "friends": [0,1,2,3] }';

let user = JSON.parse(userData);

alert( user.friends[1] ); // 1
```

- 典型错误
```javascript
let json = `{
  name: "John",                     // 错误：属性名没有双引号
  "surname": 'Smith',               // 错误：值使用的是单引号（必须使用双引号）
  'isAdmin': false                  // 错误：键使用的是单引号（必须使用双引号）
  "birthday": new Date(2000, 2, 3), // 错误：不允许使用 "new"，只能是裸值
  "friends": [0,1,2,3]              // 这个没问题
}`;
```

### 使用 reviver

```javascript
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';

let meetup = JSON.parse(str);

alert( meetup.date.getDate() ); // Error!
```


```javascript
let str = '{"title":"Conference","date":"2017-11-30T12:00:00.000Z"}';

let meetup = JSON.parse(str, function(key, value) {
  if (key == 'date') return new Date(value);
  return value;
});

alert( meetup.date.getDate() ); // 现在正常运行了！
```

- 也适用于嵌套对象：
```javascript
let schedule = `{
  "meetups": [
    {"title":"Conference","date":"2017-11-30T12:00:00.000Z"},
    {"title":"Birthday","date":"2017-04-18T12:00:00.000Z"}
  ]
}`;

schedule = JSON.parse(schedule, function(key, value) {
  if (key == 'date') return new Date(value);
  return value;
});

alert( schedule.meetups[1].date.getDate() ); // 正常运行了！
```