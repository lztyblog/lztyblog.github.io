def concat_dico(dico1 , dico2):
    totla_dico = {}

    def add_value(key, value):  
            if key in totla_dico:  
                if isinstance(totla_dico[key], list):  
                    totla_dico[key].append(value)  
                else:  
                    totla_dico[key] = [totla_dico[key], value]  
            else:  
                totla_dico[key] = value  
        
    
    for key, value in dico1.items():  
            add_value(key, value)  
         
    for key, value in dico2.items():  
            add_value(key, value)  
        
    return totla_dico  

if __name__ == "__main__":
      dico1 = {"a":1 , "b":2 , "c":3}
      dico2 = {"a":4 , "b":5 , "c":6}
      result = concat_dico(dico1 , dico2)
      print(result)
      print(dico1)
      print(dico2)