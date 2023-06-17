from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views., name='users_index'),
    path('create/', views., name='users_create'),
    path('<int:pk>/update/', views., name='users_update'),
    path('<int:pk>/delete/', views., name='users_delete'),
]
