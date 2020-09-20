from tkinter import *
from tkinter import filedialog, messagebox

import databaseput,encode_faces,cluster_faces,home,splash
class startup_screen():
    def __init__(self):
        self.startup_win=Tk()
        self.startup_win.geometry("500x500+350+200")
        self.startup_win.resizable(False,False)
        #top frame
        mainframe = Frame(self.startup_win, width=500, height=400, background="white")
        wel_label = Label(mainframe, text="welcome to faceOpedia",borderwidth=2 ,width=50,
                          relief="solid", font="Verdana 10 bold",bg="white").pack()
        select_label = Label(mainframe, text="Select folders to Continue", font="Verdana 10 bold",bg="white").pack(pady=20)
        self.folders_path=[]
        select_btn = Button(mainframe, width=50, text="Select Folder",bg="white", font="Verdana 10 bold",command=self.selectfolder_terminal).pack(pady=20)
        self.list_folders_box=Listbox(mainframe,width=70)
        self.list_folders_box.pack()
        mainframe.pack(side="top", fill="both", expand=True)
        #bottom frame
        bot_frame=Frame(self.startup_win, width=500, height=100, background="red")
        continue_btn=Button(bot_frame,width=50,text="Continue>>>",font="Verdana 10 bold",bg="white",command=self.on_continue).pack(pady=20)
        bot_frame.pack(side="bottom", fill="both")

        self.startup_win.mainloop()


    def selectfolder_terminal(self):
        get_files = filedialog.askdirectory(parent=self.startup_win, title='Choose a file')
        self.folders_path.append(get_files)
        self.list_folders_box.insert(0,get_files)
        print(self.folders_path)
    def on_continue(self):
        if len(self.folders_path)>0:

            for path in self.folders_path:
                print(path,type(path))
                d=databaseput.addfolder("startup",path)
            encode_faces.encoding()
            self.startup_win.destroy()
            runsplash=splash.splash()
        else:
            messagebox.showwarning("warning", "No Folders Selected Added")


#startup_screen()