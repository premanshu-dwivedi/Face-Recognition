from django.urls import path
from .views import face_recognition_api_view

app_name = "recapi"
urlpatterns = [
    path('overview', face_recognition_api_view, name='api_overview'),
]
