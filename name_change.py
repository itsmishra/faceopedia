import os
import shutil
from shutil import copyfile
from tkinter import *

import psutil
import pyodbc
from PIL import ImageTk, Image


class namechange():
    def __init__(self ,loc_name,btn):
        self.update_name_btn=btn
        self.changeloc=loc_name
        self.name_change_root = Tk()
        self.name_change_root.geometry("400x200+350+200")
        self.name_change_root.resizable(False, False)
        # top frame
        mainframe = Frame(self.name_change_root, width=500, height=400, background="white")
        wel_label = Label(mainframe, text="Change Name", borderwidth=2, width=50,
                          relief="solid", font="Verdana 10 bold", bg="white").pack()
        entername_label = Label(mainframe, text="Enter Name", font="Verdana 10 bold", bg="white").pack(pady=10)

        self.enter_name_field=Entry(mainframe,width=30,borderwidth=2,relief="solid", font="Verdana 10 bold", bg="white",
                               justify='center')
        self.enter_name_field.focus_set()
        self.enter_name_field.pack(pady=10)
        mainframe.pack(side="top", fill="both", expand=True)
        # bottom frame
        bot_frame = Frame(self.name_change_root, width=500, height=100, background="red")
        continue_btn = Button(bot_frame, width=50, text="Continue>>>", font="Verdana 10 bold", bg="white",
                              command=self.continue_clicked).pack(pady=20)
        bot_frame.pack(side="bottom", fill="both")
        self.name_change_root.mainloop()


    def continue_clicked(self):
        print(self.changeloc,self.enter_name_field.get())
        update_name_get=self.enter_name_field.get()
        ex_db=set()
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=D:\faceopedia\facerec.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""SELECT * FROM id_location""")
        myresult = cursor.fetchall()
        for x in myresult:
            ex_db.add(x[0])
        if update_name_get=="":
            print("error")
        elif update_name_get in ex_db:
            print("ERROR")
        else:
            cursor.execute("""UPDATE id_location 
                                SET label_id=?
                                WHERE label_id=?""",(update_name_get,self.changeloc))
            conn.commit()
            os.mkdir("./people_faces/"+update_name_get)

            cpy_source=new_name = "./people_faces/" + str(self.changeloc) + "/face-" + self.changeloc + ".jpg"
            cpy_des=new_name = "./people_faces/" + update_name_get + "/face-" + update_name_get + ".jpg"
            copyfile(cpy_source,cpy_des)
            shutil.rmtree("./people_faces/" + str(self.changeloc))

        self.update_name_btn.configure(text=update_name_get)
        self.name_change_root.destroy()
        print("db updated")


        

#namechange("ben")