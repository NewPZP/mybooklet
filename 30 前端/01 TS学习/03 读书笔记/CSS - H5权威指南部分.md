## 参考资料
- 游戏学习 css
	- https://codingfantasy.com/
	- [gridcritters.com/](https://link.zhihu.com/?target=https%3A//gridcritters.com/) 好像要钱
	- [CodeCombat - 玩游戏学编程|零基础Python, Javascript入门|CodeCombat 个人版 | CodeCombat](https://codecombat.cn/)
	- [https://knightsoftheflexboxtable.com/](https://link.zhihu.com/?target=https%3A//knightsoftheflexboxtable.com/)
	- [codingame.com](https://link.zhihu.com/?target=https%3A//www.codingame.com)
	- [css-challenges.com/](https://link.zhihu.com/?target=https%3A//css-challenges.com/)
- 书
	- html 5 权威指南
	- css 高效开发实战

## 选择器
### CSS 基本选择器
- 选择所有元素
```CSS
	* {
			border: thin black solid
	}
```
- 根据类型选择
	```CSS
	a {
		border: thin black solid
	}
	```
- 根据类名选择
```CSS
.class2 {
	border: thin black solid
}
span.class1.class2{ 
	border: thin black solid
}
```

- 根据id 选择
```CSS
#w3canchor {
	border: thin black solid
}
```
- 根据属性进行选择

```CSS
-  打头^= ,结尾$=,包含*=, 多个值中的一个~=,|= 分割后的第一个值
[herf] {
	border: thin black solid
}
[lang|="eb"]{
	border: thin black solid
}
```
### 复合选择器
- 并集选择器
```CSS
a,[lang|="en"] {
	border: thin black solid
}

```
- 后代选择器
```CSS
p span{
	border: thin black solid
}
#mytable td{
	border: thin black solid
}


```
- 选择子元素
和后代选择器很像，区别是只匹配元素中的直接后代
```CSS
body > * > span, tr > th{
	border: thin black solid
}

```
- 选择兄弟元素
	-  + 相邻的第一个 ～指定元素之后，但不一定相邻
```CSS
p + a {
	border: thin black solid
}
p ~ a{
	border: thin black solid
}

```
### 伪元素选择器
- 伪元素
	- 实际是不存在的，为了方便你选中文档中的内容
-  使用 ::first-line 选择器
```CSS
 ::first-line {
 	border: thin black solid
 }
```
- ::first-letter
- :before 与:after
	在选择中的元素 前 或 后 插入内容
```CSS
a:before {
	content: "Click here to"
}
a:after {
	content: "!"
}
```
- 使用CSS 计数器
```CSS
body {
	counter-reset: paracount;
}
p:before{
	content: counter(paracount) ". ";
	counter-increment: paracount;
}

```
### 使用结构性伪类选择器
- 根元素选择器
	:root 不怎么使用，总是返回html元素
- 子元素选择器
	- :first-child :last-child
	-  :only-child 
	-  :only-of-type
- 使用 :nth-child选择器
	- :nth-child(n) :nth-last-child(n) 
	- :nth-of-type(n) :nth-last-of-type(n)

### 使用UI伪类选择器
- 使用启用或禁用元素
	:enable :disable
- 选择已勾选元素
```CSS
	:checked + span{
		background-color: red;
	}

```
- 选择默认元素 :default  
-  :invalid :valid 匹配符合和不符合输入验证要求的input元素
- 选择限定范的input 元素:in-range :out-of-range
- 选择必须和可选的input元素 :require :optional
### 使用动态伪类选择器
- :link 匹配超链接，:visited 匹配已访问过的链接
- :hover 匹配用户鼠标悬停上的任意元素
- :active 当前被用户激活的元素
- :focus 匹配当前获得的焦点元素
### 其他
- 否定选择器 :not
```CSS
a:not([href*="apress"]){
		background-color: red;
}
```
- :empty 定义没有任何子元素的元素
- :lang 匹配基于lang全局属性值的元素
```CSS
:lang(en) {
		border: thin black solid
}
```
```HTML
<a lang="en" id="oasd">shuould be thin black solid </a>
```
- :target  匹配url片段标识符指向的元素
	- url片段标识符 url#id 可以跳转到指定的元素
## 边框背景

### 应用边框样式
- border-with 
	- 单位 em px cm
	- 百分数 
	- thin medium thick
- border-style
	- none dashed doteed double groove inset outset ridge solid
- border-color
#### 为一条边应用边框样式
- border-top-width
- border-top-style
- border-top-color
- .....
#### 简写
- border: medium solid black
- border-top: solid 10px
#### 圆角边框
- border-radius 用这个简写
- border-top-left-radius
- border-top-right-radius
- border-bottom-left-radius
- border-bottom-right-radius
#### 图像做边框
- border-image
- border-image-source
- border-image-width
- border-image-outset
- border-image-repeat   strech repeat round space
### 元素背景
```CSS
p {
	border: medium solid black;
	background-color: lightgray;
	background-image: url(banana.png);
	background-size: 40px 40px;
	background-repeat: repeat-x;
}

```
- background-repeat
	- repeat
	- repeat-x
	- repeat-y
	- space 统一间距，确保不截断
	- round 调整图像大小 确保不截断
	- no-repeat
- background-size
	- 长度值 px
	- 百分数 
		- contain 等比例缩放，使较长边与容器重合
		- cover  等比例缩放，使图像至少覆盖容器
		- auto
- background-position
	- background-position: 30px 30px  距左边和顶部各30像素
	- 预定义
		- top
		- left
		- right
		- bottom
		- center
- background-attatchment 背景附着方式
	- fixed 内容滚动时背景不动
	- local 背景随内容一起
	- scroll 背景固定到元素上，不会随内容一起动
#### 背景图像的开始位置和裁剪样式
- background-origin  boder-box padding-box content-box
- background-clip
------
- box-shadow
### 应用轮廓
- outline
- outline-offset
- outline-style
- outline-width
- outline-color

## 盒模型
### 内边距
- padding-top
- padding-bottom
- padding-right
- padding-left
- padding 简写
### 外边距
- margin-xxx
- margin 简写
### 元素尺寸
- width height   取值： auto  长度值 百分数
- min-width min-width
- max-width max-width
- box-sizing ？？
### 处理溢出内容
- overflow-x
- overflow-y
- overflow  取值auto  hidden no-content no-display  scroll visible
### 控制元素可见性
- visibility  取值  collapse hidden visable
### 设置元素盒类型 display
#### 块级元素
- 和换行符效果类似
```CSS
span {
	display: block;
}

```
#### 行内元素
- 和周围内容显示没什么区别
- display : inline
#### 行内-块级元素
- display: inline-block
- 会创建一个其盒子混合了块和行特征的元素
- 可以将盒子的属性应用上
#### 插入元素
- display: run-in
- 如果包含一个block元素则为block
- 如果相邻是block 则为inline
- 如果相邻是inline 则为block

#### 隐藏元素
- display： none

### 创建浮动盒 ？？
- 参考 [CSS 布局 - 浮动和清除 (w3schools.cn)](https://www.w3schools.cn/css/css_float.html)
- float
	- left - 使其左边界挨着保护块的左边界
	- right
	- none
#### 阻止浮动元素堆叠
- clear 可以阻止
## 布局
### 定位内容
#### 设置定位类型
- position
	- static 普通布局 默认值
	- releative 元素位置相对于普通位置定位
	- absolute  元素相对于position不为static的第一位祖先元素定位
	- fixed 元素相对于浏览窗口来定位
#### 设置元素的层叠顺序
- z-index  取值 数字允许负值，值越小越靠后，会被挡住
### 创建多列布局
- 允许在多个垂直列中布局内容
- column-count
- column-fill    balance 不同列之间的长度差异尽可能小， auto 按照顺序填充列
- column-gap
- column-rule-color
- column-rule-style
- column-rule-width
- column-rule 上面简写
- column-span  元素跨多少列
- column-width 
- columns 上面简写
### 创建弹性布局
- [CSS3 Flexbox (Flexible Box) 弹性盒子 (w3schools.cn)](https://www.w3schools.cn/css/css3_flexbox.html)
dispaly 为flexbox时，使用下面的几个属性
- flex-algin
- flex-direction
- flex-order
- flex-pack

## 文本样式
### 基本文本样式
#### 对齐文本
- text-align
	- start
	- end
	- left
	- right
	- center
	- justify
- text-justify 如果text-align使用了justify,则使用该属性
	- auto
	- none
	- inner-word
	- inter-ideograph
	- distribute
#### 处理空白
- whitespace
	- normal 空白符被压缩，自动换行
	- nowrap 空白符被压缩 不自动换行
	- pre 空白符被保留 遇到换行符才换行
	- pre-line 空白符被压缩 遇到换行符或一行排满时才换行
	- pre-wrap 空白符被保留 遇到换行符或一行排满时才换行
#### 指定文本方向
- direction
	- ltr
	- rtl
#### 指定单词，字母，行之间的间距
- letter-spacing     normal 与长度值
- word-spacing
- line-height
#### 控制断词
- word-wrap  
	- normal   较长的单词可能会使文本 行结尾非常不整齐
	- break-word  会使单词不好理解
#### 首行缩进
- text-indent  长度值或百分数字
### 文本装饰与大小写转换
- text-decoration
	- none
	- underline
	- overline
	- line-through
	- blink
- text-transform
	- none
	- capitalize
	- uppercase
	- lowercase
### 创建文本阴影
- text-shadow
	-  h-shadow v-shadow blur color
```CSS
h1 {
	text-shadow: 0.1em .1em 1px lightgrey;
}

```
### 使用字体
- font-family  按优先顺序排列 
- css定义了几种任何情况都可以使用的通用字体
	- serif
	- sans-serif
	- cursive
	- fantasy
	- monospace
- font-size 设置字体大小
	- xx-small x-small small
	- medium
	- large x-large xx-large
	- smaller
	- larger
	- 长度值
	- %
- font-weight 粗细
- font-style 设置字体样式
	- 斜体 假斜体 正常
### 使用web字体
```CSS
@font-face {
	font-family: 'MyFont';
	font-style: normal;
	font-weight: normal;
	src: url('http://titan/listings/MtFont.woff');
}
p {
	font-family: MyFont, cursive;
}

```

## 过渡 动画 变换属性
### 使用过渡
- transition-delay 过渡开始之前延迟时间
- tansition-duration 过渡持续时间
- transition-property 应用过渡属性
- transition-timing-function 过渡间计算中间值的方式
- transition  简写
```CSS
p {
	padding: 5px;
	border: medium double black;
	background-color: lightgray;
	font-family: sans-serif;
}
#banana {
	font-size: large;
	border: medium solid black
	-webkit-transition-delay:10ms;
	-webkit-transition-duration: 250ms;
}

#banana:hover {
	font-size: x-large;
	border: medium solid white;
	background-color: green;
	color: white;
	padding: 4px;
	-webkit-transition-delay: 100ms;
	-webkit-transition-property: background-color, color, padding,
		font-size, border;
	-webkit-transition-duration: 500ms;
	-webkit-transition-timing-function: linear;
}

```
#### 反向过渡
	- 如上
#### 选择中间值的计算方式
- ease
- linner
- ease-in
- ease-out
- ease-in-out
### 使用动画
- 本质是增强的过渡
- animation-delay
- animation-direction 设置重复方向
	- normal 每次的向前播放
	- alternate 先向前播放 后反方向播放
- animation-duration
- animation-iteration-count 
- animation-name
- animation-play-state
- animation-timing-function
```CSS
#banana:hover {
	-webkit-animation-delay:100ms;
	-webkit-animation-duration: 500ms;
	-webkit-animation-iteration-count: infinte;
	-webkit-animation-timing-function: linear;
	-webkit-animation-name: 'GrowShrink'; 
	
}
@-webit-frames Growshrink{
	from {
		font-size: xx-small;
		background-color: red;
	}
	50% {
		background-color: yellow;
		padding: 1px;
	}
	75% {
		color: white;
		padding: 2px;
	}
	to{
		font-size: x-large;
		border: medium solid white;
		background-color: green;
		color: white;
		padding: 4px
	}
}

```
#### 理解结束状态
- 想保留动画结束时的状态，必须使用过度

#### 可重用
#### 应用多个动画
#### 停止和启动动画
- animation-play-state
	- puased
	- playing
### 使用变换
- 就是可以旋转，缩放，倾斜，平移
- tansform
	- translate(<长度或百分指>) 水平或垂直方向平移
	- translteX
	- translateY
	- scale
	- scaleX
	- scaleY
	- rotate(<角度>)
	- skew(<角度>) 倾斜一定角度
	- skewX
	- skewY
	- matrix(4-6个数值，逗号隔开)
#### 指定变换起点
	- transform-origin
		- <%>
		- <长度值>
		- left/right/center ，top/bottom/center

## 其它
### 颜色和透明度
- color 
- opacity
### 表格样式
- border-collapse
	- collapse
	- separate
- border-spacing 
	- 1~2个长度值
- caption-side 表格标题位置
	- top
	- bottom
- empty-cells 是否显示边框
	- hide
	- show
- table-layout 布局样式
	- fixed
	- auto
### 列表样式
- list-style-type
	- none
	- box
	- check
	- diamand
	- disc
	- dash
	- square
	- decimal
	- binary
	- lower-alpha
	- upper-alpha
- list-style-image 图像作为标记
- list-style-position 
	- inside
	- outide
- list-style 简写形式
### 光标样式
- cursor
	- auto
	- progress
	- 