def to_upper_case(input_file, output_file):
    try:
        with open (input_file , 'r') as infile:
            world = infile.read()
        
        UpperWold = world.upper()

        with open (output_file , 'w') as outfile:
            outfile.write(UpperWold)
        
        print(f"have dnoe, have save in {output_file}")

    except IOError as e:
        print("have a error as {e}")
    
    except FileNotFoundError:
        print(" have not found this file")

to_upper_case("input.txt" , "output.txt")