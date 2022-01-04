from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('abonnements/',views.abonnements,name="abonnements"),
    path('flux/',views.flux,name="flux"),
    path('posts/',views.posts,name="posts"),
    path('ticket/<str:pk>',views.ticket,name="ticket"),
    path('create_ticket/',views.create_ticket,name="create_ticket"),
    path('create_review/<str:pk>',views.create_review,name="create_review"),
    path('ticket_review/',views.ticket_review,name="ticket_review"),
    path('edit/<str:pk>/<str:content_type>',views.edit,name="edit"),
    path('edit/',views.edit),
    path('delete/<str:pk>/<str:content_type>',views.delete,name="delete"),
    path('unfollow/<str:pk>',views.unfollow,name="unfollow"),
]