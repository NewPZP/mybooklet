## generator
- generator 可以按需一个接一个地返回（“yield”）多个值。它们可与 [iterable](https://zh.javascript.info/iterable) 完美配合使用，从而可以轻松地创建数据流。
```javascript
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}

let generator = generateSequence();

let one = generator.next();
alert(JSON.stringify(one)); // {value: 1, done: false}

let two = generator.next();
alert(JSON.stringify(two)); // {value: 2, done: false}

```
- `function* f(…)` 或 `function *f(…)`？ 
	- 两种语法都正确，倾向第一种

### generator 是可迭代的
- 使用for of 时的问题， 下面不会输出3 当 `done: true` 时，`for..of` 循环会忽略最后一个 `value`。
```javascript
function* generateSequence() {
  yield 1;
  yield 2;
  return 3;
}

let generator = generateSequence();

for(let value of generator) {
  alert(value); // 1，然后是 2
}
```
- 可用spread 语法，
```javascript
function* generateSequence() {
  yield 1;
  yield 2;
  yield 3;
}

let sequence = [0, ...generateSequence()];

alert(sequence); // 0, 1, 2, 3
```

### 使用 generator 进行迭代
- 下面的代码可以用 生成器改写
```javascript
let range = {
  from: 1,
  to: 5,

  // for..of range 在一开始就调用一次这个方法
  [Symbol.iterator]() {
    // ...它返回 iterator object：
    // 后续的操作中，for..of 将只针对这个对象，并使用 next() 向它请求下一个值
    return {
      current: this.from,
      last: this.to,

      // for..of 循环在每次迭代时都会调用 next()
      next() {
        // 它应该以对象 {done:.., value :...} 的形式返回值
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

// 迭代整个 range 对象，返回从 `range.from` 到 `range.to` 范围的所有数字
alert([...range]); // 1,2,3,4,5
```
```javascript
let range = {
  from: 1,
  to: 5,

  *[Symbol.iterator]() { // [Symbol.iterator]: function*() 的简写形式
    for(let value = this.from; value <= this.to; value++) {
      yield value;
    }
  }
};

alert( [...range] ); // 1,2,3,4,5
```

- generator 可以永远产出（yield）值

```javascript
function* generateSequence(start, end) {
  for (let i = start; i <= end; i++) yield i;
}

function* generateAlphaNum() {

  // yield* generateSequence(48, 57);
  for (let i = 48; i <= 57; i++) yield i;

  // yield* generateSequence(65, 90);
  for (let i = 65; i <= 90; i++) yield i;

  // yield* generateSequence(97, 122);
  for (let i = 97; i <= 122; i++) yield i;

}

let str = '';

for(let code of generateAlphaNum()) {
  str += String.fromCharCode(code);
}

alert(str); // 0..9A..Za..z
```

### “yield” 是一条双向路
- 它不仅可以向外返回结果，而且还可以将外部的值传递到 generator 内。调用 `generator.next(arg)`，我们就能将参数 `arg` 传递到 generator 内部。这个 `arg` 参数会变成 `yield` 的结果。

```javascript
function* gen() {
  let ask1 = yield "2 + 2 = ?";

  alert(ask1); // 4

  let ask2 = yield "3 * 3 = ?"

  alert(ask2); // 9
}

let generator = gen();

alert( generator.next().value ); // "2 + 2 = ?"

alert( generator.next(4).value ); // "3 * 3 = ?"

alert( generator.next(9).done ); // true
```

### generator.throw
```javascript
function* generate() {
  let result = yield "2 + 2 = ?"; // 这行出现 error
}

let generator = generate();

let question = generator.next().value;

try {
  generator.throw(new Error("The answer is not found in my database"));
} catch(e) {
  alert(e); // 显示这个 error
}
```

### generator.return
- generator.return(value)` 完成 generator 的执行并返回给定的 `value`。
```javascript
function* gen() {
  yield 1;
  yield 2;
  yield 3;
}

const g = gen();

g.next();        // { value: 1, done: false }
g.return('foo'); // { value: "foo", done: true }
g.next();        // { value: undefined, done: true }
```

## 异步迭代和 generator

- 异步迭代允许我们对按需通过异步请求而得到的数据进行迭代

### 回顾可迭代对象

```javascript
let range = {
  from: 1,
  to: 5,

  [Symbol.iterator]() { // 在 for..of 循环开始时被调用一次
    return {
      current: this.from,
      last: this.to,

      next() { // 每次迭代时都会被调用，来获取下一个值
        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

for(let value of range) {
  alert(value); // 1，然后 2，然后 3，然后 4，然后 5
}
```

### 异步可迭代对象
- 要使对象异步迭代：
	1. 使用 `Symbol.asyncIterator` 取代 `Symbol.iterator`。
	2. `next()` 方法应该返回一个 `promise`（带有下一个值，并且状态为 `fulfilled`）
	3. 我们应该使用 `for await (let item of iterable)` 循环来迭代这样的对象

```javascript
let range = {
  from: 1,
  to: 5,

  [Symbol.asyncIterator]() { // (1)
    return {
      current: this.from,
      last: this.to,

      async next() { // (2)

        // 注意：我们可以在 async next 内部使用 "await"
        await new Promise(resolve => setTimeout(resolve, 1000)); // (3)

        if (this.current <= this.last) {
          return { done: false, value: this.current++ };
        } else {
          return { done: true };
        }
      }
    };
  }
};

(async () => {

  for await (let value of range) { // (4)
    alert(value); // 1,2,3,4,5
  }

})()
```

- Spread 语法 `...` 无法异步工作

### 异步generator

- 在 `function*` 前面加上 `async`。这即可使 generator 变为异步的。
```javascript
async function* generateSequence(start, end) {

  for (let i = start; i <= end; i++) {

    // 哇，可以使用 await 了！
    await new Promise(resolve => setTimeout(resolve, 1000));

    yield i;
  }

}

(async () => {

  let generator = generateSequence(1, 5);
  for await (let value of generator) {
    alert(value); // 1，然后 2，然后 3，然后 4，然后 5（在每个 alert 之间有延迟）
  }

})();
```

### 异步的可迭代对象 range
```javascript
let range = {
  from: 1,
  to: 5,

  // 这一行等价于 [Symbol.asyncIterator]: async function*() {
  async *[Symbol.asyncIterator]() {
    for(let value = this.from; value <= this.to; value++) {

      // 在 value 之间暂停一会儿，等待一些东西
      await new Promise(resolve => setTimeout(resolve, 1000));

      yield value;
    }
  }
};

(async () => {

  for await (let value of range) {
    alert(value); // 1，然后 2，然后 3，然后 4，然后 5
  }

})();
```

### 实际例子 分页的数据

- 很多在线服务都是发送的分页的数据（paginated data）。例如，当我们需要一个用户列表时，一个请求只返回一个预设数量的用户（例如 100 个用户）—— “一页”，并提供了指向下一页的 URL。

- GitHub 允许使用相同的分页提交（paginated fashion）的方式找回 commit：
	- 我们应该以 `https://api.github.com/repos/<repo>/commits` 格式创建进行 `fetch` 的网络请求。
	- 它返回一个包含 30 条 commit 的 JSON，并在返回的 `Link` header 中提供了指向下一页的链接。
	- 然后我们可以将该链接用于下一个请求，以获取更多 commit，以此类推。
```javascript
async function* fetchCommits(repo) {
  let url = `https://api.github.com/repos/${repo}/commits`;

  while (url) {
    const response = await fetch(url, { // (1)
      headers: {'User-Agent': 'Our script'}, // github 需要任意的 user-agent header
    });

    const body = await response.json(); // (2) 响应的是 JSON（array of commits）

    // (3) 前往下一页的 URL 在 header 中，提取它
    let nextPage = response.headers.get('Link').match(/<(.*?)>; rel="next"/);
    nextPage = nextPage?.[1];

    url = nextPage;

    for(let commit of body) { // (4) 一个接一个地 yield commit，直到最后一页
      yield commit;
    }
  }
}


(async () => {

  let count = 0;

  for await (const commit of fetchCommits('javascript-tutorial/en.javascript.info')) {

    console.log(commit.author.login);

    if (++count == 100) { // 让我们在获取了 100 个 commit 时停止
      break;
    }
  }

})();
```


