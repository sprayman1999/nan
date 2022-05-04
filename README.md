# Nan
## Introduction
### 本代码存在很多问题，而且有很多垃圾代码，另外也有没有注释
### 本人简单的毕业设计，不喜勿喷。因为大学期间没有好好学编译原理，通过毕业设计好好督促自己能好好静下来重新学习，也没有想到要设计的多复杂多好用，只是单纯的学习。
### 最大的核心就是实现了根据文法规则产生Parser Table，不需要人工构造这个表。
### 简单实现了可以生成IR的前端，基本没啥功能，就二元加减乘除、函数调用。
### 词法分析器就是简单的切割，然后组成二元组。语法分析器基于LR(0)
### 生成IR之后，可以通过LLVM直接编译出可执行文件
## 代码案例
```
func hello_world(): void{
    puts("call Hello World!");
}
func main(): void{
    hello_world();
    puts("this is main!");
}
```
## 测试代码如下
```
python3 ./shell.py xxx.nan -o xxx && ./xxx
```
