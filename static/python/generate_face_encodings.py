import os
import face_recognition
import cv2
import sys
import io
import shutil
import numpy

if len(sys.argv) != 2:
    print("Please input schedule.py [Image File Path]")
    exit(0)
path = sys.argv[1]
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




for image_path in os.listdir(path):
    if allowed_file(image_path):
        print("MAPPING " + image_path)
        directory = path + "/" + os.path.splitext(image_path)[0]
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(directory + "/image")
            os.makedirs(directory + "/encoding")
            shutil.move(path + "/" + image_path, directory + "/image/" + image_path)
        input_path = directory + "/image/" + image_path
        face_image = face_recognition.load_image_file(input_path)
        face_encoding = face_recognition.face_encodings(face_image)

        if len(face_encoding) == 1:
            output_path = directory + "/encoding/" + os.path.splitext(image_path)[0] + ".txt"
            with io.FileIO(output_path, "w") as file:
                numpy.savetxt(output_path, face_encoding[0], delimiter=",")
            print(output_path + " SUCCESS")

        else:
            print("ignored " + image_path + "; No Face Found")
    else:
        print("ignored " + image_path + "; Invalid File Type")
