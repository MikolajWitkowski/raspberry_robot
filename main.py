from flask import Flask, render_template, jsonify, request, url_for, redirect, session
from control import RobotMove, DistanceSensor, Camera, CameraMove
from wtforms import Form, StringField, PasswordField, BooleanField, validators
from passlib.hash import sha256_crypt
from dbconnect import connection
import os


app = Flask(__name__)
app.config.update(dict(TITLE='Raspberry PI robot'))
app.config['SECRET_KEY'] = "secret_key"

robot = RobotMove()
th = DistanceSensor()
camera = Camera()
camera_move = CameraMove()

   
@app.route('/index/')
def index():
    username = session["username"]	
    return render_template('index.html')


@app.route('/control_panel')
def control_panel():
    return render_template('control_panel.html')


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.DataRequired()])


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    c, conn = connection()
    if request.method == 'POST' and form.validate():     
        username = form.username.data
        password = form.password.data
        sql = "SELECT username, password FROM users WHERE username=%s"
        c.execute(sql, (username,))
        try:
            password_db = c.fetchone()[1]
            if sha256_crypt.verify(password, password_db):
                session['logged_in'] = True
                session['username'] = username
             
                return redirect(url_for('control_panel'))

        except Exception:
            return redirect(url_for('login'))         

    return render_template('login.html', form=form)
    

@app.route('/logout/')
def logout():
    session.clear()
    Close().gpio_cleanup()
    return redirect(url_for('login'))


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message="Passsword must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the Terms of Service', [validators.DataRequired()])


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():

        username = form.username.data
        password = sha256_crypt.encrypt((str(form.password.data)))
        c, conn = connection()
        sql = "SELECT username FROM users WHERE username=%s"
        c.execute(sql, (username,))
        result = c.fetchone()

        if result:
            
            return render_template('register.html', form=form)
        else:
            sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
            values = (username, password)
            c.execute(sql, values)
            conn.commit()
            c.close()
            conn.close()

            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/forward')
def forward():
    robot.move_robot(True, False)
    robot.update()
    return 'forward'


@app.route('/backward')
def backward():
    robot.move_robot(False, True)
    robot.update()
    return 'backward'


@app.route('/left')
def left():
    robot.move_robot(True, True)
    robot.update()
    return 'left'


@app.route('/right')
def right():
    robot.move_robot(False, False)
    robot.update()
    return 'right'


@app.route('/speed_up')
def speed_up():
    robot.speed_up(10)
    return "speed_up"


@app.route('/speed_down')
def speed_down():
    robot.speed_down(10)
    return "speed_down"


@app.route('/stop')
def stop():
    robot.stop()
    robot.update()
    return 'stop'


@app.route('/play_video')
def play_video():
    camera.cam_play()
    return 'play_video'


@app.route('/stop_video')
def stop_video():
    camera.cam_stop()
    return 'stop_video'


@app.route('/move_camera_left')
def move_camera_left():
    camera_move.cam_move(10)
    return 'camera_move_left'


@app.route('/move_camera_right')
def move_camera_right():
    camera_move.cam_move(-10)
    return 'camera_move_right'


@app.route('/start_distance')
def start_distance():
    th.start()
    return 'start_distance'


@app.route('/pause_distance')
def pause_distance():
    th.pause()
    return 'pause_distance'


@app.route('/resume_distance')
def resume_distance():
    th.resume()
    return 'resume distance'

    
@app.route('/get_data', methods=['GET'])
def get_data():
   return jsonify(distance=str(th.dist), speed=str(robot.speed))


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', threaded=True)

		
		












