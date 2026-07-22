"""THINK Module —— 解析 check 报错 + 校验 AI 修复代码"""

import ast


def parse_check_output(stdout):
    """从 check.py 输出中提取失败项和详情"""
    if not stdout:
        return {"errors": [], "summary": "check 未正常输出"}

    errors = []
    for line in stdout.splitlines():
        line = line.strip()
        if "[FAIL]" in line or "FAIL" in line:
            errors.append(line)
        elif "[FATAL]" in line:
            errors.append(line)

    return {
        "errors": errors,
        "fail_count": sum(1 for e in errors if "FAIL" in e),
        "summary": f"共 {len(errors)} 个问题" if errors else "全部通过"
    }


def validate_fix(old_code, new_code):
    """校验 AI 返回的修复代码是否合法。
    返回 (valid: bool, reason: str)"""
    if not new_code or len(new_code.strip()) < 10:
        return False, "代码为空或太短"

    # 1. 语法检查
    try:
        ast.parse(new_code)
    except SyntaxError as e:
        return False, f"语法错误: {e}"

    # 2. 函数保留检查——修复不能删掉已有函数
    old_funcs = set()
    try:
        old_tree = ast.parse(old_code)
        for node in ast.walk(old_tree):
            if isinstance(node, ast.FunctionDef):
                old_funcs.add(node.name)
    except SyntaxError:
        pass  # 旧代码可能有 bug，跳过

    new_funcs = set()
    new_tree = ast.parse(new_code)
    for node in ast.walk(new_tree):
        if isinstance(node, ast.FunctionDef):
            new_funcs.add(node.name)

    missing = old_funcs - new_funcs
    if missing:
        return False, f"删除了函数: {', '.join(missing)}"

    # 3. 函数签名变化检查
    for node in ast.walk(new_tree):
        if isinstance(node, ast.FunctionDef) and node.name in old_funcs:
            # 检查参数数量是否一致
            old_node = None
            for n in ast.walk(old_tree):
                if isinstance(n, ast.FunctionDef) and n.name == node.name:
                    old_node = n
                    break
            if old_node and len(old_node.args.args) != len(node.args.args):
                return False, f"{node.name} 函数签名变了"

    return True, "通过"


def clean_ai_response(content):
    """清理 AI 返回的原始内容——去掉 markdown 包装、多余空白"""
    content = content.strip()
    # Strip BOM and other invisible chars
    content = content.replace(chr(0xFEFF), "").replace(chr(0x200B), "")
    if content.startswith("```python"):
        content = content[len("```python"):].strip()
    elif content.startswith("```"):
        content = content[3:].strip()
    if content.endswith("```"):
        content = content[:-3].strip()
    return content
