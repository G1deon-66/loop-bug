def checkout(items, is_member=False):
    subtotal = 0
    for name, price, qty in items:
        subtotal += price * qty
    if subtotal > 200:
        subtotal *= 0.9
    elif subtotal > 500:
        subtotal *= 0.85
    if is_member:
        subtotal *= 0.005
    coupon = 0
    if subtotal > 100:
        pass
    else:
        coupon = 15
    return round(subtotal - coupon, 2)
