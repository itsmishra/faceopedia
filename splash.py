from tkinter import *
from  tkinter.ttk import *

import os
import home
import startup
class splash():
    def __init__(self):

        root =  Tk()
        root.title("splash")
        root.overrideredirect(True)
        root.geometry("842x450+350+200")



        img =  PhotoImage(file=".\img\splash.png")


        panel = Label(root, image = img)
        panel.pack()

        # Progress bar widget
        progress = Progressbar(root, orient = HORIZONTAL, length = 1000)

        # Function responsible for the updation
        # of the progress bar value
        def bar():
            progress['value'] = 0
            for i in range(0,100):


                import time
                progress['value'] = i
                progress.update()
                time.sleep(0.01)
                if (i ==99):
                    root.destroy()

                    if os.path.isdir("./database") == TRUE:
                        try:
                            count=0
                            openall=open("./database/all.txt","r")
                            for i in openall:
                                count+=1
                            openall.close()
                            print(count)
                            if count==0:
                                callstartup=startup.startup_screen()
                            else:
                                callhome=home.home()
                        except FileNotFoundError as fnfe:
                            callstartup = startup.startup_screen()





        progress.pack()
        # This button will initialize
        # the progress bar
        bar()


        root.mainloop()
if __name__ == '__main__':
    run = splash()
