from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.MainPageView.as_view(), name='main_page'),
    path('list_2d/', views.GalleryList2DView.as_view(), name='gallery_list_2d'),
    path('list_3d/', views.GalleryList3DView.as_view(), name='gallery_list_3d'),
    path('detail/<int:pk>/', views.GalleryDetailView.as_view(), name='gallery_detail'),
    path('by_tag/<int:pk>/', views.GalleryByTagsView.as_view(), name='by_tags'),
    path('search/', views.GallerySearchView.as_view(), name='search'),
    path('add_picture/', views.add_gallery, name='add_picture'),
    path('profile_gallery_pictures/<int:pk>/', views.profile_gallery, name='author_gallery'),
    path('detail_author_pictures/<int:pk>/', views.detail_author_gallery, name='detail_author_gallery'),
    path('update_pictures/<int:pk>/', views.update_gallery, name='update_gallery'),
    path('delete_pictures/<int:pk>/', views.delete_picture, name='delete_gallery'),
]