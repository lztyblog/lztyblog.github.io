def is_power(a,b):
    if a <1 or b<=1:
        return False
    
    if a == 1:
        return True
    
    if a%b != 0:
        return False
    
    return is_power(a//b , b)

print(is_power(27 ,3))

print(is_power(18 ,3))