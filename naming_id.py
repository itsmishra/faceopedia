import os
from tkinter import *
from tkinter import messagebox

from PIL import ImageTk, Image




class naming():
    def __init__(self):
        self.root = Tk()
        self.root.title("NAMING")
        self.root.geometry("500x720+50+50")



        # --------------------left frame





        # -------------------main frame
        homeframe = Frame(self.root, borderwidth=6,bg="#ff6347")
        #homeframe.pack(side=LEFT, fill="y")

        canvas = Canvas(homeframe,width=1345)
        scrollbar = Scrollbar(homeframe, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas,bg="white")

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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

        try:
            self.gat = []  # list of locations

            path = "./people_faces"
            print(path)

            if not path:
                pass
            else:

                # get file
                # r=root, d=directories, f = files
                for r, d, f in os.walk(path):
                    splitRoot=r.split("\\")
                    if splitRoot[-1] == "-1":
                        pass
                    else:
                        for file in f:
                            if '.jpg' in file:
                                self.gat.append(os.path.join(r, file).replace("/", "\\"))

            #print(self.gat)

            length = len(self.gat)  # no of images
            rem = length % 6  # remainig no.
            print(length, rem)



            self.rem_photos = [0 for x in range(length)]  # list of remaing
            print(self.rem_photos)
            len_of_matrix = length - rem

            for addr in range(length):
                self.rem_photos[addr] = ImageTk.PhotoImage(
                    Image.open(self.gat[addr]).resize((150, 100), Image.ANTIALIAS))
            print(self.rem_photos)

            self.rem_btn = [0 for x in range(length)]
            self.enter = [0 for x in range(length)]


            count = 0
            row=0
            for x in range(length):


                self.rem_btn[x] = Button(scrollable_frame, image=self.rem_photos[x],bg="white",relief=RIDGE, width=200, height=100)
                self.rem_btn[x].grid(column=0, row=x, padx=10, pady=10)
                self.enter[x] = Entry(scrollable_frame, width=20)
                self.enter[x].grid(column=1, row=x, padx=10, pady=10)
                self.savebtn = Button(scrollable_frame, width=10,text="SAVE",command=lambda x1=x: self.rem_get_name(x1))
                self.savebtn.grid(column=2, row=x, padx=10, pady=10)


        except FileNotFoundError as fnfe:
            messagebox.showwarning("warning", "No Files Added Yet")
            #databaseput.addfolder()

        self.root.mainloop()




    def rem_get_name(self, ind):

        rem_location = self.gat[ ind]
        print(rem_location)
        fol_name = self.gat[ind].split("\\")
        exname = fol_name[-2]
        print(exname)
        dir=rem_location.split("\\")
        print(dir)
        dir[2]="mishra"
        print(dir)










naming()