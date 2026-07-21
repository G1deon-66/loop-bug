"""
选择排序模块 —— 故意埋了一个 bug。
bug 说明:
  selection_sort() 找的是最大值而非最小值，导致降序排列。
"""

def selection_sort(arr):
    """
    使用选择排序对列表进行升序排列。
    参数:
      arr: 整数列表
    返回:
      升序排列后的新列表
    """
    result = list(arr)
    n = len(result)
    for i in range(n):
        max_idx = i  # BUG: 在找最大值，应该找最小值 min_idx
        for j in range(i + 1, n):
            if result[j] > result[max_idx]:  # BUG: 应该是 <
                max_idx = j
        result[i], result[max_idx] = result[max_idx], result[i]
    return result
