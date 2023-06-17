from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User

from recapi.views import face_recognition_api_view

from recapi.serializers import UserProfileSerializer, UserProfile

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import cv2
import face_recognition
import os, sys
import numpy as np
import math

# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('C:/Python/FaceRecogProject/FaceRec/static/faces'):
            face_image = face_recognition.load_image_file(f"C:/Python/FaceRecogProject/FaceRec/static/faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)

        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Face Recognition (Press q to exit)', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        
        return str(name)
        
        



from templates_dirs.template_dirs import (
    home_page_template, detail_page_template,
    about_page_template,
)


def home_view(request):
    # RENDERS THE HOME PAGE ON REQUEST
    return render(request, home_page_template)


def detail_view(request, username):
    # Renders the suspects picture with text about the person after a succesful match
    username = get_object_or_404(User, username=username)
    user = UserProfile.objects.get(username=username)
    context = {"user": user}
    return render(request, detail_page_template, context=context)


def about_view(request):
    # Renders the about us page on request
    return render(request, about_page_template)


@api_view(['GET'])
def face_recognition_view(request):
    fr = FaceRecognition()
    suspect_name = fr.run_recognition()
    dot_index = suspect_name.index(".")
    suspect_name = suspect_name[0:dot_index]
    print(suspect_name)
    return redirect("recapp:detail_view", username=suspect_name)


@api_view(['GET'])
def detect_motion_view(request):
    video = cv2.VideoCapture(0)
    while video.isOpened():
        ret, frame = video.read()
        ret, frame2 = video.read()
        
        diff_frame = cv2.absdiff(frame, frame2) # CREATING DIFFERENCE OF THE TWO FRAME TO DETECT CHANGE IN FRAME
        gray = cv2.cvtColor(diff_frame, cv2.COLOR_RGB2GRAY) # CONVERTING FROM RGB TO GRAY
        
        blur = cv2.GaussianBlur(gray, (5, 5), 0) 
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY) #CONVERTING TO THRESHOLD WITH THRESHOLD VALUES AND TYPE
        
        dialeted = cv2.dilate(thresh, None, iterations=3) #DIALATE THE THRESHOLD VALUE AND HAVING THE KERNEL AS NONE
        contours, _ = cv2.findContours(dialeted, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #GETTING PART OF OBJECT MOVING AND DRAW ON IT
        # cv2.drawContours(frame, contours, -1, (0, 255, 0), 2) # Draw green color on the object moving
        
        # LOOP THROUGH CONTOURS (OBJECT PART) AND ONLY DETECT BIGER PART MOVING
        for contour in contours:
            if cv2.contourArea(contour) < 2000:
                continue
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        cv2.imshow("Capturing", frame)
        
        if cv2.waitKey(10)  == ord('q') or cv2.waitKey(10) == ord('Q'):
            break
    cv2.destroyAllWindows()
    
    data = {'Function': "Motion Detection"}
    return Response(data=data, status=status.HTTP_200_OK)