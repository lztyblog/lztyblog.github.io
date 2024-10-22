''想法思路
1.先判断有没有重复值
2.反转这个字典的值
3.给函数赋值
4.打印输出的值'''

def requvers_dictionary(dico):
    value_set = set()
    for value in dico.values():
        if value in value_set:
            print("error")
            return None
        value_set.add(value)
    
    reversed_dico = {value : key for key ,value in dico.items()}

    return reversed_dico 

total_dict = {'a':1 , 'b':2 , 'c':3}
reversed_dict = requvers_dictionary(total_dict)
print(reversed_dict)
