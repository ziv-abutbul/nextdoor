from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignupPageView, create_request, requests, view_request, support_view, user_count
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #---------------------------- setUp user--------------------------------------#
    path('signup/', SignupPageView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Rulse/', views.Rulse, name='Rulse'),
    #---------------------------- setUp user Profile--------------------------------------#
    path('user_profile/<str:pk_test>/', views.user_profile, name="user_profile"),
    path('user_profile/<str:pk_test>/Make_user_to_support', views.Make_user_to_support, name="Make_user_to_support"),
    path('user_profile/<str:pk_test>/Remove_user_to_support', views.Remove_user_to_support, name="Remove_user_to_support"),
    path('user_profile/<str:pk_test>/edit/', views.edit_profile, name="edit_profile"),
    path('user_profile/<str:pk_test>/delete_user/', views.delete_user, name="delete_user"),
    path('user_profile/<str:pk_test>/create_request/', create_request, name="create_request"),
    path('user_profile/<str:pk_test>/requests/', requests, name="requests"),
    path('user_profile/<str:pk_test>/messaging/', views.messaging, name="messaging"),
    path('user_profile/<str:pk_test>/inbox/', views.inbox, name="inbox"),
    path('user_profile/<str:pk_test>/user_ticket/', views.user_ticket, name="user_ticket"),
    path('user_profile/<str:pk_test>/inbox/<int:pk>/messaging_read', views.messaging_read, name="messaging_read"),
    path('user_profile/<str:pk_test>/inbox/<int:pk>/messaging_delete', views.messaging_delete, name="messaging_delete"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/', view_request, name="view_request"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/delete_request/', views.delete_request, name="delete_request"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/close_request/', views.close_request, name="close_request"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/edit_request/', views.edit_request, name="edit_request"),
    path('user_profile/<str:pk_test>/view_request/<int:pk>/edit_comment/', views.edit_comment, name="edit_comment"),
    path('support_ticket/', views.support_ticket, name="support_ticket"),
    path('RemoveBan/', views.RemoveBan, name="RemoveBan"),
    path('request_to_delete/', views.request_to_delete, name="request_to_delete"),
    path('Open_support_tickets/', views.Open_support_tickets, name="Open_support_tickets"),
    path('Banned_list/', views.Banned_list, name="Banned_list"),
    path('Open_support_tickets/<int:pk>/', views.change_status_ticket, name="change_status_ticket"),
    path('change_user_to_Active/<str:pk>/', views.change_user_to_Active, name="change_user_to_Active"),
    path('change_user_to_not_Active/<str:pk>/', views.change_user_to_not_Active, name="change_user_to_not_Active"),
    path('support_view/', support_view, name="support_view"),
    path('user_count/', user_count, name="user_count"),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)