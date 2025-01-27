from api.models import Doctor, News
from api.serializers import DoctorSerializer, NewsSerializer, RegisterSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_simplejwt.tokens import RefreshToken


class DoctorAPIView(APIView):

    throttle_classes = [AnonRateThrottle]
    def get(self, request, pk=None):
        if pk:
            try:
                doctor = Doctor.objects.get(pk=pk)
                serializer = DoctorSerializer(doctor)
                return Response(serializer.data)
            except:
                return Response({'error': 'Doctor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            doctor = Doctor.objects.all()
            serializer = DoctorSerializer(doctor, many=True)
            return Response(serializer.data)


class NewsAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                news = News.objects.get(pk=pk)
                serializer = NewsSerializer(news)
                return Response(serializer.data)
            except:
                return Response({'error': 'News does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            news = News.objects.all()
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)


class DoctorFilterView(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['location', 'clinic_name']
    filterset_fields = ['experience', 'rating_percentage', 'location', 'cunsultation_fee']


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            # Generate jwt

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                    'refresh': str(refresh),
                    'access': access_token,
                    'username': serializer.data
                }, status=status.HTTP_201_CREATED
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
