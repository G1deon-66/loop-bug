"""
自动评判脚本 —— 检查 selection_sort 排序函数是否正确。
"""
import sys, os
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _parent)


def run_tests():
    try:
        from target import selection_sort as sort_func
    except Exception as e:
        print(f"[FATAL] 无法导入: {e}")
        return False, [("import", False, str(e))]

    results = []
    cases = [
        ("普通乱序", [3,1,4,1,5,9,2,6], [1,1,2,3,4,5,6,9]),
        ("空列表",   [],                []),
        ("单元素",   [42],              [42]),
        ("已排序",   [1,2,3,4,5],       [1,2,3,4,5]),
        ("逆序",     [5,4,3,2,1],       [1,2,3,4,5]),
        ("重复元素", [2,2,2,1,1],       [1,1,2,2,2]),
    ]
    for name, inp, expected in cases:
        try:
            got = sort_func(inp)
            assert got == expected, f"期望 {expected}, 实际 {got}"
            results.append((name, True, None))
        except AssertionError as e:
            results.append((name, False, str(e)))
        except Exception as e:
            results.append((name, False, f"异常: {e}"))

    all_pass = all(p for _, p, _ in results)
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
