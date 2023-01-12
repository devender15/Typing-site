from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import *
from UserAuthentication.serializers import PerformanceSerializer
from .models import *
from UserAuthentication.models import Performance
from exams.models import Tests


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
                host = request.user.fname

                # getting test_id from Tests model
                test_id = Tests.objects.get(name=test).id

                # writing data to Room model
                room = Room(host=host, exam=exam, test_name=test, test_id=test_id, time=time,
                            paragraph=paragraph, criteria=criteria)
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
                participants += 1
                room.participants = participants
                room.save(update_fields=['participants'])
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
            # print(performances[0].student.fname)
            serializer = PerformanceSerializer(performances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'Bad Request': 'Only Teacher and Admin are authorized to perform this operation!'}, status=status.HTTP_400_BAD_REQUEST)
