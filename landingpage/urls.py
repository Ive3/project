from django.urls import path
from . import views

app_name = 'landingpage'

urlpatterns = [
    path('', views.AllView, name='allview'),

    path('request_course_save/', views.sign_course_post, name='sign_course'),
    path('msg_save/', views.msg_save, name='msg_save'),

    path('edit/', views.edit, name='edit'),
    path('edit/journal/', views.JournalView, name='journal'),
    path('edit/messages/', views.ContactMsgView.as_view(), name='contact_msg'),
    path('edit/course_messages/', views.SignMsgView.as_view(), name='sign_msg'),

    path('user_page/<int:pk>/', views.UserPageView.as_view(), name='user_page'),
    path('user_page/user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_page/user_edit/user_journal/<int:pk>/', views.UserJournalView, name='user_journal'),

    path('user/edit/add_student/', views.StudenView.as_view(), name='add_student'),
    path('user/edit/add_teacher/', views.TeacherView.as_view(), name='add_teacher'),
    path('user/edit/add_group/', views.GroupView.as_view(), name='add_group'),
    path('user/edit/add_course/', views.CourseView.as_view(), name='add_course'),
    path('user/edit/add_gallery/', views.GalleryView.as_view(), name='add_gallery'),
    path('user/edit/add_location/', views.LocationView.as_view(), name='add_location'),
    path('edit/add_social/', views.AddSocialView.as_view(), name='add_social'),

    path('user/edit/update_course/<int:pk>/', views.UpdateCourseView.as_view(), name='update_course'),
    path('user/edit/update_teacher/<int:pk>/', views.UpdateTeacherView.as_view(), name='update_teacher'),
    path('user/edit/update_location/<int:pk>/', views.UpdateLocationView.as_view(), name='update_location'),
    path('user/edit/update_gallery/<int:pk>/', views.UpdateGalleryView.as_view(), name='update_gallery'),
    path('user/edit/journal/update_student/<int:pk>/', views.UpdatePupilView.as_view(), name='update_student'),
    path('user/edit/journal/update_social/<int:pk>/', views.update_social, name='update_social'),
    path('user/edit/update_group/<int:pk>/', views.UpdateGroupView.as_view(), name='update_group'),
    
    path('delete/course/<int:pk>/', views.DelCourseView.as_view(), name='delete_course'),
    path('delete/teacher/<int:pk>/', views.DelTeacherView.as_view(), name='delete_teacher'),
    path('delete/gallery/<int:pk>/', views.DelGalleryView.as_view(), name='delete_gallery'),
    path('delete/location/<int:pk>/', views.DelLocationView.as_view(), name='delete_location'),
    path('delete/group/<int:pk>/', views.DelGroupView.as_view(), name='delete_group'),
    path('delete/social/<int:pk>/', views.del_social, name='delete_social'),
    path('delete/student/<int:pk>/', views.DelStudentView.as_view(), name='delete_student'),
]