
import os
import flask
from flask import Flask, request, redirect, session, g, redirect, url_for, abort, render_template, flash, jsonify, json
import sys
import numpy
from flaskext.mysql import MySQL
from datetime import datetime

PATH_TO_FACEREC = "/Users/Clemsut/Desktop/facerec/facerec"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Put this into database
app = Flask(__name__,static_url_path='/static') # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py
mysql = MySQL()
reload(sys)
sys.setdefaultencoding('utf8')

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Invictus711!'
app.config['MYSQL_DATABASE_DB'] = 'facerec'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# ----------------------------------------------------------------------------------- #

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def verify(coursename, coursenum):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        if coursename and coursenum:
            cursor.execute("select Teacher_uniqname from courses where Coursename=%s and Coursenum=%s" ,[coursename, coursenum])
            rows = cursor.fetchmany(size=2)
            if len(rows) == 1:
                return True, rows[0]
            return False, "lonnybreaux"
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

def get_encoding_from_name(name):
    encoding = []
    directory = PATH_TO_FACEREC + "/data/known_people/" + name + "/encoding/" + name + ".txt"
    if os.path.exists(directory):
        encoding = numpy.loadtxt(directory, delimiter=',')
        return True, encoding
    else:
        return False, encoding
#------------------------------------------------------------------------------------------------------
@app.route('/')
def main_page():
    return flask.render_template('index.html')

@app.route('/portal', methods=['GET','POST'])
def get_course():
    if request.method == 'POST':
        coursename = request.form["coursename"]
        coursenum = request.form["coursenum"]
        verification = verify(coursename, coursenum)
        if not verification[0]:
            return '''<h1> Class Not Found </h1>'''
        encoding_present, face_encoding = get_encoding_from_name(verification[1][0])
        if not encoding_present:
            return '''<h1> Teacher Not Found </h1>'''
        return flask.render_template('upload_picture_confirm_attendance.html', teacher_encoding = face_encoding, course=coursename + coursenum)
    elif request.method == 'GET':
        return flask.render_template('collection_manager.html')

@app.route('/auth', methods=['GET', 'POST'])
def authenticate_teacher():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename): # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

@app.route('/attendance', methods=['GET', 'POST'])
def authenticate_students():
    return flask.render_template('index.html')

@app.route('/addCollection', methods=['POST'])
def addCollection():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        a_name = request.form['CollectionName']
        a_arn = request.form['CollectionArn']
        if a_name and a_arn:            # validate the received values
            cursor.callproc('sp_addCollection',(a_name,a_arn))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':  a_name + ' added to collectionsDB successfully!'})
            else:
                return json.dumps({'SQLerror':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/delCollection', methods=[ 'POST'])
def delCollection():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        d_name = request.form['CollectionName']
        if d_name:          # validate the received values
            cursor.callproc('sp_delCollection',[d_name,])
            data_1 = cursor.fetchall()
            cursor.callproc('sp_delFacesWithCollection',[d_name])
            data_2 = cursor.fetchall()
            if len(data_1) + len(data_2) is 0:
                conn.commit()
                return json.dumps({'message':d_name + ' removed from collectionsDB successfully!'})
            else:
                return json.dumps({'SQLerror':str(data[0])})

        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/addFace', methods=['POST'])
def addFace():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        collection_name = request.form['curCollection']
        umid = int(request.form['umid'])
        uniq_name = request.form['uniqname']
        first_name = request.form['first']
        last_name = request.form['last']
        face_id = request.form['faceid']

        if collection_name and umid and uniq_name and first_name and last_name and face_id:
            cursor.callproc('sp_addFace',(umid, uniq_name, first_name, last_name, face_id, collection_name))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':uniq_name + ' added to biometricsDB successfully!'})
            else:
                return json.dumps({'SQLerror':str(data[0])})
        else:
            return json.dumps({'InputError':'Enter the required fields'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/confirmStudent', methods=['POST'])
def confirmStudent():
    response = "Error"
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        FaceId = request.form['FaceId']
        Course = request.form['Course']
        if FaceId and Course:
            sql = 'select FirstName, LastName, UMID from biometrics inner join  ' + Course + ' on UMID where FaceId=%s limit 1 ; '
            cursor.execute(sql ,(FaceId))
            rows = cursor.fetchall()
            if len(rows) > 0:
                date = datetime.now().strftime('%Y-%m-%d %H')
                sql = 'insert into attendance(UMID,course,timestamp_in)values(%s,%s,%s);'
                cursor.execute( sql ,(str(rows[0][2]), Course, date))
                conn.commit()
                response = "Thanks " + rows[0][0] + " " + rows[0][1] + ". Your attendance in " + Course + " has been noted!"
            else:
                response = "Your FaceID does not match anyone in this class. Please try again. "
    except Exception as e:
        return json.dumps({'error':str(e)})
    except MySQL.IntegrityError:
        logging.warn("Failed to note your attendance in %s", Course)
    finally:
        cursor.close()
        conn.close()
    return response



if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)
