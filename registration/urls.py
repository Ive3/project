from django.urls import path
from . import views

app_name = 'registration'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('registration/done/', views.RegistrationDoneView.as_view(), name='registration_done'),
    path('registration/activate/<str:sign>/', views.user_activeted, name='user_activated'),


    path('profile/<int:pk>/', views.ProfileView, name='profile'),
    path('cahge_info/<int:pk>/', views.UpdateProfile, name='change_info'),
    path('delete_user/', views.DeleteUserView.as_view(), name='delete_user'),
    path('delete_user_done/', views.DeleteUserDone.as_view(), name='delete_user_done'),


    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('logout_view/', views.logout_view, name='logout_view'),

    path('change_password/', views.change_password, name='change_password'),
    path('change_password_done/', views.ChangePasswordDone.as_view(), name='change_password_done'),

    path('reset_password/', views.ResetPassView.as_view(), name='reset_password'),
    path('reset_password_done/', views.ResetPassViewDone.as_view(), name='reset_password_done'),
    path('reset_password_confirm/<uidb64>/<token>/', views.ResetPassViewConfirm.as_view(), name='reset_password_confirm'),
    path('reset_password_complete/', views.ResetPassViewComplete.as_view(), name='reset_password_complete'),
]