import os
import shutil
import tkinter
from tkinter import *

import pyodbc
import startup
import databaseput
import  people
from PIL import ImageTk, Image
import preview



class home():
    def __init__(self):
        self.root = Tk()
        self.root.title("HOME")
        self.root.geometry("1200x720+50+50")
        self.root.state('zoomed')
        # ----------------------top frame
        topframe = Frame(self.root, bg="#ff6347")
        topframe.pack(side=TOP, fill="x")

        homebtn = Button(topframe, width=10, text="HOME", height=2, bg="white")
        homebtn.pack(side=LEFT, padx=5, pady=5)

        peoplebtn = Button(topframe, width=10, text="PEOPLE",command=self.runpeople ,height=2, bg="white")
        peoplebtn.pack(side=LEFT, padx=5, pady=5)

        refreshbtn = Button(topframe, width=10, text="REFRESH", command=self.refresh, height=2, bg="white")
        refreshbtn.pack(side=RIGHT, padx=5, pady=5)

        # --------------------left frame

        leftframe = Frame(self.root, bg="#ff6347", borderwidth=6)
        leftframe.pack(side=LEFT, fill="y")

        addfolder = Button(leftframe, width=20, text="Add Folder", bg="white", borderwidth=1,
                           command=self.runDB)
        addfolder.pack(anchor=NW)
        cleardb = Button(leftframe, width=20, text="Clear Data", bg="white", borderwidth=1,
                         command=self.clear_db)
        cleardb.pack(anchor=S,pady=20)

        # -------------------main frame
        homeframe = Frame(self.root, borderwidth=6)
        #homeframe.pack(side=LEFT, fill="y")

        try:
            self.gat = []  # list of locations

            all = open("./database/all.txt", "r")
            for e in all:
                self.gat.append(e[0:-1].replace("\\", "/"))  # put in gat
            all.close()
            length = len(self.gat)  # no of images
            rem = length % 6  # remainig no.
            canvas = Canvas(homeframe,width=1345)
            scrollbar = Scrollbar(homeframe, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas)

            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            if length>30:
                canvas.bind_all("<MouseWheel>", _on_mousewheel)



            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
            )

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

            canvas.configure(yscrollcommand=scrollbar.set)
            homeframe.pack(side=LEFT, fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")


            print(length, rem)


            print(length, rem)

            self.photo = [[0 for x in range(length // 6)] for x in range(6)]  # creating matrix
            print(self.photo)

            self.rem_photos = [0 for x in range(rem)]  # list of remaing
            print(self.rem_photos)
            len_of_matrix = length - rem

            for addr in range(rem):
                self.rem_photos[addr] = ImageTk.PhotoImage(
                    Image.open(self.gat[len_of_matrix]).resize((150, 100), Image.ANTIALIAS))
                len_of_matrix += 1
            print(self.rem_photos)

            self.btn = [[0 for x in range(length // 6)] for x in range(6)]
            self.rem_btn = [0 for x in range(rem)]

            self.f_rows = length - rem
            count = 0
            y=0
            for x in range(6):
                for y in range(length // 6):
                    self.photo[x][y] = ImageTk.PhotoImage(
                        Image.open(self.gat[count]).resize((150, 100), Image.ANTIALIAS))
                    self.btn[x][y] = Button(scrollable_frame,image=self.photo[x][y], width=200, height=100,
                                            command=lambda x1=x, y1=y: self.get_name(x1, y1))
                    self.btn[x][y].grid(column=x, row=y, padx=10, pady=10)
                    count += 1
            else:
                r = y + 1
                for i in range(rem):
                    self.rem_btn[i] = Button(scrollable_frame, image=self.rem_photos[i], width=200, height=100,
                                             command=lambda x1=i: self.rem_get_name(x1, self.f_rows))
                    self.rem_btn[i].grid(column=i, row=r, padx=10, pady=10)



        except FileNotFoundError as fnfe:
            tkinter.messagebox.showwarning("warning", "No Files Added Yet")
            databaseput.addfolder("home","")

        self.root.mainloop()



    def get_name(self, x, y):
        print(x, y)
        col = x + 1
        row = y + 1

        trows = self.f_rows // 6
        if col == 1:
            ind = row
        if col == 2:
            ind = trows * 1 + row
        if col == 3:
            ind = trows * 2 + row
        if col == 4:
            ind = trows * 3 + row
        if col == 5:
            ind = trows * 4 + row
        if col == 6:
            ind = trows * 5 + row


        location = self.gat[ind - 1]
        print(location)
        p1 = preview.Preview(location)


    def rem_get_name(self, ind, ex):
        print(ex + ind + 1)
        rem_location = self.gat[ex + ind]
        print(rem_location)
        p2=preview.Preview(rem_location)


    def refresh(self):
        self.root.destroy()
        h2 = home()
    def runpeople(self):
        self.root.destroy()
        p1 = people.people()

    def runDB(self):
        bdput=databaseput.addfolder("home","")
    def clear_db(self):
        #1 txt database
        txtpath="./database/"
        files=[]
        for r, d, f in os.walk(txtpath):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))
        print(files)
        for txtfile in files:
            os.remove(txtfile)

        facepath="./people_faces/"
        face_files=[]
        for r, d, f in os.walk(facepath):
            for file in f:
                if '.jpg' in file:
                    face_files.append(os.path.join(r, file))
        print(face_files)
        for facefile in face_files:
            os.remove(facefile)


        print("deleted")
        self.root.destroy()
        startup_run=startup.startup_screen()



#h1 = home()
