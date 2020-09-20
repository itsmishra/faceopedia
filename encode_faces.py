
from tkinter.ttk import Progressbar

from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os,time
import cluster_faces
from tkinter import *

class encoding():
    def __init__(self):
        root = Tk()
        root.title("#encoding")
        root.overrideredirect(True)
        root.geometry("300x100+350+200")

        mainframe = Frame(root, width=500, height=400, background="white")
        wel_label = Label(mainframe, text="Encoding", borderwidth=2, width=50,
                          relief="solid", font="Verdana 10 bold", bg="white").pack()
        panel = Label(mainframe, text="",bg="white")


        # Progress bar widget
        progress = Progressbar(mainframe, orient=HORIZONTAL, length=300)

        # Function responsible for the updation
        # of the progress bar value
        def bar():
            print("[INFO] quantifying faces...")
            imagePaths = []
            ef = open("./database/all.txt", "r")
            for e in ef:
                imagePaths.append(e[0:-1].replace("\\", "/"))
            ef.close()
            progress['value'] = 0
            print(len(imagePaths))


            data = []

            print("reached")
            # loop over the image paths
            for (i, imagePath) in enumerate(imagePaths):
                cal = i / len(imagePaths)
                print(i,len(imagePaths),cal)
                progress['value'] = cal * 100
                panel.config(text=imagePath)
                progress.update()
                time.sleep(0.01)
                # load the input image and convert it from RGB (OpenCV ordering)
                # to dlib ordering (RGB)
                print("[INFO] processing image {}/{}".format(i + 1,
                                                             len(imagePaths)))
                print(imagePath)
                image = cv2.imread(imagePath)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                # detect the (x, y)-coordinates of the bounding boxes
                # corresponding to each face in the input image
                boxes = face_recognition.face_locations(rgb,
                                                        model="detection_method")

                # compute the facial embedding for the face
                encodings = face_recognition.face_encodings(rgb, boxes)

                # build a dictionary of the image path, bounding box location,
                # and facial encodings for the current image
                d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
                     for (box, enc) in zip(boxes, encodings)]
                data.extend(d)


            # dump the facial encodings data to disk
            print("[INFO] serializing encodings...")
            f = open("./pickel_file/encodings.pickle", "wb")
            f.write(pickle.dumps(data))
            f.close()


        panel.pack(pady=20)
        progress.pack()
        mainframe.pack(side="top", fill="both", expand=True)
        # This button will initialize
        # the progress bar
        bar()
        #root.mainloop()
        root.destroy()
        cluster_faces.create_cluster()



        """"""





#e=encoding()