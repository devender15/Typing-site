from django.urls import path
from .views import *


urlpatterns = [
    path('list_all', ListExams.as_view()),
    path('tests', ListTests.as_view()),
    path('add_exam', AddExam.as_view()),
    path('add_test', AddTest.as_view()),
    path('get_live_tests/<int:test_id>', GetLiveTests.as_view()),
]
