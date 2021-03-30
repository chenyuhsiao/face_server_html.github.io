import numpy as np
import face_recognition
from PIL import Image 

face_encoding_list=[]
known_face_name=[]
biden_img = face_recognition.load_image_file("biden.jpeg")
obama_img = face_recognition.load_image_file("obama.jpeg")
trump_img = face_recognition.load_image_file("trump.jpeg")
brian_img = face_recognition.load_image_file("brian.jpeg")
#hongjun_img=face_recognition.load_image_file("hongjun.jpg")
#xuguiru_img=face_recognition.load_image_file("xuguiru.jpg")
biden_encoding = face_recognition.face_encodings(biden_img)[0]
obama_encoding = face_recognition.face_encodings(obama_img)[0]
brian_encoding = face_recognition.face_encodings(brian_img)[0]
trump_encoding = face_recognition.face_encodings(trump_img)[0]
#hongjun_encoding = face_recognition.face_encodings(hongjun_img)[0]
#xuguiru_encoding = face_recognition.face_encodings(xuguiru_img)[0]

face_encoding_list=[biden_encoding,obama_encoding,trump_encoding]
known_face_name=["biden","obama","trump","brian"]

#file=open("data_encoding.txt",mode="w",encoding="utf-8")
#file.write(str(face_encoding_list))
#file.close()

#file=open("data_name.txt",mode="w",encoding="utf-8")
#file.write(str(known_face_name))
#file.close()

#with open ("data_encoding.txt",mode="r",encoding="utf-8")as file:
#    data_encoding=file.read()
#    k=file.readlines()
#print(k)
#face_encoding_list=data_encoding
#print(face_encoding_list)

#with open ("data_name.txt",mode="r",encoding="utf-8")as file:
 #   data_name=file.read()
#known_face_name=data_name
last=len(face_encoding_list)
np.save("data_encoding",face_encoding_list,allow_pickle=True, fix_imports=True)
np.load("data_encoding.npy")
data_encoding=np.load("data_encoding.npy")
print(data_encoding[last-1])

np.save("data_name",known_face_name,allow_pickle=True, fix_imports=True)
np.load("data_name.npy")
data_name=np.load("data_name.npy")
print(data_name[last-1])