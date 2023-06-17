from django.urls import path 
from .views import (
    home_view, detail_view,
    about_view, face_recognition_view,
    detect_motion_view,
)

app_name = "recapp"
urlpatterns = [
    path("", home_view, name="home_view"),
    path("suspect-detail/<str:username>/", detail_view, name="detail_view"),
    path("about-us/", about_view, name="about_view"),
    path("face-recognition/", face_recognition_view, name="face_recognition_view"),
    path("motion-detection/", detect_motion_view, name="detect_motion_view"),
]
