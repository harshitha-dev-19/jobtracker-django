from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('add/', views.add_job, name='add_job'),
    path('update/<int:id>/', views.update_job, name='update_job'),
    path('delete/<int:id>/', views.delete_job, name='delete_job'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]