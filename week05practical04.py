def concat_dico(dico1,dico2):

    total_dico = {}

    for key ,val in dico1.items():
        total_dico[key] = val

    for key ,val in dico2.items():
        total_dico[key] = val

    return total_dico

if __name__ == "__main__":
    dico1 = {"a":1 , "b":2 , "c":3}
    dico2 = {"b":4 , "d":5 , "e":6}
    result = concat_dico(dico1 , dico2)
    print(result)
    print(dico1)
    print(dico2)