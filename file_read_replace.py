def read(filename, n=float("inf"), **kwargs):
    """
    
    A generator that reads and yields n lines and replaces data from
     the start of the file or until EOF.
    
    File length is determined when generator is defined.
    File is overwritten at end of generator.
    
    At end of generator, lines that are read are replaced with whitespace
    and a counter at the start to indicate number of overwritten characters.
    
    Arguments:
     n: Number of lines to read and yield.
     kwargs: kwargs are passed to the builtin open() function.
     
    --- Example ---
    
    test.txt:
     abcde\nfghij\nklmno\npqrst
     
    for line in read("test.txt", 2):
        print(line)
        
    Output:
     "abcde\n"
     "fghij\n"
    
    test.txt:
     @14          \nklmno\npqrst

    """

    with open(filename, "r+", **kwargs) as fp:
        fp.seek(0, 2)
        file_length = fp.tell()
        fp.seek(0)

        skip = 0
        if fp.read(1) == "@":
            while True:
                char = fp.read(1)
                if not char.isdigit():
                    break
                    
                skip = skip*10 + int(char)
                if skip >= file_length:
                    raise StopIteration

        fp.seek(skip)

        try:
            counter = 0
            while counter < n:
                counter += 1
                if fp.tell() == file_length:
                    raise StopIteration

                yield fp.readline()
        finally:
            point = fp.tell()

            if point:           
                fp.seek(0)
                fp.write(f"@{point}{' '*(point-2-len(str(point)))}")
