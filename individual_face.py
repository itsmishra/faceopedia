import os
from tkinter import *
from tkinter import messagebox, filedialog
from shutil import copyfile
import cv2
import pyodbc
from PIL import ImageTk, Image
import databaseput
import home
import name_change
import people
import preview


class collection:
    def __init__(self, loc_name):
        files = self.get_location_from_database(loc_name)
        print(files)
        self.root = Tk()
        self.root.title("PEOPLE")
        self.root.geometry("1200x720+50+50")
        self.root.state('zoomed')
        # ----------------------top frame
        topframe = Frame(self.root, bg="#ff6347")
        topframe.pack(side=TOP, fill="x")

        homebtn = Button(topframe, width=10, text="HOME", command=self.runhome, height=2, bg="white")
        homebtn.pack(side=LEFT, padx=5, pady=5)

        peoplebtn = Button(topframe, width=10, text="PEOPLE", command=self.runpeople, height=2, bg="white")
        peoplebtn.pack(side=LEFT, padx=5, pady=5)

        exportbtn = Button(topframe, width=10, text="EXPORT", command=self.runexport, height=2, bg="white")
        exportbtn.pack(side=RIGHT, padx=5, pady=5)

        # --------------------left frame

        leftframe = Frame(self.root, bg="#ff6347", borderwidth=6)
        leftframe.pack(side=LEFT, fill="y")

        leftimagelocation="./people_faces/"+str(loc_name)+"/face-"+loc_name+".jpg"
        leftimage=ImageTk.PhotoImage(Image.open(leftimagelocation))
        DP = Label(leftframe,image=leftimage, bg="white", borderwidth=5)
        DP.pack(anchor=N,padx=20)

        self.changingNameLocation=loc_name
        if str(loc_name).isdigit():
            nametext="ID : "+loc_name
        else:
            nametext=loc_name
        self.namebtn = Button(leftframe, width=14, text=nametext, bg="white", borderwidth=1,
                              command=self.changeName)
        self.namebtn.pack(pady=20)

        # -------------------main frame
        peoplecollectionframe = Frame(self.root, borderwidth=6, width=20, bg="white")
        try:
            self.gat = files
            length = len(self.gat)  # no of images
            rem = length % 6  # remainig no.
            canvas = Canvas(peoplecollectionframe, width=1345)
            scrollbar = Scrollbar(peoplecollectionframe, orient="vertical", command=canvas.yview)
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
            peoplecollectionframe.pack(side=LEFT, fill="y")
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")




            self.photo = [[0 for x in range(length // 6)] for x in range(6)]  # creating matrix


            self.rem_photos = [0 for x in range(rem)]  # list of remaing
            len_of_matrix = length - rem

            for addr in range(rem):
                self.rem_photos[addr] = ImageTk.PhotoImage(
                    Image.open(self.gat[len_of_matrix]).resize((150, 100), Image.ANTIALIAS))
                len_of_matrix += 1

            self.btn = [[0 for x in range(length // 6)] for x in range(6)]
            self.rem_btn = [0 for x in range(rem)]

            self.f_rows = length - rem
            count = 0
            y = 0
            for x in range(6):
                for y in range(length // 6):
                    selectname = self.retrivename(self.gat[count].replace("\\", "/"))

                    self.photo[x][y] = ImageTk.PhotoImage(
                        Image.open(self.gat[count]).resize((150, 100), Image.ANTIALIAS))
                    self.btn[x][y] = Button(scrollable_frame, text=selectname, compound="top", image=self.photo[x][y],
                                            width=200, height=110,
                                            command=lambda x1=x, y1=y: self.get_name(x1, y1))
                    self.btn[x][y].grid(column=x, row=y, padx=10, pady=10)

                    count += 1
            else:
                r = y + 1
                for i in range(rem):
                    selectname = self.retrivename(self.gat[count].replace("\\", "/"))

                    self.rem_btn[i] = Button(scrollable_frame, text=selectname, compound="top",
                                             image=self.rem_photos[i], width=200, height=110,
                                             command=lambda x1=i: self.rem_get_name(x1, self.f_rows))
                    self.rem_btn[i].grid(column=i, row=r, padx=10, pady=10)

                    count += 1

        except FileNotFoundError as fnfe:
            messagebox.showwarning("warning", "No Files Added Yet")
            # databaseput.addfolder()

        self.root.mainloop()

        # peoplecollectionframe.pack(side=LEFT, fill="y")

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
        prev_location=preview.Preview(location)

    def rem_get_name(self, ind, ex):
        rem_location = self.gat[ex + ind]
        openprev=preview.Preview(rem_location)

    def runexport(self):
        path = filedialog.askdirectory()
        for p in self.gat:
            n = self.retrivename(p)
            copyfile(p, path + "/" + n)
        if len(path)>0:
            messagebox.showinfo("info", "EXPORTED!")

    def runhome(self):
        self.root.destroy()
        h3 = home.home()

    def runpeople(self):
        self.root.destroy()
        h3 = people.people()

    def retrivename(self, location):
        replaceobject = location.replace("\\", "/")
        splitname = replaceobject.split("/")
        selectname = splitname[-1]
        return selectname



    def get_location_from_database(self,loc):
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=D:\faceopedia\facerec.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        files=[]
        cursor.execute('select location from id_location where label_id=(?)', (loc))
        for row in cursor.fetchall():
            files.append(row[0])
        return files
    def runDB(self):
        bdput=databaseput.addfolder("faces","")
    def clear_db(self):
        #1 txt database
        txtpath="./database/"
        files=[]
        for r, d, f in os.walk(txtpath):
            for file in f:
                if '.txt' in file:
                    files.append(os.path.join(r, file))
        for txtfile in files:
            os.remove(txtfile)

        facepath="./people_faces/"
        face_files=[]
        for r, d, f in os.walk(facepath):
            for file in f:
                if '.jpg' in file:
                    face_files.append(os.path.join(r, file))
        for facefile in face_files:
            os.remove(facefile)

        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=D:\faceopedia\facerec.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""DELETE FROM id_location""")
        conn.commit()


    def changeName(self):
        name_change.namechange(self.changingNameLocation,self.namebtn)
        print("done")


#h=collection("4")