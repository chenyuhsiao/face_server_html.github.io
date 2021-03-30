from flask import Flask
#網頁傳值用套件
from werkzeug.utils import secure_filename
from flask import Flask, render_template, jsonify, request, make_response, send_from_directory, abort,redirect, url_for
import os
from PIL import Image 
#臉部辨識套件
import face_recognition
import cv2
import numpy as np

#臉部辨識程式
face_encoding_list=[]
known_face_name=[]
#biden_img = face_recognition.load_image_file("biden.jpg")
#obama_img = face_recognition.load_image_file("obama.jpg")
#brian_img = face_recognition.load_image_file("brian.jpg")
#trump_img = face_recognition.load_image_file("trump.jpg")
#biden_encoding = face_recognition.face_encodings(biden_img)[0]
#obama_encoding = face_recognition.face_encodings(obama_img)[0]
#brian_encoding = face_recognition.face_encodings(brian_img)[0]
#trump_encoding = face_recognition.face_encodings(trump_img)[0]
#face_encoding_list=[biden_encoding,obama_encoding,brian_encoding,trump_encoding]
#known_face_name=["biden","obama","brian","trump"]

#np.save("data_encoding",face_encoding_list,allow_pickle=True, fix_imports=True)
#np.load("data_encoding.npy")
face_encoding_list=np.load("data_encoding.npy")

#np.save("data_name",known_face_name,allow_pickle=True, fix_imports=True)
#np.load("data_name.npy")
known_face_name=np.load("data_name.npy")

#網站圖片儲存位置
UPLOAD_FOLDER = '/Users/chenyuxiao/Desktop/app1_server'
RECOGNIZE_FLODER='/Users/chenyuxiao/Desktop/app1_server'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif'])

#網站程式
app=Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RECOGNIZE_FLODER'] = RECOGNIZE_FLODER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

basedir = os.path.abspath(os.path.dirname(__file__))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():

    return render_template('server_face_recognition.html')
#upload_pic
@app.route('/upload_pic', methods=['GET','POST'])
def upload_pic():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename ="test.jpeg" #secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #if request.values['upload']=='上傳圖片':
            #name2=request.values["user"]

    return render_template('server_face_recognition.html',name1=request.values["user"])

@app.route('/recognize_pic', methods=['GET', 'POST'])
def recognize_pic():
    if request.method=="POST":
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename ="test.jpeg" #secure_filename(file.filename)
            file.save(os.path.join(app.config['RECOGNIZE_FLODER'], filename))

#臉部辨識程式
    unknown_img = face_recognition.load_image_file("test.jpeg")
    unknown_face_locations = face_recognition.face_locations(unknown_img) 
    location_count=len(unknown_face_locations)
    print("圖片中總共有",location_count,"張臉")

    save_count=0
    output_name=[]

#儲存圖片中每一個臉
    for face_location in unknown_face_locations:
        top, right, bottom, left = face_location  
        #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))    
        face_image = unknown_img[top:bottom, left:right]  
        pil_image = Image.fromarray(face_image)  
        #pil_image.show()

        save_count=save_count+1
        save_name="test"+str(save_count)+".jpeg"
        pil_image.save(save_name)

#針對每個臉做compare
        image=face_recognition.load_image_file(save_name)
        unknown_face_encoding=face_recognition.face_encodings(image)[0]
        results=face_recognition.compare_faces(face_encoding_list,unknown_face_encoding)
        #print(results)

#標示人名:
        if str(results[0])=="True":
            output_name.append("Biden")
        #else:
            #output_name.append("unknown")
        if str(results[1])=="True":
            output_name.append("Obama")
        #else:
            #output_name.append("unknown")
        if str(results[2])=="True":
            output_name.append("trump")

        #else:
            #output_name.append("unknown")

    #unknown_face_encoding = face_recognition.face_encodings(unknown_img)[0]
    #results = face_recognition.face_distance(face_encoding_list,unknown_face_encoding)

    #march=0
    #output1=[]
   # p=0
   # for (i, r) in enumerate(results):
        #if r==0:
            #march=100
            #output1=[known_face_name[i]]
            #output1.append(known_face_name[i])
        #else:
            #p=100-round(r*100)
            #if p>march:
                #march=p
                #if march>=0:
                    #output1=[known_face_name[i]]
                    #output1.append(known_face_name[i])

    return render_template('server_face_recognition.html',output=output_name)

    #return render_template('index.html',name1=request.values["user"])
      #      return redirect(url_for('recognize',filename=filename))

if __name__=="__main__":

    app.run(debug=True,port=8000)

