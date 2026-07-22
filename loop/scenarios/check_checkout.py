"""裁判 —— 购物计算器（预期值匹配函数设计：先打折再减券）"""

import sys, os
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _parent)

def run_tests():
    from target import checkout
    results = []

    # 300 -> 9折=270, 减15=255; 600 -> 85折=510, 减15=495
    try:
        assert checkout([("A", 100, 3)]) == 255.0
        assert checkout([("A", 100, 6)]) == 495.0
        results.append(("discount", True, None))
    except AssertionError as e:
        results.append(("discount", False, str(e)))

    # 200*0.95=190 -> 减15=175
    try:
        assert checkout([("A", 50, 4)], True) == 175.0
        results.append(("member", True, None))
    except AssertionError as e:
        results.append(("member", False, str(e)))

    # 150 -> 减15=135; 10 -> 不变=10
    try:
        assert checkout([("A", 50, 3)]) == 135.0
        assert checkout([("A", 10, 1)]) == 10.0
        results.append(("coupon", True, None))
    except AssertionError as e:
        results.append(("coupon", False, str(e)))

    all_pass = all(p for _, p, _ in results)
    return all_pass, results

if __name__ == "__main__":
    all_pass, results = run_tests()
    for name, passed, detail in results:
        s = "[PASS]" if passed else "[FAIL]"
        d = f"  -> {detail}" if detail else ""
        print(f"  {s} {name}{d}")
    if all_pass:
        print("\n  *** ALL TESTS PASSED ***")
        sys.exit(0)
    else:
        n = sum(1 for _, p, _ in results if not p)
        print(f"\n  *** {n} TEST(S) FAILED ***")
        sys.exit(1)
