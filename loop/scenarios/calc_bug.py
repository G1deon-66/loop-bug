"""
一个小型计算器模块 —— 故意埋了三个 bug，供 AI 自动修复 loop 使用。

bug 说明:
  1. add()    返回了 a - b，应该是 a + b
  2. multiply() 用了除法 /，应该是乘法 *
  3. fibonacci() 循环结束后返回了 a，应该是 b
"""


def add(a, b):
    """返回 a + b"""
    return a - b  # BUG: 应该是 +


def multiply(a, b):
    """返回 a * b"""
    return a / b  # BUG: 应该是 *


def fibonacci(n):
    """返回第 n 个斐波那契数（0-indexed: fib(0)=0, fib(1)=1, fib(2)=1）"""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return a  # BUG: 应该返回 b
