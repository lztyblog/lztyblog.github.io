def save_list2file(sentences , filename):

    try:
        with open ("exto1.txt" , 'w') as file:
            for sentences in sentences:
                file.write(sentences + "\n" ) 
        print(f"the sentences has save in {filename}")

    except IOError as e:
        print("Can not found this file")
        


sentences = [
    "1. hello" 
    "2. welcome the test"
    "3. have a lucky day"
]

save_list2file(sentences , "exto1.txt")