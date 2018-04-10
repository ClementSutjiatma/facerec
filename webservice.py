
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

import face_recognition
from flask import Flask, jsonify, request, redirect
import flask

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Put this into database
ALLOWED_CLASSES = ['ECON', 'EECS', 'TO']
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def verify(coursename, coursenum):
    #check whether in ALLOWED_CLASSES Database
    if coursename in ALLOWED_CLASSES:
        return True
    return False

def get_name_encoding(course):

    return "this", "that"

@app.route('/')
def main_page():
    return flask.render_template('index.html' , teacher_encoding=)

@app.route('/portal', methods=['POST'])
def get_course():
    if request.method == 'POST':
        coursename = request.args.get('coursename')
        coursenum = request.args.get('coursenum')
        if verify(coursename, coursenum):
            return '''<h1> Class Not Found </h1>'''
        face_encoding, face_name = get_name_encoding(coursename + coursenum)
    return flask.render_template('verify_teacher.html', teacher_encoding = face_encoding, teacher_name = face_name)

@app.route('/test', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    clement_image = face_recognition.load_image_file("./known_people/Clement Sutjiatma.jpg")
    known_face_encoding = face_recognition.face_encodings(clement_image)[0]

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)

    face_found = False
    is_obama = False

    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_obama = True

    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)
