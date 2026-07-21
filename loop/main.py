"""
AI 自动修 bug 主循环 —— THINK → ACT → OBSERVE

架构说明:
  THINK:  调用 AI 模型，输入"当前代码 + 测试失败信息"，输出"修复后的代码"
  ACT:    将 AI 返回的代码写入 target.py
  OBSERVE: 运行 check.py，拿到 PASS/FAIL 结果

护栏 (guardrails):
  1. 最大轮数 (MAX_ROUNDS)：防止无限循环
  2. 每轮备份 (backup)：每次修改前先备份当前 target.py，出问题可回滚
  3. 超时保护：check.py 运行超过 30 秒视为异常

用法:
  python main.py              # 使用真实 API
  python main.py --mock       # 使用模拟 AI 回复（测试 loop 逻辑，无需 API key）
"""

import os
import sys
import subprocess
import shutil
import datetime
import argparse
from pathlib import Path

# ─── 配置 ────────────────────────────────────────────

# 尝试加载 .env 文件
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
except ImportError:
    pass  # python-dotenv 未安装也没关系，可以用系统环境变量

# API 配置（优先环境变量，其次默认值）
API_KEY = os.getenv("OPENAI_API_KEY", "")
BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# 文件路径
LOOP_DIR = Path(__file__).parent
TARGET_FILE = LOOP_DIR / "target.py"
CHECK_FILE = LOOP_DIR / "check.py"
BACKUP_DIR = LOOP_DIR / "backups"
MAX_ROUNDS = 10

# ─── 工具函数 ────────────────────────────────────────


def read_file(path):
    """读取文件内容。"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path, content):
    """写入文件内容。"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def backup_target(round_num):
    """
    【护栏】备份当前 target.py。
    每轮修改前先备份，这样即使 AI 改坏了也能回滚到上一轮。
    """
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"target_r{round_num:02d}_{timestamp}.py"
    shutil.copy(TARGET_FILE, backup_path)
    print(f"  [BACKUP] {backup_path.name}")


# ─── ACT / OBSERVE: 运行 check.py ─────────────────────

def run_check():
    """
    【ACT → OBSERVE】运行 check.py 获取评判结果。

    返回值:
      (passed: bool, stdout: str, stderr: str)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(CHECK_FILE)],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(LOOP_DIR),
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "check.py 运行超时 (>30s)"
    except Exception as e:
        return False, "", f"check.py 运行异常: {e}"


# ─── THINK: 调用 AI 模型 ──────────────────────────────

SYSTEM_PROMPT = """\
你是一个 Python 调试专家。你的任务是根据测试的失败信息，修复 target.py 中的 bug。

规则:
1. 只修复 bug，不改变函数签名、不添加新功能、不删除正常代码。
2. 保持原有的代码风格和注释。
3. 输出完整的修复后 target.py 文件内容。
4. 直接输出 Python 代码，不需要 markdown 代码块标记（不要 ```python ... ```）。
5. 不要添加任何解释性文字。"""


def call_ai_fix(target_code, check_output):
    """
    【THINK】调用 AI 模型，输入当前代码 + 测试结果，返回修复后的完整代码。
    """
    from openai import OpenAI

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    user_message = f"""\
以下是当前 target.py 的代码:

{target_code}

以下是运行 check.py 的结果:

{check_output}

请根据测试失败信息修复 bug，直接输出完整的修复后 target.py 代码。"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # 清理可能的 markdown 包装
    if content.startswith("```python"):
        content = content[len("```python"):].strip()
    elif content.startswith("```"):
        content = content[3:].strip()
    if content.endswith("```"):
        content = content[:-3].strip()

    return content


# ─── Mock 模式: 模拟 AI 回复（用于测试 loop 逻辑）─────

MOCK_FIX = '''"""
一个排序模块 —— 修复后的版本（供 Mock 模式使用）。

修复说明: sort_list() 的比较条件从 < 改为 >，现在正确进行升序排序。
"""


def sort_list(arr):
    """
    使用冒泡排序对列表进行升序排列。

    参数:
      arr: 整数列表

    返回:
      升序排列后的新列表
    """
    result = list(arr)
    n = len(result)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result
'''


def call_mock_fix(target_code, check_output):
    """模拟 AI 修复：直接返回正确的代码。"""
    print("  [MOCK] 模拟 AI 返回修复后的代码（跳过真实 API 调用）")
    return MOCK_FIX


# ─── 主循环 ───────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="AI Auto-Fix Loop")
    parser.add_argument(
        "--mock", action="store_true",
        help="使用模拟 AI 回复测试 loop 逻辑（无需 API key）"
    )
    parser.add_argument(
        "--target", type=str, default=None,
        help="指定靶程序文件路径（默认: target.py）"
    )
    parser.add_argument(
        "--check", type=str, default=None,
        help="指定裁判脚本路径（默认: check.py）"
    )
    parser.add_argument(
        "--max-rounds", type=int, default=None,
        help="最大轮数（默认: 10）"
    )
    args = parser.parse_args()

    # 允许命令行参数覆盖默认值
    global TARGET_FILE, CHECK_FILE, MAX_ROUNDS
    if args.target:
        TARGET_FILE = Path(args.target).resolve()
    if args.check:
        CHECK_FILE = Path(args.check).resolve()
    if args.max_rounds:
        MAX_ROUNDS = args.max_rounds

    use_mock = args.mock

    # 选择 THINK 函数
    think_func = call_mock_fix if use_mock else call_ai_fix
    if not use_mock and not API_KEY:
        print("错误: 未设置 OPENAI_API_KEY 环境变量。")
        print("  方法 1: 创建 .env 文件，写入 OPENAI_API_KEY=你的key")
        print("  方法 2: set $env:OPENAI_API_KEY='你的key'")
        print("  方法 3: 用 --mock 模式测试 loop 逻辑（无需 API）")
        sys.exit(1)

    print("=" * 60)
    print("  AI Auto-Fix Loop")
    print("  THINK -> ACT -> OBSERVE")
    print("=" * 60)
    print(f"  靶程序:   {TARGET_FILE.name}")
    print(f"  裁判:     {CHECK_FILE.name}")
    print(f"  模型:     {'MOCK' if use_mock else MODEL}")
    print(f"  最大轮数: {MAX_ROUNDS}")
    print(f"  备份目录: {BACKUP_DIR.name}/")
    print("=" * 60)

    for round_num in range(1, MAX_ROUNDS + 1):
        print(f"\n{'─' * 50}")
        print(f"  >>> Round {round_num} / {MAX_ROUNDS}")
        print(f"{'─' * 50}")

        # ────────── OBSERVE: 检查当前状态 ──────────
        print("\n  [OBSERVE] 运行 check.py 检查当前代码 ...")
        passed, stdout, stderr = run_check()

        if passed:
            print(f"  >>> 全部测试通过！修复成功。")
            if stdout.strip():
                for line in stdout.strip().split("\n"):
                    print(f"      {line}")
            break
        else:
            print(f"  >>> 测试失败，开始本轮修复流程。")
            if stdout.strip():
                for line in stdout.strip().split("\n"):
                    print(f"      {line}")
            if stderr.strip():
                print(f"      [stderr] {stderr.strip()}")

        # ────────── 护栏: 备份当前代码 ──────────
        print(f"\n  [GUARD] 备份当前 target.py ...")
        backup_target(round_num)

        # ────────── THINK: AI 分析并生成修复 ──────────
        print(f"\n  [THINK] 调用 AI 模型分析 bug 并生成修复 ...")
        target_code = read_file(TARGET_FILE)

        try:
            # 构造完整的上下文给 AI
            context = stdout if stdout else "check.py 无法正常运行，可能是语法错误或导入错误。"
            fixed_code = think_func(target_code, context)
        except Exception as e:
            print(f"  [ERROR] AI 调用失败: {e}")
            print(f"  >>> 跳过本轮，继续下一轮...")
            continue

        # 简单校验: AI 返回的内容不能为空或太短
        if not fixed_code or len(fixed_code.strip()) < 20:
            print(f"  [WARNING] AI 返回内容太短或为空，跳过本轮。")
            continue

        # ────────── ACT: 写入修复后的代码 ──────────
        print(f"\n  [ACT] 将修复后的代码写入 {TARGET_FILE.name} ...")
        write_file(TARGET_FILE, fixed_code)
        print(f"  >>> 写入完成 ({len(fixed_code)} 字符)")

    else:
        # ────────── 护栏: 耗尽最大轮数 ──────────
        print(f"\n{'─' * 50}")
        print(f"  [GUARD] 已达到最大轮数 ({MAX_ROUNDS})，循环终止。")
        print(f"  请手动检查 target.py 和 {BACKUP_DIR.name}/ 中的备份文件。")
        print(f"{'─' * 50}")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  修复结束: 成功于第 {round_num} 轮")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
