from django.urls import path
from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path('author_create/', views.author_create, name='author_create'),
    path('quotes/<int:author_id>/', views.author_page, name='author_page'),
    path('quote_page/<int:tag_id>/', views.quote_page, name='quote_page'),
    path('author/delete/', views.author_confirm_delete, name='author_confirm_delete'),
]
