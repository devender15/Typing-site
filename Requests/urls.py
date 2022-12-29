from django.urls import path
from .views import *


urlpatterns = [
    path('list_all', ListAllRequests.as_view()),
    path('pending', PendingRequests.as_view()),
    path('propose', ProposeRequest.as_view()),
    path('approved/<int:id>', ProposalApproved.as_view()),
    path('rejected/<int:id>', ProposalRejected.as_view()),
]
