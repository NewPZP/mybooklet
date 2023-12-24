## 摘要
- 主要是参考官方参考手册
- 主要关注每个版本更新哪些PEP
- https://docs.python.org/3/whatsnew/3.11.html


## python 3.11
- python 3.11 平均比 python3.10 快 10-60%左右
### 新特性
-   [PEP 654: Exception Groups and except*](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep654)
-  [PEP 678: Exceptions can be enriched with notes](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep678)
- [**PEP 680**](https://peps.python.org/pep-0680/): [`tomllib`](https://docs.python.org/3/library/tomllib.html#module-tomllib "tomllib: Parse TOML files.")
### 提升
- -   [PEP 657: Fine-grained error locations in tracebacks](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep657)
- -   New [`-P`](https://docs.python.org/3/using/cmdline.html#cmdoption-P) command line option and [`PYTHONSAFEPATH`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONSAFEPATH) environment variable to [disable automatically prepending potentially unsafe paths](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pythonsafepath) to [`sys.path`](https://docs.python.org/3/library/sys.html#sys.path "sys.path")

### 新类型特性
-   [PEP 646: Variadic generics](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep646)
-   [PEP 655: Marking individual TypedDict items as required or not-required](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep655)
-   [PEP 673: Self type](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep673)
-   [PEP 675: Arbitrary literal string type](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep675)
-   [PEP 681: Data class transforms](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep681)

### 废弃与约束
-   [**PEP 594**](https://peps.python.org/pep-0594/): [Many legacy standard library modules have been deprecated](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep594) and will be removed in Python 3.13
-   [**PEP 624**](https://peps.python.org/pep-0624/): [Py_UNICODE encoder APIs have been removed](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep624)
-   [**PEP 670**](https://peps.python.org/pep-0670/): [Macros converted to static inline functions](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep670)


## python 3.10

### 新语法特性
-   [**PEP 634**](https://peps.python.org/pep-0634/), Structural Pattern Matching: Specification
-   [**PEP 635**](https://peps.python.org/pep-0635/), Structural Pattern Matching: Motivation and Rationale
-   [**PEP 636**](https://peps.python.org/pep-0636/), Structural Pattern Matching: Tutorial
-   [bpo-12782](https://bugs.python.org/issue?@action=redirect&bpo=12782), Parenthesized context managers are now officially allowed.
### 标准库新特性
-   [**PEP 618**](https://peps.python.org/pep-0618/), Add Optional Length-Checking To zip.

### 解释器优化
-   [**PEP 626**](https://peps.python.org/pep-0626/), Precise line numbers for debugging and other tools.
### 类型约束新特性
-   [**PEP 604**](https://peps.python.org/pep-0604/), Allow writing union types as X | Y
-   [**PEP 612**](https://peps.python.org/pep-0612/), Parameter Specification Variables
-   [**PEP 613**](https://peps.python.org/pep-0613/), Explicit Type Aliases
-   [**PEP 647**](https://peps.python.org/pep-0647/), User-Defined Type Guards
### 废弃与约束
-   [**PEP 644**](https://peps.python.org/pep-0644/), Require OpenSSL 1.1.1 or newer
-   [**PEP 632**](https://peps.python.org/pep-0632/), Deprecate distutils module.
-   [**PEP 623**](https://peps.python.org/pep-0623/), Deprecate and prepare for the removal of the wstr member in PyUnicodeObject.
-   [**PEP 624**](https://peps.python.org/pep-0624/), Remove Py_UNICODE encoder APIs
-   [**PEP 597**](https://peps.python.org/pep-0597/), Add optional EncodingWarning


