'''想法思路
1.先比较两个值 keys 和 values 的长度是否保持一致
2.在for循环中用range函数为i赋值
3.在下面输入所赋的值：keys_list 和 value_list 
4.最后输出所打印的值
'''

def map_list(keys , values):

    if len(keys) != len(values):
        return None
    #把两个字典合并成一个字典（创建一个新的字典）
    the_end_dict = {keys[i]: values[i] for i in range(len(keys))}

    return the_end_dict

keys_list = ['a' , 'b' ,'c']
values_list = [1,2,3]
resule = map_list(keys_list , values_list)
print(resule)

