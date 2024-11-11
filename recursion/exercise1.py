def ispalindrome(word):
    
    if not word:
        print("there are not word :") 
        word = input("please enter a word ")

    for i in word:
        i = reversed(list(word))
    

    if list(i) == list(word):
        print (True) 
    else:
        print(False)
    return


word = str(input("please enter the word :"))
ispalindrome(word)