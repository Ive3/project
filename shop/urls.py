from django.urls import path
from . import views
app_name = 'shop'

urlpatterns = [
    path('cart/cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/add_cart/<int:pk>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:pk>/', views.remove_cart, name='remove_cart'),
    
    path('', views.shop, name='shop'),
    path('all_products/', views.ProductView.as_view(), name='products'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('category/<int:pk>/', views.sub_categories, name='sub_categories'),
    path('sub_category/<int:pk>/', views.by_category, name='by_category'),
    path('cart_order/', views.CartOrder.as_view(), name='cart_order'),
    path('order_list/', views.OrderView.as_view(), name='order_list'),
    path('search/', views.Search.as_view(), name='search'),
    path('add_product/', views.add_product, name='add_product'),
    path('author_product/<int:pk>/', views.author_product, name='author_product'),
    path('the_most_viewed_products/', views.viewed_product, name='viewed_product'),
    path('the_most_viewed_categories/', views.viewed_category, name='viewed_category'),
    path('filter_product/', views.filter_product, name='filter_product'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('user_products/<int:pk>/', views.UserProductsView.as_view(), name='user_products'),
    path('user_detail_product/<int:pk>/', views.UserDetailProductView.as_view(), name='user_detail_product'),
    path('user_update_product/<int:pk>/', views.update_user_product, name='user_update_product'),
    path('user_delete_product/<int:pk>/', views.DelUserProductView.as_view(), name='user_delete_product'),

]