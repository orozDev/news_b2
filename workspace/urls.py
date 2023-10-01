from django.urls import path

from . import views

urlpatterns = [
    path('', views.workspace, name='workspace'),
    path('categories/', views.list_of_categories, name='workspace_categories'),
    path('categories/create/', views.create_category, name='workspace_create_category'),
    path('categories/<int:id>/update/', views.update_category, name='workspace_update_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='workspace_delete_category'),
    path('news/', views.workspace),
    path('news/<int:id>/', views.detail_news, name='workspace_detail_news'),
    path('news/create/', views.create_news, name='workspace_create_news'),
    path('news/<int:id>/update/', views.update_news, name='workspace_update_news'),
    path('news/<int:id>/delete/', views.delete_news, name='workspace_delete_news'),
    path('news/category/<int:id>/', views.filter_news_by_cat, name='workspace_filter_news_by_cat'),
    path('news/tags/<int:id>/', views.filter_news_by_tag, name='workspace_filter_news_by_tag'),
    path('tags/', views.list_of_tags, name='workspace_tags'),
    path('tags/create/', views.create_tag, name='workspace_create_tag'),
    path('tags/<int:id>/update/', views.update_tag, name='workspace_update_tag'),
    path('tags/<int:id>/delete/', views.delete_tag, name='workspace_delete_tag'),
    path('ajax/delete_comment/<int:id>', views.delete_comment_ajax, name='workspace_delete_comment_ajax'),

]
