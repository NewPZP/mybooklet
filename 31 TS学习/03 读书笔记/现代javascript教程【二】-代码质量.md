## 浏览器中调试

### 条件断点
### debugger命令

- 完整手册
	- [https://developers.google.com/web/tools/chrome-devtools](https://developers.google.com/web/tools/chrome-devtools)。

## 代码风格
### 花括号
- 最好的方式
 ```javascript
    if (n < 0) {
      alert(`Power ${n} is not supported`);
    }
```
- 写成一行，不带花括号 —— 如果短的话，也是可以的：
```javascript
    if (n < 0) alert(`Power ${n} is not supported`);
```

### 行的长度
- 一行代码的最大长度应该在团队层面上达成一致。通常是 80 或 120 个字符。
```javascript
// 回勾引号 ` 允许将字符串拆分为多行
let str = `
  ECMA International's TC39 is a group of JavaScript developers,
  implementers, academics, and more, collaborating with the community
  to maintain and evolve the definition of JavaScript.
`;
```

```javascript
if (
  id === 123 &&
  moonPhase === 'Waning Gibbous' &&
  zodiacSign === 'Libra'
) {
  letTheSorceryBegin();
}
```
### 缩进
- **水平方向上的缩进：2 或 4 个空格。**

```javascript
    show(parameters,
         aligned, // 左边有 5 个空格
         one,
         after,
         another
      ) {
      // ...
    }
    ```
- **垂直方向上的缩进：用于将代码拆分成逻辑块的空行。**
```javascript
function pow(x, n) {
  let result = 1;
  //              <--
  for (let i = 0; i < n; i++) {
    result *= x;
  }
  //              <--
  return result;
}
```
-   插入一个额外的空行有助于使代码更具可读性。写代码时，不应该出现连续超过 9 行都没有被垂直分割的代码。
### 分号
- 每一个语句后面都应该有一个分号。即使它可以被跳过。
### 嵌套的层级
```javascript
for (let i = 0; i < 10; i++) {
  if (cond) {
    ... // <- 又一层嵌套
  }
}
```

我们可以这样写：
```javascript
for (let i = 0; i < 10; i++) {
  if (!cond) continue;
  ...  // <- 没有额外的嵌套
}
```

### 函数的位置

1.  在调用这些函数的代码的 **上方** 声明这些函数：
 ```javascript
    // 函数声明
    function createElement() {
      ...
    }
    
    function setHandler(elem) {
      ...
    }
    
    function walkAround() {
      ...
    }
    
    // 调用函数的代码
    let elem = createElement();
    setHandler(elem);
    walkAround();
```
    
2.  先写调用代码，再写函数
```javascript
    // 调用函数的代码
    let elem = createElement();
    setHandler(elem);
    walkAround();
    
    // --- 辅助函数 ---
    function createElement() {
      ...
    }
    
    function setHandler(elem) {
      ...
    }
    
    function walkAround() {
      ...
    }
```
3.  混合：在第一次使用一个函数时，对该函数进行声明。
- 大多数情况下，第二种方式更好。

### 风格指南
- 一些受欢迎的选择：
	-   [Google JavaScript 风格指南](https://google.github.io/styleguide/jsguide.html)
	-   [Airbnb JavaScript 风格指南](https://github.com/airbnb/javascript)
	-   [Idiomatic.JS](https://github.com/rwaldron/idiomatic.js)
	-   [StandardJS](https://standardjs.com/)
### 自动检查器

下面是一些最出名的代码检查工具：
-   [JSLint](https://www.jslint.com/) —— 第一批检查器之一。
-   [JSHint](https://www.jshint.com/) —— 比 JSLint 多了更多设置。
-   [ESLint](https://eslint.org/) —— 应该是最新的一个。
- 
## 注释
### 糟糕的注释
#### 配方：分解函数

- 有时候，用一个函数来代替一个代码片段是更好的，就像这样：
```javascript
function showPrimes(n) {
  nextPrime:
  for (let i = 2; i < n; i++) {

    // 检测 i 是否是一个质数（素数）
    for (let j = 2; j < i; j++) {
      if (i % j == 0) continue nextPrime;
    }

    alert(i);
  }
}
```
- 更好的是使用自描述的形式
```javascript
function showPrimes(n) {

  for (let i = 2; i < n; i++) {
    if (!isPrime(i)) continue;

    alert(i);
  }
}

function isPrime(n) {
  for (let i = 2; i < n; i++) {
    if (n % i == 0) return false;
  }

  return true;
}
```

#### 配方 创建函数
```javascript
// 在这里我们添加威士忌（译注：国外的一种酒）
for(let i = 0; i < 10; i++) {
  let drop = getWhiskey();
  smell(drop);
  add(drop, glass);
}

// 在这里我们添加果汁
for(let t = 0; t < 3; t++) {
  let tomato = getTomato();
  examine(tomato);
  let juice = press(tomato);
  add(juice, glass);
}

// ...
```
- 我们像下面这样，将上面的代码重构为函数，可能会是一个更好的变体：
```javascript
addWhiskey(glass);
addJuice(glass);

function addWhiskey(container) {
  for(let i = 0; i < 10; i++) {
    let drop = getWhiskey();
    //...
  }
}

function addJuice(container) {
  for(let t = 0; t < 3; t++) {
    let tomato = getTomato();
    //...
  }
}
```
### 好的注释
- 描述架构
- 记录函数的参数和用法
```javascript
/**
 * 返回 x 的 n 次幂的值。
 *
 * @param {number} x 要改变的值。
 * @param {number} n 幂数，必须是一个自然数。
 * @return {number} x 的 n 次幂的值。
 */
function pow(x, n) {
  ...
}
```

## 忍者代码
- 不要为秀而秀

## 使用 Mocha 进行自动化测试

-   [Mocha](http://mochajs.org/) —— 核心框架：提供了包括通用型测试函数 `describe` 和 `it`，以及用于运行测试的主函数。
-   [Chai](http://chaijs.com/) —— 提供很多断言（assertion）支持的库。它提供了很多不同的断言，现在我们只需要用 `assert.equal`。
-   [Sinon](http://sinonjs.org/) —— 用于监视函数、模拟内建函数和其他函数的库，我们在后面才会用到它。

## Polyfill 和转译器
- 如何让我们现代的代码在还不支持最新特性的旧引擎上工作？
	1.  转译器（Transpilers）。
	2.  垫片（Polyfills）。
### 转译器（Transpilers）
- 说到名字，[Babel](https://babeljs.io/) 是最著名的转译器之一。

### 垫片（Polyfills）
- 新的语言特性可能不仅包括语法结构和运算符，还可能包括内建函数。
- 由于我们谈论的是新函数，而不是语法更改，因此无需在此处转译任何内容。我们只需要声明缺失的函数。
- 更新/添加新函数的脚本被称为“polyfill”。它“填补”了空白并添加了缺失的实现。
两个有趣的 polyfill 库：
-   [core js](https://github.com/zloirock/core-js) 支持了很多特性，允许只包含需要的特性。
-   [polyfill.io](http://polyfill.io/) 提供带有 polyfill 的脚本的服务，具体取决于特性和用户的浏览器。

