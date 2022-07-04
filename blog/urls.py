from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('post/<slug:post_slug>/', views.detail_post, name='detail_post'),
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<slug:post_slug>/', views.update_post, name='update_post'),
    path('delete_post/<slug:post_slug>/', views.DeletePostView.as_view(), name='delete_post'),
    path('categories_list/', views.categories_list, name='categories_list'),
    path('by_category/<slug:category_slug>/', views.ByCategory.as_view(), name='by_category'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),
    path('search/', views.SearchView.as_view(), name='search_list'),
    path('like/<slug:slug>/', views.like_post, name='like_post'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    path('user_posts/<int:pk>/', views.UserPosts.as_view(), name='user_posts'),
    path('user_detail_post/<slug:post_slug>/', views.user_detail_post, name='user_detail_post'),
    path('delete_comment/<int:pk>/', views.delete_commet, name='delete_comment'),
]