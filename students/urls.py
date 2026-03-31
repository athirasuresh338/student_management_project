from django.urls import path
from . import views
from . views import StudentViewSet
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('list/',views.student_list,name='student_list'),
    path('add/',views.add_student,name='add_student'),
    path('view/<int:id>/', views.view_student, name='view_student'),
    path('update/<int:id>/',views.update_student,name='update_student'),
    path('delete/<int:id>/',views.delete_student,name='delete_student'),
]

router = DefaultRouter()
router.register('', StudentViewSet)

urlpatterns += router.urls
