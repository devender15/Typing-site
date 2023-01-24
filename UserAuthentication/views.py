from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from .renderers import UserJsonRenderer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import check_password

from .models import Performance

User = get_user_model()

# generate token manually


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


class ListUsers(ListAPIView):
    queryset = User.objects.all()
    serializer_class = [UserSerializer]
    permission_classes = [IsAuthenticated]


class RegisterUser(APIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    renderer_classes = [UserJsonRenderer]

    def post(self, request, *args, **kwargs):

        # print(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({
            "user": serializer.data,
            "token": token,
            "message": "Account successfully created !"
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    serializer_class = LoginSerializer
    renderer_classes = [UserJsonRenderer]
    permission_classes = [AllowAny]

    def authenticate_user(self, email, password):
        user = authenticate(email=email, password=password)
        if (user is not None):
            token = get_tokens_for_user(user)
            return Response({'token': token, 'success': 'Login Successfull !'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': {'non_field_errors': 'Username or password is not valid !'}}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        role = serializer.data.get('role')

        filtered_user = User.objects.get(email=email)

        if (role == "admin"):
            if (filtered_user.is_superuser):
                return self.authenticate_user(email, password)
            else:
                return Response({"error": "This user is not an admin!"}, status=status.HTTP_401_UNAUTHORIZED)

        if (role == "teacher"):
            if (not filtered_user.is_superuser and filtered_user.is_staff):
                return self.authenticate_user(email, password)
            else:
                return Response({"error": "This user is not teacher!"}, status=status.HTTP_401_UNAUTHORIZED)

        if (role == "student"):
            if (not filtered_user.is_superuser and not filtered_user.is_staff):
                return self.authenticate_user(email, password)
            else:
                return Response({"error": "This user is not student!"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({"error": "Something is wrong!"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    renderer_classes = [UserJsonRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserDetails(APIView):
    renderer_classes = [UserJsonRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        userActualPassword = request.user.password
        userId = request.data.get('userId')
        email = request.data.get('email')
        fname = request.data.get('fname')
        phone = request.data.get('phone')
        password = request.data.get('password')

        match = check_password(password, userActualPassword)

        if (match):
            user = User.objects.get(id=userId)
            user.email = email
            user.fname = fname
            user.phone = phone
            user.save()

            return Response({'status': 'success', 'msg': 'Successfully details updated !'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': 'Invalid password entered!'}, status=status.HTTP_401_UNAUTHORIZED)


class UpdatePassword(APIView):
    renderer_classes = [UserJsonRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        userActualPassword = request.user.password
        oldPassEntered = request.data.get('oldPass')
        userId = request.data.get('userId')

        match = check_password(oldPassEntered, userActualPassword)

        if (match):
            newPassword = request.data.get('newPass1')
            user = User.objects.get(id=userId)
            user.set_password(newPassword)
            user.save()
            return Response({'status': 'success', 'msg': 'Successfully password updated !'}, status=status.HTTP_201_CREATED)

        else:
            return Response({'status': 'error', 'msg': 'Invalid password entered!'}, status=status.HTTP_401_UNAUTHORIZED)


class SaveProgress(APIView):
    renderer_classes = [UserJsonRenderer]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        user = User.objects.get(id=request.user.id)
        room = request.user.room
        wpm = request.data.get('wpm', 0)
        cpm = request.data.get('cpm', 0)
        accuracy = request.data.get('accuracy', 0)
        half_mistakes = request.data.get('half_mistakes', 0)
        full_mistakes = request.data.get('full_mistakes', 0)
        errors = request.data.get('errors', 0)
        time_taken = request.data.get('time_taken', 0)

        # saving the perform to the database
        performance = Performance(student=user, room=room, wpm=wpm, cpm=cpm, accuracy=accuracy,
                                  half_mistakes=half_mistakes, full_mistakes=full_mistakes, errors=errors, time_taken=time_taken)
        performance.save()

        return Response({'success': 'Successfully progress saved !'}, status=status.HTTP_201_CREATED)


class ViewProgress(ListAPIView):
    serializer_class = PerformanceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            performances = Performance.objects.filter(
                student=user).order_by('-id')
            serializer = PerformanceSerializer(performances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'status': 'Something went wrong !'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
