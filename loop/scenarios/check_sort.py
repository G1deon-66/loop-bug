"""
自动评判脚本 —— 检查 sort_list 排序函数是否行为正确。

测试覆盖:
  - 普通乱序列表
  - 空列表
  - 单元素列表
  - 已排序列表
  - 逆序列表
  - 包含重复元素的列表
"""

import sys
import os

# 确保能找到 target 模块（从 scenarios/ 运行时需要）
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _parent)


def run_tests():
    """运行所有测试，返回 (全部通过?, 结果列表)。"""
    try:
        from target import sort_list
    except Exception as e:
        print(f"[FATAL] 无法导入 sort_list: {e}")
        return False, [("import", False, str(e))]

    results = []

    # ── 测试 1: 普通乱序列表 ──
    try:
        assert sort_list([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9], \
            f"期望 [1,1,2,3,4,5,6,9], 实际 {sort_list([3,1,4,1,5,9,2,6])}"
        results.append(("普通列表", True, None))
    except AssertionError as e:
        results.append(("普通列表", False, str(e)))
    except Exception as e:
        results.append(("普通列表", False, f"异常: {e}"))

    # ── 测试 2: 空列表 ──
    try:
        assert sort_list([]) == [], f"sort_list([]) 期望 [], 实际 {sort_list([])}"
        results.append(("空列表", True, None))
    except AssertionError as e:
        results.append(("空列表", False, str(e)))
    except Exception as e:
        results.append(("空列表", False, f"异常: {e}"))

    # ── 测试 3: 单元素 ──
    try:
        assert sort_list([42]) == [42], f"sort_list([42]) 期望 [42], 实际 {sort_list([42])}"
        results.append(("单元素", True, None))
    except AssertionError as e:
        results.append(("单元素", False, str(e)))
    except Exception as e:
        results.append(("单元素", False, f"异常: {e}"))

    # ── 测试 4: 已排序列表 ──
    try:
        assert sort_list([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5], \
            f"sort_list([1,2,3,4,5]) 期望 [1,2,3,4,5], 实际 {sort_list([1,2,3,4,5])}"
        results.append(("已排序", True, None))
    except AssertionError as e:
        results.append(("已排序", False, str(e)))
    except Exception as e:
        results.append(("已排序", False, f"异常: {e}"))

    # ── 测试 5: 逆序列表 ──
    try:
        assert sort_list([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5], \
            f"sort_list([5,4,3,2,1]) 期望 [1,2,3,4,5], 实际 {sort_list([5,4,3,2,1])}"
        results.append(("逆序", True, None))
    except AssertionError as e:
        results.append(("逆序", False, str(e)))
    except Exception as e:
        results.append(("逆序", False, f"异常: {e}"))

    # ── 测试 6: 含重复元素 ──
    try:
        assert sort_list([2, 2, 2, 1, 1]) == [1, 1, 2, 2, 2], \
            f"sort_list([2,2,2,1,1]) 期望 [1,1,2,2,2], 实际 {sort_list([2,2,2,1,1])}"
        results.append(("重复元素", True, None))
    except AssertionError as e:
        results.append(("重复元素", False, str(e)))
    except Exception as e:
        results.append(("重复元素", False, f"异常: {e}"))

    all_pass = all(passed for _, passed, _ in results)
    return all_pass, results


if __name__ == "__main__":
    all_pass, results = run_tests()

    for name, passed, detail in results:
        status = "[PASS]" if passed else "[FAIL]"
        detail_str = f"  -> {detail}" if detail else ""
        print(f"  {status} {name}{detail_str}")

    if all_pass:
        print("\n  *** ALL TESTS PASSED ***")
        sys.exit(0)
    else:
        print("\n  *** SOME TESTS FAILED ***")
        sys.exit(1)
