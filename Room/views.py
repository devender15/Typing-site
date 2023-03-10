from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q


from .serializers import *
from .models import *
from UserAuthentication.models import Performance
from exams.models import Tests, Exams


# User model
User = get_user_model()

# Create your views here.


class RoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        isTeacher = not request.user.is_superuser and request.user.is_staff

        if (isTeacher):

            serializer = self.serializer_class(data=request.data)
            user = User.objects.get(email=request.user.email)

            if (serializer.is_valid()):
                exam = serializer.data.get('exam')
                test = serializer.data.get('test_name')
                time = serializer.data.get('time')
                paragraph = serializer.data.get('paragraph')
                criteria = serializer.data.get('criteria')
                paragraphText = serializer.data.get('paragraphText')
                host = request.user.fname

                print(paragraphText)

                # getting test_id from Tests model
                test_id = Tests.objects.get(name=test).id

                # writing data to Room model
                room = Room(host=host, exam=exam, test_name=test, test_id=test_id, time=time,
                            paragraph=paragraph, criteria=criteria, paragraphText=paragraphText)
                room.save()
                # saving room property in user's data
                user.room = room
                user.save(update_fields=['room'])

                # changing the LIVE property of that particular test
                test_queryset = Tests.objects.get(name=test)
                live_val = test_queryset.live
                live_val += 1
                test_queryset.live = live_val
                test_queryset.save(update_fields=['live'])

                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'Bad Request': 'Only Teacher can access this resource'}, status=status.HTTP_401_UNAUTHORIZED)


class GetRoom(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = RoomSerializer
    lookup_url_kwargs = 'code'

    def get(self, request, format=None):

        code = request.GET.get(self.lookup_url_kwargs)
        if (code != None):
            room = Room.objects.filter(code=code)
            if (len(room) > 0):
                data = self.serializer_class(room[0]).data
                data['is_host'] = request.user.fname == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_url_kwargs = 'code'

    def post(self, request, format=None):

        code = request.data.get(self.lookup_url_kwargs)
        user = User.objects.get(email=request.user.email)

        if (code != None):
            room_result = Room.objects.filter(code=code)

            if (len(room_result) > 0):
                room = room_result[0]
                participants = room.participants
                user.room = room
                user.save(update_fields=['room'])

                # incrementing the participants count
                participants += 1
                room.participants = participants
                room.save(update_fields=['participants'])

                # incrementing the exam attempts
                exam = Exams.objects.get(id=room.exam)
                old_attempts = exam.attempts 
                exam.attempts = old_attempts + 1
                exam.save(update_fields=['attempts'])

                return Response({'message': 'Room joined !'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room code !'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'bad request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        user = User.objects.get(email=request.user.email)

        data = {
            "code": user.room.code if user.room != None else None
        }

        return Response(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):

        user = User.objects.get(email=request.user.email)
        room_id = user.room.id

        if (user.room != None):
            user.room = None
            user.save(update_fields=['room'])

            # updating the participants field in Room
            room = Room.objects.get(id=room_id)
            participants = room.participants
            participants -= 1
            room.participants = participants
            room.save(update_fields=['participants'])

            # now checking if the user is host or not, if yes then we have to delete the room
            host_id = request.user.fname
            room_results = Room.objects.filter(host=host_id)
            if (len(room_results) > 0):

                room = room_results.last()  # always get the latest queryset
                room.isExpired = True
                room.save(update_fields=['isExpired'])

                # changing the LIVE property of that particular test
                test_queryset = Tests.objects.get(id=room.test_id)
                live_val = test_queryset.live
                live_val -= 1
                test_queryset.live = 0 if (live_val < 0) else live_val
                test_queryset.save(update_fields=['live'])

            return Response({'success': 'Leaved room successfully!'}, status=status.HTTP_200_OK)
        return Response({'error': 'You are not in any room!'}, status=status.HTTP_404_NOT_FOUND)


class ViewAllPerformances(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, roomId):
        user = User.objects.get(email=request.user.email)
        if (user.is_superuser or user.is_staff):
            performances = Performance.objects.filter(room=roomId)

            records = []
            for performance in performances:

                # converting our django model instance to standard python dictionary first
                old_data = {**performance.__dict__}
                # removing the state property from the dictionary
                del old_data['_state']

                student_data = {"student": {"name": performance.student.fname, "email": performance.student.email,
                                            "phone": performance.student.phone, "institute": performance.student.institute, "board": performance.student.board}}

                # joining two dictionaries together and then pushing to records array
                records.append(old_data | student_data)

            return JsonResponse(records, safe=False, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Only Teacher and Admin are authorized to perform this operation!'}, status=status.HTTP_400_BAD_REQUEST)


class GetRank(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.get(email=request.user.email)
        room = user.room
        print(room.code)
        if (room != None):
            performances = Performance.objects.filter(room=room.id)
            performances = sorted(
                performances, key=lambda x: x.wpm, reverse=True)
            rank = 1
            for performance in performances:
                
                # filtering out same user if he/she enters more than one time
                one_type = Performance.objects.filter(Q(room=room.id) & Q(student=user.id)).latest('recorded_at')
                # matching the current user and checking if the recorded_at is latest or not
                if (performance.student.email == user.email and performance.recorded_at == one_type.recorded_at):
                    # saving the rank to the user's performance object
                    # in case multiple object returns, so we are catching that exception
                    try:
                        performer = Performance.objects.get(student=user.id)
                    except MultipleObjectsReturned:
                        performer = Performance.objects.filter(
                            student=user.id).last()
                    performer.rank = rank
                    performer.save(update_fields=['rank'])
    
                    # if the current user is not the topper then sending topper's details
                    if (rank != 1):
                        topper = performances[0]
                        return Response({"rank": rank, "topper": {"name": topper.student.fname, "wpm": topper.wpm, "errors": topper.errors, "accuracy": topper.accuracy, "time_taken": topper.time_taken}}, status=status.HTTP_200_OK)
                    
                    return Response({"rank": rank}, status=status.HTTP_200_OK)

                rank += 1

            # saving the rank to the user's performance object
            performer = Performance.objects.filter(student=user.id)
            performer.rank = rank
            performer.save(update_fields=['rank'])

            return Response({"rank": "Not Found"}, status=status.HTTP_200_OK)
        return Response({"rank": "Not Found"}, status=status.HTTP_200_OK)


class LiveRoom(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RoomSerializer

    def get(self, request, format=None):
        user = User.objects.get(email=request.user.email)

        if (user.is_staff):
            rooms = Room.objects.filter(Q(isExpired=False) & Q(host=user.fname))
            serializer = self.serializer_class(rooms, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Only Teacher and Admin are authorized to perform this operation!'}, status=status.HTTP_400_BAD_REQUEST)