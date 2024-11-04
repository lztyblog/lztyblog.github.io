def save_to_log(entry , logfile):

    try:
        with open (logfile , 'w') as f:
            f.write(entry + "\n")

        print("have done")
    except IOError as e:
        print("can not found as error :{e}")

save_to_log(input("") , "text.log")