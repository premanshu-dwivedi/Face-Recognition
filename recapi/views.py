from django.shortcuts import render,get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .serializers import UserProfileSerializer
from .models import UserProfile

import cv2


@api_view(["GET"])
def face_recognition_api_view(request):
    video = cv2.VideoCapture(0)
    
    while(True):
        ret, frame = video.read()
        cv2.imshow("Capturing", frame)
        
        if cv2.waitKey(1) & 0XFF == ord('1'):
            break
    cv2.release()
    cv2.destroyAllWindows()
    
    data = {'working': True}
    return Response(data=data, status=status.HTTP_200_OK)





