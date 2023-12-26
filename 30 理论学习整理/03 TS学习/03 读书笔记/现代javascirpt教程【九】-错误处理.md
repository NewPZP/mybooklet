## "try...catch"

- 语法
```javascript
try {

  // 代码...

} catch (err) {

  // 错误捕获

}
```

- 要使得 `try...catch` 能工作，代码必须是可执行的
- `try...catch` 同步执行
```javascript
try {
  setTimeout(function() {
    noSuchVariable; // 脚本将在这里停止运行
  }, 1000);
} catch (err) {
  alert( "不工作" );
}
```

- 为了捕获到计划的（scheduled）函数中的异常，那么 `try...catch` 必须在这个函数内：
```javascript
setTimeout(function() {
  try {
    noSuchVariable; // try...catch 处理 error 了！
  } catch {
    alert( "error 被在这里捕获了！" );
  }
}, 1000);
```

### Error 对象
- 3个属性
```javascript
try {
  lalala; // error, variable is not defined!
} catch (err) {
  alert(err.name); // ReferenceError
  alert(err.message); // lalala is not defined
  alert(err.stack); // ReferenceError: lalala is not defined at (...call stack)

  // 也可以将一个 error 作为整体显示出来
  // error 信息被转换为像 "name: message" 这样的字符串
  alert(err); // ReferenceError: lalala is not defined
}
```

### 可选的 “catch” 绑定
- 如果我们不需要 error 的详细信息，`catch` 也可以忽略它：
```javascript
try {
  // ...
} catch { // <-- 没有 (err)
  // ...
}
```

### 抛出我们自定义的 error

- JavaScript 中有很多内建的标准 error 的构造器：`Error`，`SyntaxError`，`ReferenceError`，`TypeError` 等。我们也可以使用它们来创建 error 对象。

```javascript
let json = '{ "age": 30 }'; // 不完整的数据

try {

  let user = JSON.parse(json); // <-- 没有 error

  if (!user.name) {
    throw new SyntaxError("数据不全：没有 name"); // (*)
  }

  alert( user.name );

} catch(err) {
  alert( "JSON Error: " + err.message ); // JSON Error: 数据不全：没有 name
}
```

### 再次抛出（Rethrowing）

```javascript
let json = '{ "age": 30 }'; // 不完整的数据
try {

  let user = JSON.parse(json);

  if (!user.name) {
    throw new SyntaxError("数据不全：没有 name");
  }

  blabla(); // 预料之外的 error

  alert( user.name );

} catch (err) {

  if (err instanceof SyntaxError) {
    alert( "JSON Error: " + err.message );
  } else {
    throw err; // 再次抛出 (*)
  }

}
```

### try…catch…finally
```javascript
try {
   ... 尝试执行的代码 ...
} catch (err) {
   ... 处理 error ...
} finally {
   ... 总是会执行的代码 ...
}
```

```javascript
let num = +prompt("输入一个正整数？", 35)

let diff, result;

function fib(n) {
  if (n < 0 || Math.trunc(n) != n) {
    throw new Error("不能是负数，并且必须是整数。");
  }
  return n <= 1 ? n : fib(n - 1) + fib(n - 2);
}

let start = Date.now();

try {
  result = fib(num);
} catch (err) {
  result = 0;
} finally {
  diff = Date.now() - start;
}

alert(result || "出现了 error");

alert( `执行花费了 ${diff}ms` );
```


- 变量和 `try...catch...finally` 中的局部变量
	- 我们使用 `let` 在 `try` 块中声明变量，那么该变量将只在 `try` 块中可见。

- `finally` 和 `return`
```javascript
//这种情况下，`finally` 会在控制转向外部代码前被执行。
function func() {

  try {
    return 1;

  } catch (err) {
    /* ... */
  } finally {
    alert( 'finally' );
  }
}

alert( func() ); // 先执行 finally 中的 alert，然后执行这个 alert
```

### 全局 catch

```html
<script>
  window.onerror = function(message, url, line, col, error) {
    alert(`${message}\n At ${line}:${col} of ${url}`);
  };

  function readData() {
    badFunc(); // 啊，出问题了！
  }

  readData();
</script>
```

## 自定义 Error，扩展 Error
```javascript
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

// 用法
function readUser(json) {
  let user = JSON.parse(json);

  if (!user.age) {
    throw new ValidationError("No field: age");
  }
  if (!user.name) {
    throw new ValidationError("No field: name");
  }

  return user;
}

// try..catch 的工作示例

try {
  let user = readUser('{ "age": 25 }');
} catch (err) {
  if (err instanceof ValidationError) {
    alert("Invalid data: " + err.message); // Invalid data: No field: name
  } else if (err instanceof SyntaxError) { // (*)
    alert("JSON Syntax Error: " + err.message);
  } else {
    throw err; // 未知的 error，再次抛出 (**)
  }
}
```

### 深入继承

```javascript
class MyError extends Error {
  constructor(message) {
    super(message);
    this.name = this.constructor.name;
  }
}

class ValidationError extends MyError { }

class PropertyRequiredError extends ValidationError {
  constructor(property) {
    super("No property: " + property);
    this.property = property;
  }
}

// name 是对的
alert( new PropertyRequiredError("field").name ); // PropertyRequiredError
```

### 包装异常
- 这种方法被称为“包装异常（wrapping exceptions）”，因为我们将“低级别”的异常“包装”到了更抽象的 `ReadError` 中。
```javascript
class ReadError extends Error {
  constructor(message, cause) {
    super(message);
    this.cause = cause;
    this.name = 'ReadError';
  }
}

class ValidationError extends Error { /*...*/ }
class PropertyRequiredError extends ValidationError { /* ... */ }

function validateUser(user) {
  if (!user.age) {
    throw new PropertyRequiredError("age");
  }

  if (!user.name) {
    throw new PropertyRequiredError("name");
  }
}

function readUser(json) {
  let user;

  try {
    user = JSON.parse(json);
  } catch (err) {
    if (err instanceof SyntaxError) {
      throw new ReadError("Syntax Error", err);
    } else {
      throw err;
    }
  }

  try {
    validateUser(user);
  } catch (err) {
    if (err instanceof ValidationError) {
      throw new ReadError("Validation Error", err);
    } else {
      throw err;
    }
  }

}

try {
  readUser('{bad json}');
} catch (e) {
  if (e instanceof ReadError) {
    alert(e);
    // Original error: SyntaxError: Unexpected token b in JSON at position 1
    alert("Original error: " + e.cause);
  } else {
    throw e;
  }
}
```
