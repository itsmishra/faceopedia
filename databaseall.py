import encode_faces

def merger(currentfile,flag):
    exist = []
    currentfileexist = []
    print(currentfile)
    try:
        ef = open("./database/all.txt", "r")
        for e in ef:
            exist.append(e[0:-1].replace("\\","/"))
        ef.close()
    except FileNotFoundError as fnfe:
        f = open("./database/all.txt", "w")
        f.close()


    cf=open("./database/"+currentfile,"r")
    for e in cf:
        currentfileexist.append(e[0:-1].replace("\\","/"))
    cf.close()

    

    insertfile = set(exist).union(currentfileexist)
    insertfile = list(insertfile)


    insert_in_all=open("./database/all.txt","w")
    for i in range(0,len(insertfile)):
        insert_in_all.write(insertfile[i]+"\n")
    insert_in_all.close()
    if flag != "startup":
        encode_faces.encoding()
