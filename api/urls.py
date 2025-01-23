from django.urls import path
from api.views import DoctorAPIView, NewsAPIView

urlpatterns = [
    path('doctor', DoctorAPIView.as_view(), name='doctors-list'),
    path('news', NewsAPIView.as_view(), name='news-list'),
    path('news/<int:pk>', NewsAPIView.as_view(), name='news-detail'),
    path('doctor/<int:pk>', DoctorAPIView.as_view(), name='doctors-detail'),
]
