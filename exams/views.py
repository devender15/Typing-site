from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

from .models import *
from Room.models import Room
from Room.serializers import RoomSerializer

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

        if (isAdmin or isTeacher):
            exam_name = request.data.get('exam_name')

            # checking if the exam already exists or not
            isExist = Exams.objects.filter(name=exam_name).exists()

            if (not isExist):
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

        if (isAdmin or isTeacher):
            # getting data from frontend
            test_name = request.data.get("test_name")
            exam_id = request.data.get("exam_id")
            language = request.data.get("language")
            teacher = request.user.fname
            institute = request.user.institute

            # checking whether test already exists or not
            isExists = Tests.objects.filter(name=test_name).exists()

            if (isExists):
                return Response({"error": "This test already exists!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                # filtering out in which exam we have to set this test
                exam = Exams.objects.get(id=exam_id)

                # saving all the data in the database
                test = Tests(name=test_name, language=language,
                             teacher=teacher, institute=institute, exam=exam)
                test.save()

                return Response({"success": "Test added successfully!"}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Only admin and teacher are authorized to do this action!"}, status=status.HTTP_401_UNAUTHORIZED)


class GetLiveTests(APIView):

    permission_classes = [AllowAny]
    serializer_class = RoomSerializer

    def get(self, request, test_id):

        rooms = Room.objects.filter(test_id=test_id)
        if (len(rooms) > 0):
            serializer = self.serializer_class(rooms, many=True)
            unexpired_rooms = [
                room for room in serializer.data if not room['isExpired']]
            return Response(unexpired_rooms, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No test is live!"}, status=status.HTTP_200_OK)


class Rate(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        # checking if the user is student or not
        isStudent = not request.user.is_staff and not request.user.is_superuser

        if (isStudent):
            user = request.user
            exam_id = int(request.data.get("exam"))
            filtered_exam = Exams.objects.get(id=exam_id)

            already_users = [] if not isinstance(filtered_exam.user_rated, list) else filtered_exam.user_rated

            # checking whether this user has already rated this exam or not

            if (user.id in already_users):
                return Response({"error": "You have already gave rating to this exam!"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                user_ratings = request.data.get("ratings")

                exam = Exams.objects.get(id=exam_id)
                already_users.append(user.id)
                exam.user_rated = already_users

                # we have to add average ratings to the exam
                ratings_arr = [] if exam.ratings == 0 else exam.ratings
                ratings_arr.append(user_ratings)
                average_rating = sum(ratings_arr) / len(ratings_arr)
                exam.rating = average_rating
                exam.ratings = ratings_arr
                exam.save(update_fields=['user_rated', 'ratings', 'rating'])

                return Response({"success": "Rating added successfully!"}, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Only student is authorized to do this action!"}, status=status.HTTP_401_UNAUTHORIZED)


class CheckRated(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, exam_id):

        try:
            exam = Exams.objects.get(id=exam_id)
            user = request.user.id

            already_rated = [] if not isinstance(exam.user_rated, list) else exam.user_rated 
            
            if (user in already_rated):
                return Response({"success": "You have already rated this exam!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "You have not rated this exam!"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
