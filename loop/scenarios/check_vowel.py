"""自动评判脚本 —— 检查 count_vowels 是否正确统计元音（含大小写）"""
import sys, os
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _parent)


def run_tests():
    try:
        from target import count_vowels
    except Exception as e:
        print(f"[FATAL] 无法导入: {e}")
        return False, [("import", False, str(e))]

    results = []
    cases = [
        ("纯小写",  "Hello",  2),
        ("纯大写",  "HELLO",  2),
        ("无元音",  "xyz",    0),
        ("全大写元音", "AEIOU", 5),
        ("空字符串", "",       0),
        ("混合",    "Codex",  2),
    ]
    for name, inp, expected in cases:
        try:
            got = count_vowels(inp)
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
