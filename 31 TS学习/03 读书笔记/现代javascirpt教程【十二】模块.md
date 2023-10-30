## 模块简介

### 什么是模块？
- 一个模块（module）就是一个文件。一个脚本就是一个模块。就这么简单。
- 模块可以相互加载，并可以使用特殊的指令 `export` 和 `import` 来交换功能，
```javascript
// 📁 sayHi.js
export function sayHi(user) {
  alert(`Hello, ${user}!`);
}
```
```javascript
// 📁 main.js
import { sayHi } from './sayHi.js';

alert(sayHi); // function...
sayHi('John'); // Hello, John!
```

- 浏览器的例子
```javascript
export function sayHi(user) {
  return `Hello, ${user}!`;
}
```
```html
<!doctype html>
<script type="module">
  import {sayHi} from './say.js';

  document.body.innerHTML = sayHi('John');
</script>
```

### 模块核心功能

#### 始终使用 “use strict”
- 模块始终在严格模式下运行
#### 模块级作用域
- 每个模块都有自己的顶级作用域（top-level scope）。换句话说，一个模块中的顶级作用域变量和函数在其他脚本中是不可见的。

#### 模块代码仅在第一次导入时被解析

```javascript
// 📁 alert.js
alert("Module is evaluated!");
```
```javascript
// 在不同的文件中导入相同的模块

// 📁 1.js
import `./alert.js`; // Module is evaluated!

// 📁 2.js
import `./alert.js`; // (什么都不显示)
```

- 规则
	- 层模块代码应该用于初始化，创建模块特定的内部数据结构。如果我们需要多次调用某些东西 —— 我们应该将其以函数的形式导出，就像我们在上面使用 `sayHi` 那样。
```javascript
// 📁 admin.js
export let admin = {
  name: "John"
};
```
```javascript
// 📁 1.js
import { admin } from './admin.js';
admin.name = "Pete";

// 📁 2.js
import { admin } from './admin.js';
alert(admin.name); // Pete

// 1.js 和 2.js 引用的是同一个 admin 对象
// 在 1.js 中对对象做的更改，在 2.js 中也是可见的
```
- 一个配置例子
```javascript
// 📁 admin.js
export let config = { };

export function sayHi() {
  alert(`Ready to serve, ${config.user}!`);
}
```
```javascript
// 📁 init.js
import { config } from './admin.js';
config.user = "Pete";
```
```javascript
// 📁 another.js
import { sayHi } from './admin.js';

sayHi(); // Ready to serve, Pete!
```

#### import.meta
- `import.meta` 对象包含关于当前模块的信息。
- 在浏览器环境中，它包含当前脚本的 URL，或者如果它是在 HTML 中的话，则包含当前页面的 URL。
```html
<script type="module">
  alert(import.meta.url); // 脚本的 URL
  // 对于内联脚本来说，则是当前 HTML 页面的 URL
</script>
```

#### 在一个模块中，“this” 是 undefined
```html
<script>
  alert(this); // window
</script>

<script type="module">
  alert(this); // undefined
</script>
```

### 浏览器特定功能
- 与常规脚本相比，拥有 `type="module"` 标识的脚本有一些特定于浏览器的差异。
#### 模块脚本是延迟的
- 与 `defer` 特性对外部脚本和内联脚本（inline script）的影响相同。
	- 下载外部模块脚本 `<script type="module" src="...">` 不会阻塞 HTML 的处理，它们会与其他资源并行加载。
	- 模块脚本会等到 HTML 文档完全准备就绪（即使它们很小并且比 HTML 加载速度更快），然后才会运行。
	- 保持脚本的相对顺序：在文档中排在前面的脚本先执行。
- 副作用
	- 模块脚本总是会“看到”已完全加载的 HTML 页面，包括在它们下方的 HTML 元素。
	- 下面面的第二个脚本实际上要先于前一个脚本运行！所以我们会先看到 `undefined`，然后才是 `object`。
	- 在 HTML 页面加载完成后才会执行 JavaScript 模块，所有有时候会造成困惑，可以加“加载指示器（loading indicator）”

```html
<script type="module">
  alert(typeof button); // object：脚本可以“看见”下面的 button
  // 因为模块是被延迟的（deferred，所以模块脚本会在整个页面加载完成后才运行
</script>

相较于下面这个常规脚本：

<script>
  alert(typeof button); // button 为 undefined，脚本看不到下面的元素
  // 常规脚本会立即运行，常规脚本的运行是在在处理页面的其余部分之前进行的
</script>

<button id="button">Button</button>
```
#### Async 适用于内联脚本（inline script）
- 对于非模块脚本，`async` 特性（attribute）仅适用于外部脚本。异步脚本会在准备好后立即运行，独立于其他脚本或 HTML 文档。
- 下面的内联脚本具有 `async` 特性，因此它不会等待任何东西。
```html
<!-- 所有依赖都获取完成（analytics.js）然后脚本开始运行 -->
<!-- 不会等待 HTML 文档或者其他 <script> 标签 -->
<script async type="module">
  import {counter} from './analytics.js';

  counter.count();
</script>
```

#### 外部脚本
- 具有 `type="module"` 的外部脚本（external script）在两个方面有所不同：
	- 具有相同 `src` 的外部脚本仅运行一次：
	```html
    <!-- 脚本 my.js 被加载完成（fetched）并只被运行一次 -->
    <script type="module" src="my.js"></script>
    <script type="module" src="my.js"></script>
    ```
- 从另一个源（例如另一个网站）获取的外部脚本需要 [CORS](https://developer.mozilla.org/zh/docs/Web/HTTP/CORS) header，
```html
<!-- another-site.com 必须提供 Access-Control-Allow-Origin -->
<!-- 否则，脚本将无法执行 -->
<script type="module" src="http://another-site.com/their.js"></script>
```

#### 不允许裸模块（“bare” module）
- 下面这个 `import` 是无效的：
```javascript
import {sayHi} from 'sayHi'; // Error，“裸”模块
// 模块必须有一个路径，例如 './sayHi.js' 或者其他任何路径
```

#### 兼容性，“nomodule”
- 旧时的浏览器不理解 `type="module"`。未知类型的脚本会被忽略。对此，我们可以使用 `nomodule` 特性来提供一个后备：
```html
<script type="module">
  alert("Runs in modern browsers");
</script>

<script nomodule>
  alert("Modern browsers know both type=module and nomodule, so skip this")
  alert("Old browsers ignore script with unknown type=module, but execute this.");
</script>
```

### 构建工具
- 构建工具做以下这些事儿：
	1. 从一个打算放在 HTML 中的 `<script type="module">` “主”模块开始。
	2. 分析它的依赖：它的导入，以及它的导入的导入等。
	3. 使用所有模块构建一个文件（或者多个文件，这是可调的），并用打包函数（bundler function）替代原生的 `import` 调用，以使其正常工作。还支持像 HTML/CSS 模块等“特殊”的模块类型。
	4. 在处理过程中，可能会应用其他转换和优化：
		-  删除无法访问的代码。
		- 删除未使用的导出（“tree-shaking”）。
		- 删除特定于开发的像 `console` 和 `debugger` 这样的语句。
		- 可以使用 [Babel](https://babeljs.io/) 将前沿的现代的 JavaScript 语法转换为具有类似功能的旧的 JavaScript 语法。
		- 压缩生成的文件（删除空格，用短的名字替换变量等）。

```html
<!-- 假设我们从诸如 Webpack 这类的打包工具中获得了 "bundle.js" 脚本 -->
<script src="bundle.js"></script>
```

## 导出导入

###  在声明前导出
- 我们可以通过在声明之前放置 `export` 来标记任意声明为导出，无论声明的是变量，函数还是类都可以。
```javascript
// 导出数组
export let months = ['Jan', 'Feb', 'Mar','Apr', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// 导出 const 声明的变量
export const MODULES_BECAME_STANDARD_YEAR = 2015;

// 导出类
export class User {
  constructor(name) {
    this.name = name;
  }
}
```

- 导出 class/function 后没有分号
	- 在类或者函数前的 `export` 不会让它们变成 [函数表达式](https://zh.javascript.info/function-expressions)。尽管被导出了，但它仍然是一个函数声明。
```javascript
export function sayHi(user) {
  alert(`Hello, ${user}!`);
}  // 在这里没有分号 ;
```

### 导出与声明分开

```javascript
// 📁 say.js
function sayHi(user) {
  alert(`Hello, ${user}!`);
}

function sayBye(user) {
  alert(`Bye, ${user}!`);
}

export {sayHi, sayBye}; // 导出变量列表
```
- 从技术上讲，我们也可以把 `export` 放在函数上面。
### Import *
```javascript
// 📁 main.js
import * as say from './say.js';

say.sayHi('John');
say.sayBye('John');
```

- 我们通常为什么要明确列出我们需要导入的内容？
	1. 现代的构建工具（[webpack](https://webpack.js.org/) 和其他工具）将模块打包到一起并对其进行优化，以加快加载速度并删除未使用的代码。
	2.  明确列出要导入的内容会使得名称较短：`sayHi()` 而不是 `say.sayHi()`。
	3.  导入的显式列表可以更好地概述代码结构：使用的内容和位置。它使得代码支持重构，并且重构起来更容易。
### Import “as”
```javascript
// 📁 main.js
import {sayHi as hi, sayBye as bye} from './say.js';

hi('John'); // Hello, John!
bye('John'); // Bye, John!
```
### Export “as”
```javascript
// 📁 say.js
...
export {sayHi as hi, sayBye as bye};
```
```javascript
// 📁 main.js
import * as say from './say.js';

say.hi('John'); // Hello, John!
say.bye('John'); // Bye, John!
```

### Export default
- 每个文件最多只能有一个默认的导出，导出的实体可能没有名称。
- `import` 命名的导出时需要花括号，而 `import` 默认的导出时不需要花括号。
```javascript
// 📁 user.js
export default class User { // 只需要添加 "default" 即可
  constructor(name) {
    this.name = name;
  }
}
```

```javascript
// 📁 main.js
import User from './user.js'; // 不需要花括号 {User}，只需要写成 User 即可

new User('John');
```

#### “default” 名称
```javascript
// 📁 user.js
export default class User {
  constructor(name) {
    this.name = name;
  }
}

export function sayHi(user) {
  alert(`Hello, ${user}!`);
}
```
- 上面混合导出，一般很少用，可以用下面两种方式导入
```javascript
// 📁 main.js
import {default as User, sayHi} from './user.js';

new User('John');
```
```javascript
// 📁 main.js
import * as user from './user.js';

let User = user.default; // 默认的导出
new User('John');
```

#### 我应该使用默认的导出吗？
```javascript
import User from './user.js'; // 有效
import MyUser from './user.js'; // 也有效
// 使用任何名称导入都没有问题
```

- 团队成员可能会使用不同的名称来导入相同的内容，不建议这样做
- 为了避免这种情况并使代码保持一致，可以遵从这条规则，即导入的变量应与文件名相对应
###  重新导出
```javascript
export {sayHi} from './say.js'; // 重新导出 sayHi

export {default as User} from './user.js'; // 重新导出 default
```

- 实际导出的功能分散在 package 中，所以我们可以将它们导入到 `auth/index.js`，然后再从中导出它们：
```javascript
// 📁 auth/index.js
// 重新导出 login/logout
export {login, logout} from './helpers.js';

// 将默认导出重新导出为 User
export {default as User} from './user.js';
...
```
#### 重新导出默认导出
- 假设有下面的默认导出
```javascript
// 📁 user.js
export default class User {
  // ...
}
```
1. `export User from './user.js'` 无效。这会导致一个语法错误。要重新导出默认导出，我们必须明确写出 `export {default as User}`，就像上面的例子中那样。
2. `export * from './user.js'` 重新导出只导出了命名的导出，但是忽略了默认的导出。如果我们想将命名的导出和默认的导出都重新导出，那么需要两条语句：
    ```javascript
    export * from './user.js'; // 重新导出命名的导出
    export {default} from './user.js'; // 重新导出默认的导出
    ```

## 动态导入

### import() 表达式
- `import(module)` 表达式加载模块并返回一个 promise，该 promise resolve 为一个包含其所有导出的模块对象。
```javascript
let modulePath = prompt("Which module to load?");

import(modulePath)
  .then(obj => <module object>)
  .catch(err => <loading error, e.g. if no such module>)
```

- 例子1
```javascript
// 📁 say.js
export function hi() {
  alert(`Hello`);
}

export function bye() {
  alert(`Bye`);
}
```

```javascript
let {hi, bye} = await import('./say.js');

hi();
bye();
```
- 例子2
```javascript
// 📁 say.js
export default function() {
  alert("Module loaded (export default)!");
}
```
```javascript
let obj = await import('./say.js');
let say = obj.default;
// or, in one line: let {default: say} = await import('./say.js');

say();
```

