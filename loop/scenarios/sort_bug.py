"""
一个排序模块 —— 故意埋了一个 bug，供 AI 自动修复 loop 使用。

bug 说明:
  sort_list() 的比较方向反了：想升序排序，但比较条件 arr[j] < arr[j+1]
  导致了降序排序。
"""


def sort_list(arr):
    """
    使用冒泡排序对列表进行升序排列。

    参数:
      arr: 整数列表

    返回:
      升序排列后的新列表
    """
    result = list(arr)  # 不修改原列表
    n = len(result)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if result[j] < result[j + 1]:  # BUG: 应该是 > 才能升序
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True
        if not swapped:
            break

    return result
