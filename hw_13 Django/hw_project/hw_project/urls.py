from django.contrib import admin
from django.urls import path, include
from quotes import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quotes.urls")),
    path("users/", include("users.urls")),
    path('author_create/', views.author_create, name='author_create'),
    path('quotes/<int:author_id>/', views.author_page, name='author_page'),
    path('quote_page/<int:tag_id>/', views.quote_page, name='quote_page'),
    path("<int:page>", views.main, name="root_paginate"),
]
