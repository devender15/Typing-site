from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

from .models import *
from .serializers import *


# User model
User = get_user_model()

# Create your views here.


class ListAllRequests(ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class PendingRequests(APIView):
    serializer_class = RequestSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        # checking if the access token is of admin or not
        isAdmin = request.user.is_superuser

        if (isAdmin):
            pending_requests = Request.objects.filter(tag="PENDING")
            serializer = self.serializer_class(pending_requests, many=True)
            try:
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except Exception as _:
                return Response({"error": "Some error has occured!"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Only admin can access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)


class ProposeRequest(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # matching the conditions for a teacher
        isTeacher = request.user.is_staff and not request.user.is_superuser

        if (isTeacher):
            text = request.data.get("text")
            teacher_name = request.user

            # saving data in db
            req = Request(text=text, teacher_name=teacher_name)
            req.save()

            return Response({"success": "Request sent successfully!"}, status=status.HTTP_201_CREATED)

        else:
            return Response({"error": "Only teachers can send request!"}, status=status.HTTP_401_UNAUTHORIZED)


class ProposalApproved(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        # checking if the access token is of admin or not
        isAdmin = request.user.is_superuser

        if (isAdmin):
            req = Request.objects.get(id=id)  # getting the request from id
            req.tag = "APPROVED"  # updating the tag field
            req.save()

            # updating the approved status of the user
            user = User.objects.get(email=req.teacher_name)
            user.approved = True
            user.save()

            return Response({"success": "Request has been approved"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"error": "Only admin can access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)


class ProposalRejected(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        # checking if the access token is of admin or not
        isAdmin = request.user.is_superuser

        if (isAdmin):
            req = Request.objects.get(id=id)  # getting the request from id
            req.tag = "REJECTED"  # updating the tag field
            req.save()
            return Response({"success": "Request has been rejected!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Only admin can access this resource!"}, status=status.HTTP_401_UNAUTHORIZED)
