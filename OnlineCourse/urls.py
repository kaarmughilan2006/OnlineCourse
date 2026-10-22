from django.urls import path
from . import views

app_name = 'OnlineCourse'

urlpatterns = [
    # Course catalog and details
    path('', views.popular_course_list, name='popular_course_list'),
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Mock exam view
    path('course/<int:course_id>/mock_exam/', views.mock_exam_view, name='mock_exam'),
    
    # Required paths for Task 6
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    
    # Additional convenient path aliases
    path('<int:course_id>/submit/', views.submit, name='submit_alt'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result_alt'),
]
