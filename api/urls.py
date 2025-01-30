from re import search

from django.urls import path
from api.views import DoctorAPIView, NewsAPIView,DoctorFilterView,RegisterAPIView,LoginAPIView

urlpatterns = [
    path('doctor', DoctorAPIView.as_view(), name='doctors-list'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='doctors-register'),
    path('news', NewsAPIView.as_view(), name='news-list'),
    path('search', DoctorFilterView.as_view(), name='search-list'),
    path('news/<int:pk>', NewsAPIView.as_view(), name='news-detail'),
    path('doctor/<int:pk>', DoctorAPIView.as_view(), name='doctors-detail'),
]


