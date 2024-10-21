def display_dico(dico):

    for key , val in dico.items():
        print(f"{key} : {val}")

key_value = {"un":1 , "deux":2 , "trois":3}
display_dico(key_value)