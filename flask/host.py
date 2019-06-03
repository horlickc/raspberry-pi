from flask import Flask, request, render_template, redirect, url_for, Response
import pymysql
import cv2


class VideoCamera(object):
	def __init__(self):
		self.video = cv2.VideoCapture(0)

	def __del__(self):
		self.video.release()

	def get_frame(self):
		success, image = self.video.read()

		ret, jpeg = cv2.imencode('.jpg', image)
		return jpeg.tobytes()

app = Flask(__name__)

#open database connection
db = pymysql.connect(host='localhost', user='toby', password='toby', db='data')

@app.route("/")
def index():
	return render_template("index.html")


@app.route("/signup", methods = ['POST', 'GET'])
def signup():
	error = None
	if request.method == "POST":
		usrname = request.form["username"]
		pwd = request.form["password"]
		# prepare a cursor object using cursor() method
		cursor = db.cursor()
		#maxid = cursor.fetchone()
		# Execute the SQL command
		cursor.execute("""INSERT INTO user (username, password) VALUES (%s, %s)""", (usrname, pwd))
		# Commit your changes in the database
		db.commit()
		return render_template("signup_.html", error = error)
	db.close()

@app.route("/login", methods=['POST', 'GET'])
def login():
	error = None
	if request.method == 'POST':
		usrname = request.form["username"]
		pwd = request.form["password"]
		# prepare a cursor object using cursor() method
		cursor = db.cursor()
		#maxid = cursor.fetchone()
		# Execute the SQL command
		sql = ("SELECT username, password FROM user WHERE username = '"+usrname+"'")
		cursor.execute(sql)
		# Commit your changes in the database
		#db.commit()
		results = cursor.fetchall()
		for row in results:
			callun = row[0]
			callpw = row[1]
			if usrname == callun and pwd == callpw:
				cursor.close()
			return render_template("a.html", error=error)
			#print ("Customer Name = %s, Password = %s" % (custName, custPassword))
			#return redirect(url_for('customer', guest = custName))
			##custPwd = password

	db.close()

@app.route("/feed", methods=['POST', 'GET'])
def feed():
	return render_template('a.html')


def gen(camera):
	while True:
		frame = camera.get_frame()

		yield (b'--frame\r\n'
			   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed', methods=['POST', 'GET'])
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.debug = True
	app.run(host="0.0.0.0", port=5000)
