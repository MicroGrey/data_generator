import os



with open ("./log/log.txt", "r") as f:
    lines = f.readlines()
    lines = [line[:-5] for line in lines]
    print(lines)
    for line in lines:
        print(line)
        os.remove("../all/"+line+".txt")
        os.remove("../all/"+line+".png")