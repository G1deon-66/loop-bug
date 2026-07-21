# AI Auto-Fix Loop (AI 自动修 bug 最小环)

## 是什么

一个 AI 自动修 bug 的最小闭环系统：AI 模型读取有 bug 的代码 → 尝试修复 → 裁判 (check.py) 验证 → 未通过就继续修复，直到通过或达到最大轮数。

## 核心架构: THINK → ACT → OBSERVE

```
  当前代码 ──→ [OBSERVE] 运行 check.py 获取测试结果
       ↑                    ↓ (FAIL)
       │              [THINK] 调用 AI 模型分析并生成修复
       │                    ↓
       └──── [ACT] 将修复代码写入 target.py
```

每一轮的具体步骤：
- **OBSERVE**: 运行 `check.py` 对 `target.py` 做自动化测试，得到 PASS/FAIL
- **THINK**: 如果 FAIL，把当前代码 + 测试失败信息发给 AI 模型，让它分析 bug 并给出修复
- **ACT**: 把 AI 返回的修复后代码写入 `target.py`

## 护栏 (Guardrails)

1. **最大轮数 (MAX_ROUNDS=10)**: 防止无限循环烧 token
2. **每轮备份 (backups/)**: 修改前先备份当前 `target.py`，改坏了可以回滚
3. **超时保护**: `check.py` 运行超过 30 秒视为异常

## 为什么 check.py 是"裁判"

check.py 是外部真理：它不关心代码长什么样，只关心行为对不对。
如果删掉 check.py，让 AI 自己判断"修没修好"，AI 很可能产生幻觉——声称修好了但实际没修好。

## 文件说明

```
loop/
  main.py          主循环：THINK→ACT→OBSERVE
  target.py        靶程序（有 bug 的代码，等待 AI 修复）
  check.py         裁判脚本（对 target.py 运行测试用例）
  backups/         每轮自动备份（运行中生成）
  scenarios/       场景库
    calc_bug.py     场景 1: 有 bug 的计算器
    sort_bug.py     场景 2: 有 bug 的排序函数
    check_sort.py   场景 2: 排序函数的裁判脚本
```

## 使用方法

### 1. 安装依赖
```bash
pip install -r ../requirements.txt
```

### 2. 配置 API Key
```bash
cp ../.env.example ../.env
# 编辑 .env 填入你的 OPENAI_API_KEY
```

### 3. 运行
```bash
# Mock 模式（无需 API，测试 loop 逻辑）
python main.py --mock

# 真实 API 模式（场景 1: 计算器）
python main.py

# 真实 API 模式（场景 2: 排序）
copy scenarios\sort_bug.py target.py
python main.py --check scenarios\check_sort.py
```

### 4. 切换场景
```bash
# 切换到排序场景
copy scenarios\sort_bug.py target.py

# 切换到计算器场景
copy scenarios\calc_bug.py target.py
```
