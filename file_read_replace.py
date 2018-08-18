import os

def read(filename, n):
    """

    A generator function that yields n lines and removes data from the start 
    of the file or until EOF.

    When lines are read, they are overwritten with whitespace and a counter
    at the start to indicate number of overwritten characters.
    Beginning of file will be replaced with "@N" when edited
    where N is number of characters to skip.

    Access and overwrite speed is fast and indepentent of file length.

    File will be deleted when no more data is available.

    Usage:
        for line in read(filename, number_of_lines):
            # Process line

    """

    try:
        with open(filename, "r+") as fp:
            skip = ["0"]
            if fp.read(1) == "@":
                while True:
                    char = fp.read(1)
                    if char.isdigit():
                        skip.append(char)
                    else:
                        break

            fp.seek(int("".join(skip)))

            try:
                for _ in range(n):
                    current_pos = fp.tell()
                    fp.seek(0, 2)
                    EOF = fp.tell()
                    fp.seek(current_pos, 0)

                    if EOF == current_pos:
                        raise EOFError
                    else:
                        yield fp.readline()
            finally:
                point = fp.tell()

                if point:           
                    fp.seek(0)
                    fp.write(f"@{point}")
                    fp.write(" " * (point - 1 - len(f"@{point}")))
    except EOFError:
        os.remove(filename)