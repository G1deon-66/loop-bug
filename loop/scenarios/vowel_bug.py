def count_vowels(text):
    """返回字符串里元音字母的个数（有 bug：不认大写）"""
    vowels = "aeiou"
    count = 0
    for char in text:
        if char in vowels:
            count += 1
    return count
