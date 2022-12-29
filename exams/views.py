from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *

# Create your views here.

class ListExams(ListAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]

class ListTests(ListAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [AllowAny]


class AddExam(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # checking if the user is admin or not
        isAdmin = request.user.is_superuser
        isTeacher = request.user.is_staff and not isAdmin

        # print(request.data)

        if(isAdmin or isTeacher):
            exam_name = request.data.get('exam_name')

            # checking if the exam already exists or not
            isExist = Exams.objects.filter(name=exam_name).exists()

            if(not isExist):
                exam = Exams(name=exam_name)
                exam.save()
                return Response({"success": "Exam added successfully!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "This exam already exists!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"error": "Only admin and teacher are authorized to do this action!"}, status=status.HTTP_401_UNAUTHORIZED)


class AddTest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        isAdmin = request.user.is_superuser
        isTeacher = request.user.is_staff and not isAdmin

        if(isAdmin or isTeacher):
            # getting data from frontend
            test_name = request.data.get("test_name")
            exam_id = request.data.get("exam_id")
            language = request.data.get("language")
            teacher = request.user.fname
            institute = request.user.institute

            # checking whether test already exists or not
            isExists = Tests.objects.filter(name=test_name).exists()

            if(isExists):
                return Response({"error": "This test already exists!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # filtering out in which exam we have to set this test
                exam = Exams.objects.get(id=exam_id)

                # saving all the data in the database
                test = Tests(name=test_name, language=language, teacher=teacher, institute=institute, exam=exam)
                test.save()

                return Response({"success": "Test added successfully!"}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Only admin and teacher are authorized to do this action!"}, status=status.HTTP_401_UNAUTHORIZED)
