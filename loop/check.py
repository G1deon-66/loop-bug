"""
自动评判脚本（裁判）—— 对 target.py 中的函数运行测试用例，输出 PASS/FAIL。

check.py 是整个 loop 的"裁判"：它不关心代码怎么写的，只关心行为对不对。
如果没有这个裁判，AI 可能声称自己修好了但实际上没修好（幻觉）。
"""

import sys


def run_tests():
    """运行所有测试，返回 (全部通过?, 结果列表)。"""
    # 尝试导入 target 模块
    try:
        from target import add, multiply, fibonacci
    except Exception as e:
        print(f"[FATAL] 无法导入 target.py: {e}")
        return False, [("import", False, str(e))]

    results = []

    # ── 测试 add ──
    try:
        assert add(2, 3) == 5, f"add(2,3) 期望 5, 实际 {add(2, 3)}"
        assert add(-1, 1) == 0, f"add(-1,1) 期望 0, 实际 {add(-1, 1)}"
        assert add(0, 0) == 0, f"add(0,0) 期望 0, 实际 {add(0, 0)}"
        assert add(100, 200) == 300, f"add(100,200) 期望 300, 实际 {add(100, 200)}"
        results.append(("add", True, None))
    except AssertionError as e:
        results.append(("add", False, str(e)))
    except Exception as e:
        results.append(("add", False, f"异常: {e}"))

    # ── 测试 multiply ──
    try:
        assert multiply(2, 3) == 6, f"multiply(2,3) 期望 6, 实际 {multiply(2, 3)}"
        assert multiply(-2, 3) == -6, f"multiply(-2,3) 期望 -6, 实际 {multiply(-2, 3)}"
        assert multiply(0, 5) == 0, f"multiply(0,5) 期望 0, 实际 {multiply(0, 5)}"
        assert multiply(7, 8) == 56, f"multiply(7,8) 期望 56, 实际 {multiply(7, 8)}"
        results.append(("multiply", True, None))
    except AssertionError as e:
        results.append(("multiply", False, str(e)))
    except Exception as e:
        results.append(("multiply", False, f"异常: {e}"))

    # ── 测试 fibonacci ──
    try:
        assert fibonacci(0) == 0, f"fib(0) 期望 0, 实际 {fibonacci(0)}"
        assert fibonacci(1) == 1, f"fib(1) 期望 1, 实际 {fibonacci(1)}"
        assert fibonacci(2) == 1, f"fib(2) 期望 1, 实际 {fibonacci(2)}"
        assert fibonacci(5) == 5, f"fib(5) 期望 5, 实际 {fibonacci(5)}"
        assert fibonacci(10) == 55, f"fib(10) 期望 55, 实际 {fibonacci(10)}"
        results.append(("fibonacci", True, None))
    except AssertionError as e:
        results.append(("fibonacci", False, str(e)))
    except Exception as e:
        results.append(("fibonacci", False, f"异常: {e}"))

    all_pass = all(passed for _, passed, _ in results)
    return all_pass, results


if __name__ == "__main__":
    all_pass, results = run_tests()

    for name, passed, detail in results:
        status = "[PASS]" if passed else "[FAIL]"
        detail_str = f"  → {detail}" if detail else ""
        print(f"  {status} {name}{detail_str}")

    if all_pass:
        print("\n  *** ALL TESTS PASSED ***")
        sys.exit(0)
    else:
        print("\n  *** SOME TESTS FAILED ***")
        sys.exit(1)
