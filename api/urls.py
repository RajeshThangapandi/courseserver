from django.urls import path
from .views import (
    course_detail,
    courses_list,
    list_course_instances,
    get_course_instance,
    delete_course_instance,
    manage_course_instances,
)

urlpatterns = [
    path('courses/', courses_list, name='courses_list'),
    path('courses/<str:course_code>/', course_detail, name='course_detail'),
    path('instances/', manage_course_instances, name='manage_course_instances'),
    path('instances/<int:year>/<int:semester>/', list_course_instances, name='list_course_instances'),
    path('instances/<int:year>/<int:semester>/<str:course_code>/', get_course_instance, name='get_course_instance'),
    path('instances/<int:year>/<int:semester>/<str:course_code>/delete/', delete_course_instance, name='delete_course_instance'),
]
