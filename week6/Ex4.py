def read_and_print(filepath):
    try:
        with open ("text.log" , 'r') as f:
            world = f.read()

        UpperWorld = world.upper()

        print(UpperWorld)
    
    except FileNotFoundError:
        print("did not found this file")
    except IOError as e:
        print(f"this file is a error of :{e}")

    read_and_print("text.log")
    