from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('categories/', views.list_of_categories, name='workspace_categories'),
    path('categories/create/', views.create_category, name='workspace_create_category'),
    path('categories/<int:id>/update/', views.update_category, name='workspace_update_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='workspace_delete_category'),
    path('news/', views.workspace),
    path('news/<int:id>', views.detail_news, name='workspace_detail_news'),
    path('news/create', views.create_news, name='workspace_create_news'),
]
