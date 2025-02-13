#pip3 install opencv-contrib-python
import imghdr
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sklearn.preprocessing import LabelEncoder
from flask import Flask,render_template,request,redirect,url_for,flash,session
import numpy as np
import mysql.connector
import cv2,os
import pandas as pd
from PIL import Image
import datetime
import time
import math
import pickle
import requests
import csv


app=Flask(__name__)
app.config['SECRET_KEY']='Missing Person'
db = mysql.connector.connect(host="localhost", user="root", passwd="", database="missing_child", port=3306)
cur = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login1')
def login1():
    return render_template('login1.html')

@app.route('/admin_home',methods=["POST","GET"])
def admin_home():
    if request.method=='POST':
        useremail=request.form['useremail']
        session['useremail']=useremail
        userpasword = request.form['userpassword']

        if useremail == 'admin@gmail.com' and userpasword =="admin":
            msg = 'Login Successfull !!!!'
            return render_template('admin_home.html',name=msg)
        else:
            msg = 'Invalid Credentials'
            return render_template('login1.html', name = msg)
    return render_template('login1.html')

@app.route('/addpolice',methods=["POST","GET"])
def addpolice():
    if request.method=='POST':
        username=request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        email = request.form['email']
        sid = request.form['sid']

        sql="select * from police_station where station_id='%s' "%(sid)
        cur.execute(sql)
        data=cur.fetchall()
        db.commit()
        print(data)
        if data==[]:
                
            sql = "insert into police_station(station_id,station_name,contact_number,email,address)values(%s,%s,%s,%s,%s)"
            val=(sid,username,contact,email,address)
            cur.execute(sql,val)
            db.commit()
            flash(" User Added Successfully","success")
            return render_template("addpolice.html")
        else:
            flash("Details already Exists","warning")
            return render_template("addpolice.html")

    return render_template('addpolice.html')
@app.route('/view_station_details')
def view_station_details():
    sql="select * from police_station"
    cur.execute(sql, db)
    data=cur.fetchall()
    db.commit()
    return render_template('view_station_details.html',data=data)
@app.route('/updatedata/<id>',methods=['POST','GET'])
def updatedata(id=0):
    sql="select * from police_station where id='"+id+"'"
    cur.execute(sql)
    data=cur.fetchall()
    return render_template('updatedata.html',data=data)

@app.route('/updateback',methods=['POST'])
def updateback():
    if request.method=='POST':
        username = request.form['name']
        contact = request.form['contact']
        address = request.form['address']
        sid = request.form['sid']
        id=request.form['id']

        sq="update police_station set station_id='"+sid+"',station_name='"+username+"',contact_number='"+contact+"', address='"+address+"' where id='"+id+"'"
        cur.execute(sq,db)
        db.commit()
        flash("Data updated successfully","success")
        return redirect(url_for('view_station_details'))
@app.route('/delete_data/<id>',methods=['POST'])
def delete_data(id=0):
    sql="delete from police_station where id='"+id+"'"
    cur.execute(sql,db)
    db.commit()
    flash("Data deleted successfully", "success")
    return redirect(url_for('view_station_details'))

@app.route("/addface", methods=['POST','GET'])
def addface():
    if request.method=='POST':
        Id=request.form['id']
        name=request.form['name']
        pname=request.form['pname']
        contact = request.form['contact']
        address = request.form['address']

        cam = cv2.VideoCapture(0)
        harcascadePath = "Haarcascade/haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        sampleNum = 0
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        # incrementing sample number
                sampleNum = sampleNum + 1
                        # saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage/ " + name + "." + Id + '.' + str(
                            sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                        # display the frame

            else:
                cv2.imshow('frame', img)
                    # wait for 100 miliseconds
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
                    # break if the sample number is morethan 100
            elif sampleNum > 150:
                    break

        cam.release()
        cv2.destroyAllWindows()
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        sq="insert into missing_child_data(child_id,child_name,parent_name,parent_number,address,date,time) values(%s,%s,%s,%s,%s,%s,%s)"
        val=(Id,name,pname,contact,address,date,timeStamp)
        cur.execute(sq,val)
        db.commit()
        flash("Data added successfully","success")
        return render_template("addface.html")
    s="select count(*) from missing_child_data"
    ss=pd.read_sql_query(s,db)
    count=ss.values[0][0]
    if count==0:
        return render_template('addface.html',data='MSID1')
    else:
        s1="select child_id from missing_child_data ORDER BY ID DESC LIMIT 1"
        ss1=pd.read_sql_query(s1,db)
        cid=str(ss1.values[0][0])
        text = ""
        numbers = ""
        digits = "0123456789"
        res = []
        for i in cid:
            if (i in digits):
                numbers += i
            else:
                text += i
        res.append(text)
        res.append(numbers)
        res=int(res[1])+1
        cid_number="MSID"+str(res)
    return render_template("addface.html", data=cid_number)
def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        print(imagePath)
        if imagePath == "TrainingImage\Thumbs.db":
            continue;
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = str(os.path.split(imagePath)[-1].split(".")[1])
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids

@app.route('/train')
def train():
    le = LabelEncoder()
    faces, Id = getImagesAndLabels("TrainingImage")
    Id = le.fit_transform(Id)
    output = open('label_encoder.pkl', 'wb')
    pickle.dump(le, output)
    output.close()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(Id))
    recognizer.save(r"Trained_Model\Trainner.yml")

    flash("Model Trained Successfully", "success")
    return redirect(url_for('addface'))
@app.route('/trackface')
def trackface():
    return render_template('trackface.html')

@app.route("/trackImages")
def trackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read(r"Trained_Model\Trainner.yml")
    harcascadePath = r"Haarcascade\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    global cam
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    pkl_file = open('label_encoder.pkl', 'rb')
    le = pickle.load(pkl_file)
    pkl_file.close()
    global tt
    count = []
    flag = 0
    det = 0
    global val_data, global_stop
    global_stop = False
    import datetime
    import time
    while True:
        _, frame = cam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            print(conf)
            if (conf < 50):
                det += 1
                print(det)
                tt = le.inverse_transform([Id])
                tt=str(tt[0])
                sq = "select child_name,parent_name,parent_number from missing_child_data where child_id='" + tt + "'"
                xx = pd.read_sql_query(sq, db)
                cname = str(xx.values[0][0])
                pname = str(xx.values[0][1])
                pnumber = str(xx.values[0][2])
                if det==10:
                    sql1 = "select * from police_station"
                    x1 = pd.read_sql_query(sql1, db)
                    pno = x1['email'].values
                    import random
                    arr = np.array(pno)
                    email = arr.tolist()
                    secure_random = random.SystemRandom()
                    email = secure_random.choice(email)
                    print(email)
                    nn=random.randint(0,100)
                    noOfFile = str(tt)+str(nn)+'.jpg'
                    print(type(noOfFile))

                    cv2.imwrite("static/Missing_Child/"+ noOfFile, frame[y:y + h, x:x + w])

                    ts = time.time()
                    date1 = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

                    sql="insert into child_identification_data(child_id,child_name,parent_name,parent_number,date,time,station_email,photo) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                    val=(tt,cname,pname,pnumber,date1,timeStamp,email,noOfFile)
                    cur.execute(sql,val)
                    db.commit()
                    msg = 'Dear Sir,'
                    m = 'We have captured a missing child face and the child id is '
                    dt = "Detected on "
                    tm= 'at '
                    im = "Kindly have a look on the attached photo and take necessary actions. "
                    t = 'Regards,'
                    t1 = 'Missing Child Identification Center.'
                    mail_content = msg + ',' + '\n' + m + ' ' + str(tt) +'.'+ dt +  date1 + tm + timeStamp + '.' + im + '\n' + '\n' + t + '\n' + t1
                    sender_address = 'usha96760@gmail.com'
                    sender_pass = 'ralucuegcicsvern'
                    receiver_address = 'usha96760@gmail.com'
                    message = MIMEMultipart()
                    message['From'] = sender_address
                    message['To'] = receiver_address
                    message['Subject'] = 'Missing Child Recognition System'
                    message.attach(MIMEText(mail_content, 'plain'))
                    ses = smtplib.SMTP('smtp.gmail.com', 587)
                    ses.starttls()
                    ses.login(sender_address, sender_pass)
                    text = message.as_string()
                    ses.sendmail(sender_address, receiver_address, text)
                    ses.quit()
                    #
                    newMessage = EmailMessage()
                    newMessage['Subject'] = "Missing Child Recognition System"
                    newMessage['From'] = sender_address
                    newMessage['To'] = receiver_address
                    newMessage.set_content(
                        'We have captured a missing child face')
                    
                    with open('static/Missing_Child/'+noOfFile, 'rb') as f:
                        image_data = f.read()
                        image_type = imghdr.what(f.name)
                        image_name = f.name
                    
                    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
                    
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                        smtp.login(sender_address, sender_pass)
                        smtp.send_message(newMessage)
                    
                    # url = "https://www.fast2sms.com/dev/bulkV2"
                    # print(url)
                    # m2 = 'We have captured your child face and the child id is '
                    
                    # mail_content = 'Dear ' + pname+  ',' + '\n' + m2 + ' ' + str(tt) + '.' + dt + date + tm + timeStamp + '.' + im + '\n' + '\n' + t + '\n' + t1
                    # no = pnumber
                    # data = {
                    #     "route": "q",
                    #     "message": mail_content,
                    #     "language": "english",
                    #     "flash": 0,
                    #     "numbers": no,
                    # }
                    
                    # headers = {
                    #     "authorization": "9qXilM8snkgvUPYaBDWISdfEO67ZVAtru5GFTmRexhQCL1jpJH2r8GPja9NTuZhQ7wMI5YdgSxOWyAUB",
                    #     "Content-Type": "application/json"
                    # }
                    # response = requests.post(url, headers=headers, json=data)
                    # print(response)
                    det = 0
                    break
            else:
                cname='Normal'

            cv2.putText(frame,str(cname), (x, y + h),font, 1, (255, 255, 255), 2)
           
        cv2.imshow('im', frame)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    return render_template("index.html")




@app.route('/history')
def history():
    sql="select * from child_identification_data"
    cur.execute(sql,db)
    data=cur.fetchall()
    return render_template('history.html',data=data)

if __name__=='__main__':
    app.run(debug=True)

