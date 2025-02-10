from django.urls import path
from api.views import DoctorAPIView, NewsAPIView,DoctorFilterView,RegisterAPIView,LoginAPIView,DoctorUpdateApiView,UserUpdateAPIView,BookingAPIView,DoctorDateAPIView

urlpatterns = [
    path('doctor', DoctorAPIView.as_view(), name='doctors-list'),
    path("date/", DoctorDateAPIView.as_view(), name="doctors"),
    path("booking/<int:pk>/", BookingAPIView.as_view(), name="booking"),
    path('doctor/update/<int:pk>',DoctorUpdateApiView.as_view(), name='doctors-update'),
    path('user/update<int:pk>',UserUpdateAPIView.as_view(), name='users-list'),
    path('login', LoginAPIView.as_view(), name='login'),
    path('register', RegisterAPIView.as_view(), name='doctors-register'),
    path('news', NewsAPIView.as_view(), name='news-list'),
    path('search', DoctorFilterView.as_view(), name='search-list'),
    path('news/<int:pk>', NewsAPIView.as_view(), name='news-detail'),
    path('doctor/<int:pk>', DoctorAPIView.as_view(), name='doctors-detail'),
]


