"""
    将多维列表 mlist 转换为一维列表。
    
    参数:
    mlist (list): 多维列表，可能包含嵌套列表。
    
    返回:
    list: 一维列表，包含 mlist 中的所有元素（忽略空列表）。
    """
def flatten(mlist):
    result= []

    def helper(sublist):
        for i in sublist:
            if isinstance(i ,list):
                helper(i)
            else:
                result.append(i)

    helper(mlist)

    return result

print(flatten([1,[2,[3,4],5],6]))
