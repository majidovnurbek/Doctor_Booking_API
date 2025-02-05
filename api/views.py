from api.models import Doctor, News, User
from api.serializers import DoctorSerializer, NewsSerializer, RegisterSerializer,LoginSerializer,DoctorUpdateSerializer,UserUpdateSerializer
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser




class DoctorAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
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

class DoctorUpdateApiView(APIView):
    # permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Doctor Update",
        description="Doctor update data",
        request=DoctorUpdateSerializer,  # Specify request body fields
        responses={
            200: OpenApiParameter(name="Update", description="Doctor update data"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials or validation errors"),
        },
        tags=["Doctor Update"]
    )
    def put(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorUpdateSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=400)




class NewsAPIView(APIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]
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


class LoginAPIView(APIView):
    throttle_classes = [AnonRateThrottle,UserRateThrottle]

    @extend_schema(
        summary='User login',
        description='Login useing email and password',
        request=LoginSerializer,
        responses={
            200: OpenApiParameter(name="Token",description='Get token'),
            400: OpenApiParameter(name="errors",description='Get token'),
        },
        tags=['Login autication'],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user=User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    return Response({'error': 'User is inactive'}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({'refresh': str(refresh), 'access': str(access_token)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        summary="User Registration",
        description="Register user",
        request=UserUpdateSerializer,
        responses={
            200: OpenApiParameter(name="User Updated", description="User data updated"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials")
        },
        tags=["User Update"]
    )
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserUpdateSerializer(instance=user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
