from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
     path('admin_home/', views.admin_home_view, name='admin_home'),
    path('home/', views.home, name='home'),
    path('add-clothes/', views.add_clothes, name='add_clothes'),
    path('view-wardrobe/', views.view_wardrobe, name='view_wardrobe'),
    path('create-outfit/', views.create_outfit, name='create_outfit'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('users/', views.list_users_view, name='list_users'),  # Add this line
    path('users/<int:user_id>/change_password/', views.change_password_view, name='change_password'),
]
   