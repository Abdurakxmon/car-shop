from django.urls import path
from .import views

app_name='car'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:car_slug>', views.product_detail, name='product_detail'),
    path('cars/', views.all_cars, name='all_cars'),
    path('news/', views.PostView.as_view(), name='posts'),
    path('news/<str:post_slug>', views.PostViewDetail.as_view(), name='post_detail'),
    path('comment/<int:post_id>', views.AddComment.as_view(), name='addcomment_view'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('results/', views.FilterPostsView.as_view(), name='serch_posts'),

    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path("profile/", views.userpage, name = "profile"),
   
    
]
