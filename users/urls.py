from django.urls import path
from django.contrib.auth import views as auth_views
from users import views


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('create/', views.create_view, name='user_create'),
    path('<int:pk>/update/', views.CustomUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
