from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('news/<int:id>/', views.detail_news, name='detail_news'),
    path('about/', views.about, name='about'),
    path('news/', views.main, name='main2'),
    path('news/category/<int:id>/', views.news_by_category, name='news_by_category'),
    path('ajax/create_comment/', views.create_comment_ajax, name='create_comment_ajax'),

    path('login/', views.login_profile, name='login'),
    path('logout/', views.logout_profile, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change_profile/', views.change_profile, name='change_profile'),
    path('profile/change_password/', views.change_password, name='change_password'),
]
