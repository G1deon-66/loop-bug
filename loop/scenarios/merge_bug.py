"""
归并排序模块 —— 故意埋了一个 bug。
bug 说明:
  merge() 中比较方向反了：left[i] > right[j] 应该是 <，导致降序。
"""

def merge_sort(arr):
    """归并排序主函数"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)


def merge(left, right):
    """合并两个已排序的列表"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:  # BUG: 应该是 <
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result
