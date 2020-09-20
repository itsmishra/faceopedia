from tkinter import filedialog,messagebox
import databaseall
import os

def addfolder(flag,path):
    files = []
    existingfiles = []

    if flag != "startup":

        path = filedialog.askdirectory()

    if not path:
        pass
    else:

        #get file
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))
                if '.jpeg' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))
                if '.JPG' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))
                if '.JEPG' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))
                if '.PNG' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))
                if '.png' in file:
                    files.append(os.path.join(r, file).replace("/","\\"))

        #get existing files


        ss = path.split("/")
        maindb = ss[-1] + ".txt"


        try:
            ef = open("./database/"+maindb, "r")
            for e in ef:
                existingfiles.append(e[0:-1].replace("/","\\"))
            ef.close()
        except FileNotFoundError as fnfe:
            f = open("./database/"+maindb, "w")
            f.close()



        putfile=set(files).union(existingfiles)
        putfile=list(putfile)





        print(path)
        print(putfile)
        homedatabase = open("./database/"+maindb, 'w')
        for i in range(0,len(putfile)):

            homedatabase.write(putfile[i]+"\n")
        homedatabase.close()

        (">>>>>>>>>>>")

        databaseall.merger(maindb,flag)




