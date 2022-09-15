from flask import *
import cv2
import os
import  sqlite3
import threading
import bcrypt
import shutil
import urllib
from random import randint
from werkzeug.utils import secure_filename
from datetime import *

app=Flask(__name__)
database = sqlite3.connect('database.db',check_same_thread=False)

# app.config['D:\\program\\devrev\\yolov5\\videofeeduploads']
import threading
import os
class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print( "Starting " + self.previewName)
        # camPreview(self.previewName, self.camID)
        os.system('python detect.py --source '+str(self.camID)+' --weights weights/runs/train/exp3/weights/bestpc1.pt --img 416 --save-txt --save-crop --save-conf')
        

def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    if cam.isOpened():  # try to get the first frame
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        cv2.imshow(previewName, frame)
        rval, frame = cam.read()
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows





@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file1():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      os.system('python detect.py --source '+str(f.filename)+' --weights weights/runs/train/exp3/weights/best_ir.pt --img 416 --save-txt --save-crop --save-conf')
    #   dirs = os.listdir('runs/detect/')
    #   video = 'runs/detect/'+dirs[-1]+'/'+f.filename
    #   return render_template('irout.html',output=video)
      return "Detected"
   return 'Hii'


def create_user(name,email,passw):
    cursor = database.cursor()
    unid = randint(000000000,999999999)
    userid = 'U'+str(unid)
    # password = (bcrypt.hashpw(passw.encode('utf-8'),bcrypt.gensalt()))
    # print(password)
    password = passw
    # query = f"Insert into users values('{userid}','{name}','{password}','{email}')"
    query = 'Insert into users values("'+userid+'","'+name+'","'+password+'","'+email+'")'
    # print(query)
    cursor.execute(query)
    database.commit()



def validate(email,passw):
    cursor = database.cursor()
    users = cursor.execute(f'select password from users where email = "{email}"')
    users = cursor.fetchall()
    if len(users)>0:
        # if bcrypt.checkpw(passw.encode('utf-8'),users[0][0].encode('utf-8')):
        if passw == users[0][0]:
            cursor.close()
            return True

def getDrones():
    ans = os.listdir('runs/detect/')
    # print(ans)
    all_files = []
    for i in ans:
        # print(i)
        try:
            ans1 = os.listdir('runs/detect/'+i+'/crops/Drone')
            all_files.append('runs/detect/'+i+'/crops/Drone/'+ans1[0])
            
        except:
            pass    

    return (all_files)


def run_detect():
    # thread1 = camThread("Camera 1", 0)
    # thread2 = camThread("Camera 2", 1)
    # thread1.start()
    # thread2.start()
    os.system('python detect.py --source 0 --weights weights/runs/train/exp3/weights/besthrd.pt --img 416 --save-txt --save-crop --save-conf')

def run_website():
    return 'detect'

@app.route('/history')
def history():

    # images = getDrones()
    # for i in images:
    #     shutil.copy(i,'static/history')

    # images = os.listdir('static/history/') 
    # path =   'static/history/'
    # final_imgs = []
    # times = []
    # for i in images:
    #     final_imgs.append(path+i)
    #     time = str(i).split('_')[1]
    #     # time = time[::-1]
    #     time = time[6:8]+'-'+time[4:6]+'-'+time[:4]+' '+time[8:10]+':'+time[10:12]
    #     times.append(time)

    # lenth = len(times)    
    # data = 

    req = urllib.request.urlopen('http://10.1.1.203:5000/api/history')
    data = req.read()
    data = json.loads(data)
    final_imgs = []
    times = []
    data = data["data"]

    # for i in data
    # # print(data[1])
    lenth = (len(data))
    for i in range(lenth):
        final_imgs.append(data[i][str(i)]['img'])
        times.append(data[i][str(i)]['datetime'])
    return render_template('historyy.html',imgs = final_imgs,time = times,length=lenth)


@app.route('/livecam')
def livecam():
    run_detect()
    return redirect(url_for('history'))


@app.route('/detect')
def detect():

    # t1=threading.Thread(target=run_detect())
    # # t2 = threading.Thread(target=)
    # t1.start()
    # # # t2.start()
    # t1.join()
    # run_detect()
    # t2.join()

    return render_template('detect.html')
    # return 'detect'


@app.route('/register',methods=['GET','POST'])
def register():

    if request.method == "POST":
        name = request.form['name']
        email = request.form['Emails']
        passw = request.form['Password']
        cpass = request.form['cnfpass']
        if passw == cpass: 
         print(passw)   
         create_user(name,email,passw)
        # redirect('')
        return redirect(url_for('init'))  
    else:     
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['Emails']
        passw = request.form['Password']
        if validate(email,passw):
            return redirect(url_for('home'))
        else:
            return render_template('login.html')    
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('about.html')
    # return redirect(url_for('history'))

@app.route('/')
def init():
    return render_template('index.html')

@app.route('/api/users/<email>')
def apiCall(email):
    cursor = database.cursor()
    query = f'select password from users where email = "'+email+'"'
    cursor.execute(query)
    users = cursor.fetchall()
    # return str(users)
    if len(users)>0:
        return jsonify({'password':users[0][0]})
    return jsonify({'password':''})    


@app.route('/api/history')
def apiCallHistory():
    images = getDrones()
    for i in images:
        shutil.copy(i,'static/history')

    images = os.listdir('static/history/') 
    path =   'static/history/'
    final_imgs = []
    times = []
    for i in images:
        final_imgs.append(path+i)
        time = str(i).split('_')[1]
        # time = time[::-1]
        time = time[6:8]+'-'+time[4:6]+'-'+time[:4]+' '+time[8:10]+':'+time[10:12]
        times.append(time)
    # data = {"data":}
    data = []
    for i in range(len(final_imgs)):
        idata={}
        idata['img']='http://10.1.1.203:5000/'+final_imgs[i]
        idata['datetime']=times[i]
        data.append({str(i):idata})
    return jsonify({"data":data})    






if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
    # http://10.8.1.182:5000/