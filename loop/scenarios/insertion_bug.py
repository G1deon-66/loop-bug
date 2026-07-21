"""
插入排序模块 —— 故意埋了一个 bug。
bug 说明:
  insertion_sort() 内层 while 循环比较方向反了：result[j] < key 应该是 >，导致降序排列。
"""

def insertion_sort(arr):
    """
    使用插入排序对列表进行升序排列。
    参数:
      arr: 整数列表
    返回:
      升序排列后的新列表
    """
    result = list(arr)
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] < key:  # BUG: 应该是 >
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result
