# Face-Recognition
# Face-recognition
This is a face reognition project that uses opencv, face_recogntion python framework , django and it's components to match human and detect faces.

#STeps on how to run the app on your computer

##Download the github repo
## ensure you have python and pip installed on your computer
## run pip install -r requirements.txt
## if it's inatlled under vitual env, ensure to activate it
## locate the directory with manage.py
## run mange.py runserver
## you can click on facerecogtion to recognize faces and detect for motion detection

## Visit the url http://127.0.0.1:8000/admin (8000) depends on your port number
## enter the username and password as 'admin', 'command22' respectively
or you can create your own admin with python manage.py createsuperuser and enter your credentials
## go to users in the admin dashboard and create a user
## then go to userprofiles in the admin dashboard and enter the informtion of the user and save it with the known face(picture) you want to recognize
## Then got to http://127.0.0.1:8000 and click on recognition
## place your face on the camera and press 'q' once it detects your face
