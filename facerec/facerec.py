
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/
import os
import sqlite3
import flask
from flask import Flask, request, redirect, session, g, redirect, url_for, abort, render_template, flash, jsonify
import face_recognition
import sys

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Put this into database
app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='secret',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Database initialized.')

# ----------------------------------------------------------------------------------- #

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def verify(request):
    db = get_db()
    coursename = request.form["coursename"]
    coursenum = request.form["coursenum"]
    cur = db.execute('select teacher_uniqname from courses where coursename=? and coursenum=?' ,[coursename, coursenum])
    rows = cur.fetchall()
    if len(rows) == 1:
        teacher_uniqname = rows[0]
        return True, teacher_uniqname
    return False, "lonnybreaux"

def get_name_encoding(course):

    return "this", "that"

@app.route('/')
def main_page():
    return flask.render_template('index.html')

@app.route('/portal', methods=['POST'])
def get_course():
    if request.method == 'POST':
        verification = verify(request)
        if not verification[0]:
            return '''<h1> Class Not Found </h1>'''
        face_encoding= get_name_encoding(verification[1])
    return flask.render_template('verify_teacher.html', teacher_encoding = face_encoding, teacher_name = verification[1])

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
