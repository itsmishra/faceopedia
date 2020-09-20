from sklearn.cluster import DBSCAN
from imutils import build_montages
import numpy as np
import argparse
import pickle
import cv2
import os
import shutil
import pyodbc
class create_cluster():
    def __init__(self):

        #db
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=D:\faceopedia\facerec.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("DELETE * FROM id_location")
        conn.commit()
        facespath="./people_faces"
        if os.path.exists(facespath):
            shutil.rmtree("./people_faces")
            os.mkdir("./people_faces/")
        else:
            os.mkdir("./people_faces/")
        # load the serialized face encodings + bounding box locations from
        # disk, then extract the set of encodings to so we can cluster on
        # them
        print("[INFO] loading encodings...")
        data = pickle.loads(open("./pickel_file/encodings.pickle", "rb").read())
        data = np.array(data)
        encodings = [d["encoding"] for d in data]

        # cluster the embeddings
        print("[INFO] clustering...")
        clt = DBSCAN(metric="euclidean", n_jobs=-1)
        clt.fit(encodings)

        # determine the total number of unique faces found in the dataset
        labelIDs = np.unique(clt.labels_)
        numUniqueFaces = len(np.where(labelIDs > -1)[0])
        print("[INFO] # unique faces: {}".format(numUniqueFaces))

        # loop over the unique face integers
        for labelID in labelIDs:
            # find all indexes into the `data` array that belong to the
            # current label ID, then randomly sample a maximum of 25 indexes
            # from the set

            print("[INFO] faces for face ID: {}".format(labelID))
            idxs = np.where(clt.labels_ == labelID)[0]
            idxs = np.random.choice(idxs, size=min(25, len(idxs)),replace=False)

            # initialize the list of faces to include in the montage
            faces = []
            """sep_path="./seperated/"+str(labelID)
            try:
                os.mkdir(sep_path)
            except FileExistsError as fe:
                shutil.rmtree(sep_path)
                os.mkdir(sep_path)"""
            face_locate="./people_faces/"+str(labelID)
            try:
                os.mkdir(face_locate)
            except FileExistsError as fe2:
                shutil.rmtree(face_locate)
                os.mkdir(face_locate)

            # loop over the sampled indexes
            for i in idxs:
                # load the input image and extract the face ROI
                image = cv2.imread(data[i]["imagePath"])
                (top, right, bottom, left) = data[i]["loc"]
                face = image[top:bottom, left:right]

                # force resize the face ROI to 96x96 and then add it to the
                # faces montage list
                face = cv2.resize(face, (96, 96))
                faces.append(face)
                print(len(faces))
                cursor.execute('''INSERT INTO id_location (label_id,location)
                                        VALUES(?,?)''', (int(labelID),data[i]["imagePath"]))

                #cv2.imwrite(sep_path+"/face-" + str(labelID)+"@" + str(len(faces)) + "@.jpg", image)
                cv2.imwrite(face_locate + "/face-" + str(labelID)+".jpg", face)

            # create a montage using 96x96 "tiles" with 5 rows and 5 columns
            montage = build_montages(faces, (96, 96), (5, 5))[0]

            # show the output montage
            title = "Face ID #{}".format(labelID)
            title = "Unknown Faces" if labelID == -1 else title
            #cv2.imshow(title, montage)
            #cv2.waitKey(0)
            #update unrecognized
            conn.commit()
        conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=D:\faceopedia\facerec.accdb;'
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("""UPDATE id_location
                                    SET label_id=?
                                    WHERE label_id=?""", ("Unrecognized", "-1"))
        conn.commit()
        os.mkdir("./people_faces/Unrecognized")
        cpy_source = new_name = "./people_faces/-1/face--1.jpg"
        cpy_des = new_name = "./people_faces/Unrecognized/face-Unrecognized.jpg"
        shutil.copyfile(cpy_source, cpy_des)
        shutil.rmtree("./people_faces/-1/")
#create_cluster()
