## 文档对象模型（DOM）
- 文档对象模型（Document Object Model），简称 DOM，将所有**页面内容**表示为可以修改的对象。
- 规范中有属性和方法的详细描述：[DOM Living Standard](https://dom.spec.whatwg.org/)。
- 用于样式的 CSSOM，另外也有一份针对 CSS 规则和样式表的、单独的规范 [CSS Object Model (CSSOM)](https://www.w3.org/TR/cssom-1/)，这份规范解释了如何将 CSS 表示为对象，以及如何读写这些对象。

## 浏览器对象 BOM
- 浏览器对象模型（Browser Object Model），简称 BOM，表示由浏览器（主机环境）提供的用于处理文档（document）之外的所有内容的其他对象。
- 例子
	-  [navigator](https://developer.mozilla.org/zh/docs/Web/API/Window/navigator) 对象提供了有关浏览器和操作系统的背景信息。navigator 有许多属性，但是最广为人知的两个属性是：`navigator.userAgent` —— 关于当前浏览器，`navigator.platform` —— 关于平台（有助于区分 Windows/Linux/Mac 等）。
	- [location](https://developer.mozilla.org/zh/docs/Web/API/Window/location) 对象允许我们读取当前 URL，并且可以将浏览器重定向到新的 URL。
- BOM 是通用 [HTML 规范](https://html.spec.whatwg.org/) 的一部分。


